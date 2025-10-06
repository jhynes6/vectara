import os
import json
import glob
import argparse
import time
import base64
import io
from pathlib import Path
from dotenv import load_dotenv
from pdf2image import convert_from_path
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
from pdfminer.high_level import extract_text
from openai import OpenAI
import concurrent.futures
from tqdm import tqdm

def load_processing_log(log_file="pdf_gpt_processing_log.json"):
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

def save_processing_log(log_data, log_file="pdf_gpt_processing_log.json"):
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

def convert_doc_to_images(path):
    """Convert PDF to images"""
    try:
        images = convert_from_path(path)
        return images
    except Exception as e:
        print(f"❌ Error converting PDF to images: {e}")
        return []

def extract_text_from_doc(path):
    """Extract text from PDF using pdfminer"""
    try:
        text = extract_text(path)
        return text
    except Exception as e:
        print(f"❌ Error extracting text: {e}")
        return ""

def get_img_uri(img):
    """Convert PIL image to base64 data URI"""
    png_buffer = io.BytesIO()
    img.save(png_buffer, format="PNG")
    png_buffer.seek(0)
    base64_png = base64.b64encode(png_buffer.read()).decode('utf-8')
    data_uri = f"data:image/png;base64,{base64_png}"
    return data_uri

def analyze_image(client, data_uri):
    """Analyze image with GPT-4o"""
    system_prompt = '''
You will be provided with an image of a PDF page or a slide. Your goal is to deliver a detailed and engaging presentation about the content you see, using clear and accessible language suitable for a 101-level audience.

If there is an identifiable title, start by stating the title to provide context for your audience.

Describe visual elements in detail:
- **Diagrams**: Explain each component and how they interact. For example, "The process begins with X, which then leads to Y and results in Z."
- **Tables**: Break down the information logically. For instance, "Product A costs X dollars, while Product B is priced at Y dollars."

Focus on the content itself rather than the format:
- **DO NOT** include terms referring to the content format.
- **DO NOT** mention the content type. Instead, directly discuss the information presented.

Keep your explanation comprehensive yet concise:
- Be exhaustive in describing the content, as your audience cannot see the image.
- Exclude irrelevant details such as page numbers or the position of elements on the image.

Use clear and accessible language:
- Explain technical terms or concepts in simple language appropriate for a 101-level audience.

Engage with the content:
- Interpret and analyze the information where appropriate, offering insights to help the audience understand its significance.

------

If there is an identifiable title, present the output in the following format:
{TITLE}

{Content description}

If there is no clear title, simply provide the content description.
'''

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": data_uri
                            }
                        }
                    ]
                },
            ],
            max_tokens=500,
            temperature=0,
            top_p=0.1
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"❌ Error analyzing image: {e}")
        return ""

def analyze_doc_image(client, img):
    """Wrapper function for concurrent processing"""
    img_uri = get_img_uri(img)
    data = analyze_image(client, img_uri)
    return data

# Add this new function before the main() function to make PDF processing reusable

def process_pdf_with_gpt(file_path: str, openai_client: OpenAI, include_first_page: bool = True) -> dict:
    """
    Process a single PDF file with GPT-4o analysis - reusable function for other scripts
    
    Args:
        file_path: Path to the PDF file
        openai_client: Initialized OpenAI client
        include_first_page: Whether to include the first page (default: False, skips first page)
    
    Returns:
        dict with 'success', 'error', 'extracted_text', 'pages_description', 'total_pages', 'pages_analyzed'
    """
    file_name = os.path.basename(file_path)
    
    # Initialize result
    result = {
        "success": False,
        "error": None,
        "extracted_text": "",
        "pages_description": [],
        "total_pages": 0,
        "pages_analyzed": 0
    }
    
    try:
        # Extract text using pdfminer
        text = extract_text_from_doc(file_path)
        result['extracted_text'] = text
        
        # Convert to images
        images = convert_doc_to_images(file_path)
        if not images:
            raise Exception("Failed to convert PDF to images")
        
        result['total_pages'] = len(images)
        
        # Analyze pages with GPT-4o
        pages_description = []
        
        # Choose which pages to process
        if include_first_page:
            images_to_process = images
        else:
            # Remove the first slide as suggested in the docs (usually just intro)
            images_to_process = images[1:] if len(images) > 1 else images
        
        # Process with concurrent execution for speed
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(analyze_doc_image, openai_client, img)
                for img in images_to_process
            ]
        
            with tqdm(total=len(images_to_process), desc=f"Analyzing {file_name}", leave=False) as pbar:
                for future in concurrent.futures.as_completed(futures):
                    page_result = future.result()
                    if page_result:
                        pages_description.append(page_result)
                    pbar.update(1)

        result['pages_analyzed'] = len(pages_description)
        result['pages_description'] = pages_description
        result['success'] = True
    
        return result
        
    except Exception as e:
        result['error'] = str(e)
        return result

def process_single_pdf(client, file_path, output_directory):
    """Process a single PDF file"""
    file_name = os.path.basename(file_path)
    file_stem = Path(file_name).stem

    print(f"📄 Processing: {file_name}")
    print(f"📁 File size: {os.path.getsize(file_path):,} bytes")

    # Initialize document data
    doc_data = {
        "filename": file_name,
        "file_path": file_path,
        "processing_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "file_size_bytes": os.path.getsize(file_path),
        "success": False,
        "error": None
    }

    # Use the new reusable function
    result = process_pdf_with_gpt(file_path, client, include_first_page=True)

    # Update doc_data with results
    doc_data.update(result)
    
    if result['success']:
        # Combine content for markdown output
        markdown_content = f"# {file_stem}\n\n"
        markdown_content += f"**Source:** {file_name}\n"
        markdown_content += f"**Processed:** {doc_data['processing_timestamp']}\n"
        markdown_content += f"**Pages:** {result['total_pages']}\n\n"
    
        # Add extracted text if available
        if result['extracted_text'].strip():
            markdown_content += "## Extracted Text\n\n"
            # Clean up the text a bit
            cleaned_text = result['extracted_text'].replace('\f', '\n\n---\n\n')  # Replace form feeds with section breaks
            markdown_content += cleaned_text + "\n\n"

        # Add GPT-4o analysis
        if result['pages_description']:
            markdown_content += "## GPT-4o Page Analysis\n\n"
            for i, description in enumerate(result['pages_description'], 1):
                markdown_content += f"### Page {i + 1}\n\n"  # +1 because we skip first page
                markdown_content += description + "\n\n"
                markdown_content += "---\n\n"

        # Save markdown file
        md_output_file = os.path.join(output_directory, f"{file_stem}.md")
        with open(md_output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"💾 Saved markdown: {md_output_file}")
        
        # Save metadata JSON file
        json_output_file = os.path.join(output_directory, f"{file_stem}.json")
        
        # Prepare JSON metadata (exclude large text content for cleaner JSON)
        json_metadata = doc_data.copy()
        json_metadata['pages_description'] = result['pages_description']
        json_metadata['output_files'] = {
    'markdown': md_output_file,
            'json': json_output_file
        }

        with open(json_output_file, 'w', encoding='utf-8') as f:
            json.dump(json_metadata, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved metadata: {json_output_file}")

    return doc_data



def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Process PDF files using GPT-4o image analysis')
    parser.add_argument('--input', '-i', 
                       default='ingestion/input', 
                       help='Input directory containing PDF files (default: ingestion/input)')
    parser.add_argument('--output', '-o', 
                       default='ingestion/output', 
                       help='Output directory for processed files (default: ingestion/output)')
    
    args = parser.parse_args()
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Configuration
    input_directory = args.input
    output_directory = args.output
    log_file = "pdf_gpt_processing_log.json"
    
    # Check for required environment variables
    api_key = os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in environment or .env file.")
        print("Please either:")
        print("  1. Add OPENAI_API_KEY=your-api-key-here to your .env file, OR")
        print("  2. Set environment variable: export OPENAI_API_KEY='your-api-key-here'")
        return
    
    print(f"🔑 Using OpenAI API key: {api_key[:8]}..." if len(api_key) > 8 else "🔑 API key set")
    print(f"📂 Input directory: {input_directory}")
    print(f"📁 Output directory: {output_directory}")
    
    # Create output directory
    os.makedirs(output_directory, exist_ok=True)
    
    # Load processing log
    processing_log = load_processing_log(log_file)
    
    # Find PDF files
    pdf_files = find_pdf_files(input_directory)
    if not pdf_files:
        print(f"❌ No PDF files found in {input_directory}")
        return
    
    print(f"📋 Found {len(pdf_files)} PDF files to process")
    
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Process each PDF file
    processed_results = {}
    successful_count = 0
    
    for i, file_path in enumerate(pdf_files, 1):
        file_name = os.path.basename(file_path)
        print(f"\n📄 [{i}/{len(pdf_files)}] Starting: {file_name}")
        
        # Check if already processed successfully
        if file_name in processing_log and processing_log[file_name].get('success'):
            print(f"⏭️  File already processed successfully, skipping")
            continue
        
        # Process the PDF
        result = process_single_pdf(client, file_path, output_directory)
        
        # Update log
        processing_log[file_name] = result
        processed_results[file_name] = result
        
        if result['success']:
            successful_count += 1
            print(f"✅ Successfully processed {file_name}")
        else:
            print(f"❌ Failed to process {file_name}: {result.get('error', 'Unknown error')}")
        
        # Save log after each file
        save_processing_log(processing_log, log_file)
        
        # Add a small delay to avoid rate limiting
        time.sleep(1)
    
    # Summary
    print(f"\n🎉 PROCESSING COMPLETE!")
    print(f"📊 Total files found: {len(pdf_files)}")
    print(f"📄 Files processed this run: {len(processed_results)}")
    print(f"✅ Successful extractions: {successful_count}")
    print(f"📝 Log file updated: {log_file}")
    print(f"📁 Output directory: {output_directory}")

if __name__ == "__main__":
    main()
