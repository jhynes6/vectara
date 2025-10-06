# Client Name Metadata Implementation

## Problem Solved ✅

Every file uploaded to the Vertex AI RAG corpus now has a standardized `client_name` metadata field, regardless of source type (website or Drive materials).

## Changes Made

### 1. Website Ingestion (`ingest_client_website.py`)
- **Already supported** `--client-name` parameter
- Automatically adds `client_name` to all website metadata

### 2. Drive Ingestion (`ingest_specific_drive_folder.py`)
**Modified to support client_name:**

#### Constructor Changes:
```python
def __init__(self, credentials_file: str, delegated_user: str, folder_id: str, 
             days_back: int = 30, output_dir: str = "./ingestion/client_ingestion_outputs",
             pdf_processor: str = "gpt", client_name: str = ""):  # ← NEW
    # ...
    self.client_name = client_name  # ← NEW
```

#### Metadata Updates:
```python
# Client Intake Files
intake_metadata = {
    'source': 'client_intake',
    'content_type': 'client_intake',
    'client_name': self.client_name,  # ← ADDED
    'id': file_id,
    # ... rest of metadata
}

# Regular Client Materials
file_metadata = {
    'source': 'client_materials', 
    'content_type': content_type,
    'client_name': self.client_name,  # ← ADDED
    'id': file_id,
    # ... rest of metadata
}
```

#### Command Line Support:
```bash
--client-name "client-name-here"  # ← NEW PARAMETER
```

### 3. Main Workflow (`new_client_ingestion.py`)
**Modified to pass client_name to both processes:**

#### Website Ingestion:
```python
website_args = [
    "--url", self.client_homepage_url,
    "--output-dir", self.client_output_dir,
    "--workers", str(self.workers),
    "--client-name", self.client_id  # ← Already existed
]
```

#### Drive Ingestion:
```python
drive_args = [
    "--folder-id", self.drive_folder_id,
    "--output-dir", self.client_output_dir,
    "--credentials", self.credentials_file,
    "--pdf-processor", self.pdf_processor,
    "--client-name", self.client_id  # ← ADDED
]
```

### 4. PDF Re-processing (`reprocess_failed_pdfs.py`)
- **No changes needed** - preserves existing metadata including `client_name`
- Only updates: `word_count`, `reprocessed`, `reprocessing_method`

## Result: Standardized Metadata Structure

### Website Files:
```json
{
  "source": "website",
  "content_type": "homepage", 
  "client_name": "prospex",
  "url": "https://prospex.ai",
  "title": "Homepage",
  "domain": "prospex.ai",
  "scraped_time": "2025-10-03T17:30:00.000000",
  "word_count": 450
}
```

### Drive Files - Client Materials:
```json
{
  "source": "client_materials",
  "content_type": "pitch_decks",
  "client_name": "prospex", 
  "id": "1MLykqa6SInOqeWTNPpfc-Yf0ZQFatVBE",
  "name": "MintLeads_Deck_v3.pdf",
  "url": "https://drive.google.com/file/d/1MLykqa6SInOqeWTNPpfc-Yf0ZQFatVBE/view",
  "scraped_time": "2025-10-03T17:48:47.484525",
  "word_count": 1338
}
```

### Drive Files - Client Intake:
```json
{
  "source": "client_intake",
  "content_type": "client_intake",
  "client_name": "prospex",
  "id": "1ABC123xyz",
  "name": "Client Intake Form.docx", 
  "url": "https://docs.google.com/document/d/1ABC123xyz/view",
  "scraped_time": "2025-10-03T17:48:47.484525",
  "word_count": 2500
}
```

## Usage Examples

### Standalone Scripts:
```bash
# Website ingestion
python ingestion/ingest_client_website.py \
  --url "https://example.com" \
  --client-name "example-client" \
  --output-dir "./output"

# Drive ingestion  
python ingestion/ingest_specific_drive_folder.py \
  --folder-id "1ABC123xyz" \
  --client-name "example-client" \
  --output-dir "./output"
```

### Complete Workflow:
```bash
# Automatically uses client_id as client_name for both processes
python run_complete_workflow.py \
  --client-id "example-client" \
  --drive-folder-id "1ABC123xyz" \
  --client-homepage-url "https://example.com"
```

## Benefits

### ✅ Data Consistency
- **Every file** in the corpus has `client_name` field
- **Standardized** across all source types
- **Automatic** - no manual intervention needed

### ✅ Better RAG Queries  
- Filter by client: `WHERE client_name = 'prospex'`
- Multi-client corpus support
- Clear data attribution

### ✅ Metadata-Rich Corpus
- Enhanced filtering capabilities
- Better data organization  
- Improved brief generation accuracy

### ✅ Backward Compatibility
- All existing functionality preserved
- Optional parameter for standalone scripts
- Graceful handling of missing client_name

## Verification

After ingestion, all metadata files will contain:
```json
{
  "client_name": "client-id-here",
  // ... other metadata fields
}
```

Files uploaded to Vertex AI RAG corpus will have this metadata for enhanced querying and organization. 🎯
