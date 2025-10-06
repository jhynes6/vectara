# Google Drive Permissions Troubleshooting

## Error: "File not found: [FOLDER_ID]"

### What This Means

The Google Drive API is returning a 404 "File not found" error, which actually means:
- The folder exists, BUT
- Your service account doesn't have permission to access it

This is Google's security design - it returns "not found" instead of "access denied" to prevent information leakage.

## Solution: Share the Folder with Your Service Account

### Step 1: Find Your Service Account Email

```bash
# Look in your service_account.json file
cat service_account.json | grep client_email
```

You'll see something like:
```json
"client_email": "your-service-account@project-id.iam.gserviceaccount.com"
```

**Copy this email address!**

### Step 2: Share the Google Drive Folder

1. Open Google Drive in your browser
2. Navigate to the folder with ID: `1gaOLC7F0cEQmW69Z1cLEL2tfZp07NLcm`
   - Or paste this URL in your browser:
   - `https://drive.google.com/drive/folders/1gaOLC7F0cEQmW69Z1cLEL2tfZp07NLcm`
3. Right-click the folder → "Share"
4. In the "Add people and groups" field, paste the service account email
5. Set permission to "Editor" (allows upload)
6. Click "Send" (uncheck "Notify people" if you want)

### Step 3: Share the PARENT Folder Too

The brief uploads to the **parent** of the folder you specify, so you also need to:

1. In Drive, click on the folder you just shared
2. Look at the breadcrumb path at the top to find the parent folder
3. Click the parent folder name
4. Share that folder with the service account email (Editor permission)

### Step 4: Retry

```bash
python run_complete_workflow.py \
    --client-id "YOUR_CLIENT" \
    --drive-folder-id "1gaOLC7F0cEQmW69Z1cLEL2tfZp07NLcm" \
    --client-homepage-url "https://example.com"
```

## Alternative: Use a Different Folder

If you can't access that specific folder, use a different one:

```bash
# Create a new folder in your Google Drive
# Share it with your service account
# Use that folder ID instead
```

## Verify Service Account Email

```bash
# Extract just the email
python3 -c "import json; print(json.load(open('service_account.json'))['client_email'])"
```

Expected output:
```
something@project-id.iam.gserviceaccount.com
```

## Common Issues

### "I shared the folder but still getting 404"

**Wait a few seconds** - Drive permissions can take a moment to propagate.

```bash
# Wait 30 seconds then retry
sleep 30
python run_complete_workflow.py ...
```

### "I don't have access to that folder"

The folder ID might be from a different Google account or organization.

**Solutions:**
1. Use a folder you control
2. Ask the folder owner to share it with your service account
3. Create a test folder to verify setup works

### "How do I find the folder in Drive?"

```bash
# Use this URL (replace FOLDER_ID)
https://drive.google.com/drive/folders/FOLDER_ID
```

For your case:
```
https://drive.google.com/drive/folders/1gaOLC7F0cEQmW69Z1cLEL2tfZp07NLcm
```

## Testing Setup

### Create a Test Folder

1. Go to Google Drive
2. Create a new folder called "Test Client Materials"
3. Share it with your service account email (Editor)
4. Copy the folder ID from the URL
5. Test with:

```bash
python client_brief_generator.py \
    --client-id "test-client" \
    --drive-folder-id "YOUR_TEST_FOLDER_ID"
```

## Required Permissions

Your service account needs:

1. **View access** to the client materials folder (to get parent ID)
2. **Edit access** to the parent folder (to upload the brief)

### Minimum Setup

```
Google Drive:
└── Client Folder (Parent) ← Service account needs EDITOR access
    └── Client Materials (Child) ← Service account needs VIEWER access
        ├── document1.pdf
        └── document2.pdf
```

## Service Account Scopes

The script requests these scopes:

**For reading** (ingest_specific_drive_folder.py):
- `https://www.googleapis.com/auth/drive.readonly`
- `https://www.googleapis.com/auth/documents.readonly`

**For uploading** (client_brief_generator.py):
- `https://www.googleapis.com/auth/drive.file`

These are correct and secure.

## Debug Commands

### Check if service account can access folder

```python
# Test script to check access
python3 << 'EOF'
from google.oauth2 import service_account
from googleapiclient.discovery import build

credentials = service_account.Credentials.from_service_account_file(
    './service_account.json',
    scopes=['https://www.googleapis.com/auth/drive.readonly']
)

service = build('drive', 'v3', credentials=credentials)

try:
    folder = service.files().get(
        fileId='1gaOLC7F0cEQmW69Z1cLEL2tfZp07NLcm',
        fields='id, name, parents'
    ).execute()
    print(f"✅ Success! Folder name: {folder['name']}")
    print(f"   Parents: {folder.get('parents', [])}")
except Exception as e:
    print(f"❌ Error: {e}")
EOF
```

### Check service account email

```bash
cat service_account.json | python3 -m json.tool | grep client_email
```

## Quick Fix Checklist

- [ ] Get service account email from `service_account.json`
- [ ] Open the Drive folder in browser
- [ ] Share folder with service account email
- [ ] Set permission to "Editor"
- [ ] Share the PARENT folder too
- [ ] Wait 30 seconds for propagation
- [ ] Retry the script

## If All Else Fails

### Option 1: Skip Drive Upload

```bash
python run_complete_workflow.py \
    --client-id "YOUR_CLIENT" \
    --drive-folder-id "1gaOLC7F0cEQmW69Z1cLEL2tfZp07NLcm" \
    --client-homepage-url "https://example.com" \
    --skip-brief
```

Then manually run brief generation without upload:

```bash
python client_brief_generator.py \
    --client-id "YOUR_CLIENT" \
    --no-upload-to-drive
```

### Option 2: Use Different Folder

Create a new folder you control and use that instead.

## Still Having Issues?

1. Verify the folder ID is correct
2. Verify you're using the right Google account
3. Verify the service account JSON is valid
4. Check Google Cloud Console for service account status
5. Ensure Drive API is enabled in your Google Cloud project

---

**Most Common Fix:** Share the folder with your service account email! 🔑


