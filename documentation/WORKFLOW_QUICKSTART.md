# Workflow Quick Start

## One Command, Complete Onboarding! 🚀

```bash
python run_complete_workflow.py
```

Follow the prompts. That's it!

## What You Get

✅ Client website scraped  
✅ Google Drive materials downloaded  
✅ All content uploaded to Vectara  
✅ Comprehensive client brief generated  
✅ Brief automatically uploaded to Google Drive  

**Time**: 8-15 minutes total

## Batch Mode (No Prompts)

```bash
python run_complete_workflow.py \
    --client-id "CLIENT_NAME" \
    --drive-folder-id "1ABC123XYZ..." \
    --client-homepage-url "https://example.com"
```

## What Happens

```
Step 1: Client Ingestion (5-10 min)
├── Scrape website
├── Download Drive files
├── Process PDFs with MarkItDown
└── Upload to Vectara

⏳ Wait 10 seconds for indexing

Step 2: Brief Generation (2-5 min)
├── Auto-discover case studies
├── Analyze intake forms
├── Analyze website content
├── Generate markdown brief
└── Upload to Google Drive parent folder

🎉 Done!
```

## Quick Options

### Use GPT-4o for PDFs
```bash
python run_complete_workflow.py \
    --client-id "CLIENT_NAME" \
    --drive-folder-id "1ABC..." \
    --client-homepage-url "https://example.com" \
    --pdf-processor gpt
```

### More Workers (Faster)
```bash
python run_complete_workflow.py \
    --client-id "CLIENT_NAME" \
    --drive-folder-id "1ABC..." \
    --client-homepage-url "https://example.com" \
    --workers 8
```

### Ingestion Only (No Brief)
```bash
python run_complete_workflow.py \
    --client-id "CLIENT_NAME" \
    --drive-folder-id "1ABC..." \
    --client-homepage-url "https://example.com" \
    --skip-brief
```

## Output Files

```
📁 ingestion/client_ingestion_outputs/CLIENT_NAME/
   ├── website/              # Website pages
   ├── client_materials/     # Drive files
   └── client_intake_form/   # Intake form

📁 outputs/
   └── CLIENT_NAME_client_brief_20250103_143045.md

☁️  Google Drive/
   └── [Parent Folder]/
       └── CLIENT_NAME_client_brief_20250103_143045.md
```

## If Something Fails

### Ingestion Failed
```bash
# Fix the issue, then re-run the whole workflow
python run_complete_workflow.py --client-id "CLIENT_NAME" ...
```

### Brief Generation Failed
```bash
# Re-run just the brief generation
python client_brief_generator.py \
    --client-id "CLIENT_NAME" \
    --drive-folder-id "1ABC..."
```

## Need Help?

- Full guide: `COMPLETE_WORKFLOW_GUIDE.md`
- PDF options: `PDF_PROCESSOR_GUIDE.md`
- Drive upload: `DRIVE_UPLOAD_GUIDE.md`

## Requirements

✅ `.env` file with `VECTARA_API_KEY`  
✅ `service_account.json` in project root  
✅ Drive folder shared with service account  
✅ All dependencies installed  

## Pro Tips

1. **Start Interactive** - Run with no args to see options
2. **Use MarkItDown** - Fast and free (default)
3. **Check Logs** - `new_client_ingestion.log` has details
4. **Be Patient** - First run takes ~10-15 minutes
5. **Test Small** - Try with a test client first

## The Old Way vs New Way

### Before (3 steps)
```bash
python new_client_ingestion.py ...
# wait...
python client_brief_generator.py ...
```

### Now (1 step)
```bash
python run_complete_workflow.py ...
```

**50% fewer commands. 100% automated.** 🎯

