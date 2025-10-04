#!/usr/bin/env python3
"""
PDF Reprocessing Script - Fix Failed PDF Extractions

This script scans for markdown files with PDF_PLACEHOLDER markers
and attempts to re-extract the content using alternative methods.

Usage:
    python reprocess_failed_pdfs.py --output-dir ./path/to/client/output
"""

import os
import sys
import json
import argparse
import logging
from pathlib import Path
from typing import List, Tuple, Dict, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FailedPDFReprocessor:
    """Handles reprocessing of failed PDF extractions"""
    
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.failed_files = []
        self.reprocessed_files = []
        self.still_failed = []
        
    def scan_for_failed_pdfs(self) -> List[Tuple[str, str, Dict]]:
        """
        Scan for markdown files containing PDF_PLACEHOLDER
        
        Returns:
            List of tuples: (md_file_path, file_id, metadata)
        """
        failed_pdfs = []
        
        # Search in client_materials directory
        materials_dir = self.output_dir / "client_materials"
        if not materials_dir.exists():
            logger.warning(f"Client materials directory not found: {materials_dir}")
            return failed_pdfs
        
        for md_file in materials_dir.glob("*.md"):
            try:
                content = md_file.read_text(encoding='utf-8')
                if 'PDF_PLACEHOLDER' in content:
                    # Load metadata
                    metadata_file = md_file.with_suffix('.md.metadata.json')
                    if metadata_file.exists():
                        with open(metadata_file, 'r') as f:
                            metadata = json.load(f)
                        file_id = metadata.get('file_id', '')
                        failed_pdfs.append((str(md_file), file_id, metadata))
                    else:
                        logger.warning(f"Metadata file not found for {md_file}")
            except Exception as e:
                logger.error(f"Error processing {md_file}: {e}")
        
        return failed_pdfs
    
    def reprocess_failed_pdf(self, md_file_path: str, file_id: str, metadata: Dict, 
                           method: str = 'auto', credentials_file: str = './service_account.json'):
        """
        Attempt to reprocess a failed PDF
        
        Args:
            md_file_path: Path to the markdown file with PDF_PLACEHOLDER
            file_id: Google Drive file ID
            metadata: Original metadata dict
            method: Processing method ('auto', 'pdfplumber', 'markitdown', 'gpt')
            credentials_file: Path to service account credentials
        """
        logger.info(f"Reprocessing: {Path(md_file_path).name}")
        
        try:
            # Import PDF processors
            from ingest_specific_drive_folder import (
                extract_pdf_with_pdfplumber,
                extract_pdf_with_markitdown,
                extract_pdf_with_gpt,
                download_drive_file
            )
            from google.oauth2 import service_account
            from googleapiclient.discovery import build
            
            # Initialize Drive API
            SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
            creds = service_account.Credentials.from_service_account_file(
                credentials_file, scopes=SCOPES
            )
            service = build('drive', 'v3', credentials=creds)
            
            # Download the PDF file
            pdf_content = download_drive_file(service, file_id)
            if not pdf_content:
                logger.error(f"Failed to download file {file_id}")
                self.still_failed.append(md_file_path)
                return
            
            # Try extraction methods in order
            extracted_text = None
            
            if method == 'auto':
                # Try MarkItDown first (best balance), then pdfplumber, then GPT
                methods = ['markitdown', 'pdfplumber', 'gpt']
            else:
                methods = [method]
            
            for extraction_method in methods:
                try:
                    if extraction_method == 'markitdown':
                        extracted_text = extract_pdf_with_markitdown(pdf_content)
                    elif extraction_method == 'pdfplumber':
                        extracted_text = extract_pdf_with_pdfplumber(pdf_content)
                    elif extraction_method == 'gpt':
                        extracted_text = extract_pdf_with_gpt(pdf_content, metadata.get('original_filename', ''))
                    
                    if extracted_text and len(extracted_text.strip()) > 100:
                        logger.info(f"✅ Successfully extracted with {extraction_method}")
                        break
                except Exception as e:
                    logger.warning(f"Method {extraction_method} failed: {e}")
                    continue
            
            if not extracted_text or len(extracted_text.strip()) <= 100:
                logger.error(f"All extraction methods failed for {md_file_path}")
                self.still_failed.append(md_file_path)
                return
            
            # Update the markdown file
            md_path = Path(md_file_path)
            md_path.write_text(extracted_text, encoding='utf-8')
            
            # Update metadata
            metadata['reprocessed_at'] = datetime.utcnow().isoformat() + 'Z'
            metadata['extraction_method'] = extraction_method
            metadata_path = md_path.with_suffix('.md.metadata.json')
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            self.reprocessed_files.append(md_file_path)
            logger.info(f"✅ Successfully reprocessed: {md_path.name}")
            
        except Exception as e:
            logger.error(f"Error reprocessing {md_file_path}: {e}")
            self.still_failed.append(md_file_path)
    
    def generate_report(self):
        """Generate and display reprocessing report"""
        print("\n" + "=" * 80)
        print("PDF RE-PROCESSING REPORT")
        print("=" * 80)
        print(f"Total files scanned: {len(self.failed_files)}")
        print(f"Successfully reprocessed: {len(self.reprocessed_files)}")
        print(f"Still failed: {len(self.still_failed)}")
        
        if self.reprocessed_files:
            print("\n✅ Successfully Reprocessed:")
            for file_path in self.reprocessed_files:
                print(f"  • {Path(file_path).name}")
        
        if self.still_failed:
            print("\n❌ Still Failed:")
            for file_path in self.still_failed:
                print(f"  • {Path(file_path).name}")
        
        print("=" * 80)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Reprocess failed PDF extractions'
    )
    parser.add_argument('--output-dir', required=True,
                       help='Client output directory containing failed PDFs')
    parser.add_argument('--method', choices=['auto', 'pdfplumber', 'markitdown', 'gpt'],
                       default='auto', help='Extraction method (default: auto)')
    parser.add_argument('--credentials', default='./service_account.json',
                       help='Path to service account JSON')
    
    args = parser.parse_args()
    
    # Initialize reprocessor
    reprocessor = FailedPDFReprocessor(output_dir=args.output_dir)
    
    # Scan for failed PDFs
    logger.info("🔍 Scanning for failed PDFs...")
    failed_pdfs = reprocessor.scan_for_failed_pdfs()
    reprocessor.failed_files = [{'file': Path(f[0]).name, 'file_id': f[1]} for f in failed_pdfs]
    
    if not failed_pdfs:
        logger.info("✅ No failed PDFs found!")
        return 0
    
    logger.info(f"Found {len(failed_pdfs)} failed PDF(s)")
    
    # Reprocess each failed PDF
    for md_file_path, file_id, metadata in failed_pdfs:
        reprocessor.reprocess_failed_pdf(
            md_file_path, file_id, metadata, 
            method=args.method,
            credentials_file=args.credentials
        )
    
    # Generate report
    reprocessor.generate_report()
    
    # Return exit code
    if reprocessor.still_failed:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
