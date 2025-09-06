# New Client Onboarding Guide

This guide explains how to use the `new_client_ingestion.py` script to onboard new clients into Vectara with comprehensive content ingestion.

## Overview

The new client onboarding script automates the entire process of setting up a new client in Vectara by:

1. **Creating a new Vectara corpus** with proper metadata structure
2. **Ingesting website content** from the client's homepage
3. **Ingesting client materials** from Google Drive
4. **Uploading all processed documents** to the Vectara corpus with rich metadata

## Prerequisites

### Environment Variables

Ensure these environment variables are set in your `.env` file:

```bash
# Required for Vectara operations
VECTARA_API_KEY=your_vectara_api_key_here

# Required for LLM categorization (optional but recommended)
OPENAI_API_KEY=your_openai_api_key_here

# Required for PDF processing (optional)
VECTORIZE_API_KEY=your_vectorize_api_key_here
VECTORIZE_ORGANIZATION_ID=your_vectorize_org_id_here
```

### Files Required

- `service_account.json`: Google service account credentials file for Drive access
- The client's Google Drive folder must be publicly accessible ("Anyone with the link can view")

### Python Dependencies

Install required packages:

```bash
pip install vectara python-dotenv requests beautifulsoup4 python-slugify
```

## Usage

### Interactive Mode (Recommended)

Simply run the script and it will prompt you for all required information:

```bash
python new_client_ingestion.py
```

The script will interactively ask for:
- **Client ID**: Unique identifier (alphanumeric with hyphens/underscores)
- **Google Drive folder**: ID or full URL to the client materials folder
- **Homepage URL**: Client's website URL (protocol optional)
- **Optional settings**: Output directory, workers, LLM categorization, credentials path

### Batch Mode

For automated/scripted usage, provide all arguments via command line:

```bash
python new_client_ingestion.py \
  --batch-mode \
  --client-id "acme-corp" \
  --drive-folder-id "1ABC123DEF456GHI789JKL" \
  --client-homepage-url "https://acme-corp.com"
```

### Command Line Arguments

#### Batch Mode Arguments

- `--batch-mode`: Enable non-interactive batch mode (requires all other required arguments)
- `--client-id`: Unique identifier for the client (used as corpus key)
  - Must be alphanumeric with hyphens/underscores only
  - Example: `"acme-corp"`, `"client_123"`

- `--drive-folder-id`: Google Drive folder ID containing client materials
  - Can be extracted from Drive URL: `https://drive.google.com/drive/folders/1ABC123...`
  - Example: `"1ABC123DEF456GHI789JKL"`

- `--client-homepage-url`: Client's website homepage URL
  - Must include protocol (http:// or https://)
  - Example: `"https://acme-corp.com"`

#### Optional Arguments (Both Modes)

- `--output-dir`: Base output directory (default: `./ingestion/client_ingestion_outputs`)
- `--workers`: Number of parallel workers for website scraping (default: 4)
- `--no-llm-categories`: Disable LLM categorization (uses simple keyword-based categorization)
- `--credentials`: Path to Google service account JSON file (default: `./service_account.json`)

### Example Commands

#### Interactive mode (recommended):
```bash
# Simply run the script - it will prompt for all inputs
python new_client_ingestion.py
```

#### Batch mode - basic onboarding:
```bash
python new_client_ingestion.py \
  --batch-mode \
  --client-id "d2-creative" \
  --drive-folder-id "1ABC123DEF456GHI789JKL" \
  --client-homepage-url "https://d2creative.com"
```

#### Batch mode - custom settings:
```bash
python new_client_ingestion.py \
  --batch-mode \
  --client-id "tech-startup" \
  --drive-folder-id "1XYZ789ABC123DEF456GHI" \
  --client-homepage-url "https://techstartup.io" \
  --output-dir "/custom/path/outputs" \
  --workers 8
```

#### Batch mode - without LLM categorization:
```bash
python new_client_ingestion.py \
  --batch-mode \
  --client-id "budget-client" \
  --drive-folder-id "1DEF456GHI789JKL012MNO" \
  --client-homepage-url "https://budgetclient.com" \
  --no-llm-categories
```

## What the Script Does

### Step 0: Directory Setup
- Creates client-specific directory structure:
  ```
  ingestion/client_ingestion_outputs/
  └── {client-id}/
      ├── client_intake_form/
      ├── client_materials/
      └── website/
  ```

### Step 1: Corpus Creation
- Creates a new Vectara corpus with the client ID as the key
- Sets up metadata filters for:
  - `content_type`: Categories content (case_studies, client_intake_form, etc.)
  - `source`: Document source (website, client_intake_form, client_materials)
  - `is_title`: Boolean flag for title content
  - `lang`: Detected language code

### Step 2: Content Ingestion
Runs two ingestion processes in parallel:

#### Website Ingestion
- Discovers URLs from sitemap.xml
- Scrapes website content with intelligent content extraction
- Categorizes pages using LLM (homepage, services_products, blogs_resources, etc.)
- Saves as markdown files with rich metadata

#### Google Drive Ingestion
- Crawls the specified Drive folder and subdirectories
- Processes various file types (PDFs, Google Docs, text files)
- Uses vectorize.io API for advanced PDF processing
- Categorizes documents using LLM (capabilities_overview, case_studies, etc.)
- Separates Client Intake forms from other materials

### Step 3: Document Upload
- Uploads all processed files to the Vectara corpus
- Includes comprehensive metadata for each document
- Enables table extraction for structured content
- Uses appropriate filenames based on content type

### Step 4: Reporting
- Generates a comprehensive onboarding report
- Includes upload statistics and file locations
- Saves as `onboarding_report.json` in the client directory

## Output Structure

After successful onboarding, you'll have:

```
ingestion/client_ingestion_outputs/{client-id}/
├── client_intake_form/
│   ├── client_intake_{safe-name}.md
│   └── client_intake_{safe-name}.md.metadata.json
├── client_materials/
│   ├── {category}_{safe-name}.md
│   └── {category}_{safe-name}.md.metadata.json
├── website/
│   ├── {page-name}.md (with frontmatter)
│   └── ...
├── crawl_summary.json
├── scraping_summary.json
├── url_categories.json
├── urls_discovered.txt
├── urls_successful.txt
└── onboarding_report.json
```

## File Naming Conventions

### Client Intake Forms
- Filename in Vectara: `{client-id}_client_intake_form`
- Local file: `client_intake_{safe-name}.md`

### Client Materials
- Filename in Vectara: Lowercase version of original filename from metadata
- Local file: `{category}_{safe-name}.md`

### Website Files
- Filename in Vectara: Original markdown filename
- Local file: `{url-path-based-name}.md`

## Metadata Structure

Each uploaded document includes comprehensive metadata:

```json
{
  "source": "website|client_intake_form|client_materials",
  "content_type": "homepage|services_products|case_studies|...",
  "created_at": "2025-01-01T12:00:00Z",
  "last_updated_at": "2025-01-01T12:00:00Z",
  "client_id": "acme-corp",
  "upload_timestamp": "2025-01-01T12:00:00Z",
  "file_size_bytes": 1024
}
```

## Testing

Before running the full workflow, test your setup:

```bash
python test_new_client_ingestion.py
```

This validates:
- Environment variables are set
- Directory creation works
- Vectara client initialization succeeds
- File discovery functions properly

## Troubleshooting

### Common Issues

1. **"No module named 'vectara'"**
   ```bash
   pip install vectara
   ```

2. **"VECTARA_API_KEY not found"**
   - Check your `.env` file
   - Ensure the API key has appropriate permissions

3. **"Error accessing folder"**
   - Verify the Drive folder ID is correct
   - Ensure the folder is publicly accessible
   - Check service account credentials

4. **"Corpus already exists"**
   - The script continues if the corpus exists
   - Use a different client-id if needed

5. **Website scraping fails**
   - Check if the website has a sitemap.xml
   - Verify the URL is accessible
   - Some sites may block automated requests

6. **Upload errors with table extraction**
   - Table extraction only works with PDF files
   - The script automatically handles this, but older versions may have issues
   - Error: "Tabular data extraction feature supported only for pdf files"

### Logs and Debugging

The script provides detailed logging:
- `INFO` level: Progress updates and success messages
- `WARNING` level: Non-critical issues (missing files, etc.)
- `ERROR` level: Critical failures that stop processing

## Performance Considerations

### Parallel Processing
- Website scraping uses configurable worker threads
- Drive and website ingestion run concurrently
- PDF processing is batched for efficiency

### LLM Usage
- LLM categorization improves content organization
- Processes in batches to respect rate limits
- Falls back to keyword-based categorization if LLM fails

### File Size Limits
- Vectara supports files up to 10MB
- Large PDFs are processed with vectorize.io
- Very large files may timeout during processing

## Best Practices

1. **Test with a small client first** to verify your setup
2. **Use LLM categorization** for better content organization
3. **Monitor the logs** during processing for any issues
4. **Keep backups** of your service account credentials
5. **Use descriptive client IDs** that won't conflict
6. **Verify Drive folder permissions** before starting

## Support

For issues with:
- **Vectara API**: Check the [Vectara documentation](https://docs.vectara.com)
- **Google Drive API**: Verify service account setup and permissions
- **Website scraping**: Check site accessibility and sitemap availability
- **PDF processing**: Ensure vectorize.io credentials are correct

## Next Steps

After successful onboarding:
1. **Test queries** against the new corpus in the Vectara Console
2. **Review uploaded content** for accuracy and completeness
3. **Set up monitoring** for ongoing content updates
4. **Create client-specific applications** using the Vectara SDK
