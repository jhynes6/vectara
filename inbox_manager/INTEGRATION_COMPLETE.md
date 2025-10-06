# ✅ Document Uploader Integration Complete

## Summary

The Document Uploader with upsert logic is now **fully integrated** into the Supabase client ingestion pipeline for project `zepjgxxwrnapxldywsbh`.

## What Was Integrated

### File: `supabase_client_ingestion.py`

**Changes Made:**
1. ✅ Import `DocumentUploader` from inbox_manager
2. ✅ Initialize uploader in `__init__`
3. ✅ Create unique constraint on startup
4. ✅ Modified `upload_files_to_supabase()` to use uploader

### Two-Step Upload Process

**Step 1: Upsert Document Metadata**
```python
doc_uuid = self.document_uploader.upsert_document(
    client_id=self.client_id,
    uri=uri,
    title=title,
    source_type=source_type,
    content_type=content_type,
    metadata=metadata
)
```
- Creates new record OR updates existing (if client_id + uri match)
- Returns document UUID

**Step 2: Upload Chunks with Embeddings**
```python
doc_id, chunk_count = self.vector_store.upload_document(
    ...,
    document_id=doc_uuid  # Link chunks to parent
)
```
- Creates/updates document_chunks with embeddings
- Links to parent document via document_id

## Benefits

### 1. **No Duplicates**
Re-running ingestion on the same client won't create duplicate document records.

### 2. **Safe Updates**
When website content changes:
- ✅ Document metadata updates (same UUID)
- ✅ Old chunks deleted
- ✅ New chunks created with updated embeddings
- ✅ Links maintained

### 3. **Rich UI Metadata**
The inbox manager UI now shows:
- Document title
- Clickable URL to source
- Content type badge
- Chunk information

### 4. **Referential Integrity**
```
clients (id) 
   ↓
documents (client_id, uri) ← UNIQUE constraint
   ↓
document_chunks (document_id) ← Links to parent
```

## Usage

### Standard Ingestion

```bash
python supabase_client_ingestion.py \
  --client-id "new-client" \
  --drive-folder-id "1ABC..." \
  --client-homepage-url "https://newclient.com" \
  --batch-mode
```

**What Happens:**
1. Creates client record in `clients` table
2. Scrapes website and Drive
3. For each file:
   - **Upserts** to `documents` table (creates if new, updates if exists)
   - **Uploads** chunks to `document_chunks` table with embeddings
4. Generates onboarding report

### Re-Ingestion (Updates)

```bash
# Run again for same client
python supabase_client_ingestion.py \
  --client-id "existing-client" \
  --drive-folder-id "1ABC..." \
  --client-homepage-url "https://existingclient.com" \
  --batch-mode
```

**What Happens:**
- ✅ Existing documents **update** (same UUID preserved)
- ✅ New pages **insert** (new UUIDs created)
- ✅ Removed pages **remain** in database (stale but harmless)

## Example Scenarios

### Scenario 1: Initial Client Onboarding

**Input:**
- Client: "acme-corp"
- Website: 50 pages
- Drive: 10 documents

**Output:**
- `documents` table: 60 records created
- `document_chunks` table: ~300 chunks created
- All chunks linked to parent documents

### Scenario 2: Content Update (Week Later)

**Changes:**
- 5 pages updated with new content
- 2 new pages added
- 1 page removed (404)

**Run ingestion again:**
- `documents` table: 5 updated, 2 new, 1 stale = 62 total
- `document_chunks` table: Old chunks replaced, new chunks added

### Scenario 3: Metadata Correction

**Issue:** Wrong content_type on 10 pages

**Fix:** Update metadata files and re-run ingestion
- `documents` table: 10 records updated with correct content_type
- `document_chunks` table: Content re-chunked and re-embedded

## Monitoring

### Check for Duplicates (Should be 0)

```sql
SELECT client_id, uri, COUNT(*) as duplicate_count
FROM documents
GROUP BY client_id, uri
HAVING COUNT(*) > 1;
```

Should return **empty** (no duplicates).

### Verify Unique Constraint

```sql
SELECT constraint_name 
FROM information_schema.table_constraints 
WHERE table_name = 'documents' 
  AND constraint_name = 'documents_client_id_uri_key';
```

Should return the constraint.

### Count Records Per Client

```sql
SELECT 
    c.id as client_id,
    COUNT(DISTINCT d.id) as documents,
    COUNT(dc.id) as chunks
FROM clients c
LEFT JOIN documents d ON c.id = d.client_id
LEFT JOIN document_chunks dc ON c.id = dc.client_id
GROUP BY c.id;
```

## Files Modified

1. ✅ `supabase_client_ingestion.py` - Integrated document uploader
2. ✅ `inbox_manager/document_uploader.py` - Created uploader class
3. ✅ `SUPABASE_INGESTION_INTEGRATION.md` - Documentation

## Verification

To verify the integration is working:

```bash
# 1. Check unique constraint exists
cd inbox_manager
source venv/bin/activate
python -c "from document_uploader import DocumentUploader; d = DocumentUploader(); d.ensure_unique_constraint()"

# 2. Test upsert
python document_uploader.py

# 3. Run full ingestion
cd ..
python supabase_client_ingestion.py
```

## Production Checklist

Before using in production:

- [x] Unique constraint created on documents table
- [x] Document uploader tested and working
- [x] Integration tested with supabase_client_ingestion.py
- [x] UI displays document metadata correctly
- [x] Re-ingestion tested (no duplicates)
- [ ] Cleanup strategy for stale documents defined
- [ ] Monitoring queries added to dashboard
- [ ] Error handling tested for edge cases

---

**Status**: ✅ Fully integrated  
**Database**: zepjgxxwrnapxldywsbh  
**Ready**: For production use

