# Quick Start: Upload Client Briefs to Google Drive

## TL;DR

```bash
python client_brief_generator.py \
    --client-id "YOUR_CLIENT_NAME" \
    --drive-folder-id "YOUR_DRIVE_FOLDER_ID"
```

That's it! Brief generation and Drive upload are now default behaviors.

## What You Need

1. ✅ Client ID (same as from onboarding)
2. ✅ Drive folder ID (from `new_client_ingestion.py` run)
3. ✅ Service account credentials: `./service_account.json` (default location)

## Where to Find the Drive Folder ID

### Option 1: From Previous Onboarding
Look at your `new_client_ingestion.py` command:
```bash
python new_client_ingestion.py \
    --drive-folder-id "1ABC123XYZ..."  # ← This one!
```

### Option 2: From Google Drive URL
```
https://drive.google.com/drive/folders/1ABC123XYZ
                                         ↑
                                    Copy this part
```

### Option 3: From Pipeline Logs
Check `client_pipeline_log.json` for the folder ID used during onboarding.

## Where Does It Upload?

```
Your Drive:
└── 📁 Client Folder (Parent)           ← Brief goes here! 📄
    └── 📁 Client Materials (Child)     ← You provide this ID
        ├── doc1.pdf
        └── doc2.pdf
```

**The brief uploads to the PARENT of the folder you specify.**

## Common Commands

### Generate + Upload (Default)
```bash
python client_brief_generator.py \
    --client-id "client-name" \
    --drive-folder-id "1ABC..."
```

### Generate Without Upload
```bash
python client_brief_generator.py \
    --client-id "client-name" \
    --no-upload-to-drive
```

### With Custom Credentials
```bash
python client_brief_generator.py \
    --client-id "client-name" \
    --drive-folder-id "1ABC..." \
    --credentials "/path/to/creds.json"
```

### With Verbose Output
```bash
python client_brief_generator.py \
    --client-id "client-name" \
    --drive-folder-id "1ABC..." \
    --verbose
```

## Quick Troubleshooting

| Error | Fix |
|-------|-----|
| "Google Drive service not initialized" | Check `service_account.json` exists |
| "403 Forbidden" | Share folder with service account email |
| "No parent folder found" | Folder is at Drive root - this is OK |
| "--drive-folder-id not provided" | Add `--drive-folder-id "1ABC..."` |

## Service Account Email

Your service account email is in `service_account.json`:
```json
{
  "client_email": "name@project.iam.gserviceaccount.com"  ← Share folders with this
}
```

## Output Example

```
✅ Client brief successfully uploaded to Google Drive parent folder
   📄 File ID: 1DEF456GHI...
   🔗 View link: https://drive.google.com/file/d/...
```

## Need More Help?

- Full guide: `DRIVE_UPLOAD_GUIDE.md`
- All options: `python client_brief_generator.py --help`
- Changelog: `BRIEF_UPLOAD_CHANGELOG.md`

