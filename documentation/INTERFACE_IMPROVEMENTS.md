# Client Brief Generator - Interface Improvements

## Summary of Changes

Made three key interface improvements to simplify the CLI and make it more intuitive:

### 1. ✅ Drive Upload is Now Default Behavior
- **Before**: Required `--upload-to-drive` flag
- **After**: Automatic when `--drive-folder-id` is provided
- **To Disable**: Use `--no-upload-to-drive` flag

### 2. ✅ Brief Generation is Default Action
- **Before**: Required `--generate-brief` flag
- **After**: Default action (no flag needed)
- **Other Actions**: `--list-agents` and `--list-corpora` still available

### 3. ✅ Renamed `--corpus-key` to `--client-id`
- **Before**: `--corpus-key "client-name"`
- **After**: `--client-id "client-name"`
- **Reason**: More intuitive and matches `new_client_ingestion.py` terminology

## Before vs After

### Old Interface (Complex)
```bash
python client_brief_generator.py \
    --generate-brief \
    --corpus-key "client-name" \
    --drive-folder-id "1ABC123..." \
    --upload-to-drive
```

### New Interface (Simple)
```bash
python client_brief_generator.py \
    --client-id "client-name" \
    --drive-folder-id "1ABC123..."
```

**That's 4 arguments down to 2!** 🎉

## Usage Examples

### Most Common Use Case
```bash
# Generate brief and upload to Drive (automatic)
python client_brief_generator.py \
    --client-id "client-name" \
    --drive-folder-id "1ABC123..."
```

### Generate Without Upload
```bash
# Only generate locally, don't upload
python client_brief_generator.py \
    --client-id "client-name" \
    --no-upload-to-drive
```

### With Custom Options
```bash
# With verbose output and custom credentials
python client_brief_generator.py \
    --client-id "client-name" \
    --drive-folder-id "1ABC123..." \
    --credentials "/path/to/creds.json" \
    --verbose
```

### Utility Commands (Unchanged)
```bash
# List available agents
python client_brief_generator.py --list-agents

# List available corpora
python client_brief_generator.py --list-corpora
```

## Complete Workflow

### Step 1: Client Onboarding
```bash
python new_client_ingestion.py \
    --client-id "acme-corp" \
    --drive-folder-id "1ABC123XYZ..." \
    --client-homepage-url "https://acme.com"
```

### Step 2: Generate Client Brief (Automatic Upload)
```bash
python client_brief_generator.py \
    --client-id "acme-corp" \
    --drive-folder-id "1ABC123XYZ..."
```

**Done!** The brief is:
- ✅ Generated locally in `outputs/`
- ✅ Automatically uploaded to Google Drive parent folder
- ✅ Accessible via the Drive link shown in output

## Backward Compatibility

### ⚠️ Breaking Changes
These changes are **slightly breaking**:
- `--corpus-key` renamed to `--client-id` (old flag no longer works)
- `--upload-to-drive` replaced with `--no-upload-to-drive` (inverted logic)
- `--generate-brief` removed (now default)

### Migration Guide

If you have existing scripts using the old interface:

**Old Script:**
```bash
python client_brief_generator.py \
    --generate-brief \
    --corpus-key "$CLIENT" \
    --upload-to-drive
```

**Updated Script:**
```bash
python client_brief_generator.py \
    --client-id "$CLIENT" \
    --drive-folder-id "$FOLDER_ID"
```

## Help Text Improvements

The help text now clearly shows:
```
Usage: python client_brief_generator.py --client-id CLIENT_NAME [--drive-folder-id FOLDER_ID]

Examples:
  client_brief_generator.py --client-id "dodeka-digital" --drive-folder-id "1ABC123..."
      # Generate brief and upload to Drive (default)

  client_brief_generator.py --client-id "dodeka-digital" --no-upload-to-drive
      # Generate without upload

Google Drive Upload (Default Behavior):
  By default, briefs are uploaded to Google Drive when --drive-folder-id is provided.
  The brief uploads to the parent folder of the specified Drive folder (client materials folder).
  Use --no-upload-to-drive to disable automatic upload.
```

## User Feedback Improvements

### When Drive Upload is Enabled (Default)
```
📤 UPLOADING CLIENT BRIEF TO GOOGLE DRIVE
================================================================================
✅ Found parent folder ID: 1XYZ789ABC...
📤 Uploading client-name_client_brief_20250103_143022.md...
✅ Successfully uploaded to Google Drive parent folder
   📄 File ID: 1DEF456GHI...
   🔗 View link: https://drive.google.com/file/d/...
```

### When Upload is Disabled
```
⏭️  Skipping Google Drive upload (--no-upload-to-drive specified)
```

### When No Drive Folder Provided
```
💡 Tip: Add --drive-folder-id to automatically upload brief to Google Drive
```

## Benefits of New Interface

1. **Simpler**: Fewer required arguments
2. **Intuitive**: Default behavior matches most common use case
3. **Consistent**: `--client-id` matches terminology in `new_client_ingestion.py`
4. **Discoverable**: Help text clearly explains defaults
5. **Flexible**: Easy to opt-out with `--no-upload-to-drive`

## Testing

All existing functionality works with the new interface:

```bash
# Test basic generation + upload
python client_brief_generator.py --client-id "test-client" --drive-folder-id "1ABC..."

# Test without upload
python client_brief_generator.py --client-id "test-client" --no-upload-to-drive

# Test with custom queries
python client_brief_generator.py --client-id "test-client" --website-query "Focus on services"

# Test verbose mode
python client_brief_generator.py --client-id "test-client" --verbose

# Test utility commands
python client_brief_generator.py --list-agents
python client_brief_generator.py --list-corpora
```

## Documentation Updated

All documentation files have been updated:
- ✅ `DRIVE_UPLOAD_GUIDE.md` - Full guide updated
- ✅ `BRIEF_UPLOAD_QUICKSTART.md` - Quick reference updated
- ✅ `test_brief_upload.sh` - Test script updated
- ✅ In-script help text updated
- ✅ Examples in epilog updated

## Summary

The interface is now **much simpler** and follows the principle of "sensible defaults":
- Most common use case requires minimal arguments
- Default behavior is what users want 90% of the time
- Easy to override defaults when needed
- Consistent terminology across scripts
- Clear, helpful feedback at every step

