# OAuth2 Google Drive Setup Guide

This guide shows how to set up OAuth2 authentication to bypass service account storage quota limitations.

## Why OAuth2?

Service accounts have storage quota limitations - they can't store files in folders they create. OAuth2 allows you to authenticate as a real user, using your personal Google Drive storage quota.

## Setup Steps

### 1. Create OAuth2 Credentials

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/

2. **Select Your Project**
   - Choose the same project as your service account (instantly-376001)

3. **Enable APIs**
   - Go to "APIs & Services" → "Library"
   - Search for "Google Drive API"
   - Click "Enable"

4. **Create OAuth2 Credentials**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - Choose "Desktop application"
   - Give it a name (e.g., "Drive Uploader")
   - Click "Create"

5. **Download Credentials**
   - Click the download button (⬇️) next to your new OAuth client
   - Save as `oauth_credentials.json` in your project directory

### 2. Install Required Dependencies

```bash
pip install google-auth-oauthlib
```

### 3. Use the OAuth Uploader

```bash
# Upload to existing folder
python oauth_drive_uploader.py \
    --file outputs/client_brief.md \
    --folder-id "1ABC123XYZ..."

# Create new folder and upload
python oauth_drive_uploader.py \
    --file outputs/client_brief.md \
    --create-folder "Client Briefs" \
    --name "Client Brief.md"
```

## First Run Authentication

The first time you run the OAuth uploader:

1. **Browser window opens** - Google OAuth consent screen
2. **Sign in** with your Google account
3. **Grant permissions** - Allow access to Google Drive
4. **Token saved** - `oauth_token.json` created automatically
5. **Future runs** - No browser interaction needed (token auto-refreshes)

## Advantages of OAuth2

✅ **No Storage Limits** - Uses your personal Google Drive quota  
✅ **Full Access** - Can create folders and store files anywhere  
✅ **User Permissions** - Inherits your Google Drive permissions  
✅ **No Sharing Required** - No need to share folders with service accounts  
✅ **Flexible** - Works with any Google account  

## Comparison: Service Account vs OAuth2

| Feature | Service Account | OAuth2 |
|---------|----------------|--------|
| Storage Quota | ❌ Limited | ✅ Full user quota |
| Create Folders | ✅ Yes | ✅ Yes |
| Store Files | ❌ Only in shared folders | ✅ Anywhere |
| Setup Complexity | ✅ Simple | ⚠️ Requires OAuth setup |
| User Interaction | ✅ None | ⚠️ First run only |
| Security | ✅ Service account | ✅ User account |

## Integration with Existing Scripts

You can modify your existing scripts to use OAuth2 instead of service accounts:

```python
# Replace this:
from google.oauth2 import service_account
credentials = service_account.Credentials.from_service_account_file(
    './service_account.json',
    scopes=['https://www.googleapis.com/auth/drive.file']
)

# With this:
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# OAuth2 initialization code (see oauth_drive_uploader.py)
```

## Troubleshooting

### "OAuth credentials file not found"
- Make sure `oauth_credentials.json` is in your project directory
- Verify you downloaded the OAuth client credentials correctly

### "Browser authentication failed"
- Make sure you're signed into the correct Google account
- Check that Google Drive API is enabled in your project

### "Permission denied"
- The OAuth consent screen needs to be configured
- Go to Google Cloud Console → APIs & Services → OAuth consent screen
- Add your email to test users if in testing mode

## Security Notes

- **Keep credentials secure** - Don't commit `oauth_credentials.json` to version control
- **Token management** - `oauth_token.json` contains refresh tokens, keep it secure
- **Scope limitations** - Only requests `drive.file` scope (minimal permissions)

## Quick Test

```bash
# Test OAuth setup
python oauth_drive_uploader.py \
    --file outputs/white-label-digital_client_brief_20251003_053728.md \
    --create-folder "OAuth Test" \
    --name "Test Upload.md"
```

If this works, your OAuth2 setup is complete!



