#!/usr/bin/env python3
"""
Folder-Specific Google Drive Content Scraper

This script downloads and categorizes files from a SPECIFIC PUBLIC Google Drive folder 
and its subdirectories, saving them locally with LLM-based content categorization.
Works with publicly shared folders - no domain-wide delegation required.

Usage:
    python ingest_specific_drive_folder.py --folder-id 1ABC123...

Required:
    --folder-id: Google Drive folder ID to crawl (folder must be publicly accessible)

Optional:
    --credentials: Path to Google service account JSON file (default: ./service_account.json)
    --days-back: Number of days back to crawl modified files (default: 0=all files)
    --output-dir: Output directory for client materials (default: ./ingestion/client_ingestion_outputs)
    --no-llm-categories: Disable LLM categorization (LLM is enabled by default)

Note: The Google Drive folder must be shared as "Anyone with the link can view" for this to work.
"""


import os
import sys
import argparse
import logging
import json
import io
import asyncio
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv
from typing import List, Optional, Set, Dict
from slugify import slugify

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
from openai import AsyncOpenAI

# PDF processing imports
import PyPDF2
from io import BytesIO
import pdfplumber
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
import tempfile
import time
import urllib3
import vectorize_client as v

# LLM-based content categorization system (same as website scraper)
CATEGORIZATION_SYSTEM_PROMPT = """
You are helping categorize document content based on the type of information in each document.

Categories and definitions:

- capabilities_overview: content that provides an overview of the company's capabilities
- case_studies: content with case studies detailing success stories or project examples
- brochures_newsletters: content with brochures or newsletters
- other: use this if you cannot confidently assign the content to one of the provided categories
- pitch_decks: content with pitch decks

Your output should contain only the category name with no other text.
"""

VALID_CATEGORIES = [
    'capabilities_overview', 'case_studies', 'brochures_newsletters', 'other', 'pitch_decks'
]

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

def get_credentials(delegated_user: str, credentials_file: str) -> service_account.Credentials:
    """Get delegated credentials for Google Drive API"""
    credentials = service_account.Credentials.from_service_account_file(
        credentials_file, scopes=SCOPES)
    delegated_credentials = credentials.with_subject(delegated_user)
    return delegated_credentials

def get_gdrive_url(file_id: str, mime_type: str = '') -> str:
    """Generate Google Drive URL for a file"""
    if mime_type == 'application/vnd.google-apps.document':
        url = f'https://docs.google.com/document/d/{file_id}/view'
    elif mime_type == 'application/vnd.google-apps.spreadsheet':
        url = f'https://docs.google.com/spreadsheets/d/{file_id}/view'
    elif mime_type == 'application/vnd.google-apps.presentation':
        url = f'https://docs.google.com/presentation/d/{file_id}/view'
    else:
        url = f'https://drive.google.com/file/d/{file_id}/view'
    return url

async def categorize_single_document_with_llm(content: str, filename: str, client: AsyncOpenAI) -> str:
    """Categorize a single document using LLM based on its content"""
    try:
        # Limit content size for LLM processing (first 4000 chars)
        truncated_content = content[:4000] + "..." if len(content) > 4000 else content
        
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": CATEGORIZATION_SYSTEM_PROMPT},
                {"role": "user", "content": f"Categorize this document content. Filename: {filename}\n\nContent: {truncated_content}"}
            ],
            temperature=0.1,
            max_tokens=20,
            top_p=1
        )
        
        category = response.choices[0].message.content.strip().lower()
        
        if category not in VALID_CATEGORIES:
            logger.warning(f"⚠️  Invalid category '{category}' for {filename}, defaulting to 'other'")
            category = 'other'
            
        return category
        
    except Exception as e:
        logger.error(f"❌ Error categorizing {filename}: {e}")
        return 'other'

def categorize_document_simple(filename: str, content: str = "") -> str:
    """Simple keyword-based categorization as fallback"""
    filename_lower = filename.lower()
    content_lower = content.lower()
    
    # Check filename and content for keywords
    combined_text = f"{filename_lower} {content_lower}"
    
    if any(keyword in combined_text for keyword in ['case study', 'case-study', 'success story', 'portfolio']):
        return 'case_studies'
    elif any(keyword in combined_text for keyword in ['pitch deck', 'pitch-deck', 'presentation', 'slide deck']):
        return 'pitch_decks'
    elif any(keyword in combined_text for keyword in ['brochure', 'newsletter', 'flyer', 'leaflet']):
        return 'brochures_newsletters'
    elif any(keyword in combined_text for keyword in ['capabilities', 'capability', 'overview', 'services overview', 'what we do']):
        return 'capabilities_overview'
    else:
        return 'other'

class FolderSpecificDriveCrawler:
    def __init__(self, credentials_file: str, delegated_user: str, folder_id: str, 
                 days_back: int = 30, output_dir: str = "./ingestion/client_ingestion_outputs"):
        self.credentials_file = credentials_file
        self.delegated_user = delegated_user
        self.folder_id = folder_id
        self.days_back = days_back
        self.output_dir = output_dir
        self.crawled_files = []
        self.pdf_temp_dir = None
        self.pdf_files_to_process = []  # List of (file_info, temp_path) tuples
        
        # Initialize services (public folder access - no delegation needed)
        self.credentials = service_account.Credentials.from_service_account_file(
            credentials_file,
            scopes=[
                'https://www.googleapis.com/auth/drive.readonly',
                'https://www.googleapis.com/auth/documents.readonly'
            ]
        )
        
        self.drive_service = build('drive', 'v3', credentials=self.credentials)
        self.docs_service = build('docs', 'v1', credentials=self.credentials)
        
        # Date threshold for filtering files
        self.date_threshold = datetime.now() - timedelta(days=days_back)
        
    def setup(self):
        """Initialize output directory"""
        logger.info(f"🔑 Setting up Google Drive service for public folder access")
        os.makedirs(self.output_dir, exist_ok=True)
        
    def get_folder_info(self, folder_id: str) -> Optional[dict]:
        """Get folder information"""
        try:
            folder = self.drive_service.files().get(
                fileId=folder_id,
                fields='id, name, mimeType, parents'
            ).execute()
            return folder
        except HttpError as e:
            logger.error(f"Error accessing folder {folder_id}: {e}")
            return None
            
    def list_files_in_folder(self, folder_id: str, recursive: bool = True) -> List[dict]:
        """List all files in a specific folder and optionally its subdirectories"""
        all_files = []
        folders_to_process = [folder_id]
        processed_folders = set()
        
        while folders_to_process:
            current_folder_id = folders_to_process.pop(0)
            
            if current_folder_id in processed_folders:
                continue
                
            processed_folders.add(current_folder_id)
            logger.info(f"📁 Crawling folder: {current_folder_id}")
            
            # Get folder info for logging
            folder_info = self.get_folder_info(current_folder_id)
            if folder_info:
                logger.info(f"📂 Folder name: {folder_info.get('name', 'Unknown')}")
            
            # Query for files in this specific folder
            page_token = None
            query = f"'{current_folder_id}' in parents and trashed=false"
            
            # Add date filter if specified
            if self.days_back > 0:
                date_str = self.date_threshold.isoformat() + 'Z'
                query += f" and modifiedTime > '{date_str}'"
            
            while True:
                try:
                    params = {
                        'q': query,
                        'fields': 'nextPageToken, files(id, name, mimeType, modifiedTime, createdTime, owners, size, parents)',
                        'supportsAllDrives': True,
                        'includeItemsFromAllDrives': True
                    }
                    if page_token:
                        params['pageToken'] = page_token
                        
                    response = self.drive_service.files().list(**params).execute()
                    files = response.get('files', [])
                    
                    for file in files:
                        if file['mimeType'] == 'application/vnd.google-apps.folder':
                            # It's a subfolder - add to processing queue if recursive
                            if recursive:
                                folders_to_process.append(file['id'])
                                logger.info(f"📁 Found subfolder: {file['name']} ({file['id']})")
                        else:
                            # It's a file - add to results
                            all_files.append(file)
                            logger.info(f"📄 Found file: {file['name']} ({file.get('size', 'N/A')} bytes)")
                    
                    page_token = response.get('nextPageToken')
                    if not page_token:
                        break
                        
                except HttpError as e:
                    logger.error(f"Error listing files in folder {current_folder_id}: {e}")
                    break
        
        return all_files
    
    def find_client_intake_files(self, folder_id: str) -> List[dict]:
        """Find Client Intake files in the main directory only (not subdirectories)"""
        intake_files = []
        
        try:
            # Query for files in main folder only with "Client Intake" in the name
            query = f"'{folder_id}' in parents and trashed=false and name contains 'Client Intake'"
            
            # Add date filter if specified
            if self.days_back > 0:
                date_str = self.date_threshold.isoformat() + 'Z'
                query += f" and modifiedTime > '{date_str}'"
            
            response = self.drive_service.files().list(
                q=query,
                fields='files(id, name, mimeType, modifiedTime, createdTime, owners, size, parents)',
                supportsAllDrives=True,
                includeItemsFromAllDrives=True
            ).execute()
            
            files = response.get('files', [])
            
            for file in files:
                if file['mimeType'] == 'application/vnd.google-apps.document':
                    logger.info(f"📋 Found Client Intake file: {file['name']}")
                    intake_files.append(file)
                else:
                    logger.warning(f"⚠️  Client Intake file is not a Google Doc: {file['name']} ({file['mimeType']})")
            
        except HttpError as e:
            logger.error(f"Error finding Client Intake files: {e}")
        
        return intake_files
    
    def get_document_text(self, doc_id: str) -> str:
        """Get all text from a Google Doc as plain text."""
        try:
            document = self.docs_service.documents().get(documentId=doc_id).execute()
            
            # Extract all text
            content = document.get('body', {}).get('content', [])
            full_text = []
            
            for element in content:
                # Handle paragraphs
                if 'paragraph' in element:
                    text = self._get_paragraph_text(element['paragraph'])
                    if text.strip():
                        full_text.append(text)
                
                # Handle tables
                elif 'table' in element:
                    table_text = self._get_table_text(element['table'])
                    if table_text.strip():
                        full_text.append(table_text)
                
                # Handle lists
                elif 'list' in element:
                    list_text = self._get_list_text(element['list'])
                    if list_text.strip():
                        full_text.append(list_text)
            
            # Join with double newlines for better separation
            return '\n\n'.join(full_text)
            
        except Exception as e:
            logger.error(f"Error getting document text: {str(e)}")
            return ""
    
    def _get_paragraph_text(self, paragraph: Dict) -> str:
        """Extract text from a paragraph element"""
        text = []
        for element in paragraph.get('elements', []):
            if 'textRun' in element:
                content = element['textRun'].get('content', '')
                # Preserve important whitespace
                if content.strip() or '\n' in content:
                    text.append(content)
        return ''.join(text)

    def _get_table_text(self, table: Dict) -> str:
        """Extract text from a table element"""
        rows = []
        for row in table.get('tableRows', []):
            cells = []
            for cell in row.get('tableCells', []):
                cell_text = []
                for content in cell.get('content', []):
                    if 'paragraph' in content:
                        text = self._get_paragraph_text(content['paragraph'])
                        if text.strip():
                            cell_text.append(text)
                cells.append(' '.join(cell_text))
            rows.append(' | '.join(filter(None, cells)))
        return '\n'.join(filter(None, rows))

    def _get_list_text(self, list_item: Dict) -> str:
        """Extract text from a list element"""
        items = []
        for item in list_item.get('listItems', []):
            if 'paragraph' in item:
                text = self._get_paragraph_text(item['paragraph'])
                if text.strip():
                    items.append(f"• {text}")
        return '\n'.join(items)

    def _download_and_process_file(self, file: Dict) -> str:
        """Download and extract content from a file based on its type"""
        try:
            mime_type = file['mimeType']
            file_name = file['name']
            
            # Handle Google Docs
            if mime_type == 'application/vnd.google-apps.document':
                return self.get_document_text(file['id'])
            
            # Handle plain text files (excluding CSV)
            elif mime_type in ['text/plain', 'text/markdown']:
                request = self.drive_service.files().get_media(fileId=file['id'])
                content = request.execute().decode('utf-8')
                return content

            # Explicitly skip CSV files
            elif mime_type == 'text/csv':
                logger.warning(f"Skipping CSV file processing: {file_name}")
                return None
            
            # Handle PDFs - save for batch processing with vectorize
            elif mime_type == 'application/pdf':
                return self._save_pdf_for_batch_processing(file)
            
            # Handle other binary files
            elif mime_type in ['application/msword']:
                logger.warning(f"Binary file type {mime_type} not yet supported: {file_name}")
                return None
            
            else:
                logger.warning(f"Unsupported file type {mime_type}: {file_name}")
                return None
                
        except Exception as e:
            logger.error(f"Error downloading file {file['name']}: {str(e)}")
            return None

    def _save_pdf_for_batch_processing(self, file: Dict) -> str:
        """Save PDF file to temp directory for later batch processing with vectorize"""
        try:
            # Create temp directory if it doesn't exist
            if self.pdf_temp_dir is None:
                self.pdf_temp_dir = tempfile.mkdtemp(prefix="drive_pdfs_")
                logger.info(f"📁 Created temp directory for PDFs: {self.pdf_temp_dir}")
            
            # Download the PDF file
            file_id = file['id']
            file_name = file['name']
            temp_path = os.path.join(self.pdf_temp_dir, file_name)
            
            request = self.drive_service.files().get_media(fileId=file_id)
            file_content = request.execute()
            
            with open(temp_path, 'wb') as f:
                f.write(file_content)
                
            logger.info(f"📄 Saved PDF for batch processing: {file_name}")
            
            # Add to processing queue
            self.pdf_files_to_process.append((file, temp_path))
            
            # Return placeholder text - will be replaced after vectorize processing
            return f"[PDF_PLACEHOLDER_{file_id}]"
                
        except Exception as e:
            logger.error(f"Error saving PDF {file['name']}: {str(e)}")
            return None

    def _extract_pdf_text(self, file_id: str) -> str:
        """Extract text, tables, and images from a PDF file"""
        try:
            # Download the PDF file
            request = self.drive_service.files().get_media(fileId=file_id)
            file_content = request.execute()
            
            text_content = []
            
            # Process with pdfplumber for text and tables
            with pdfplumber.open(BytesIO(file_content)) as pdf:
                for page in pdf.pages:
                    # Extract regular text
                    text = page.extract_text()
                    if text:
                        text_content.append(text)
                    
                    # Extract tables
                    tables = page.extract_tables()
                    if tables:
                        for table in tables:
                            table_text = self._format_table(table)
                            text_content.append(table_text)
                    
                    # Check if page needs OCR
                    if not text and not tables:
                        ocr_text = self._process_page_with_ocr(page)
                        if ocr_text:
                            text_content.append(ocr_text)
            
            return '\n\n'.join(text_content)
            
        except Exception as e:
            logger.error(f"Error extracting PDF text: {str(e)}")
            return None

    def _format_table(self, table: List[List[str]]) -> str:
        """Format a table into a readable string"""
        # Remove empty cells and clean whitespace
        cleaned_table = [
            [str(cell).strip() if cell else '' for cell in row]
            for row in table
        ]
        
        # Get maximum width for each column
        col_widths = [
            max(len(str(row[i])) for row in cleaned_table)
            for i in range(len(cleaned_table[0]))
        ]
        
        # Format rows with proper spacing
        formatted_rows = []
        for row in cleaned_table:
            formatted_row = " | ".join(
                str(cell).ljust(width) for cell, width in zip(row, col_widths)
            )
            formatted_rows.append(formatted_row)
        
        # Add separator line after header
        separator = "-" * len(formatted_rows[0])
        formatted_rows.insert(1, separator)
        
        return "\n".join(formatted_rows)

    def _process_page_with_ocr(self, page) -> str:
        """Process a page with OCR to extract text from images"""
        try:
            # Use pdfplumber's built-in capability to get a PIL Image
            # Increase resolution for potentially better OCR quality
            page_image = page.to_image(resolution=300) 
            
            # pdfplumber's to_image returns an object with a .original attribute holding the PIL Image
            pil_image = page_image.original 

            if not pil_image:
                logger.warning(f"Could not convert page {page.page_number} to image for OCR.")
                return ""

            # Enhance the PIL image directly
            enhanced = self._enhance_image(pil_image)
            
            # Perform OCR on the enhanced PIL image
            text = pytesseract.image_to_string(enhanced)
            
            return text.strip() # Return stripped text
            
        except Exception as e:
            logger.error(f"Error in OCR processing for page {page.page_number}: {str(e)}", exc_info=True)
            return ""

    def _enhance_image(self, image: Image) -> Image:
        """Enhance image for better OCR results"""
        # Convert to grayscale
        image = image.convert('L')
        
        # Increase contrast
        enhanced = Image.eval(image, lambda x: 255 if x > 128 else 0)
        
        return enhanced

    def _batch_process_pdfs_with_vectorize(self) -> Dict[str, str]:
        """Process all collected PDFs using vectorize.io API"""
        if not self.pdf_files_to_process:
            return {}
            
        logger.info(f"🚀 Starting batch PDF processing with vectorize.io for {len(self.pdf_files_to_process)} PDFs")
        
        # Load environment variables
        load_dotenv()
        api_key = os.getenv('VECTORIZE_API_KEY')
        organization_id = os.getenv('VECTORIZE_ORGANIZATION_ID')
        
        if not api_key or not organization_id:
            logger.error("❌ VECTORIZE_API_KEY or VECTORIZE_ORGANIZATION_ID not found in environment")
            logger.warning("⚠️  Falling back to pdfplumber for PDF processing")
            return self._fallback_pdf_processing()
        
        try:
            # Initialize the API client
            config = v.Configuration(host="https://api.vectorize.io/v1")
            apiClient = v.ApiClient(config)
            apiClient.set_default_header('Authorization', f'Bearer {api_key}')
            
            files_api = v.FilesApi(apiClient)
            extraction_api = v.ExtractionApi(apiClient)
            
            # Phase 1: Upload PDFs and start extractions
            extraction_jobs = {}
            content_type = "application/pdf"
            http = urllib3.PoolManager()
            
            for file_info, temp_path in self.pdf_files_to_process:
                file_name = file_info['name']
                file_id = file_info['id']
                
                try:
                    logger.info(f"⬆️  Uploading PDF: {file_name}")
                    
                    # Start file upload
                    start_file_upload_response = files_api.start_file_upload(
                        organization_id,
                        start_file_upload_request=v.StartFileUploadRequest(
                            content_type=content_type,
                            name=file_name,
                        )
                    )
                    
                    # Upload the file
                    with open(temp_path, "rb") as f:
                        response = http.request(
                            "PUT",
                            start_file_upload_response.upload_url,
                            body=f,
                            headers={
                                "Content-Type": content_type,
                                "Content-Length": str(os.path.getsize(temp_path))
                            }
                        )
                        
                    if response.status != 200:
                        logger.error(f"❌ Upload failed for {file_name}: status {response.status}")
                        continue
                    
                    # Start extraction
                    extraction_response = extraction_api.start_extraction(
                        organization_id,
                        start_extraction_request=v.StartExtractionRequest(
                            file_id=start_file_upload_response.file_id
                        )
                    )
                    
                    extraction_jobs[file_id] = {
                        'extraction_id': extraction_response.extraction_id,
                        'file_name': file_name,
                        'file_info': file_info
                    }
                    logger.info(f"🔄 Started extraction for {file_name}: {extraction_response.extraction_id}")
                    
                except Exception as e:
                    logger.error(f"❌ Error uploading {file_name}: {e}")
                    continue
            
            # Phase 2: Wait for extractions to complete
            logger.info(f"⏳ Waiting for {len(extraction_jobs)} extractions to complete...")
            extracted_content = {}
            pending_jobs = extraction_jobs.copy()
            
            max_wait_time = 300  # 5 minutes max wait
            start_time = time.time()
            
            while pending_jobs and (time.time() - start_time) < max_wait_time:
                for file_id, job_info in list(pending_jobs.items()):
                    try:
                        response = extraction_api.get_extraction_result(
                            organization_id, 
                            job_info['extraction_id']
                        )
                        
                        if response.ready:
                            if response.data.success:
                                extracted_content[file_id] = response.data.text
                                logger.info(f"✅ Extraction completed: {job_info['file_name']}")
                                del pending_jobs[file_id]
                            else:
                                logger.error(f"❌ Extraction failed for {job_info['file_name']}: {response.data.error}")
                                del pending_jobs[file_id]
                        else:
                            logger.debug(f"⏳ Still processing: {job_info['file_name']}")
                            
                    except Exception as e:
                        logger.error(f"❌ Error checking extraction for {job_info['file_name']}: {e}")
                        del pending_jobs[file_id]
                
                if pending_jobs:
                    time.sleep(5)
            
            # Handle any remaining pending jobs
            if pending_jobs:
                logger.warning(f"⚠️  {len(pending_jobs)} extractions timed out, using fallback processing")
                for file_id, job_info in pending_jobs.items():
                    # Try fallback processing for timed out files
                    try:
                        content = self._extract_pdf_with_fallback(file_id)
                        if content:
                            extracted_content[file_id] = content
                    except Exception as e:
                        logger.error(f"❌ Fallback processing failed for {job_info['file_name']}: {e}")
            
            logger.info(f"🎉 PDF batch processing completed: {len(extracted_content)}/{len(self.pdf_files_to_process)} successful")
            return extracted_content
            
        except Exception as e:
            logger.error(f"❌ Error in vectorize batch processing: {e}")
            return self._fallback_pdf_processing()

    def _fallback_pdf_processing(self) -> Dict[str, str]:
        """Fallback PDF processing using pdfplumber if vectorize fails"""
        logger.info("🔄 Using fallback pdfplumber processing for PDFs...")
        extracted_content = {}
        
        for file_info, temp_path in self.pdf_files_to_process:
            try:
                file_id = file_info['id']
                # Read the temporary file and process with pdfplumber
                with open(temp_path, 'rb') as f:
                    file_content = f.read()
                
                text_content = []
                with pdfplumber.open(BytesIO(file_content)) as pdf:
                    for page in pdf.pages:
                        text = page.extract_text()
                        if text:
                            text_content.append(text)
                
                if text_content:
                    extracted_content[file_id] = '\n\n'.join(text_content)
                    logger.info(f"✅ Fallback processing completed: {file_info['name']}")
                    
            except Exception as e:
                logger.error(f"❌ Fallback processing failed for {file_info['name']}: {e}")
        
        return extracted_content

    def _extract_pdf_with_fallback(self, file_id: str) -> str:
        """Extract content from a specific PDF using fallback method"""
        for file_info, temp_path in self.pdf_files_to_process:
            if file_info['id'] == file_id:
                try:
                    with open(temp_path, 'rb') as f:
                        file_content = f.read()
                    
                    text_content = []
                    with pdfplumber.open(BytesIO(file_content)) as pdf:
                        for page in pdf.pages:
                            text = page.extract_text()
                            if text:
                                text_content.append(text)
                    
                    return '\n\n'.join(text_content) if text_content else ""
                except Exception as e:
                    logger.error(f"❌ Fallback extraction failed: {e}")
                    return ""
        return ""

    def _cleanup_temp_files(self):
        """Clean up temporary PDF files"""
        if self.pdf_temp_dir and os.path.exists(self.pdf_temp_dir):
            try:
                shutil.rmtree(self.pdf_temp_dir)
                logger.info(f"🧹 Cleaned up temp directory: {self.pdf_temp_dir}")
            except Exception as e:
                logger.warning(f"⚠️  Could not clean up temp directory: {e}")
    
    def is_supported_file_type(self, mime_type: str, file_name: str) -> bool:
        """Check if file type is supported for processing"""
        supported_mime_types = [
            'application/pdf',
            'application/msword',
            'text/plain',
            'text/markdown',
            'application/vnd.google-apps.document',
            'application/rtf'
        ]
        
        supported_extensions = ['.doc', '.docx', '.pdf', '.txt', '.md', '.rtf']
        
        mime_supported = any(mime_type.startswith(supported) for supported in supported_mime_types)
        extension_supported = any(file_name.lower().endswith(ext) for ext in supported_extensions)
        
        return mime_supported or extension_supported
    
    async def crawl_and_save_locally(self, use_llm_categories: bool = False):
        """Crawl folder and save files locally with metadata"""
        logger.info(f"🚀 Starting folder-specific crawl of: {self.folder_id}")
        
        # Create output directories
        client_materials_dir = os.path.join(self.output_dir, "client_materials")
        client_intake_dir = os.path.join(self.output_dir, "client_intake_form")
        os.makedirs(client_materials_dir, exist_ok=True)
        os.makedirs(client_intake_dir, exist_ok=True)
        
        # First, look for Client Intake form in the main directory (not subdirectories)
        intake_files = self.find_client_intake_files(self.folder_id)
        
        # Then get all other files from the folder and subfolders
        files = self.list_files_in_folder(self.folder_id, recursive=True)
        logger.info(f"📊 Found {len(files)} total files to process")
        logger.info(f"📋 Found {len(intake_files)} Client Intake files")
        
        # Filter to supported file types
        supported_files = [f for f in files if self.is_supported_file_type(f['mimeType'], f['name'])]
        logger.info(f"📋 {len(supported_files)} files are supported for processing")
        
        # Setup LLM client if needed
        openai_client = None
        if use_llm_categories:
            try:
                load_dotenv()
                api_key = os.getenv('OPENAI_API_KEY')
                if api_key:
                    openai_client = AsyncOpenAI(api_key=api_key)
                    logger.info("🤖 LLM categorization enabled")
                else:
                    logger.warning("⚠️  OPENAI_API_KEY not found, using simple categorization")
            except Exception as e:
                logger.error(f"❌ Failed to initialize OpenAI client: {e}")
                logger.warning("⚠️  Falling back to simple categorization")
        
        # Phase 1: Process Client Intake files separately
        intake_processed_count = 0
        if intake_files:
            logger.info(f"\n📋 PHASE 1: Processing {len(intake_files)} Client Intake files...")
            for file in intake_files:
                try:
                    file_id = file['id']
                    name = file['name']
                    mime_type = file['mimeType']
                    
                    logger.info(f"📋 Processing Client Intake: {name}")
                    
                    # Extract content (should be Google Doc)
                    if mime_type == 'application/vnd.google-apps.document':
                        file_content = self.get_document_text(file_id)
                    else:
                        logger.warning(f"⚠️  Client Intake file is not a Google Doc, skipping: {name}")
                        continue
                    
                    if not file_content:
                        logger.warning(f"❌ Failed to extract content from Client Intake: {name}")
                        continue
                    
                    # Special metadata for Client Intake files
                    intake_metadata = {
                        'source': 'client_intake',
                        'content_type': 'client_intake',
                        'id': file_id,
                        'name': name,
                        'title': name,
                        'created_at': file.get('createdTime', 'N/A'),
                        'last_updated': file.get('modifiedTime', 'N/A'),
                        'owners': ', '.join([owner.get('displayName', owner.get('emailAddress', 'Unknown')) 
                                           for owner in file.get('owners', [])]),
                        'size': file.get('size', 'N/A'),
                        'url': get_gdrive_url(file_id, mime_type),
                        'folder_id': self.folder_id,
                        'mime_type': mime_type,
                        'scraped_time': datetime.now().isoformat(),
                        'word_count': len(file_content.split()) if file_content else 0
                    }
                    
                    # Save to client_intake_form directory
                    safe_name = slugify(os.path.splitext(name)[0])
                    final_filename = f"client_intake_{safe_name}.md"
                    final_file_path = os.path.join(client_intake_dir, final_filename)
                    
                    # Save extracted content
                    with open(final_file_path, 'w', encoding='utf-8') as f:
                        f.write(file_content)
                    
                    # Save metadata
                    metadata_file_path = final_file_path + '.metadata.json'
                    with open(metadata_file_path, 'w') as f:
                        json.dump(intake_metadata, f, indent=2)
                    
                    intake_processed_count += 1
                    logger.info(f"📋 ✅ Client Intake saved: {name} → {final_filename} ({intake_processed_count}/{len(intake_files)})")
                    
                    # Add to crawled files list for reporting
                    self.crawled_files.append({
                        'name': name,
                        'final_filename': final_filename,
                        'id': file_id,
                        'size': file.get('size', 'N/A'),
                        'mime_type': mime_type,
                        'content_type': 'client_intake',
                        'url': get_gdrive_url(file_id, mime_type),
                        'word_count': intake_metadata['word_count'],
                        'special_category': 'client_intake'
                    })
                    
                except Exception as e:
                    logger.error(f"❌ Error processing Client Intake {file.get('name', 'unknown')}: {e}")
        
        # Filter out intake files from regular processing to avoid duplicates
        intake_file_ids = {f['id'] for f in intake_files}
        regular_files = [f for f in files if f['id'] not in intake_file_ids]
        
        # Also filter by name to catch any missed intake files
        regular_files = [f for f in regular_files if 'client intake' not in f['name'].lower()]
        
        # Filter to supported file types
        supported_files = [f for f in regular_files if self.is_supported_file_type(f['mimeType'], f['name'])]
        logger.info(f"📋 {len(supported_files)} regular files are supported for processing (Client Intake files excluded)")
        
        # Phase 2: Process regular client materials files
        processed_count = 0
        error_count = 0
        
        if supported_files:
            logger.info(f"\n📄 PHASE 2: Processing {len(supported_files)} regular client materials...")
        
        for file in supported_files:
            try:
                file_id = file['id']
                name = file['name']
                mime_type = file['mimeType']
                
                logger.info(f"📄 Processing: {name}")
                
                # Extract content using the enhanced processing methods
                file_content = self._download_and_process_file(file)
                
                if not file_content:
                    logger.warning(f"❌ Failed to extract content from: {name}")
                    error_count += 1
                    continue
                
                # Categorize content
                if openai_client and file_content:
                    content_type = await categorize_single_document_with_llm(file_content, name, openai_client)
                else:
                    content_type = categorize_document_simple(name, file_content)
                
                # Prepare comprehensive metadata
                file_metadata = {
                    'source': 'client_materials',
                    'content_type': content_type,
                    'id': file_id,
                    'name': name,
                    'title': name,
                    'created_at': file.get('createdTime', 'N/A'),
                    'last_updated': file.get('modifiedTime', 'N/A'),
                    'owners': ', '.join([owner.get('displayName', owner.get('emailAddress', 'Unknown')) 
                                       for owner in file.get('owners', [])]),
                    'size': file.get('size', 'N/A'),
                    'url': get_gdrive_url(file_id, mime_type),
                    'folder_id': self.folder_id,
                    'mime_type': mime_type,
                    'scraped_time': datetime.now().isoformat(),
                    'word_count': len(file_content.split()) if file_content else 0
                }
                
                # Create final filename with category prefix for organization
                safe_name = slugify(os.path.splitext(name)[0])
                file_extension = ".md"  # Save extracted content as markdown
                final_filename = f"{content_type}_{safe_name}{file_extension}"
                final_file_path = os.path.join(client_materials_dir, final_filename)
                
                # Save extracted content as markdown file
                with open(final_file_path, 'w', encoding='utf-8') as f:
                    f.write(file_content)
                
                # Save metadata as JSON sidecar file
                metadata_file_path = final_file_path + '.metadata.json'
                with open(metadata_file_path, 'w') as f:
                    json.dump(file_metadata, f, indent=2)
                
                processed_count += 1
                logger.info(f"✅ Successfully processed: {name} → {final_filename} [{content_type}] ({processed_count}/{len(supported_files)})")
                
                # Add to crawled files list for reporting
                self.crawled_files.append({
                    'name': name,
                    'final_filename': final_filename,
                    'id': file_id,
                    'size': file.get('size', 'N/A'),
                    'mime_type': mime_type,
                    'content_type': content_type,
                    'url': get_gdrive_url(file_id, mime_type),
                    'word_count': file_metadata['word_count']
                })
                
            except Exception as e:
                logger.error(f"❌ Error processing {file.get('name', 'unknown')}: {e}")
                error_count += 1
        
        # Phase 2: Process PDFs with vectorize if any were found
        pdf_extracted_content = {}
        if self.pdf_files_to_process:
            logger.info(f"\n📄 PHASE 2: Processing {len(self.pdf_files_to_process)} PDFs with vectorize.io...")
            pdf_extracted_content = self._batch_process_pdfs_with_vectorize()
            
            # Update the processed files with actual PDF content (only for regular client materials, not intake forms)
            for crawled_file in self.crawled_files:
                # Skip Client Intake files - they don't have PDFs
                if crawled_file.get('special_category') == 'client_intake':
                    continue
                    
                if crawled_file['final_filename'].endswith('.md'):
                    # Check if this is a PDF placeholder
                    file_path = os.path.join(client_materials_dir, crawled_file['final_filename'])
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Look for PDF placeholder
                        if content.startswith('[PDF_PLACEHOLDER_'):
                            file_id = content.replace('[PDF_PLACEHOLDER_', '').replace(']', '')
                            if file_id in pdf_extracted_content:
                                # Replace with actual extracted content
                                actual_content = pdf_extracted_content[file_id]
                                with open(file_path, 'w', encoding='utf-8') as f:
                                    f.write(actual_content)
                                
                                # Update metadata
                                metadata_file_path = file_path + '.metadata.json'
                                if os.path.exists(metadata_file_path):
                                    with open(metadata_file_path, 'r') as f:
                                        metadata = json.load(f)
                                    metadata['word_count'] = len(actual_content.split())
                                    with open(metadata_file_path, 'w') as f:
                                        json.dump(metadata, f, indent=2)
                                
                                # Update crawled file info
                                crawled_file['word_count'] = len(actual_content.split())
                                logger.info(f"📄 Updated PDF content: {crawled_file['name']}")
                            else:
                                logger.warning(f"⚠️  No extracted content found for PDF: {crawled_file['name']}")
                    except Exception as e:
                        logger.error(f"❌ Error updating PDF content for {crawled_file['name']}: {e}")
        
        # Clean up temporary files
        try:
            self._cleanup_temp_files()
        except Exception as e:
            logger.warning(f"⚠️  Error during cleanup: {e}")
        
        # Generate summary report
        total_processed = processed_count + intake_processed_count
        self.generate_report(total_processed, error_count, len(files))
        
        logger.info(f"\n🎉 Drive folder processing completed!")
        logger.info(f"📊 Total files found: {len(files)}")
        logger.info(f"📋 Client Intake files: {intake_processed_count}")
        logger.info(f"📄 Regular client materials: {processed_count}")
        logger.info(f"✅ Total successfully processed: {total_processed}")
        logger.info(f"📄 PDFs processed with vectorize: {len(pdf_extracted_content)}")
        logger.info(f"❌ Errors: {error_count}")
        logger.info(f"📂 Client materials saved to: {client_materials_dir}")
        logger.info(f"📋 Client intake saved to: {client_intake_dir}")
        logger.info(f"📋 Report saved to: {self.output_dir}/crawl_summary.json")
    
    def generate_report(self, processed_count: int, error_count: int, total_files: int):
        """Generate a summary report of the crawl"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'folder_id': self.folder_id,
            'delegated_user': self.delegated_user,
            'days_back': self.days_back,
            'summary': {
                'total_files_found': total_files,
                'supported_files': len(self.crawled_files),
                'successfully_processed': processed_count,
                'errors': error_count
            },
            'crawled_files': self.crawled_files
        }
        
        report_file = os.path.join(self.output_dir, 'crawl_summary.json')
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"📋 Report saved: {report_file}")

def extract_folder_id_from_url(folder_input: str) -> str:
    """Extract folder ID from Google Drive URL or return the ID if already provided"""
    if folder_input.startswith('http'):
        if '/folders/' in folder_input:
            folder_id = folder_input.split('/folders/')[1].split('?')[0].split('#')[0]
            return folder_id
        else:
            raise ValueError("Invalid Google Drive folder URL format")
    else:
        return folder_input

def validate_credentials_file(credentials_path: str) -> bool:
    """Validate Google service account credentials file"""
    if not os.path.exists(credentials_path):
        logger.error(f"Credentials file not found: {credentials_path}")
        return False
    
    try:
        with open(credentials_path, 'r') as f:
            creds = json.load(f)
        
        required_fields = ['type', 'project_id', 'private_key_id', 'private_key', 'client_email']
        missing_fields = [field for field in required_fields if field not in creds]
        
        if missing_fields:
            logger.error(f"Invalid credentials file. Missing fields: {', '.join(missing_fields)}")
            return False
        
        if creds.get('type') != 'service_account':
            logger.error("Credentials file must be for a service account")
            return False
            
        return True
        
    except json.JSONDecodeError:
        logger.error("Credentials file is not valid JSON")
        return False
    except Exception as e:
        logger.error(f"Error validating credentials file: {e}")
        return False

async def main_async():
    """Async main function to handle LLM categorization"""
    parser = argparse.ArgumentParser(
        description='Download files from a specific Google Drive folder with LLM categorization',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    # Required arguments
    parser.add_argument('--folder-id', '-f', required=True,
                       help='Google Drive folder ID or full folder URL (must be publicly accessible)')
    
    # Optional arguments  
    parser.add_argument('--credentials', '-k', default='./service_account.json',
                       help='Path to Google service account JSON file (default: ./service_account.json)')
    parser.add_argument('--days-back', '-d', type=int, default=0,
                       help='Number of days back to crawl modified files (default: 0=all files)')
    parser.add_argument('--output-dir', '-o', default='./ingestion/client_ingestion_outputs',
                       help='Output directory for client materials (default: ./ingestion/client_ingestion_outputs)')
    parser.add_argument('--no-llm-categories', action='store_true',
                       help='Disable LLM categorization and use simple keyword-based categorization instead')
    
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    
    # Extract folder ID from URL if needed
    try:
        folder_id = extract_folder_id_from_url(args.folder_id)
        logger.info(f"📁 Target folder ID: {folder_id}")
    except ValueError as e:
        logger.error(f"Invalid folder ID/URL: {e}")
        return 1
    
    # Validate credentials file
    if not validate_credentials_file(args.credentials):
        logger.error("Please provide a valid Google service account credentials file")
        return 1
    
    credentials_path = os.path.abspath(args.credentials)
    
    logger.info(f"🚀 Starting folder-specific Google Drive processing")
    logger.info(f"📁 Folder ID: {folder_id}")
    logger.info(f"📅 Days back: {args.days_back}")
    use_llm_categories = not args.no_llm_categories
    logger.info(f"🤖 LLM Categorization: {'Enabled' if use_llm_categories else 'Disabled (--no-llm-categories flag used)'}")
    logger.info(f"🔑 Credentials: {credentials_path}")
    logger.info(f"📁 Output directory: {args.output_dir}/client_materials/")
    logger.info(f"🔓 Public folder access - no delegation required")
    
    try:
        # Initialize crawler
        crawler = FolderSpecificDriveCrawler(
            credentials_file=credentials_path,
            delegated_user=None,  # No user delegation needed for public folders
            folder_id=folder_id,
            days_back=args.days_back,
            output_dir=args.output_dir
        )
        
        # Setup and crawl
        crawler.setup()
        await crawler.crawl_and_save_locally(use_llm_categories=use_llm_categories)
        
        logger.info("✅ Google Drive folder processing completed successfully!")
        return 0
        
    except KeyboardInterrupt:
        logger.info("🛑 Processing interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"❌ Error during Google Drive processing: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return 1

def main():
    """Wrapper to run async main function"""
    return asyncio.run(main_async())

if __name__ == "__main__":
    sys.exit(main())
