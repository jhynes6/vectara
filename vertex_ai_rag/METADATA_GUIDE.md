# Metadata and Embedding Visibility Guide

## What's Available in Vertex AI RAG

### ✅ File-Level Metadata (Supported)

Each file in a RAG corpus has these attributes:

| Field | Type | Supported | Notes |
|-------|------|-----------|-------|
| `display_name` | string | ✅ | File name shown in console |
| `description` | string | ✅ | Text description (currently not set by our code) |
| `gcs_source` | URI | ✅ | Source GCS location |
| `create_time` | timestamp | ✅ | When file was added |
| `update_time` | timestamp | ✅ | Last modification |
| `file_status` | enum | ✅ | ACTIVE, PROCESSING, etc. |
| `size_bytes` | int | ✅ | File size |
| `user_metadata` | dict | ❌ | **NOT SUPPORTED** by Vertex AI RAG API |

### ❌ Not Available

- **Custom metadata tags**: Vertex AI RAG doesn't support custom key-value metadata on files
- **Direct embedding access**: Embeddings are generated and used internally, not exposed via API
- **Chunk-level metadata**: Can't attach metadata to individual chunks
- **Vector inspection**: Can't view or download the actual embedding vectors

## Workarounds Implemented

### 1. GCS Metadata Storage

We store metadata on the GCS objects that back the RAG files:

```python
# Metadata is stored in GCS bucket as object metadata
blob.metadata = {
    'source': 'client_materials',
    'content_type': 'pitch_deck',
    'client_id': 'mintleads'
}
```

**Pros:** Preserves metadata for later retrieval  
**Cons:** Not queryable from RAG, not used in retrieval

### 2. Description Field Encoding

We encode key metadata into the file description:

```python
description = "Source: client_materials | Type: pitch_deck | content_type: brochure"
```

**Pros:** Visible in RAG corpus listings  
**Cons:** Limited length, not structured, not queryable

## Inspection Tools

### List Files in Corpus

```bash
# Basic listing
python inspect_corpus.py --corpus-name client-mintleads

# With detailed attributes
python inspect_corpus.py --corpus-name client-mintleads --details
```

### Check File Metadata

```bash
# List all corpora
python setup_corpus.py --list

# Get corpus statistics
python setup_corpus.py --list
```

## Metadata Sources in Ingestion

### Summary

| Source Type | Metadata Location | Extraction Method |
|-------------|-------------------|-------------------|
| **Website** | YAML frontmatter at top of .md file | `_extract_frontmatter()` |
| **Client Materials** | `.md.metadata.json` sidecar file | `_load_metadata()` |
| **Client Intake** | `.md.metadata.json` sidecar file | `_load_metadata()` |

### Website Files (YAML Frontmatter)

Location: `client_ingestion_outputs/{client}/website/*.md`

Format at top of each .md file:
```yaml
---
source: "website"
content_type: "case_studies"
url: "https://mintleads.io/case-study/sock-fancy/"
title: "Sock Fancy"
domain: "mintleads.io"
path: "/case-study/sock-fancy/"
scraped_time: "2025-09-07T06:32:02.557381"
url_depth: 2
word_count: 146
client_name: "mintleads"
---
```

Extracted by: `_extract_frontmatter()` method

### Client Materials Files (JSON Sidecar)

Location: `client_ingestion_outputs/{client}/client_materials/*.md`

Metadata in: `{filename}.md.metadata.json`

Example:
- File: `case_studies_mintleads-casestudy-saber-cs-1138-6.md`
- Metadata: `case_studies_mintleads-casestudy-saber-cs-1138-6.md.metadata.json`

Format:
```json
{
  "source": "client_materials",
  "content_type": "case_studies",
  "original_filename": "mintleads-casestudy-saber-cs-1138-6.pdf",
  "doc_id": "cs-1138-6"
}
```

Extracted by: `_load_metadata()` method

### Client Intake Forms (JSON Sidecar)

Location: `client_ingestion_outputs/{client}/client_intake_form/*.md`

Metadata in: `{filename}.md.metadata.json`

Example:
- File: `client_intake_client-intake-form-g4d-productions.md`
- Metadata: `client_intake_client-intake-form-g4d-productions.md.metadata.json`
- Full path: `ingestion/client_ingestion_outputs/g4dproductions/client_intake_form/client_intake_client-intake-form-g4d-productions.md.metadata.json`

Format:
```json
{
  "source": "client_intake_form",
  "content_type": "client_intake_form",
  "form_type": "initial_intake",
  "submission_date": "2024-10-01"
}
```

Extracted by: `_load_metadata()` method

## Current Metadata Flow

```
Input Files
    ├─ website/*.md → YAML frontmatter
    ├─ client_materials/*.md → .metadata.json
    └─ client_intake_form/*.md → .metadata.json
        ↓
client_ingestion_adapter.py 
    ├─ Discovers files by source type
    ├─ Extracts metadata (frontmatter or JSON)
    ├─ Passes to VertexRAGClient.upload_file()
        ↓
VertexRAGClient.upload_file()
    ├─ Uploads file to GCS
    ├─ Sets GCS object metadata ✅
    ├─ Encodes key fields in description ✅
    ├─ Calls rag.import_files()
        ↓
Vertex AI RAG
    ├─ Creates embeddings (text-embedding-004)
    ├─ Stores in vector database
    ├─ Makes searchable
    └─ Embeddings NOT accessible ❌
```

## What You CAN Do

### 1. Filter by Display Name

```python
files = rag_client.list_files(corpus_name)
pitch_decks = [f for f in files if 'pitch_deck' in f.display_name]
```

### 2. Query with RAG Retrieval

The most useful "metadata" is the retrieval ranking itself:

```python
# Query returns relevant chunks with similarity scores
results = rag.retrieval_query(
    corpus_name=corpus_name,
    text="Tell me about pricing",
    similarity_top_k=10,
    vector_distance_threshold=0.4
)
```

### 3. Access GCS Metadata

If you need the full metadata later:

```python
from google.cloud import storage

storage_client = storage.Client()
bucket = storage_client.bucket("walkinto-473412-vertex-rag-temp")
blob = bucket.blob("rag-uploads/pricing.md")

# Get metadata
metadata = blob.metadata
# Returns: {'source': 'client_materials', 'content_type': 'pricing', ...}
```

## Recommendations

### For Now (with current limitations)

1. **Use descriptive filenames**: `client_materials_pricing_2024.md`
2. **Leverage folder structure in GCS**: `gs://bucket/client/materials/pricing/`
3. **Track metadata externally**: Keep a separate database/spreadsheet
4. **Use corpus-per-client**: Separate corpus for each client (we do this!)

### Future Possibilities

If Google adds metadata support:
- Tag files by `source`, `content_type`, `date`, `category`
- Filter retrieval by metadata
- Implement faceted search
- Track document versions

## Example: Current vs. Ideal

### Current (Limited)

```python
# Upload
upload_file(
    corpus_name="client-mintleads",
    file_path="pricing.md",
    display_name="mintleads_pricing.md",
    description="Source: client_materials | Type: pricing"
    # metadata ignored by RAG ❌
)

# Retrieve - no filtering
results = rag.retrieval_query(
    corpus_name="client-mintleads",
    text="pricing information"
)
```

### Ideal (If supported)

```python
# Upload
upload_file(
    corpus_name="client-mintleads",
    file_path="pricing.md",
    metadata={
        'source': 'client_materials',
        'content_type': 'pricing',
        'date': '2024-10-01',
        'category': 'financial'
    }
)

# Retrieve with filtering
results = rag.retrieval_query(
    corpus_name="client-mintleads",
    text="pricing information",
    metadata_filter={
        'source': 'client_materials',
        'content_type': 'pricing'
    }
)
```

## References

- [Vertex AI RAG Documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/rag-overview)
- [GCS Object Metadata](https://cloud.google.com/storage/docs/metadata)
- Our implementation: `shared/vertex_rag_client.py`

---

**Last Updated:** 2025-10-03  
**Status:** Metadata support limited by Vertex AI RAG API

