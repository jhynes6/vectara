# PDF Re-processing Integration

## Overview

The complete client onboarding workflow now includes **automatic PDF re-processing** to catch and fix any failed PDF extractions during ingestion.

## What Changed

### New Workflow Step

The workflow now has **5 steps** instead of 4:

1. **Client Ingestion** (website + Drive content)
2. **PDF Re-processing** ← NEW! Automatically fixes failed PDFs
3. **Vertex AI RAG** corpus creation and upload
4. **Client Brief Generation**
5. **Brief Upload** to Google Drive

### How It Works

After ingestion completes, the workflow automatically:

1. **Scans** the client's `client_materials` directory for `[PDF_PLACEHOLDER_*]` markers
2. **Downloads** failed PDFs from Google Drive
3. **Re-processes** them using multiple methods (GPT-4o → MarkItDown → pdfplumber)
4. **Updates** the .md files with extracted content
5. **Reports** all successes and remaining failures

### Key Features

- ✅ **Non-blocking**: Failed re-processing doesn't stop the workflow
- ✅ **Automatic**: No manual intervention required
- ✅ **Multi-method**: Tries 3 different extraction methods
- ✅ **Detailed reporting**: Shows exactly what was fixed and what failed
- ✅ **Intelligent wait**: Adds extra RAG indexing time if PDFs were re-processed

## Usage

### Complete Workflow (Automatic)

```bash
python run_complete_workflow.py \
    --client-id "client-name" \
    --drive-folder-id "1ABC123..." \
    --client-homepage-url "https://example.com"
```

The PDF re-processing step runs automatically between ingestion and brief generation.

### Standalone Re-processing

You can also run PDF re-processing separately:

```bash
# Re-process all clients
python ingestion/reprocess_failed_pdfs.py

# Re-process specific client
python ingestion/reprocess_failed_pdfs.py \
    --output-dir ./ingestion/client_ingestion_outputs/client-name
```

## Output

### Console Output

```
================================================================================
STEP 2: PDF RE-PROCESSING (Fixing Failed Extractions)
================================================================================
Client ID: mintleads
Scanning for PDF_PLACEHOLDER markers...

🔍 Scanning for failed PDFs...
⚠️  Found 7 failed PDF(s) that need re-processing

🔄 Re-processing failed PDFs...
🔄 Re-processing: pitch_decks_mintleads-deck-v3.md
   File ID: 1MLykqa6SInOqeWTNPpfc-Yf0ZQFatVBE
   Original: MintLeads_Deck_v3.pdf
================================================================================
📥 Downloaded PDF: MintLeads_Deck_v3.pdf
🤖 Attempting GPT-4o processing...
✅ GPT-4o processing successful (9 pages)
✅ SUCCESS! Re-processed using: gpt
   Content length: 9070 characters
   Word count: 1333
```

### Workflow Summary

```
Results:
  ✅ Ingestion: Success
  ✅ PDF Re-processing: Success
     • Re-processed: 3
     • Still failed: 0
  ✅ Brief Generation: Success
  📄 Brief File: outputs/client-name_client_brief_20250103_171153.md
  ✅ Drive Upload: Success
```

## Reports

Two reports are generated:

1. **Client-specific report**: `client_ingestion_outputs/<client>/pdf_reprocessing_report.json`
   - Lists successfully re-processed files
   - Lists files that still failed
   - Includes methods tried and statistics

2. **Workflow report**: Includes PDF re-processing statistics in the main workflow report

## Benefits

### Before Integration
❌ Failed PDFs left as placeholders  
❌ Incomplete data in RAG corpus  
❌ Manual intervention required  
❌ No visibility into failures  

### After Integration
✅ Automatic failure detection  
✅ Automatic re-processing with fallbacks  
✅ Complete data in RAG corpus  
✅ Clear visibility and reporting  
✅ Non-blocking workflow  

## Error Handling

- **If no failed PDFs**: Completes instantly with success message
- **If some PDFs fail all methods**: Continues workflow, logs warnings, marks in report
- **If re-processing encounters error**: Logs error but continues workflow (non-blocking)

## Configuration

The re-processing step uses:
- **Method**: `auto` (tries GPT-4o → MarkItDown → pdfplumber in order)
- **Credentials**: Same service account as ingestion
- **Wait time**: 15 seconds RAG indexing for re-processed PDFs (vs 10 seconds default)

## Files Modified

- `run_complete_workflow.py`: Added PDF re-processing step
- `ingestion/reprocess_failed_pdfs.py`: Standalone re-processing script

## Example: Real Success Story

**Client**: mintleads  
**Problem**: 7 PDFs failed initial extraction (6.5 MB pitch deck was problematic)  
**Solution**: Automatic re-processing caught and fixed 3 PDFs:
- `pitch_decks_mintleads-deck-v3.md`: 0 words → **1,333 words** ✅
- `other_white-label-digital-ctv-4.md`: 0 words → **307 words** ✅
- `capabilities_overview_wld-company-overview-2024.md`: 0 words → **139 words** ✅

**Result**: Complete data in RAG corpus without manual intervention!

