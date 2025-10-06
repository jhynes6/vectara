# Vertex AI RAG Integration - COMPLETE ✅

## Status: **Fully Integrated**

The integration to switch from Vectara to Vertex AI RAG for client onboarding is now **complete**. All new client onboarding workflows now use Vertex AI RAG as the vector database.

## What Changed

### 1. **new_client_ingestion.py**
- ✅ Renamed class from `VectaraClientOnboarder` to `VertexAIClientOnboarder`
- ✅ Replaced Vectara SDK imports with Vertex AI RAG components
- ✅ Updated `create_vectara_corpus()` → `create_vertex_corpus()`
- ✅ Updated `upload_files_to_vectara()` → `upload_files_to_vertex_ai()`
- ✅ Integrated with `ClientIngestionAdapter` for seamless file uploads
- ✅ All logging and user-facing messages updated to reference Vertex AI

### 2. **run_complete_workflow.py**
- ✅ Updated to use `VertexAIClientOnboarder` instead of `VectaraClientOnboarder`
- ✅ Updated all method calls to use Vertex AI equivalents
- ✅ Updated user prompts and documentation
- ✅ Adjusted indexing wait time for Vertex AI

### 3. **Architecture**
```
Client Onboarding Flow (Vertex AI RAG):
┌─────────────────────────────────────────────────────────────┐
│  1. Create directory structure                              │
│     └─ ingestion/client_ingestion_outputs/{client_id}/      │
│        ├─ website/                                          │
│        ├─ client_materials/                                 │
│        └─ client_intake_form/                               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  2. Create Vertex AI RAG Corpus                             │
│     └─ Display name: "client-{client_id}"                   │
│     └─ Stored in: Vertex AI RAG Engine                      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  3. Run Content Ingestion (parallel)                        │
│     ├─ Website scraping (Bright Data)                       │
│     └─ Google Drive ingestion                               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  4. Upload to Vertex AI RAG                                 │
│     └─ ClientIngestionAdapter handles:                      │
│        ├─ File discovery                                    │
│        ├─ Metadata extraction                               │
│        └─ Upload to Vertex AI corpus                        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  5. Generate onboarding report                              │
│     └─ ingestion/client_ingestion_outputs/{client}/         │
│        onboarding_report.json                               │
└─────────────────────────────────────────────────────────────┘
```

## Usage

**Important:** This project uses `uv` for package management. All scripts must be run with `uv run python` instead of just `python`.

### New Client Onboarding (Interactive Mode)
```bash
uv run python run_complete_workflow.py
```

### New Client Onboarding (Batch Mode)
```bash
uv run python run_complete_workflow.py \
    --client-id acme-corp \
    --drive-folder-id 1XYZ... \
    --client-homepage-url https://acme.com \
    --pdf-processor markitdown
```

### Direct Ingestion Script
```bash
uv run python new_client_ingestion.py \
    --batch-mode \
    --client-id acme-corp \
    --drive-folder-id 1XYZ... \
    --client-homepage-url https://acme.com
```

> See [RUNNING_SCRIPTS.md](../RUNNING_SCRIPTS.md) for more details on using `uv run`.

## Configuration Required

### Environment Variables (.env)
```bash
# Google Cloud / Vertex AI
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=/path/to/vertex-service-account.json

# OpenAI (for agents and LLM categorization)
OPENAI_API_KEY=your-openai-api-key

# Bright Data (for website scraping)
BRIGHT_DATA_API_KEY=your-bright-data-key
```

### Service Account Permissions
The Vertex AI service account needs:
- `aiplatform.ragCorpora.create`
- `aiplatform.ragCorpora.get`
- `aiplatform.ragCorpora.list`
- `aiplatform.ragFiles.upload`
- `aiplatform.ragFiles.get`

## Benefits of Vertex AI RAG

1. **Google Cloud Native** - Fully integrated with Google Cloud ecosystem
2. **Better Metadata Support** - Rich metadata capabilities for filtering
3. **Improved Performance** - Optimized for large-scale deployments
4. **Cost Efficiency** - More predictable pricing model
5. **Future-Proof** - Active development and feature additions from Google

## Ingestion Format

The ingestion output format remains unchanged:
- ✅ Markdown files with frontmatter metadata (website)
- ✅ Markdown files with JSON sidecar metadata (client materials)
- ✅ Same directory structure
- ✅ Same categorization system

This means:
- **No changes needed** to existing ingestion scripts
- **Compatible** with both platforms during migration
- **Easy to re-upload** existing clients to Vertex AI

## Metadata Structure

### Client Intake Form
```json
{
  "source": "client_intake_form",
  "content_type": "client_intake_form",
  "client_id": "acme-corp",
  "created_at": "2025-10-03T12:00:00Z",
  "last_updated_at": "2025-10-03T12:00:00Z"
}
```

### Client Materials
```json
{
  "source": "client_materials",
  "content_type": "case_studies|services_products|blogs_resources|...",
  "client_id": "acme-corp",
  "original_filename": "case-study.pdf",
  "drive_file_id": "1ABC...",
  "mime_type": "application/pdf"
}
```

### Website Pages
```json
{
  "source": "website",
  "content_type": "case_studies|services_products|blogs_resources|...",
  "client_id": "acme-corp",
  "url": "https://acme.com/page",
  "scraped_time": "2025-10-03T12:00:00Z"
}
```

## Migration of Existing Clients

To migrate an existing client from Vectara to Vertex AI:

```bash
# 1. Create Vertex AI corpus
uv run python vertex_ai_rag/setup_corpus.py --client-id CLIENT_ID

# 2. Upload existing ingestion output
uv run python vertex_ai_rag/ingestion/client_ingestion_adapter.py --client-id CLIENT_ID
```

The migration script will:
- ✅ Find existing ingestion output in `ingestion/client_ingestion_outputs/{client_id}/`
- ✅ Create a new Vertex AI RAG corpus
- ✅ Upload all files with proper metadata
- ✅ Preserve all categorization and metadata

## Testing

To test the integration:

1. **Test corpus creation:**
   ```bash
   uv run python vertex_ai_rag/setup_corpus.py --list
   ```

2. **Test with a sample client:**
   ```bash
   uv run python run_complete_workflow.py \
       --client-id test-client \
       --drive-folder-id YOUR_FOLDER_ID \
       --client-homepage-url https://example.com \
       --skip-brief
   ```

3. **Verify upload:**
   ```bash
   uv run python vertex_ai_rag/setup_corpus.py --list
   # Should show the new corpus with files
   ```

## Troubleshooting

### "ModuleNotFoundError: No module named 'vertexai'"
- **Problem:** You're using `python` directly instead of `uv run python`
- **Solution:** Always use `uv run python` for all scripts
- See [RUNNING_SCRIPTS.md](../RUNNING_SCRIPTS.md) for details

### "Import could not be resolved" errors
- These are linter warnings only
- Runtime will work correctly due to dynamic path manipulation
- Can be safely ignored

### "No corpus found" error
- Run: `uv run python vertex_ai_rag/setup_corpus.py --client-id CLIENT_ID`
- Verify corpus exists: `uv run python vertex_ai_rag/setup_corpus.py --list`

### Authentication errors
- Check `GOOGLE_APPLICATION_CREDENTIALS` points to valid service account JSON
- Verify service account has required Vertex AI permissions
- Check `GOOGLE_CLOUD_PROJECT` is set correctly

### Upload failures
- Check file formats (should be .md files)
- Verify metadata JSON is valid
- Check Vertex AI API quota limits

## Next Steps

1. ✅ **Integration complete** - New clients automatically use Vertex AI
2. 📝 **Update agents** - Configure agents to use client-specific corpora
3. 📊 **Migrate existing clients** - Run migration script for historical data
4. 🧪 **Production testing** - Monitor first few production onboardings
5. 🔧 **Optimize** - Fine-tune based on production experience

## Support

For issues or questions:
- Check logs in `logs/new_client_ingestion.log`
- Review onboarding report: `ingestion/client_ingestion_outputs/{client}/onboarding_report.json`
- Consult Vertex AI RAG documentation in `vertex_ai_rag/README.md`

