# Google Drive Upload Guide for Client Briefs

This guide explains how to automatically upload generated client briefs to Google Drive.

## Overview

When you generate a client brief, you can now automatically upload it to Google Drive by providing:
1. The **target folder ID** (the Google Drive folder where you want the brief uploaded)
2. The Google service account credentials file

The brief will be uploaded directly to the specified folder.

## How It Works

```
Google Drive Structure:
└── Target Folder                             ← Brief uploaded here (you specify this folder ID)
    ├── Document1.pdf
    ├── Document2.pdf
    └── ...
```

## Prerequisites

1. **Google Service Account**: You need a service account JSON credentials file
2. **Drive API Access**: The service account must have:
   - `drive.file` scope enabled
   - Write permissions to the target folder in Google Drive
3. **Folder ID**: The Google Drive folder ID where you want to upload the brief

## Finding the Drive Folder ID

You can get the folder ID from a Google Drive URL:
```
https://drive.google.com/drive/folders/1ABC123XYZ
                                         ↑
                                    Folder ID
```

Or from any Google Drive folder by:
1. Opening the folder in Google Drive
2. Copying the folder ID from the URL
3. Using that ID with the `--drive-folder-id` parameter

## Usage Examples

### Basic Usage (Default Behavior)

Generate a brief and automatically upload to Google Drive:

```bash
python client_brief_generator.py \
    --client-id "client-name" \
    --drive-folder-id "1ABC123XYZ..."
```

**Note**: Brief generation and Drive upload are now default behaviors - no extra flags needed!

### Generate Without Upload

```bash
python client_brief_generator.py \
    --client-id "client-name" \
    --no-upload-to-drive
```

### With Custom Output Location

```bash
python client_brief_generator.py \
    --client-id "client-name" \
    --drive-folder-id "1ABC123XYZ..." \
    --credentials "./path/to/service_account.json" \
    --output "./custom/path/client_brief.md"
```

### With Verbose Output

```bash
python client_brief_generator.py \
    --client-id "client-name" \
    --drive-folder-id "1ABC123XYZ..." \
    --verbose
```

## Command-Line Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--client-id` | Yes* | None | Client ID / corpus key |
| `--drive-folder-id` | No | None | Google Drive folder ID (client materials folder) |
| `--credentials` | No | `./service_account.json` | Path to Google service account credentials file |
| `--no-upload-to-drive` | No | False | Disable automatic upload to Google Drive |

\* Can also be set via `VECTARA_CORPUS_KEY` environment variable

**New Defaults**:
- Brief generation is now the default action (no `--generate-brief` flag needed)
- Drive upload is automatic when `--drive-folder-id` is provided
- Use `--no-upload-to-drive` to disable upload

## What Happens During Upload

1. **Brief Generation**: The client brief is generated and saved locally
2. **Parent Folder Lookup**: The script queries Google Drive API to find the parent folder ID
3. **Upload**: The brief file is uploaded to the parent folder
4. **Confirmation**: You'll see the file ID and view link in the output

## Example Output

```
📤 UPLOADING CLIENT BRIEF TO GOOGLE DRIVE
================================================================================
🔗 Initializing Google Drive service...
✅ Google Drive service initialized successfully
✅ Found parent folder ID: 1XYZ789ABC...
📤 Uploading client-name_client_brief_20250103_143022.md to Google Drive folder: 1XYZ789ABC...
✅ Successfully uploaded to Google Drive
   📄 File ID: 1DEF456GHI...
   🔗 View link: https://drive.google.com/file/d/1DEF456GHI.../view
✅ Client brief successfully uploaded to Google Drive parent folder
```

## Troubleshooting

### "Google Drive service not initialized"

**Problem**: The credentials file wasn't found or is invalid.

**Solution**: 
```bash
# Check if the file exists
ls -la ./service_account.json

# Verify it's valid JSON
python -c "import json; json.load(open('service_account.json'))"

# Specify explicit path
python client_brief_generator.py ... --credentials "/absolute/path/to/service_account.json"
```

### "No parent folder found"

**Problem**: The folder you specified is at the root level of Google Drive.

**Solution**: This is a warning, not an error. The folder is at the root, so there's no parent to upload to. You may need to manually move the brief or specify a different folder structure.

### "Error getting parent folder: 403"

**Problem**: The service account doesn't have permission to access the folder.

**Solution**: 
1. Share the Google Drive folder with the service account email
2. Grant "Editor" or "Writer" permissions
3. The service account email looks like: `service-account-name@project-id.iam.gserviceaccount.com`

### "Error uploading to Google Drive: 403"

**Problem**: The service account doesn't have write permissions to the parent folder.

**Solution**: Share the parent folder with the service account email and grant write permissions.

## Integration with Client Onboarding

When using `new_client_ingestion.py` to onboard a client, note the Drive folder ID:

```bash
# Step 1: During onboarding
python new_client_ingestion.py \
    --client-id "client-name" \
    --drive-folder-id "1ABC123XYZ..." \  # ← Save this ID
    --client-homepage-url "https://example.com"

# Step 2: Later, generate and upload the brief (automatic)
python client_brief_generator.py \
    --client-id "client-name" \
    --drive-folder-id "1ABC123XYZ..."  # ← Use the same ID (upload is automatic)
```

**That's it!** No additional flags needed - brief generation and upload happen automatically.

## Security Notes

1. **Service Account Credentials**: Keep your `service_account.json` file secure and never commit it to version control
2. **Access Scope**: The script only requests `drive.file` scope, which allows creating and modifying files created by the app
3. **Folder Permissions**: Only folders shared with the service account can be accessed

## Additional Resources

- [Google Drive API Documentation](https://developers.google.com/drive/api/v3/about-sdk)
- [Service Account Authentication](https://cloud.google.com/iam/docs/service-accounts)
- Main client brief generator help: `python client_brief_generator.py --help`

