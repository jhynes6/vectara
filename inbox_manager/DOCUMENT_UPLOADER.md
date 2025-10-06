# 📤 Document Uploader with Upsert Logic

## Overview

The Document Uploader handles inserting and updating documents in the `documents` table with a unique constraint on `(client_id, uri)`. If a document already exists, it updates it instead of creating a duplicate.

## Features

✅ **Upsert Logic** - Insert or update based on (client_id, uri)  
✅ **Unique Constraint** - Automatic constraint creation  
✅ **Batch Operations** - Upload multiple documents efficiently  
✅ **Safe Updates** - Existing documents update, not duplicate  
✅ **Foreign Key Support** - Works with clients table constraint

## Key Functionality

### 1. Unique Constraint

The uploader ensures a unique constraint exists:
```sql
ALTER TABLE documents 
ADD CONSTRAINT documents_client_id_uri_key 
UNIQUE (client_id, uri);
```

This allows PostgreSQL's `ON CONFLICT` to work for upserts.

### 2. Upsert on Conflict

When uploading a document:
- **If exists** (same client_id + uri) → **UPDATE** all fields
- **If new** → **INSERT** new row

```python
INSERT INTO documents (...) 
VALUES (...)
ON CONFLICT (client_id, uri) 
DO UPDATE SET
    title = EXCLUDED.title,
    metadata = EXCLUDED.metadata,
    ...
RETURNING id;
```

## Usage

### Basic Example

```python
from document_uploader import DocumentUploader

uploader = DocumentUploader()

# Ensure constraint exists (run once)
uploader.ensure_unique_constraint()

# Upload/update a document
doc_id = uploader.upsert_document(
    client_id="dodeka-digital-supa",
    uri="https://example.com/page",
    title="My Page",
    content_type="services",
    source_type="website",
    metadata={
        "url": "https://example.com/page",
        "scraped_time": "2025-10-04T12:00:00"
    }
)

print(f"Document ID: {doc_id}")
```

### Batch Upload

```python
documents = [
    {
        "client_id": "dodeka-digital-supa",
        "uri": "https://example.com/page1",
        "title": "Page 1",
        "content_type": "services"
    },
    {
        "client_id": "dodeka-digital-supa",
        "uri": "https://example.com/page2",
        "title": "Page 2",
        "content_type": "case_studies"
    }
]

ids = uploader.upsert_documents_batch(documents)
print(f"Uploaded {len(ids)} documents")
```

### Retrieve Document

```python
doc = uploader.get_document_by_uri(
    client_id="dodeka-digital-supa",
    uri="https://example.com/page"
)

if doc:
    print(f"Title: {doc['title']}")
    print(f"Metadata: {doc['metadata']}")
```

### Delete Document

```python
success = uploader.delete_document(
    client_id="dodeka-digital-supa",
    uri="https://example.com/page"
)
```

## Document Fields

### Required Fields
- **client_id** (text) - Client identifier, must exist in `clients` table
- **uri** (text) - Document URI/URL

### Optional Fields
- **title** (text) - Document title
- **sha256** (text) - Content hash for change detection
- **mime_type** (text) - MIME type (e.g., "text/html")
- **language** (text) - Language code (e.g., "en")
- **metadata** (jsonb) - Additional metadata
- **source_type** (text) - Source (e.g., "website", "gdrive")
- **content_type** (text) - Content category (e.g., "services", "case_studies")

### Auto-Generated Fields
- **id** (uuid) - Primary key, auto-generated
- **ingested_at** (timestamp) - Auto-set to current time on insert/update

## Integration with Ingestion

### From Website Scraper

```python
from document_uploader import DocumentUploader
import json

# After scraping a website page
uploader = DocumentUploader()

doc_id = uploader.upsert_document(
    client_id="client-name",
    uri=scraped_url,
    title=page_title,
    content_type=categorized_type,  # from LLM categorization
    source_type="website",
    metadata={
        "url": scraped_url,
        "domain": domain,
        "path": url_path,
        "scraped_time": datetime.now().isoformat(),
        "word_count": word_count,
        "client_name": client_name
    }
)
```

### From Google Drive

```python
doc_id = uploader.upsert_document(
    client_id="client-name",
    uri=drive_file_url,
    title=file_name,
    sha256=file_hash,
    mime_type=file_mime_type,
    content_type="case_studies",
    source_type="gdrive",
    metadata={
        "folder_id": folder_id,
        "file_id": file_id,
        "last_modified": last_modified_date,
        "owners": owners_list
    }
)
```

## Behavior Examples

### Example 1: First Upload
```python
# First time - creates new document
doc_id = uploader.upsert_document(
    client_id="client-a",
    uri="https://site.com/page",
    title="Original Title"
)
# Returns: uuid-1234-5678-...
```

### Example 2: Update Existing
```python
# Second time - updates same document
doc_id = uploader.upsert_document(
    client_id="client-a",
    uri="https://site.com/page",  # Same URI
    title="Updated Title"  # New title
)
# Returns: uuid-1234-5678-... (SAME ID!)
```

### Example 3: Different Client, Same URI
```python
# Different client - creates new document
doc_id = uploader.upsert_document(
    client_id="client-b",  # Different client
    uri="https://site.com/page",  # Same URI
    title="Client B's Version"
)
# Returns: uuid-9999-8888-... (DIFFERENT ID)
```

## Testing

Run the test suite:
```bash
cd inbox_manager
source venv/bin/activate
python document_uploader.py
```

Expected output:
```
1️⃣ Ensuring unique constraint...
   ✅ Unique constraint already exists

2️⃣ Testing single document upsert...
   Created/Updated: uuid-...

3️⃣ Updating same document with new title...
   Updated: uuid-...
   Same ID: True ✅

4️⃣ Retrieving document...
   Title: Test Page - Updated
   Metadata: {'test': True, 'updated': True}

5️⃣ Testing batch upsert...
   Created/Updated 2 documents

6️⃣ Cleaning up test documents...

✅ All tests completed!
```

## Error Handling

### Foreign Key Constraint
If client_id doesn't exist in `clients` table:
```
psycopg2.errors.ForeignKeyViolation: 
insert or update on table "documents" violates foreign key constraint
```

**Solution**: Ensure client exists before uploading documents.

### Missing Required Fields
```python
# Will skip with warning
uploader.upsert_documents_batch([
    {"title": "Missing client_id"}  # ❌ Will be skipped
])
```

## Performance

### Single Upsert
- **Speed**: ~10-50ms per document
- **Use case**: Real-time updates, single document changes

### Batch Upsert
- **Speed**: ~20-100ms for 10 documents
- **Use case**: Bulk ingestion, website scraping

### Recommendation
- Use **single upsert** for: Real-time updates, webhooks
- Use **batch upsert** for: Initial ingestion, periodic syncs

## Database Schema

```sql
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id TEXT NOT NULL REFERENCES clients(id),
    uri TEXT,
    title TEXT,
    sha256 TEXT,
    mime_type TEXT,
    language TEXT,
    metadata JSONB NOT NULL DEFAULT '{}',
    source_type TEXT,
    content_type TEXT,
    ingested_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    
    -- Unique constraint for upserts
    CONSTRAINT documents_client_id_uri_key UNIQUE (client_id, uri)
);
```

## Best Practices

### 1. Always Use Full URI
```python
# ✅ Good - full URI
uri="https://example.com/page?id=123"

# ❌ Bad - relative path
uri="/page"
```

### 2. Include Metadata
```python
# ✅ Good - rich metadata
metadata={
    "url": full_url,
    "scraped_time": timestamp,
    "word_count": count,
    "client_name": name
}

# ❌ Bad - missing metadata
metadata={}
```

### 3. Use Content Types
```python
# ✅ Good - categorized
content_type="case_studies"

# ❌ Bad - generic
content_type="other"
```

### 4. Hash for Change Detection
```python
import hashlib

content_hash = hashlib.sha256(content.encode()).hexdigest()

uploader.upsert_document(
    client_id=client_id,
    uri=uri,
    sha256=content_hash  # ✅ Can detect if content changed
)
```

## Future Enhancements

Potential improvements:
- [ ] Bulk upsert with execute_values for better performance
- [ ] Change detection based on sha256 hash
- [ ] Soft delete with is_deleted flag
- [ ] Version history tracking
- [ ] Automatic metadata extraction from content
- [ ] Webhook notifications on upsert
- [ ] Async/bulk operations with transaction batching

---

**Status**: ✅ Production ready  
**Constraint**: Unique on (client_id, uri)  
**Behavior**: Insert new or update existing

