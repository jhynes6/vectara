# Vectara Client Onboarding System

Complete automated workflow for client onboarding, content ingestion, and brief generation.

## 🚀 Quick Start

### Complete Workflow (Recommended)

Run everything in one command - ingestion + brief generation + Drive upload:

```bash
python run_complete_workflow.py
```

Follow the interactive prompts. Takes 8-15 minutes.

**What it does:**
1. ✅ Scrapes client website
2. ✅ Downloads Google Drive materials  
3. ✅ Processes PDFs with MarkItDown
4. ✅ Uploads to Vectara corpus
5. ✅ Generates comprehensive client brief
6. ✅ Uploads brief to Google Drive

### Individual Scripts

If you need to run steps separately:

```bash
# Step 1: Client ingestion only
python new_client_ingestion.py

# Step 2: Brief generation only
python client_brief_generator.py --client-id "CLIENT_NAME"
```

## 📚 Documentation

All documentation is in the `documentation/` folder:

- **[Workflow Quick Start](WORKFLOW_QUICKSTART.md)** - TL;DR guide
- **[Complete Workflow Guide](COMPLETE_WORKFLOW_GUIDE.md)** - Full documentation
- **[PDF Processor Guide](PDF_PROCESSOR_GUIDE.md)** - MarkItDown, GPT-4o, pdfplumber
- **[Drive Upload Guide](DRIVE_UPLOAD_GUIDE.md)** - Automatic brief uploads
- **[Brief Upload Quick Start](BRIEF_UPLOAD_QUICKSTART.md)** - Quick reference
- **[Folder Reorganization](FOLDER_REORGANIZATION.md)** - Project structure
- **[Project Structure](PROJECT_STRUCTURE.md)** - File organization

## 🎯 Key Features

- **One-Command Workflow** - Complete onboarding in a single command
- **Smart PDF Processing** - Choose GPT-4o, MarkItDown, or pdfplumber
- **Automatic Brief Upload** - Uploads to Google Drive parent folder
- **Comprehensive Briefs** - Auto-discovers case studies, analyzes all content
- **Progress Tracking** - Pipeline tracker with detailed logging

## 📋 Example: Complete Workflow

### Interactive Mode
```bash
python run_complete_workflow.py

# You'll be prompted for:
# - Client ID
# - Google Drive folder ID
# - Client website URL
# - PDF processor (default: markitdown)
# - Other optional settings
```

### Batch Mode
```bash
python run_complete_workflow.py \
    --client-id "acme-corp" \
    --drive-folder-id "1ABC123XYZ..." \
    --client-homepage-url "https://acme.com" \
    --pdf-processor markitdown \
    --workers 4
```

## 🛠️ Available Tools

### Workflow Scripts
- `run_complete_workflow.py` - **One-command complete workflow** (recommended)
- `new_client_ingestion.py` - Standalone ingestion (website + Drive)
- `client_brief_generator.py` - Standalone brief generation

### Ingestion Scripts
- `ingestion/ingest_client_website.py` - Website-only scraping
- `ingestion/ingest_specific_drive_folder.py` - Drive-only ingestion
- `ingestion/pdf_process_markitdown.py` - MarkItDown PDF processor
- `ingestion/pdf_process_gpt.py` - GPT-4o PDF processor

### Utility Scripts
- `workspace_inspector.py` - Inspect Vectara workspace
- `kb_querier.py` - Query knowledge bases

## 🔧 Vectara Workspace Inspector

A Python script to inspect your Vectara workspace and list:
- 🤖 All agents (if available via API)
- 📚 All corpora 
- 📄 All documents in each corpus

## Setup

### 1. Virtual Environment

The project is already set up with a Python virtual environment. To activate it:

```bash
source .venv/bin/activate
```

### 2. Dependencies

Dependencies are already installed from the consolidated requirements of:
- `vectara-agentic` (AI agent library)
- `vectara-ingest` (data ingestion framework)

###2.5 

### 3. Configuration
 python vectara_inspector.py --verbose
'

Create a `.env` file with your Vectara API key:

```bash
cp env.template .env
```

Then edit `.env` and add your actual API key:

```
VECTARA_API_KEY=your_actual_vectara_api_key_here
```

You can get your API key from the [Vectara Console](https://console.vectara.com).

## Usage

### Basic Usage

```bash
python vectara_inspector.py
```

### With Command Line Options

```bash
# Specify API key directly
python vectara_inspector.py --api-key "your-api-key"

# Enable verbose output
python vectara_inspector.py --verbose

# Use custom endpoint
python vectara_inspector.py --endpoint "https://custom-vectara.domain.com"

# Show help
python vectara_inspector.py --help
```

### Environment Variables

You can also set these environment variables:

- `VECTARA_API_KEY`: Your Vectara API key (required)
- `VECTARA_ENDPOINT`: Vectara API endpoint (optional, defaults to https://api.vectara.io)

## Output

1. **Agents**: Currently, agents are managed through the vectara-agentic library and may not be available via REST API yet.

2. **Corpora**: A table showing:
   - Corpus name
   - Corpus key
   - Description
   - Creation date

3. **Documents**: For each corpus, a table showing:
   - Document ID
   - Document title
   - Source URL
   - Creation date

## Features

- 🎨 Beautiful terminal output using Rich
- 📊 Tabular data presentation
- 🔄 Paginated API calls (handles large workspaces)
- 🛡️ Error handling with informative messages
- 🔧 Configurable via command line or environment variables

## Troubleshooting

### Authentication Errors

If you get authentication errors:
1. Verify your API key is correct
2. Make sure your API key has the necessary permissions
3. Check that you're using the correct Vectara endpoint

### No Data Found

If no corpora or documents are found:
1. Verify you're using the correct Vectara account
2. Check that your API key has read permissions
3. Ensure you have corpora created in your Vectara workspace

## Dependencies

This project combines dependencies from the Vectara ecosystem:
- Core Vectara libraries for API interaction
- Rich for beautiful terminal output
- Typer for command-line interface
- Requests for HTTP operations


