#!/usr/bin/env python3
"""
New Client Ingestion Script

This comprehensive script onboards new clients into Vectara by:
1. Creating a new corpus with proper metadata structure
2. Ingesting client website content 
3. Ingesting client materials from Google Drive
4. Uploading all processed documents to the Vectara corpus

Usage:
    # Interactive mode (recommended) - prompts for all inputs:
    python new_client_ingestion.py
    
    # Batch mode - provide all arguments via command line:
    python new_client_ingestion.py --batch-mode --client-id "client-name" --drive-folder-id "1ABC123..." --client-homepage-url "https://example.com"

Interactive Mode:
    Simply run the script and it will prompt you for:
    - Client ID (unique identifier)
    - Google Drive folder ID or URL
    - Client homepage URL
    - Optional settings (output directory, workers, LLM categorization, etc.)

Batch Mode Arguments:
    --batch-mode: Enable non-interactive batch mode (requires all other arguments)
    --client-id: Unique identifier for the client
    --drive-folder-id: Google Drive folder ID containing client materials
    --client-homepage-url: Client's website homepage URL
    --output-dir: Base output directory (default: ./ingestion/client_ingestion_outputs)
    --workers: Number of parallel workers for website scraping (default: 4)
    --no-llm-categories: Disable LLM categorization
    --credentials: Path to Google service account JSON file (default: ./service_account.json)
"""

import os
import sys
import argparse
import logging
import json
import asyncio
import shutil
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Import Vectara SDK
from vectara import Vectara
from vectara.core.api_error import ApiError

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

class VectaraClientOnboarder:
    """Handles the complete client onboarding process into Vectara"""
    
    def __init__(self, client_id: str, drive_folder_id: str, client_homepage_url: str, 
                 output_dir: str = "./ingestion/client_ingestion_outputs", 
                 workers: int = 4, credentials_file: str = "./service_account.json"):
        self.client_id = client_id
        self.drive_folder_id = drive_folder_id
        self.client_homepage_url = client_homepage_url
        self.output_dir = output_dir
        self.workers = workers
        self.credentials_file = credentials_file
        
        # Client-specific directories
        self.client_output_dir = os.path.join(output_dir, client_id)
        self.client_intake_dir = os.path.join(self.client_output_dir, "client_intake_form")
        self.client_materials_dir = os.path.join(self.client_output_dir, "client_materials")
        self.website_dir = os.path.join(self.client_output_dir, "website")
        
        # Initialize Vectara client
        self.vectara_client = None
        self._initialize_vectara_client()
        
    def _initialize_vectara_client(self):
        """Initialize Vectara client with API key"""
        load_dotenv()
        api_key = os.getenv('VECTARA_API_KEY')
        
        if not api_key:
            logger.error("❌ VECTARA_API_KEY not found in environment variables")
            raise ValueError("VECTARA_API_KEY is required")
        
        try:
            self.vectara_client = Vectara(api_key=api_key)
            logger.info("✅ Vectara client initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Vectara client: {e}")
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
    
    def create_vectara_corpus(self):
        """Create a new Vectara corpus for the client"""
        logger.info(f"🏗️  Creating Vectara corpus for client: {self.client_id}")
        
        corpus_config = {
            "key": self.client_id,
            "name": self.client_id,
            "description": "Knowledge base for the given client",
            "enabled": True,
            "queries_are_answers": False,
            "documents_are_questions": False,
            "encoder_name": "boomerang-2023-q3",
            "save_history": False,
            "filter_attributes": [
                {
                    "name": "content_type",
                    "level": "document",
                    "description": "content_type: case_studies, client_intake_form, services_products, blogs_resources, industries_markets, other",
                    "indexed": True,
                    "type": "text"
                },
                {
                    "name": "is_title",
                    "level": "part",
                    "description": "True if the text is a title.",
                    "indexed": True,
                    "type": "boolean"
                },
                {
                    "name": "lang",
                    "level": "part",
                    "description": "Detected language, as an ISO 639-3 code.",
                    "indexed": True,
                    "type": "text"
                },
                {
                    "name": "source",
                    "level": "document",
                    "description": "document source type: website, client_intake_form, client_materials, other",
                    "indexed": True,
                    "type": "text"
                }
            ]
        }
        
        try:
            response = self.vectara_client.corpora.create(
                key=corpus_config["key"],
                name=corpus_config["name"],
                description=corpus_config["description"],
                filter_attributes=corpus_config["filter_attributes"]
            )
            logger.info(f"✅ Successfully created corpus: {self.client_id}")
            return response
        except ApiError as e:
            if "already exists" in str(e).lower():
                logger.warning(f"⚠️  Corpus {self.client_id} already exists, continuing...")
                return {"key": self.client_id}
            else:
                logger.error(f"❌ Failed to create corpus: {e}")
                raise
        except Exception as e:
            logger.error(f"❌ Unexpected error creating corpus: {e}")
            raise
    
    async def run_website_ingestion(self, use_llm_categories: bool = True):
        """Run website content ingestion"""
        logger.info(f"🌐 Starting website ingestion for: {self.client_homepage_url}")
        
        # Prepare arguments for website ingestion
        website_args = [
            "--url", self.client_homepage_url,
            "--output-dir", self.client_output_dir,
            "--workers", str(self.workers),
            "--client-name", self.client_id
        ]
        
        if not use_llm_categories:
            website_args.append("--no-llm-categories")
        
        # Temporarily modify sys.argv to pass arguments to the website ingestion script
        original_argv = sys.argv.copy()
        try:
            sys.argv = ["ingest_client_website.py"] + website_args
            result = await website_ingestion()
            logger.info("✅ Website ingestion completed successfully")
            return result
        except Exception as e:
            logger.error(f"❌ Website ingestion failed: {e}")
            raise
        finally:
            sys.argv = original_argv
    
    async def run_drive_ingestion(self, use_llm_categories: bool = True):
        """Run Google Drive content ingestion"""
        logger.info(f"💾 Starting Google Drive ingestion for folder: {self.drive_folder_id}")
        
        # Prepare arguments for drive ingestion
        drive_args = [
            "--folder-id", self.drive_folder_id,
            "--output-dir", self.client_output_dir,
            "--credentials", self.credentials_file
        ]
        
        if not use_llm_categories:
            drive_args.append("--no-llm-categories")
        
        # Temporarily modify sys.argv to pass arguments to the drive ingestion script
        original_argv = sys.argv.copy()
        try:
            sys.argv = ["ingest_specific_drive_folder.py"] + drive_args
            result = await drive_ingestion()
            logger.info("✅ Google Drive ingestion completed successfully")
            return result
        except Exception as e:
            logger.error(f"❌ Google Drive ingestion failed: {e}")
            raise
        finally:
            sys.argv = original_argv
    
    def get_files_to_upload(self) -> List[Dict]:
        """Get all files that need to be uploaded to Vectara"""
        files_to_upload = []
        
        # Process client_intake_form files
        if os.path.exists(self.client_intake_dir):
            for filename in os.listdir(self.client_intake_dir):
                if filename.endswith('.md') and not filename.endswith('.metadata.json'):
                    file_path = os.path.join(self.client_intake_dir, filename)
                    metadata_path = file_path + '.metadata.json'
                    
                    # Load metadata if it exists
                    metadata = {}
                    if os.path.exists(metadata_path):
                        with open(metadata_path, 'r') as f:
                            metadata = json.load(f)
                    
                    files_to_upload.append({
                        'file_path': file_path,
                        'filename': f"{self.client_id}_client_intake_form",
                        'source': 'client_intake_form',
                        'content_type': 'client_intake_form',  # Always set to client_intake_form
                        'created_at': metadata.get('created_at', datetime.now().isoformat()),
                        'last_updated_at': metadata.get('last_updated', datetime.now().isoformat()),
                        'metadata': metadata
                    })
        
        # Process client_materials files
        if os.path.exists(self.client_materials_dir):
            for filename in os.listdir(self.client_materials_dir):
                if filename.endswith('.md') and not filename.endswith('.metadata.json'):
                    file_path = os.path.join(self.client_materials_dir, filename)
                    metadata_path = file_path + '.metadata.json'
                    
                    # Load metadata if it exists
                    metadata = {}
                    if os.path.exists(metadata_path):
                        with open(metadata_path, 'r') as f:
                            metadata = json.load(f)
                    
                    # Use the filename from metadata if available, otherwise use the actual filename
                    upload_filename = metadata.get('name', filename).lower()
                    if not upload_filename.endswith('.md'):
                        upload_filename = os.path.splitext(upload_filename)[0] + '.md'
                    
                    files_to_upload.append({
                        'file_path': file_path,
                        'filename': upload_filename,
                        'source': 'client_materials',
                        'content_type': metadata.get('content_type', 'other'),
                        'created_at': metadata.get('created_at', datetime.now().isoformat()),
                        'last_updated_at': metadata.get('last_updated', datetime.now().isoformat()),
                        'metadata': metadata
                    })
        
        # Process website files
        if os.path.exists(self.website_dir):
            for filename in os.listdir(self.website_dir):
                if filename.endswith('.md'):
                    file_path = os.path.join(self.website_dir, filename)
                    
                    # For website files, extract metadata from frontmatter if present
                    metadata = self._extract_frontmatter_metadata(file_path)
                    
                    files_to_upload.append({
                        'file_path': file_path,
                        'filename': filename,
                        'source': 'website',
                        'content_type': metadata.get('content_type', 'other'),
                        'created_at': metadata.get('scraped_time', datetime.now().isoformat()),
                        'last_updated_at': metadata.get('scraped_time', datetime.now().isoformat()),
                        'metadata': metadata
                    })
        
        logger.info(f"📊 Found {len(files_to_upload)} files to upload to Vectara")
        return files_to_upload
    
    def _extract_frontmatter_metadata(self, file_path: str) -> Dict:
        """Extract metadata from markdown frontmatter"""
        metadata = {}
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if content.startswith('---\n'):
                # Extract frontmatter
                parts = content.split('---\n', 2)
                if len(parts) >= 2:
                    frontmatter_lines = parts[1].strip().split('\n')
                    for line in frontmatter_lines:
                        if ':' in line:
                            key, value = line.split(':', 1)
                            key = key.strip()
                            value = value.strip().strip('"')
                            metadata[key] = value
        except Exception as e:
            logger.warning(f"⚠️  Could not extract frontmatter from {file_path}: {e}")
        
        return metadata
    
    def upload_files_to_vectara(self, files_to_upload: List[Dict]):
        """Upload all processed files to the Vectara corpus"""
        logger.info(f"⬆️  Starting upload of {len(files_to_upload)} files to Vectara corpus: {self.client_id}")
        
        successful_uploads = 0
        failed_uploads = 0
        
        for i, file_info in enumerate(files_to_upload, 1):
            try:
                file_path = file_info['file_path']
                filename = file_info['filename']
                
                logger.info(f"⬆️  Uploading file {i}/{len(files_to_upload)}: {filename}")
                
                # Read file content
                with open(file_path, 'rb') as f:
                    file_content = f.read()
                
                # Prepare metadata for Vectara
                vectara_metadata = {
                    "source": file_info['source'],
                    "content_type": file_info['content_type'],
                    "created_at": file_info['created_at'],
                    "last_updated_at": file_info['last_updated_at'],
                    "client_id": self.client_id,
                    "upload_timestamp": datetime.now().isoformat(),
                    "file_size_bytes": len(file_content)
                }
                
                # Ensure client intake forms always have the correct metadata fields
                if file_info['source'] == 'client_intake_form':
                    vectara_metadata["source"] = "client_intake_form"
                    vectara_metadata["content_type"] = "client_intake_form"
                
                # Add any additional metadata from the original file
                if 'metadata' in file_info and file_info['metadata']:
                    for key, value in file_info['metadata'].items():
                        if key not in vectara_metadata and isinstance(value, (str, int, float, bool)):
                            vectara_metadata[key] = value
                
                # Prepare upload configuration
                upload_config = {
                    "corpus_key": self.client_id,
                    "file": file_content,
                    "filename": filename,
                    "metadata": vectara_metadata
                }
                
                # Only enable table extraction for PDF files
                if filename.lower().endswith('.pdf'):
                    upload_config["table_extraction_config"] = {"extract_tables": True}
                
                # Upload to Vectara
                response = self.vectara_client.upload.file(**upload_config)
                
                successful_uploads += 1
                logger.info(f"✅ Successfully uploaded: {filename} [{file_info['source']}]")
                
            except Exception as e:
                failed_uploads += 1
                logger.error(f"❌ Failed to upload {file_info.get('filename', 'unknown')}: {e}")
        
        logger.info(f"📊 Upload summary: {successful_uploads} successful, {failed_uploads} failed")
        return successful_uploads, failed_uploads
    
    def generate_onboarding_report(self, upload_stats: tuple):
        """Generate a comprehensive onboarding report"""
        successful_uploads, failed_uploads = upload_stats
        
        report = {
            "client_onboarding_summary": {
                "client_id": self.client_id,
                "timestamp": datetime.now().isoformat(),
                "corpus_created": True,
                "website_url": self.client_homepage_url,
                "drive_folder_id": self.drive_folder_id,
                "output_directory": self.client_output_dir,
                "upload_statistics": {
                    "successful_uploads": successful_uploads,
                    "failed_uploads": failed_uploads,
                    "total_files_processed": successful_uploads + failed_uploads
                },
                "directories_created": [
                    self.client_intake_dir,
                    self.client_materials_dir,
                    self.website_dir
                ]
            }
        }
        
        report_file = os.path.join(self.client_output_dir, 'onboarding_report.json')
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"📋 Onboarding report saved: {report_file}")
        return report_file

def get_user_inputs():
    """Interactively collect user inputs for client onboarding"""
    print("\n🚀 Welcome to Vectara Client Onboarding!")
    print("=" * 50)
    print("Please provide the following information:\n")
    
    # Get client ID
    while True:
        client_id = input("👤 Client ID (unique identifier, alphanumeric with hyphens/underscores): ").strip()
        if client_id and all(c.isalnum() or c in '-_' for c in client_id):
            break
        print("❌ Please enter a valid client ID (alphanumeric characters, hyphens, and underscores only)")
    
    # Get Drive folder ID
    while True:
        drive_input = input("💾 Google Drive folder ID or URL: ").strip()
        if not drive_input:
            print("❌ Please enter a Google Drive folder ID or URL")
            continue
            
        # Extract folder ID from URL if provided
        try:
            if drive_input.startswith('http'):
                if '/folders/' in drive_input:
                    drive_folder_id = drive_input.split('/folders/')[1].split('?')[0].split('#')[0]
                else:
                    print("❌ Invalid Google Drive folder URL format")
                    continue
            else:
                drive_folder_id = drive_input
            break
        except Exception:
            print("❌ Invalid Google Drive folder ID or URL")
    
    # Get client homepage URL
    while True:
        homepage_url = input("🌐 Client homepage URL (e.g., https://example.com): ").strip()
        if not homepage_url:
            print("❌ Please enter a homepage URL")
            continue
            
        # Add https:// if no protocol specified
        if not homepage_url.startswith(('http://', 'https://')):
            homepage_url = 'https://' + homepage_url
        
        # Basic URL validation
        try:
            from urllib.parse import urlparse
            result = urlparse(homepage_url)
            if result.scheme and result.netloc:
                break
            else:
                print("❌ Please enter a valid URL")
        except Exception:
            print("❌ Please enter a valid URL")
    
    print("\n⚙️  Optional Settings (press Enter for defaults):")
    
    # Get output directory
    output_dir = input(f"📁 Output directory [./ingestion/client_ingestion_outputs]: ").strip()
    if not output_dir:
        output_dir = './ingestion/client_ingestion_outputs'
    
    # Get number of workers
    while True:
        workers_input = input("⚡ Number of parallel workers for website scraping [4]: ").strip()
        if not workers_input:
            workers = 4
            break
        try:
            workers = int(workers_input)
            if workers > 0:
                break
            else:
                print("❌ Please enter a positive number")
        except ValueError:
            print("❌ Please enter a valid number")
    
    # Get LLM categorization preference
    llm_choice = input("🤖 Enable LLM categorization for better content organization? [Y/n]: ").strip().lower()
    use_llm_categories = llm_choice != 'n' and llm_choice != 'no'
    
    # Get credentials file path
    credentials = input("🔑 Path to Google service account JSON file [./service_account.json]: ").strip()
    if not credentials:
        credentials = './service_account.json'
    
    print("\n📋 Configuration Summary:")
    print("-" * 30)
    print(f"👤 Client ID: {client_id}")
    print(f"🌐 Website URL: {homepage_url}")
    print(f"💾 Drive Folder ID: {drive_folder_id}")
    print(f"📁 Output Directory: {output_dir}")
    print(f"⚡ Workers: {workers}")
    print(f"🤖 LLM Categorization: {'Enabled' if use_llm_categories else 'Disabled'}")
    print(f"🔑 Credentials: {credentials}")
    
    # Confirm before proceeding
    while True:
        confirm = input("\n✅ Proceed with client onboarding? [Y/n]: ").strip().lower()
        if confirm in ['', 'y', 'yes']:
            break
        elif confirm in ['n', 'no']:
            print("❌ Onboarding cancelled by user")
            return None
        else:
            print("❌ Please enter 'y' or 'n'")
    
    return {
        'client_id': client_id,
        'drive_folder_id': drive_folder_id,
        'client_homepage_url': homepage_url,
        'output_dir': output_dir,
        'workers': workers,
        'use_llm_categories': use_llm_categories,
        'credentials': credentials
    }

async def main():
    """Main function to orchestrate the client onboarding process"""
    parser = argparse.ArgumentParser(
        description='Onboard a new client into Vectara with comprehensive content ingestion',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    # Make all arguments optional - if not provided, will prompt interactively
    parser.add_argument('--client-id',
                       help='Unique identifier for the client (will be used as corpus key)')
    parser.add_argument('--drive-folder-id',
                       help='Google Drive folder ID containing client materials')
    parser.add_argument('--client-homepage-url',
                       help='Client website homepage URL for content scraping')
    parser.add_argument('--output-dir', default='./ingestion/client_ingestion_outputs',
                       help='Base output directory (default: ./ingestion/client_ingestion_outputs)')
    parser.add_argument('--workers', type=int, default=4,
                       help='Number of parallel workers for website scraping (default: 4)')
    parser.add_argument('--no-llm-categories', action='store_true',
                       help='Disable LLM categorization for content')
    parser.add_argument('--credentials', default='./service_account.json',
                       help='Path to Google service account JSON file (default: ./service_account.json)')
    parser.add_argument('--batch-mode', action='store_true',
                       help='Run in batch mode without interactive prompts (requires all arguments)')
    
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    
    # Check if we have all required arguments for batch mode
    if args.batch_mode or (args.client_id and args.drive_folder_id and args.client_homepage_url):
        # Use command line arguments
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
            'credentials': args.credentials
        }
        
        logger.info("🚀 Starting New Client Onboarding Process (Batch Mode)")
    else:
        # Interactive mode - prompt for inputs
        config = get_user_inputs()
        if config is None:
            return 1
        
        logger.info("🚀 Starting New Client Onboarding Process (Interactive Mode)")
    
    logger.info(f"👤 Client ID: {config['client_id']}")
    logger.info(f"🌐 Website URL: {config['client_homepage_url']}")
    logger.info(f"💾 Drive Folder ID: {config['drive_folder_id']}")
    logger.info(f"📁 Output Directory: {config['output_dir']}")
    logger.info(f"⚡ Workers: {config['workers']}")
    logger.info(f"🤖 LLM Categorization: {'Enabled' if config['use_llm_categories'] else 'Disabled'}")
    
    try:
        # Initialize the onboarder
        onboarder = VectaraClientOnboarder(
            client_id=config['client_id'],
            drive_folder_id=config['drive_folder_id'],
            client_homepage_url=config['client_homepage_url'],
            output_dir=config['output_dir'],
            workers=config['workers'],
            credentials_file=config['credentials']
        )
        
        # Step 0: Create directory structure
        logger.info("\n🏗️  STEP 0: Setting up directory structure...")
        onboarder.create_client_directories()
        
        # Step 1: Create Vectara corpus
        logger.info("\n🏗️  STEP 1: Creating Vectara corpus...")
        onboarder.create_vectara_corpus()
        
        # Step 2: Run content ingestion in parallel
        logger.info("\n📥 STEP 2: Running content ingestion...")
        
        # Run website and drive ingestion concurrently
        website_task = onboarder.run_website_ingestion(config['use_llm_categories'])
        drive_task = onboarder.run_drive_ingestion(config['use_llm_categories'])
        
        website_result, drive_result = await asyncio.gather(website_task, drive_task)
        
        # Step 3: Upload all files to Vectara
        logger.info("\n⬆️  STEP 3: Uploading documents to Vectara...")
        files_to_upload = onboarder.get_files_to_upload()
        upload_stats = onboarder.upload_files_to_vectara(files_to_upload)
        
        # Step 4: Generate final report
        logger.info("\n📋 STEP 4: Generating onboarding report...")
        report_file = onboarder.generate_onboarding_report(upload_stats)
        
        # Final summary
        successful_uploads, failed_uploads = upload_stats
        logger.info(f"\n🎉 CLIENT ONBOARDING COMPLETE!")
        logger.info(f"👤 Client: {config['client_id']}")
        logger.info(f"🏗️  Corpus created: ✅")
        logger.info(f"🌐 Website ingestion: ✅")
        logger.info(f"💾 Drive ingestion: ✅")
        logger.info(f"⬆️  Files uploaded: {successful_uploads}")
        logger.info(f"❌ Upload failures: {failed_uploads}")
        logger.info(f"📋 Report: {report_file}")
        logger.info(f"📂 Client data: {onboarder.client_output_dir}")
        
        return 0
        
    except KeyboardInterrupt:
        logger.info("🛑 Onboarding interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"❌ Onboarding failed: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
