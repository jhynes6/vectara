# Client Brief Generator - Google Drive Upload Feature

## Summary

Added functionality to `client_brief_generator.py` that automatically uploads the generated client brief to the parent folder of the client materials folder in Google Drive.

## Changes Made

### 1. New Dependencies
Added Google Drive API imports to `client_brief_generator.py`:
- `google.oauth2.service_account`
- `googleapiclient.discovery`
- `googleapiclient.errors.HttpError`
- `googleapiclient.http.MediaFileUpload`

### 2. ClientBriefGenerator Class Updates

#### Constructor Parameters
Added two new optional parameters:
- `drive_folder_id`: Google Drive folder ID (client materials folder)
- `credentials_file`: Path to Google service account JSON file (default: `./service_account.json`)

#### New Methods

**`_initialize_drive_service()`**
- Initializes Google Drive API service using service account credentials
- Requests `drive.file` scope for creating/modifying files
- Handles initialization errors gracefully

**`get_parent_folder_id(folder_id: str) -> Optional[str]`**
- Queries Google Drive API to find the parent folder of a given folder
- Returns parent folder ID or None if not found
- Used to determine where to upload the brief

**`upload_brief_to_drive(file_path: str, target_folder_id: str) -> Optional[str]`**
- Uploads a file to a specified Google Drive folder
- Sets mimetype to `text/markdown`
- Returns uploaded file ID and displays view link
- Handles upload errors gracefully

### 3. Command-Line Interface Updates

Added three new command-line arguments:

```bash
--drive-folder-id FOLDER_ID    # Google Drive folder ID (client materials folder)
--credentials PATH             # Path to service account JSON (default: ./service_account.json)
--upload-to-drive              # Enable upload to Google Drive
```

### 4. Main Function Updates

Modified the main workflow to:
1. Initialize `ClientBriefGenerator` with Drive parameters
2. Generate and save the brief locally (as before)
3. If `--upload-to-drive` is specified:
   - Get the parent folder ID of the provided folder
   - Upload the brief to the parent folder
   - Display confirmation with file ID and view link

## Usage Examples

### Basic Upload
```bash
python client_brief_generator.py \
    --generate-brief \
    --corpus-key "client-name" \
    --drive-folder-id "1ABC123XYZ..." \
    --upload-to-drive
```

### With Custom Credentials Path
```bash
python client_brief_generator.py \
    --generate-brief \
    --corpus-key "client-name" \
    --drive-folder-id "1ABC123XYZ..." \
    --credentials "/path/to/service_account.json" \
    --upload-to-drive
```

### Complete Workflow from Onboarding
```bash
# Step 1: Onboard client (note the drive-folder-id)
python new_client_ingestion.py \
    --client-id "client-name" \
    --drive-folder-id "1ABC123XYZ..." \
    --client-homepage-url "https://example.com"

# Step 2: Generate and upload brief (use same drive-folder-id)
python client_brief_generator.py \
    --generate-brief \
    --corpus-key "client-name" \
    --drive-folder-id "1ABC123XYZ..." \
    --upload-to-drive
```

## Google Drive Folder Structure

The upload logic assumes this structure:

```
Google Drive:
└── Client Folder (Parent)                    ← Brief uploaded here ✓
    └── Client Materials Folder (Child)       ← You provide this folder ID
        ├── Document1.pdf
        ├── Document2.pdf
        └── ...
```

When you provide the **Client Materials Folder ID**, the script:
1. Queries the Google Drive API to get the parent folder ID
2. Uploads the brief to the parent folder

## Files Created

1. **Modified**: `client_brief_generator.py`
   - Added Google Drive upload functionality
   - Added new command-line arguments
   - Updated help text and examples

2. **New**: `test_brief_upload.sh`
   - Test script demonstrating the upload functionality
   - Configurable with environment variables

3. **New**: `DRIVE_UPLOAD_GUIDE.md`
   - Comprehensive documentation
   - Usage examples
   - Troubleshooting guide
   - Security notes

4. **New**: `BRIEF_UPLOAD_CHANGELOG.md` (this file)
   - Summary of changes
   - Technical documentation

## Requirements

### Python Packages
The following packages are required (likely already installed):
- `google-auth`
- `google-auth-oauthlib`
- `google-auth-httplib2`
- `google-api-python-client`

### Google Cloud Setup
1. Service account with Drive API access
2. Service account JSON credentials file
3. Shared folder permissions for the service account

## Backward Compatibility

All changes are **fully backward compatible**:
- New parameters are optional
- Existing workflows continue to work unchanged
- Upload is only performed when explicitly requested with `--upload-to-drive`

## Error Handling

The implementation includes robust error handling:
- Missing credentials file → Warning, continues without upload
- Invalid folder ID → Error message, continues without upload
- Permission errors → Clear error message with troubleshooting hints
- Network errors → Graceful failure with error details

## Security Considerations

1. **Minimal Permissions**: Only requests `drive.file` scope (not full Drive access)
2. **Credentials Protection**: Credentials file path is configurable and not hardcoded
3. **No Sensitive Data**: Only uploads the generated markdown file
4. **Audit Trail**: All uploads are logged with file ID and folder location

## Testing

To test the functionality:

1. Ensure you have valid service account credentials
2. Get a Drive folder ID from a previous client onboarding
3. Run the test script:
   ```bash
   # Edit test_brief_upload.sh with your values
   ./test_brief_upload.sh
   ```

## Integration Points

This feature integrates seamlessly with:
1. **`new_client_ingestion.py`**: Uses the same Drive folder ID from onboarding
2. **Existing brief generation**: All existing brief generation features work unchanged
3. **Output workflows**: Brief is still saved locally even when uploaded to Drive

## Future Enhancements

Potential future improvements:
1. Support for converting markdown to Google Docs format
2. Automatic folder creation if parent doesn't exist
3. Option to upload to specific custom folder instead of parent
4. Batch upload support for multiple briefs
5. Integration with Drive permissions (auto-sharing with specific users)

