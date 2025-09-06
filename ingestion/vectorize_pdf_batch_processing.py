import os
import time
import json
import glob
import urllib3
import argparse
import vectorize_client as v
from dotenv import load_dotenv
from pathlib import Path

def load_processing_log(log_file="vectorize_processing_log.json"):
    """Load the processing log from JSON file, create if it doesn't exist"""
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            print(f"⚠️  Warning: Could not read {log_file}, starting fresh")
            return {}
    else:
        print(f"📝 Creating new processing log: {log_file}")
        return {}

def save_processing_log(log_data, log_file="vectorize_processing_log.json"):
    """Save the processing log to JSON file"""
    try:
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
        return True
    except IOError as e:
        print(f"❌ Error saving log file: {e}")
        return False

def find_pdf_files(directory):
    """Find all PDF files in the specified directory"""
    pdf_pattern = os.path.join(directory, "*.pdf")
    pdf_files = glob.glob(pdf_pattern)
    return pdf_files

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Batch process PDF files using vectorize.io API')
    parser.add_argument('--input', '-i', 
                       default='ingestion/input', 
                       help='Input directory containing PDF files (default: input)')
    parser.add_argument('--output', '-o', 
                       default='ingestion/output', 
                       help='Output directory for extracted text files (default: output)')
    
    args = parser.parse_args()
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Configuration
    input_directory = args.input
    output_directory = args.output
    log_file = "vectorize_processing_log.json"
    
    # Check for required environment variables
    api_key = os.environ.get("VECTORIZE_API_KEY")
    organization_id = os.environ.get("VECTORIZE_ORGANIZATION_ID")
    
    if not api_key:
        print("❌ Error: VECTORIZE_API_KEY not found in environment or .env file.")
        print("Please either:")
        print("  1. Add VECTORIZE_API_KEY=your-api-key-here to your .env file, OR")
        print("  2. Set environment variable: export VECTORIZE_API_KEY='your-api-key-here'")
        return
    
    if not organization_id:
        print("❌ Error: VECTORIZE_ORGANIZATION_ID not found in environment or .env file.")
        print("Please either:")
        print("  1. Add VECTORIZE_ORGANIZATION_ID=your-org-id-here to your .env file, OR") 
        print("  2. Set environment variable: export VECTORIZE_ORGANIZATION_ID='your-org-id-here'")
        return
    
    print(f"🔑 Using API key: {api_key[:8]}..." if len(api_key) > 8 else "🔑 API key set")
    print(f"🏢 Organization ID: {organization_id}")
    print(f"📂 Input directory: {input_directory}")
    print(f"📁 Output directory: {output_directory}")

    # Load processing log
    processing_log = load_processing_log(log_file)
    
    # Find PDF files
    pdf_files = find_pdf_files(input_directory)
    if not pdf_files:
        print(f"❌ No PDF files found in {input_directory}")
        return
    
    print(f"📋 Found {len(pdf_files)} PDF files to process")

    # Initialize the API client  
    config = v.Configuration(host="https://api.vectorize.io/v1")
    apiClient = v.ApiClient(config)
    
    # Set the Authorization header manually (the library doesn't handle Bearer tokens automatically)
    apiClient.set_default_header('Authorization', f'Bearer {api_key}')
    
    print(f"🔗 API client configured with Authorization header")

    # Create API instances
    files_api = v.FilesApi(apiClient)
    extraction_api = v.ExtractionApi(apiClient)
    
    # Phase 1: Upload all PDF files
    print(f"\n🚀 PHASE 1: Uploading {len(pdf_files)} PDF files...")
    upload_results = {}
    content_type = "application/pdf"
    http = urllib3.PoolManager()
    
    for i, file_path in enumerate(pdf_files, 1):
        file_name = os.path.basename(file_path)
        print(f"\n📄 [{i}/{len(pdf_files)}] Processing: {file_name}")
        print(f"📁 File size: {os.path.getsize(file_path):,} bytes")
        
        # Check if already processed
        if file_name in processing_log:
            print(f"⏭️  File already in log with extraction ID: {processing_log[file_name]}")
            upload_results[file_name] = processing_log[file_name]
            continue
        
        try:
            # Start file upload
            print("⬆️  Starting file upload...")
            start_file_upload_response = files_api.start_file_upload(
                organization_id, 
                start_file_upload_request=v.StartFileUploadRequest(
                    content_type=content_type,
                    name=file_name,
                )
            )
            
            # Upload the file
            print("📤 Uploading file to vectorize.io...")
            with open(file_path, "rb") as f:
                response = http.request(
                    "PUT", 
                    start_file_upload_response.upload_url, 
                    body=f, 
                    headers={
                        "Content-Type": content_type, 
                        "Content-Length": str(os.path.getsize(file_path))
                    }
                )
                if response.status != 200:
                    print(f"❌ Upload failed with status {response.status}: {response.data}")
                    continue
                else:
                    print("✅ Upload successful!")
            
            # Start extraction
            print("🔄 Starting text extraction...")
            extraction_response = extraction_api.start_extraction(
                organization_id, 
                start_extraction_request=v.StartExtractionRequest(
                    file_id=start_file_upload_response.file_id
                )
            )
            extraction_id = extraction_response.extraction_id
            print(f"📝 Extraction ID: {extraction_id}")
            
            # Update log and save
            processing_log[file_name] = extraction_id
            upload_results[file_name] = extraction_id
            save_processing_log(processing_log, log_file)
            
        except Exception as e:
            print(f"❌ Error processing {file_name}: {e}")
            continue
    
    # Phase 2: Wait for all extractions to complete
    print(f"\n⏳ PHASE 2: Waiting for {len(upload_results)} extractions to complete...")
    
    completed_extractions = {}
    pending_extractions = upload_results.copy()
    
    while pending_extractions:
        print(f"📊 Checking {len(pending_extractions)} pending extractions...")
        
        for file_name, extraction_id in list(pending_extractions.items()):
            try:
                response = extraction_api.get_extraction_result(organization_id, extraction_id)
                if response.ready:
                    if response.data.success:
                        print(f"✅ {file_name}: Extraction completed successfully!")
                        completed_extractions[file_name] = response.data.text
                        del pending_extractions[file_name]
                    else:
                        print(f"❌ {file_name}: Extraction failed - {response.data.error}")
                        del pending_extractions[file_name]
                else:
                    print(f"⏳ {file_name}: Still processing...")
                    
            except Exception as e:
                print(f"❌ Error checking {file_name}: {e}")
                del pending_extractions[file_name]
        
        if pending_extractions:
            print(f"⏱️  Waiting 5 seconds before next check...")
            time.sleep(5)
    
    # Summary
    print(f"\n🎉 PROCESSING COMPLETE!")
    print(f"📊 Total files processed: {len(pdf_files)}")
    print(f"✅ Successful extractions: {len(completed_extractions)}")
    print(f"📝 Log file updated: {log_file}")
    
    # Optionally save extracted text to files
    if completed_extractions:
        os.makedirs(output_directory, exist_ok=True)
        print(f"\n💾 Saving extracted text to {output_directory}/")
        
        for file_name, text_content in completed_extractions.items():
            output_file = os.path.join(output_directory, f"{Path(file_name).stem}.txt")
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(text_content)
                print(f"💾 Saved: {output_file}")
            except Exception as e:
                print(f"❌ Error saving {output_file}: {e}")


if __name__ == "__main__":
    main()
