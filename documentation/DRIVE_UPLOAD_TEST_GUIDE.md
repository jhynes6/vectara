# Google Drive Upload Test Guide

This guide explains how to use the `test_drive_upload.py` script to test uploading client briefs to Google Drive.

## Overview

The `test_drive_upload.py` script is a standalone testing tool that:
1. Takes a brief file path and target folder ID as input
2. Verifies the target folder exists and is accessible
3. Uploads the brief directly to the target folder
4. Provides detailed feedback on the process

## Prerequisites

1. **Google Service Account**: You need a service account JSON credentials file (default: `./service_account.json`)
2. **Drive API Access**: The service account must have:
   - `drive.file` scope enabled
   - Write permissions to the target folder
3. **Brief File**: A markdown brief file to upload
4. **Folder ID**: The Google Drive folder ID where you want to upload the brief

## Usage

### Basic Usage

```bash
python test_drive_upload.py \
    --brief-file outputs/client_brief.md \
    --drive-folder-id "1ABC123XYZ..."
```

### With Custom Credentials

```bash
python test_drive_upload.py \
    --brief-file outputs/client_brief.md \
    --drive-folder-id "1ABC123XYZ..." \
    --credentials custom_credentials.json
```

### With Verbose Output

```bash
python test_drive_upload.py \
    --brief-file outputs/client_brief.md \
    --drive-folder-id "1ABC123XYZ..." \
    --verbose
```

## Command Line Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--brief-file` | Yes | Path to the client brief file to upload |
| `--drive-folder-id` | Yes | Google Drive folder ID where to upload the brief |
| `--credentials` | No | Path to Google service account JSON file (default: `./service_account.json`) |
| `--verbose` | No | Enable verbose output for debugging |

## Expected Output

When successful, the script will output:

```
================================================================================
🧪 TESTING GOOGLE DRIVE UPLOAD WORKFLOW
================================================================================
📄 Brief file: outputs/client_brief.md
📁 Target folder ID: 1ABC123XYZ...

✅ Brief file found

🔍 STEP 1: Verifying target folder...
🔍 Looking up folder info for: 1ABC123XYZ...
📁 Folder name: Client Folder
✅ Target folder verified: Client Folder

📤 STEP 2: Uploading brief to target folder...
📤 Uploading client_brief.md to Google Drive folder: 1ABC123XYZ...
📄 File size: 45,678 bytes
✅ Successfully uploaded to Google Drive
   📄 File ID: 1GHI789JKL...
   📊 Uploaded size: 45678 bytes
   🔗 View link: https://drive.google.com/file/d/1GHI789JKL.../view

🎉 UPLOAD TEST SUCCESSFUL!
   📄 Uploaded file ID: 1GHI789JKL...

✅ All tests passed!
```

## Troubleshooting

### Permission Errors

If you see permission errors:

1. **Share the folder with your service account**:
   - Open the Google Drive folder: `https://drive.google.com/drive/folders/{folder_id}`
   - Right-click → Share
   - Add the service account email (shown in the script output)
   - Give it "Editor" permissions

2. **Check service account email**:
   The script will display the service account email when it initializes:
   ```
   📧 Service account: your-service-account@project.iam.gserviceaccount.com
   ```

### Folder Not Found

If the folder ID is not found:
- Verify the folder ID is correct
- Ensure the folder exists and is accessible
- Check that the service account has been shared with the folder

### File Upload Errors

If the upload fails:
- Check that the brief file exists and is readable
- Verify the service account has write permissions to the parent folder
- Ensure the file is not too large (Google Drive has file size limits)

## Integration with Main Workflow

This test script uses the same upload logic as the main `client_brief_generator.py` script, so a successful test indicates that the main workflow will also work correctly.

The test script is particularly useful for:
- Debugging upload issues
- Verifying folder permissions
- Testing with different brief files
- Validating the upload workflow before running the full client brief generation
