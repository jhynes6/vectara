# MarkItDown File Type Support

## Overview

The client onboarding system now supports **all file types compatible with Microsoft MarkItDown**, significantly expanding our document ingestion capabilities beyond just PDFs and Google Docs.

## Supported File Types

### 📄 Documents
- **PDF** (`.pdf`) - Portable Document Format
- **Word** (`.doc`, `.docx`) - Microsoft Word documents
- **PowerPoint** (`.ppt`, `.pptx`) - Microsoft PowerPoint presentations
- **Excel** (`.xls`, `.xlsx`) - Microsoft Excel spreadsheets
- **RTF** (`.rtf`) - Rich Text Format

### 📝 Text-Based Formats
- **Plain Text** (`.txt`) - Plain text files
- **Markdown** (`.md`) - Markdown files
- **HTML** (`.html`) - Web pages
- **XML** (`.xml`) - XML documents
- **JSON** (`.json`) - JSON data files
- **CSV** (`.csv`) - Comma-separated values

### 🖼️ Images (with OCR)
- **JPEG** (`.jpg`, `.jpeg`) - JPEG images
- **PNG** (`.png`) - PNG images
- **GIF** (`.gif`) - GIF images
- **BMP** (`.bmp`) - Bitmap images

> **Note**: MarkItDown performs OCR (Optical Character Recognition) on images to extract text content.

### 🎵 Audio (with Transcription)
- **MP3** (`.mp3`) - MP3 audio files
- **WAV** (`.wav`) - WAV audio files
- **M4A** (`.m4a`) - M4A audio files

> **Note**: MarkItDown transcribes audio files to text using speech-to-text capabilities.

### 📦 Archives
- **ZIP** (`.zip`) - ZIP archives

> **Note**: MarkItDown can process files within ZIP archives.

### ☁️ Google Workspace Files
- **Google Docs** - Extracted as plain text
- **Google Slides** - Exported as PPTX, then processed with MarkItDown
- **Google Sheets** - Exported as XLSX, then processed with MarkItDown

## Processing Flow

### Direct Text Extraction
These files are processed immediately without batch processing:
- Google Docs (using Google Docs API)
- Plain text files (`.txt`, `.md`, `.html`)

### Batch Processing with MarkItDown
These files are saved to a temporary directory and processed in batch:
- PDFs
- Microsoft Office files (Word, PowerPoint, Excel)
- Images (with OCR)
- Audio files (with transcription)
- Archives (ZIP)
- Other text-based formats (CSV, JSON, XML, RTF)

### Google Workspace Export
Google Workspace files are exported to Office formats first:
1. **Google Slides** → PPTX → MarkItDown processing
2. **Google Sheets** → XLSX → MarkItDown processing
3. **Google Docs** → Direct text extraction (no export needed)

## Configuration

### Choosing the PDF Processor

When running the client onboarding workflow, you can choose which processor to use:

```bash
uv run python run_complete_workflow.py
```

Then select your processor:
- **markitdown** (Recommended) - Handles all file types listed above
- **gpt** - Uses GPT-4o for PDFs only (legacy option)
- **pdfplumber** - Basic PDF text extraction (legacy option)

### Batch Mode

```bash
uv run python run_complete_workflow.py \
    --client-id example-client \
    --drive-folder-id 1XYZ... \
    --client-homepage-url https://example.com \
    --pdf-processor markitdown
```

## Technical Implementation

### File Type Detection

The system uses two methods to detect supported file types:

1. **MIME Type Matching**:
   ```python
   mime_type in [
       'application/pdf',
       'application/vnd.openxmlformats-officedocument.presentationml.presentation',
       'image/jpeg',
       'audio/mpeg',
       # ... and more
   ]
   ```

2. **File Extension Matching**:
   ```python
   file_name.lower().endswith(('.pdf', '.pptx', '.jpg', '.mp3', ...))
   ```

### Processing Methods

#### Google Slides Export
```python
def export_google_slides_as_pptx(self, file_id: str) -> bytes:
    """Export Google Slides as PowerPoint"""
    request = self.drive_service.files().export_media(
        fileId=file_id,
        mimeType='application/vnd.openxmlformats-officedocument.presentationml.presentation'
    )
    return request.execute()
```

#### Google Sheets Export
```python
def export_google_sheets_as_xlsx(self, file_id: str) -> bytes:
    """Export Google Sheets as Excel"""
    request = self.drive_service.files().export_media(
        fileId=file_id,
        mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    return request.execute()
```

#### Generic File Processing
```python
def _save_file_for_markitdown_processing(self, file: Dict, 
                                          file_content: bytes = None, 
                                          extension: str = None) -> str:
    """Save any file to temp directory for later batch processing with MarkItDown"""
    # Downloads file from Google Drive
    # Saves to temporary directory
    # Queues for batch processing
    # Returns placeholder text
```

## Benefits

### 🎯 Comprehensive Coverage
- Process virtually any file type your clients might have
- No need to ask clients to convert files before uploading
- Automatic handling of Google Workspace files

### 🚀 Efficient Processing
- Batch processing for optimal performance
- Automatic fallback for unsupported files
- Progress tracking and detailed logging

### 🔍 Enhanced Data Extraction
- **OCR for Images**: Extract text from screenshots, diagrams, infographics
- **Audio Transcription**: Convert meeting recordings, voice notes to text
- **Spreadsheet Data**: Extract data from Excel and Google Sheets
- **Presentation Content**: Process slide decks and presentations

### 📊 Better Client Insights
- Access content from presentations (e.g., pitch decks, case studies)
- Process audio recordings (e.g., client interviews, meetings)
- Extract data from spreadsheets (e.g., metrics, reports)
- OCR images (e.g., brand guidelines, screenshots)

## Example Usage

### Processing a Google Drive Folder with Multiple File Types

```python
from ingestion.ingest_specific_drive_folder import SpecificFolderIngestion

# Initialize ingestion
ingestion = SpecificFolderIngestion(
    folder_id="1XYZ...",
    client_id="example-client",
    pdf_processor="markitdown"  # Use MarkItDown for all supported files
)

# Start crawling
ingestion.crawl_and_save_locally()
```

### Output Example

```
🚀 Starting folder-specific crawl of: 1XYZ...
📊 Exporting Google Slides: Company Overview.gslides
📈 Exporting Google Sheets: Quarterly Metrics.gsheet
📄 Processing Office file: Case Study.docx
🖼️  Processing image (OCR): Brand Logo.png
🎵 Processing audio file (transcription): Client Interview.mp3
📦 Processing ZIP archive: Marketing Materials.zip

📄 PHASE 3: Processing 15 files with MarkItDown...
   Supported: PDFs, Office docs (PPTX, DOCX, XLSX), images, audio, and more!
🚀 Starting batch processing with MarkItDown for 15 files:
   • application/pdf: 5 file(s)
   • application/vnd.openxmlformats-officedocument.presentationml.presentation: 3 file(s)
   • application/vnd.openxmlformats-officedocument.wordprocessingml.document: 2 file(s)
   • image/jpeg: 3 file(s)
   • audio/mpeg: 2 file(s)
```

## Troubleshooting

### Issue: Audio Transcription Failing

**Solution**: Ensure you have the necessary audio processing libraries installed:
```bash
cd /Users/hynes/dev/vectara
uv pip install pydub soundfile
```

### Issue: Image OCR Not Working

**Solution**: MarkItDown uses built-in OCR capabilities. If issues persist, check the image quality and format.

### Issue: Large ZIP Files Timing Out

**Solution**: Extract ZIP files manually before uploading to Google Drive, or increase timeout settings.

### Issue: Google Workspace Export Failing

**Solution**: Ensure your service account has proper permissions to access and export Google Workspace files:
```bash
# Check permissions
uv run python test_drive_access.py
```

## Performance Considerations

### File Size Limits
- **Images**: Best for files < 10MB
- **Audio**: Processing time scales with audio length (1-5 minutes typical)
- **Office Documents**: Generally fast, but large presentations (100+ slides) may take longer
- **Archives**: Depends on contents; large ZIPs may be slow

### Batch Processing
- All non-text files are processed in batch for efficiency
- Processing happens after all files are downloaded
- Progress bars show real-time status

### Memory Usage
- Large batches may consume significant memory
- Temporary files are cleaned up automatically
- Monitor system resources for very large ingestions

## Future Enhancements

- [ ] Support for video files (with transcription)
- [ ] Improved OCR for complex layouts (tables, charts)
- [ ] Parallel batch processing for faster performance
- [ ] Custom MarkItDown configuration options
- [ ] Support for additional archive formats (RAR, 7Z, TAR)

## Related Documentation

- [MarkItDown Format Update](./MARKITDOWN_FORMAT_UPDATE.md)
- [PDF Processor Guide](./PDF_PROCESSOR_GUIDE.md)
- [Complete Workflow Guide](./COMPLETE_WORKFLOW_GUIDE.md)
- [Processor Quick Reference](./PROCESSOR_QUICK_REFERENCE.md)

---

**Last Updated**: October 3, 2025  
**Version**: 1.0.0

