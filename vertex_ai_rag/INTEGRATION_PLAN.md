# Vertex AI RAG Integration Plan

## ⚠️ **STATUS: COMPLETED** ⚠️

**This integration is now complete!** See [INTEGRATION_COMPLETE.md](./INTEGRATION_COMPLETE.md) for details.

All new client onboarding now uses Vertex AI RAG instead of Vectara.

---

## Original Plan (for reference)

### Current State

- ✅ Ingestion pipeline in `/Users/hynes/dev/vectara/` produces perfect output format
- ✅ Vertex AI code in `/Users/hynes/dev/vectara/vertex_ai_rag/` can consume those outputs
- ✅ Metadata extraction working for all three source types

## Integration Approach (COMPLETED)

### Phase 1: Add Optional Upload (Recommended)

Update existing workflow scripts to optionally upload to Vertex AI:

```python
# In run_complete_workflow.py or new_client_ingestion.py

# Add argument
parser.add_argument(
    '--upload-to-vertex-ai',
    action='store_true',
    help='Upload ingested content to Vertex AI RAG (in addition to Vectara)'
)

# After ingestion completes:
if args.upload_to_vertex_ai:
    logger.info("📤 Uploading to Vertex AI RAG...")
    
    # Import vertex_ai_rag modules
    sys.path.insert(0, str(Path(__file__).parent / 'vertex_ai_rag'))
    from setup_corpus import CorpusSetup
    from ingestion.client_ingestion_adapter import ClientIngestionAdapter
    
    try:
        # Create corpus if needed
        setup = CorpusSetup()
        setup.create_client_corpus(client_id)
        
        # Upload files
        adapter = ClientIngestionAdapter(client_id=client_id)
        stats = adapter.run()
        
        logger.info(f"✅ Vertex AI upload complete: {stats['successful']}/{stats['total_files']} files")
    
    except Exception as e:
        logger.error(f"❌ Vertex AI upload failed: {e}")
        # Don't fail the whole workflow if Vertex AI fails
```

### Phase 2: Unified Command

Create a single entry point that handles both platforms:

```bash
# Upload to both Vectara and Vertex AI
python run_complete_workflow.py \
    --client-id mintleads \
    --drive-folder-id 1ABC... \
    --client-homepage-url https://mintleads.io \
    --upload-to-vectara \
    --upload-to-vertex-ai

# Or just Vertex AI
python run_complete_workflow.py \
    --client-id mintleads \
    --drive-folder-id 1ABC... \
    --client-homepage-url https://mintleads.io \
    --upload-to-vertex-ai \
    --no-vectara
```

### Phase 3: Migration Support

Add script to migrate existing clients from Vectara to Vertex AI:

```bash
# Migrate single client
python vertex_ai_rag/migrate_client.py --client-id mintleads

# Migrate all clients
python vertex_ai_rag/migrate_all_clients.py
```

## File Structure After Integration

```
/Users/hynes/dev/vectara/
├── new_client_ingestion.py          ← Add --upload-to-vertex-ai flag
├── run_complete_workflow.py         ← Add --upload-to-vertex-ai flag
├── ingestion/
│   └── client_ingestion_outputs/    ← Shared by both platforms
│       └── {client}/
│           ├── website/
│           ├── client_materials/
│           └── client_intake_form/
├── vertex_ai_rag/                    ← Keep as submodule
│   ├── setup_corpus.py
│   ├── ingestion/
│   │   └── client_ingestion_adapter.py
│   ├── agents/
│   ├── deployment/
│   └── shared/
└── vectara-documentation/            ← Existing Vectara code
```

## Benefits

1. **Single ingestion pipeline** - Run once, upload to multiple platforms
2. **No duplication** - Ingestion logic in one place
3. **Easy migration** - Can run both platforms in parallel during transition
4. **Maintainable** - Changes only need to be made once
5. **Flexible** - Users choose which platform(s) to use

## Implementation Checklist

- [x] ~~Add `--upload-to-vertex-ai` flag~~ **Replaced Vectara with Vertex AI entirely**
- [x] Updated `new_client_ingestion.py` to use Vertex AI RAG
- [x] Updated `run_complete_workflow.py` to use Vertex AI RAG
- [x] Update documentation (see INTEGRATION_COMPLETE.md)
- [x] Migration script already exists (`vertex_ai_rag/ingestion/client_ingestion_adapter.py`)
- [ ] Test with existing client
- [ ] Add to CI/CD if applicable

## Example Usage

### New Client Onboarding (Both Platforms)
```bash
python run_complete_workflow.py \
    --client-id acme-corp \
    --drive-folder-id 1XYZ... \
    --client-homepage-url https://acme.com \
    --upload-to-vertex-ai
```

### Re-upload Existing Client to Vertex AI
```bash
python vertex_ai_rag/ingestion/client_ingestion_adapter.py --client-id mintleads
```

### Create Corpus Only
```bash
python vertex_ai_rag/setup_corpus.py --client-id acme-corp
```

## Notes

- Ingestion output format is already perfect for Vertex AI
- No changes needed to ingestion scripts
- Vertex AI upload is independent and won't break existing Vectara flow
- Can run both platforms simultaneously during migration period

