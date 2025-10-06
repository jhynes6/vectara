# Complete Workflow Guide

## Overview

`run_complete_workflow.py` orchestrates the entire client onboarding process in a single command:

1. ✅ **Client Ingestion** - Website + Google Drive content
2. ✅ **Vectara Upload** - All documents to corpus
3. ✅ **Brief Generation** - Comprehensive client analysis
4. ✅ **Drive Upload** - Brief to parent folder (automatic)

## Quick Start

### Interactive Mode (Recommended)

```bash
python run_complete_workflow.py
```

You'll be prompted for:
- Client ID
- Google Drive folder ID
- Client website URL
- Optional settings (workers, PDF processor, etc.)

### Batch Mode

```bash
python run_complete_workflow.py \
    --client-id "client-name" \
    --drive-folder-id "1ABC123XYZ..." \
    --client-homepage-url "https://example.com"
```

## What Happens

### Step 1: Client Ingestion (5-10 minutes)
- Creates Vectara corpus
- Scrapes client website
- Downloads Google Drive materials
- Processes PDFs (with your chosen processor)
- Uploads everything to Vectara

**Wait Time**: 10 seconds for Vectara indexing

### Step 2: Brief Generation (2-5 minutes)
- Auto-discovers case studies
- Analyzes client intake forms
- Analyzes website content
- Generates comprehensive markdown brief
- Uploads brief to Google Drive parent folder

## Usage Examples

### Most Common: Full Workflow

```bash
# Interactive - you'll be prompted for everything
python run_complete_workflow.py

# Batch mode with defaults
python run_complete_workflow.py \
    --client-id "acme-corp" \
    --drive-folder-id "1ABC123..." \
    --client-homepage-url "https://acme.com"
```

### With Custom Settings

```bash
# Use MarkItDown for PDFs, 8 workers
python run_complete_workflow.py \
    --client-id "acme-corp" \
    --drive-folder-id "1ABC123..." \
    --client-homepage-url "https://acme.com" \
    --pdf-processor markitdown \
    --workers 8
```

### Ingestion Only (Skip Brief)

```bash
# Only run ingestion, skip brief generation
python run_complete_workflow.py \
    --client-id "acme-corp" \
    --drive-folder-id "1ABC123..." \
    --client-homepage-url "https://acme.com" \
    --skip-brief
```

## Command-Line Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--client-id` | Yes* | None | Client identifier / corpus key |
| `--drive-folder-id` | Yes* | None | Google Drive folder (client materials) |
| `--client-homepage-url` | Yes* | None | Client website homepage |
| `--workers` | No | 4 | Parallel workers for website scraping |
| `--pdf-processor` | No | `markitdown` | PDF method: `gpt`, `markitdown`, `pdfplumber` |
| `--no-llm-categories` | No | False | Disable LLM categorization |
| `--credentials` | No | `./service_account.json` | Service account file path |
| `--skip-brief` | No | False | Skip brief generation |
| `--batch-mode` | No | False | Non-interactive mode |

\* Not required in interactive mode

## Interactive Prompts

When you run without arguments, you'll see:

```
🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀
COMPLETE CLIENT ONBOARDING WORKFLOW
🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀

This will run:
  1. Client ingestion (website + Drive content)
  2. Vectara corpus upload
  3. Client brief generation
  4. Brief upload to Google Drive

Please provide the following information:

👤 Client ID (unique identifier): acme-corp
💾 Google Drive folder ID or URL (client materials): 1ABC123...
🌐 Client homepage URL (e.g., https://example.com): https://acme.com

⚙️  Optional Settings (press Enter for defaults):
⚡ Number of parallel workers [4]: 
🤖 Enable LLM categorization? [Y/n]: 

📄 PDF Processing Options:
   1. gpt - GPT-4o with image analysis
   2. markitdown - Microsoft MarkItDown (fast, LLM-optimized)
   3. pdfplumber - Basic text extraction
Select PDF processor [1/2/3, default: 2-markitdown]: 

🔑 Path to service account JSON [./service_account.json]: 
📄 Skip brief generation? [y/N]: 

📋 Configuration Summary:
--------------------------------------------------
👤 Client ID: acme-corp
🌐 Website URL: https://acme.com
💾 Drive Folder ID: 1ABC123...
⚡ Workers: 4
🤖 LLM Categorization: Enabled
📄 PDF Processor: markitdown
🔑 Credentials: ./service_account.json
📝 Brief Generation: Enabled

✅ Proceed with complete workflow? [Y/n]: 
```

## Output

### Console Output

```
🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀
COMPLETE CLIENT ONBOARDING WORKFLOW
🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀
Client: acme-corp
Started: 2025-01-03 14:30:22

================================================================================
STEP 1: CLIENT INGESTION
================================================================================
Client ID: acme-corp
Website: https://acme.com
Drive Folder: 1ABC123...
PDF Processor: markitdown

[... ingestion progress ...]

================================================================================
✅ CLIENT INGESTION COMPLETED SUCCESSFULLY
================================================================================
Files uploaded: 25/25
Report: ingestion/client_ingestion_outputs/acme-corp/onboarding_report.json

⏳ Waiting 10 seconds for Vectara indexing...

================================================================================
STEP 2: CLIENT BRIEF GENERATION
================================================================================
Client ID: acme-corp
Drive Folder ID: 1ABC123...
Auto-upload: Enabled

[... brief generation progress ...]

💾 Brief saved to: outputs/acme-corp_client_brief_20250103_143045.md
📄 File size: 15234 characters

📤 Uploading client brief to Google Drive...
✅ Client brief successfully uploaded to Google Drive

================================================================================
✅ CLIENT BRIEF GENERATION COMPLETED SUCCESSFULLY
================================================================================
Brief file: outputs/acme-corp_client_brief_20250103_143045.md
Drive upload: ✅ Success

================================================================================
🎉 COMPLETE WORKFLOW FINISHED
================================================================================
Client: acme-corp
Duration: 432.5 seconds (7.2 minutes)

Results:
  ✅ Ingestion: Success
  ✅ Brief Generation: Success
  📄 Brief File: outputs/acme-corp_client_brief_20250103_143045.md
  ✅ Drive Upload: Success
================================================================================
```

### Files Created

```
vectara/
├── ingestion/client_ingestion_outputs/acme-corp/
│   ├── website/              # All website pages as markdown
│   ├── client_materials/     # Drive files as markdown
│   ├── client_intake_form/   # Client intake form
│   └── onboarding_report.json
└── outputs/
    └── acme-corp_client_brief_20250103_143045.md  # Final brief
```

### Google Drive Structure

```
Drive:
└── Client Folder (Parent)
    ├── acme-corp_client_brief_20250103_143045.md  ← Uploaded here! 📄
    └── Client Materials (Child)
        ├── document1.pdf
        └── document2.pdf
```

## Comparison with Individual Scripts

### Old Way (3 separate commands)

```bash
# Step 1: Run ingestion
python new_client_ingestion.py \
    --client-id "acme-corp" \
    --drive-folder-id "1ABC..." \
    --client-homepage-url "https://acme.com"

# Step 2: Wait for indexing...
sleep 30

# Step 3: Generate brief
python client_brief_generator.py \
    --client-id "acme-corp" \
    --drive-folder-id "1ABC..."
```

### New Way (1 command)

```bash
# Everything in one shot!
python run_complete_workflow.py \
    --client-id "acme-corp" \
    --drive-folder-id "1ABC..." \
    --client-homepage-url "https://acme.com"
```

## Error Handling

The workflow stops if ingestion fails:

```
❌ Workflow stopped: Ingestion failed
```

If brief generation fails, you'll see:

```
✅ Ingestion: Success
❌ Brief Generation: Failed
```

You can re-run just the brief generation:

```bash
python client_brief_generator.py \
    --client-id "acme-corp" \
    --drive-folder-id "1ABC..."
```

## Timing Expectations

| Step | Typical Duration |
|------|------------------|
| Corpus Creation | 5-10 seconds |
| Website Scraping | 2-5 minutes |
| Drive Download | 1-3 minutes |
| PDF Processing | 1-5 minutes (varies by processor) |
| Vectara Upload | 1-2 minutes |
| Indexing Wait | 10 seconds |
| Brief Generation | 2-5 minutes |
| **Total** | **8-15 minutes** |

## Advanced Usage

### Only Ingestion

```bash
python run_complete_workflow.py \
    --client-id "acme-corp" \
    --drive-folder-id "1ABC..." \
    --client-homepage-url "https://acme.com" \
    --skip-brief
```

### Fast Mode (Minimal Workers)

```bash
python run_complete_workflow.py \
    --client-id "acme-corp" \
    --drive-folder-id "1ABC..." \
    --client-homepage-url "https://acme.com" \
    --workers 2 \
    --pdf-processor pdfplumber
```

### Maximum Quality

```bash
python run_complete_workflow.py \
    --client-id "acme-corp" \
    --drive-folder-id "1ABC..." \
    --client-homepage-url "https://acme.com" \
    --workers 8 \
    --pdf-processor gpt
```

## Troubleshooting

### "Client ingestion failed"
Check:
- Vectara API key in `.env`
- Service account credentials
- Website is accessible
- Drive folder is shared with service account

### "Brief generation failed"
Check:
- Corpus was created successfully
- Documents were uploaded
- Wait longer for Vectara indexing (increase wait time in script)

### "Drive upload failed"
Check:
- Service account has write permissions
- Folder is shared with service account
- Parent folder exists

### Script Hangs
- Check your internet connection
- Verify website is responsive
- Check Drive API quotas

## Tips

1. **Start with Interactive Mode** - Easier to see what's happening
2. **Use MarkItDown by Default** - Fast and high-quality
3. **Monitor Progress** - Watch the console output
4. **Check Logs** - See `new_client_ingestion.log` for details
5. **Test Small First** - Try with a test client before production

## Environment Variables

Required in `.env`:
```bash
VECTARA_API_KEY=your_api_key_here
OPENAI_API_KEY=your_openai_key_here  # Only if using GPT-4o processor
```

## Next Steps

After the workflow completes:

1. ✅ Check the brief file in `outputs/`
2. ✅ Verify it uploaded to Google Drive
3. ✅ Review the onboarding report
4. ✅ Query your Vectara corpus to test

## Related Scripts

- `new_client_ingestion.py` - Standalone ingestion
- `client_brief_generator.py` - Standalone brief generation
- `ingestion/ingest_specific_drive_folder.py` - Drive-only ingestion
- `ingestion/ingest_client_website.py` - Website-only scraping

## Support

For issues:
1. Check `new_client_ingestion.log`
2. Review `client_brief_generation.log` (if exists)
3. Verify all environment variables
4. Check service account permissions

