# Google Drive Folder Processing Test Guide

## Overview

Use `test_drive_folder_processing.py` to debug and test Google Drive folder processing in isolation. This is especially useful for:
- Debugging why certain file types aren't being processed
- Verifying folder permissions
- Testing file type detection logic
- Analyzing what files are in a folder before full ingestion

## Quick Start

### 1. List Files Only (No Processing)

```bash
uv run python test_drive_folder_processing.py \
    --folder-id YOUR_FOLDER_ID \
    --list-only
```

This will:
- List all files in the folder (recursively)
- Show MIME types and file sizes
- Categorize files as supported/unsupported
- Save analysis to JSON
- **Not download or process anything**

### 2. Full Processing Test

```bash
uv run python test_drive_folder_processing.py \
    --folder-id YOUR_FOLDER_ID \
    --client-id test-client \
    --pdf-processor markitdown
```

This will:
- List all files
- Analyze file types
- **Download and process files** (full ingestion)
- Save outputs to `test_outputs/test-client/`

## Command Options

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--folder-id` | ✅ Yes | - | Google Drive folder ID |
| `--client-id` | No | `test-client` | Client ID (used for output folder) |
| `--pdf-processor` | No | `markitdown` | Processor: `markitdown`, `gpt`, or `pdfplumber` |
| `--list-only` | No | `false` | Only list files, don't process |
| `--credentials` | No | `service_account.json` | Path to service account credentials |

## Example Workflows

### Debug Missing PPT Files

```bash
# Step 1: List files to see what's in the folder
uv run python test_drive_folder_processing.py \
    --folder-id 1abc123xyz \
    --list-only

# Step 2: Check the analysis JSON
cat test_outputs/test-client/file_analysis_*.json

# Step 3: Run full processing if files are supported
uv run python test_drive_folder_processing.py \
    --folder-id 1abc123xyz \
    --pdf-processor markitdown
```

### Test Different Processors

```bash
# Test with MarkItDown (recommended)
uv run python test_drive_folder_processing.py \
    --folder-id 1abc123xyz \
    --pdf-processor markitdown

# Test with GPT-4o (PDFs only)
uv run python test_drive_folder_processing.py \
    --folder-id 1abc123xyz \
    --pdf-processor gpt

# Test with pdfplumber (PDFs only)
uv run python test_drive_folder_processing.py \
    --folder-id 1abc123xyz \
    --pdf-processor pdfplumber
```

### Test Specific Client Folder

```bash
# Use actual client ID for realistic testing
uv run python test_drive_folder_processing.py \
    --folder-id 1abc123xyz \
    --client-id mintleads-test \
    --pdf-processor markitdown
```

## Output

### Console Output

The script provides detailed console output showing:

```
================================================================================
🧪 GOOGLE DRIVE FOLDER PROCESSING TEST
================================================================================
Folder ID: 1abc123xyz
Client ID: test-client
PDF Processor: markitdown
Credentials: service_account.json
================================================================================

📁 Test output directory: /Users/hynes/dev/vectara/test_outputs/test-client

✅ Google Drive client initialized

================================================================================
STEP 1: LISTING ALL FILES IN FOLDER
================================================================================

📄 Company Pitch Deck.pptx
   Type: application/vnd.openxmlformats-officedocument.presentationml.presentation
   ID: 1abc123
   Size: 5242880 bytes

📄 Old Presentation.ppt
   Type: application/vnd.ms-powerpoint
   ID: 1xyz789
   Size: 2097152 bytes

📄 Case Study.pdf
   Type: application/pdf
   ID: 1def456
   Size: 1048576 bytes

================================================================================
Found 3 total items
================================================================================

================================================================================
STEP 2: ANALYZING FILE TYPE SUPPORT
================================================================================

📊 Summary:
   • Total files: 3
   • Folders: 0
   • Supported files: 3
   • Unsupported files: 0

✅ SUPPORTED FILES:
   • Company Pitch Deck.pptx
     Type: application/vnd.openxmlformats-officedocument.presentationml.presentation
     Size: 5242880 bytes
   • Old Presentation.ppt
     Type: application/vnd.ms-powerpoint
     Size: 2097152 bytes
   • Case Study.pdf
     Type: application/pdf
     Size: 1048576 bytes

💾 Analysis saved to: test_outputs/test-client/file_analysis_20251003_130000.json
```

### File Output

**Analysis JSON** (`test_outputs/test-client/file_analysis_TIMESTAMP.json`):
```json
{
  "folder_id": "1abc123xyz",
  "timestamp": "2025-10-03T13:00:00",
  "total_files": 3,
  "folders": 0,
  "supported_count": 3,
  "unsupported_count": 0,
  "supported_files": [
    {
      "id": "1abc123",
      "name": "Company Pitch Deck.pptx",
      "mimeType": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
      "size": "5242880",
      "modifiedTime": "2025-10-01T10:30:00.000Z",
      "webViewLink": "https://drive.google.com/file/d/1abc123/view"
    }
  ],
  "unsupported_files": [],
  "folders": []
}
```

**Processed Files** (if not using `--list-only`):
- `test_outputs/test-client/client_materials/` - Downloaded and processed files
- `test_outputs/test-client/crawl_summary.json` - Processing summary
- `test_outputs/test-client/urls_discovered.txt` - N/A for Drive-only processing

## Troubleshooting

### Issue: "Permission denied" errors

**Problem**: Service account doesn't have access to the folder.

**Solution**:
1. Share the Google Drive folder with your service account email
2. Check service account email:
   ```bash
   cat service_account.json | grep client_email
   ```
3. In Google Drive, share the folder with that email address

### Issue: PPT files showing as "unsupported"

**Problem**: Old PowerPoint format (`.ppt`) might have wrong MIME type.

**Solution**:
1. Run with `--list-only` to see the actual MIME type:
   ```bash
   uv run python test_drive_folder_processing.py --folder-id YOUR_ID --list-only
   ```

2. Check the console output for the file's MIME type

3. If the MIME type is not in the supported list, we need to add it to `ingest_specific_drive_folder.py`

Common PPT MIME types:
- Modern: `application/vnd.openxmlformats-officedocument.presentationml.presentation` (`.pptx`)
- Legacy: `application/vnd.ms-powerpoint` (`.ppt`)
- Generic: `application/mspowerpoint`
- Alternative: `application/powerpoint`

### Issue: Files not being downloaded

**Problem**: Files are listed but not appearing in output directory.

**Solution**:
1. Check if you used `--list-only` flag (which skips processing)
2. Check the output directory: `test_outputs/YOUR_CLIENT_ID/`
3. Look for error messages in the console output
4. Check file permissions and disk space

### Issue: MarkItDown processing fails

**Problem**: MarkItDown crashes or produces empty output.

**Solution**:
1. Try a different processor:
   ```bash
   uv run python test_drive_folder_processing.py \
       --folder-id YOUR_ID \
       --pdf-processor pdfplumber
   ```

2. Check MarkItDown installation:
   ```bash
   uv run python -c "import markitdown; print('OK')"
   ```

3. Test with a single file first before processing entire folder

## Finding Your Folder ID

### Method 1: From URL
If your folder URL is:
```
https://drive.google.com/drive/folders/1abc123xyz456
```

The folder ID is: `1abc123xyz456`

### Method 2: Using Google Drive API
```bash
uv run python -c "
from google.oauth2 import service_account
from googleapiclient.discovery import build

credentials = service_account.Credentials.from_service_account_file(
    'service_account.json',
    scopes=['https://www.googleapis.com/auth/drive.readonly']
)
service = build('drive', 'v3', credentials=credentials)

# List folders shared with service account
results = service.files().list(
    q=\"mimeType='application/vnd.google-apps.folder'\",
    fields='files(id, name)',
    pageSize=10
).execute()

for folder in results.get('files', []):
    print(f'{folder[\"name\"]}: {folder[\"id\"]}')
"
```

## Common File MIME Types Reference

| File Type | Extension | MIME Type |
|-----------|-----------|-----------|
| PDF | `.pdf` | `application/pdf` |
| Word (new) | `.docx` | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` |
| Word (old) | `.doc` | `application/msword` |
| PowerPoint (new) | `.pptx` | `application/vnd.openxmlformats-officedocument.presentationml.presentation` |
| PowerPoint (old) | `.ppt` | `application/vnd.ms-powerpoint` |
| Excel (new) | `.xlsx` | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` |
| Excel (old) | `.xls` | `application/vnd.ms-excel` |
| Google Docs | - | `application/vnd.google-apps.document` |
| Google Slides | - | `application/vnd.google-apps.presentation` |
| Google Sheets | - | `application/vnd.google-apps.spreadsheet` |
| Image (JPEG) | `.jpg` | `image/jpeg` |
| Image (PNG) | `.png` | `image/png` |
| Audio (MP3) | `.mp3` | `audio/mpeg` |
| ZIP | `.zip` | `application/zip` |

## Next Steps

After identifying issues with the test script:

1. **Update file type support** in `ingestion/ingest_specific_drive_folder.py`
2. **Test again** with the updated code
3. **Run full workflow** once confirmed working:
   ```bash
   uv run python run_complete_workflow.py
   ```

## Related Documentation

- [MarkItDown File Support](./MARKITDOWN_FILE_SUPPORT.md)
- [Complete Workflow Guide](./COMPLETE_WORKFLOW_GUIDE.md)
- [Drive Upload Guide](./DRIVE_UPLOAD_GUIDE.md)

---

**Last Updated**: October 3, 2025  
**Version**: 1.0.0

