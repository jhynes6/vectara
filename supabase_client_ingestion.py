#!/usr/bin/env python3
"""
Supabase Client Ingestion Script

This comprehensive script onboards new clients into Supabase Vector DB by:
1. Creating client records in the database
2. Ingesting client website content 
3. Ingesting client materials from Google Drive
4. Uploading all processed documents to Supabase with embeddings

Usage:
    # Interactive mode (recommended):
    python supabase_client_ingestion.py
    
    # Batch mode:
    python supabase_client_ingestion.py --batch-mode \
        --client-id "client-name" \
        --drive-folder-id "1ABC123..." \
        --client-homepage-url "https://example.com"
"""

import os
import sys
import argparse
import logging
import json
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Import Supabase vector store
from supabase_vector_store import SupabaseVectorStore

# Import existing ingestion components
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ingestion.ingest_client_website import main_async as website_ingestion
from ingestion.ingest_specific_drive_folder import main_async as drive_ingestion

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SupabaseClientOnboarder:
    """Handles the complete client onboarding process into Supabase"""
    
    def __init__(self, client_id: str, drive_folder_id: str, client_homepage_url: str, 
                 output_dir: str = "./ingestion/client_ingestion_outputs", 
                 workers: int = 4, credentials_file: str = "./service_account.json",
                 pdf_processor: str = "markitdown"):
        self.client_id = client_id
        self.drive_folder_id = drive_folder_id
        self.client_homepage_url = client_homepage_url
        self.output_dir = output_dir
        self.workers = workers
        self.credentials_file = credentials_file
        self.pdf_processor = pdf_processor
        
        # Client-specific directories
        self.client_output_dir = os.path.join(output_dir, client_id)
        self.client_intake_dir = os.path.join(self.client_output_dir, "client_intake_form")
        self.client_materials_dir = os.path.join(self.client_output_dir, "client_materials")
        self.website_dir = os.path.join(self.client_output_dir, "website")
        
        # Initialize Supabase vector store
        self.vector_store = None
        self._initialize_vector_store()
        
    def _initialize_vector_store(self):
        """Initialize Supabase vector store client"""
        load_dotenv()
        
        try:
            self.vector_store = SupabaseVectorStore()
            logger.info("✅ Supabase vector store initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Supabase vector store: {e}")
            raise
    
    def create_client_directories(self):
        """Create client-specific directory structure"""
        logger.info(f"📁 Creating directory structure for client: {self.client_id}")
        
        directories = [
            self.client_output_dir,
            self.client_intake_dir,
            self.client_materials_dir,
            self.website_dir
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            logger.info(f"📁 Created directory: {directory}")
    
    def create_client_record(self):
        """Create client record in Supabase"""
        logger.info(f"🏗️  Creating client record in Supabase: {self.client_id}")
        
        try:
            # Extract domain from homepage URL
            from urllib.parse import urlparse
            parsed = urlparse(self.client_homepage_url)
            primary_domain = parsed.netloc or self.client_homepage_url
            
            client_uuid = self.vector_store.ensure_client_exists(
                client_id=self.client_id,
                primary_domain=primary_domain,
                drive_folder_id=self.drive_folder_id
            )
            
            logger.info(f"✅ Client record created/verified: {client_uuid}")
            return client_uuid
            
        except Exception as e:
            logger.error(f"❌ Failed to create client record: {e}")
            raise
    
    async def run_website_ingestion(self, use_llm_categories: bool = True):
        """Run website content ingestion"""
        logger.info("🌐 Starting website ingestion...")
        
        try:
            result = await website_ingestion(
                url=self.client_homepage_url,
                output_dir=self.client_output_dir,
                client_name=self.client_id,
                workers=self.workers,
                use_llm_categories=use_llm_categories
            )
            logger.info(f"✅ Website ingestion completed: {result}")
            return result
        except Exception as e:
            logger.error(f"❌ Website ingestion failed: {e}")
            raise
    
    async def run_drive_ingestion(self, use_llm_categories: bool = True):
        """Run Google Drive content ingestion"""
        logger.info("📁 Starting Google Drive ingestion...")
        
        try:
            result = await drive_ingestion(
                folder_id=self.drive_folder_id,
                output_dir=self.client_output_dir,
                credentials_file=self.credentials_file,
                use_llm_categories=use_llm_categories
            )
            logger.info(f"✅ Drive ingestion completed: {result}")
            return result
        except Exception as e:
            logger.error(f"❌ Drive ingestion failed: {e}")
            raise
    
    def get_files_to_upload(self) -> List[Dict[str, str]]:
        """Discover all markdown files ready for upload"""
        logger.info("🔍 Discovering files to upload...")
        
        files_to_upload = []
        
        # Website files
        website_dir = Path(self.website_dir)
        if website_dir.exists():
            for md_file in website_dir.glob("*.md"):
                files_to_upload.append({
                    'path': str(md_file),
                    'source_type': 'website',
                    'content_type': self._detect_content_type(md_file, 'website')
                })
        
        # Client materials
        materials_dir = Path(self.client_materials_dir)
        if materials_dir.exists():
            for md_file in materials_dir.glob("*.md"):
                files_to_upload.append({
                    'path': str(md_file),
                    'source_type': 'client_materials',
                    'content_type': self._detect_content_type(md_file, 'client_materials')
                })
        
        # Client intake form
        intake_dir = Path(self.client_intake_dir)
        if intake_dir.exists():
            for md_file in intake_dir.glob("*.md"):
                files_to_upload.append({
                    'path': str(md_file),
                    'source_type': 'client_intake_form',
                    'content_type': 'client_intake_form'
                })
        
        logger.info(f"Found {len(files_to_upload)} files to upload")
        return files_to_upload
    
    def _detect_content_type(self, file_path: Path, source_type: str) -> str:
        """Detect content type from metadata or filename"""
        # Try to load metadata
        metadata_path = file_path.with_suffix('.md.metadata.json')
        
        if metadata_path.exists():
            try:
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                    return metadata.get('content_type', 'other')
            except:
                pass
        
        # Fallback to filename-based detection
        filename = file_path.stem.lower()
        
        if 'case' in filename or 'study' in filename:
            return 'case_studies'
        elif 'service' in filename or 'product' in filename:
            return 'services_products'
        elif 'blog' in filename or 'article' in filename:
            return 'blogs_resources'
        elif 'industry' in filename or 'market' in filename:
            return 'industries_markets'
        else:
            return 'other'
    
    def upload_files_to_supabase(self, files: List[Dict[str, str]]) -> tuple:
        """Upload files to Supabase with embeddings"""
        logger.info(f"☁️  Uploading {len(files)} files to Supabase...")
        
        successful_uploads = 0
        failed_uploads = 0
        
        for file_info in files:
            try:
                file_path = Path(file_info['path'])
                
                # Read content
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Skip empty files
                if not content.strip():
                    logger.warning(f"⚠️  Skipping empty file: {file_path.name}")
                    continue
                
                # Load metadata if available
                metadata_path = file_path.with_suffix('.md.metadata.json')
                metadata = {}
                if metadata_path.exists():
                    with open(metadata_path, 'r') as f:
                        metadata = json.load(f)
                
                # Extract title from content or filename
                title = metadata.get('title', file_path.stem)
                uri = metadata.get('url', metadata.get('uri', str(file_path)))
                
                # Upload to Supabase
                doc_id, chunk_count = self.vector_store.upload_document(
                    client_id=self.client_id,
                    content=content,
                    title=title,
                    uri=uri,
                    source_type=file_info['source_type'],
                    content_type=file_info['content_type'],
                    metadata=metadata
                )
                
                successful_uploads += 1
                logger.info(f"✅ Uploaded {file_path.name} → {doc_id} ({chunk_count} chunks)")
                
            except Exception as e:
                failed_uploads += 1
                logger.error(f"❌ Failed to upload {file_info['path']}: {e}")
        
        logger.info(f"Upload complete: {successful_uploads} succeeded, {failed_uploads} failed")
        return successful_uploads, failed_uploads
    
    def generate_onboarding_report(self, upload_stats: tuple) -> str:
        """Generate onboarding report"""
        successful_uploads, failed_uploads = upload_stats
        total_files = successful_uploads + failed_uploads
        
        # Get client stats from Supabase
        stats = self.vector_store.get_client_stats(self.client_id)
        
        report = {
            'client_id': self.client_id,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'files_processed': total_files,
            'successful_uploads': successful_uploads,
            'failed_uploads': failed_uploads,
            'database_stats': stats,
            'output_directory': str(self.client_output_dir)
        }
        
        report_file = os.path.join(self.client_output_dir, 'onboarding_report.json')
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"📊 Onboarding report saved: {report_file}")
        return report_file


async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Onboard new clients into Supabase Vector DB',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--client-id', help='Client ID (unique identifier)')
    parser.add_argument('--drive-folder-id', help='Google Drive folder ID')
    parser.add_argument('--client-homepage-url', help='Client homepage URL')
    parser.add_argument('--output-dir', default='ingestion/client_ingestion_outputs')
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--no-llm-categories', action='store_true')
    parser.add_argument('--pdf-processor', choices=['gpt', 'markitdown', 'pdfplumber'], default='markitdown')
    parser.add_argument('--credentials', default='./service_account.json')
    parser.add_argument('--batch-mode', action='store_true')
    
    args = parser.parse_args()
    
    # Interactive or batch mode
    if args.batch_mode or (args.client_id and args.drive_folder_id and args.client_homepage_url):
        if not (args.client_id and args.drive_folder_id and args.client_homepage_url):
            logger.error("❌ Batch mode requires --client-id, --drive-folder-id, and --client-homepage-url")
            return 1
        
        config = {
            'client_id': args.client_id,
            'drive_folder_id': args.drive_folder_id,
            'client_homepage_url': args.client_homepage_url,
            'output_dir': args.output_dir,
            'workers': args.workers,
            'use_llm_categories': not args.no_llm_categories,
            'pdf_processor': args.pdf_processor,
            'credentials': args.credentials
        }
    else:
        # Interactive mode (simplified for now)
        logger.error("Interactive mode: Please use batch mode with required arguments")
        return 1
    
    # Create onboarder
    onboarder = SupabaseClientOnboarder(
        client_id=config['client_id'],
        drive_folder_id=config['drive_folder_id'],
        client_homepage_url=config['client_homepage_url'],
        output_dir=config['output_dir'],
        workers=config['workers'],
        credentials_file=config['credentials'],
        pdf_processor=config['pdf_processor']
    )
    
    # Execute onboarding
    logger.info("📁 Creating directories...")
    onboarder.create_client_directories()
    
    logger.info("🏗️  Creating client record...")
    onboarder.create_client_record()
    
    logger.info("🔄 Running content ingestion...")
    website_task = onboarder.run_website_ingestion(config['use_llm_categories'])
    drive_task = onboarder.run_drive_ingestion(config['use_llm_categories'])
    
    await asyncio.gather(website_task, drive_task)
    
    logger.info("☁️  Uploading to Supabase...")
    files = onboarder.get_files_to_upload()
    upload_stats = onboarder.upload_files_to_supabase(files)
    
    logger.info("📊 Generating report...")
    report_file = onboarder.generate_onboarding_report(upload_stats)
    
    logger.info("✅ Onboarding complete!")
    logger.info(f"Report: {report_file}")
    
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
