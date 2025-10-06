# Root Folder Cleanup Plan

## Analysis Summary

After reviewing the codebase, here's what should be **kept** vs **removed**:

## ✅ KEEP - Essential Production Files

### Core Workflow Scripts (3 files)
1. **`run_complete_workflow.py`** ⭐ - Main orchestrator (NEW - runs everything)
2. **`new_client_ingestion.py`** - Client ingestion (website + Drive)
3. **`client_brief_generator.py`** - Brief generation and upload

### Supporting Scripts (3 files)
4. **`client_pipeline_tracker.py`** - Pipeline tracking (used by new_client_ingestion.py)
5. **`kb_querier.py`** - Query knowledge bases
6. **`workspace_inspector.py`** - Inspect Vectara workspace

### Configuration Files (4 files)
7. **`service_account.json`** - Google service account credentials
8. **`package.json`** - Node.js dependencies
9. **`package-lock.json`** - Lock file
10. **`uv.lock`** - Python dependencies lock

### Documentation (10 files)
11. **`README.md`** - Main documentation
12. **`NEW_CLIENT_ONBOARDING.md`** - Onboarding guide
13. **`COMPLETE_WORKFLOW_GUIDE.md`** - Complete workflow docs
14. **`WORKFLOW_QUICKSTART.md`** - Quick reference
15. **`WORKFLOW_SUMMARY.md`** - Technical summary
16. **`DRIVE_UPLOAD_GUIDE.md`** - Drive upload docs
17. **`BRIEF_UPLOAD_QUICKSTART.md`** - Brief upload reference
18. **`BRIEF_UPLOAD_CHANGELOG.md`** - Change history
19. **`INTERFACE_IMPROVEMENTS.md`** - Interface changes
20. **`PDF_PROCESSOR_GUIDE.md`** - PDF processor docs

### Directories (Keep)
- **`ingestion/`** - All ingestion scripts and outputs
- **`outputs/`** - Generated briefs
- **`summarizers/`** - Brief generation components
- **`vectara-documentation/`** - Vectara repos
- **`node_modules/`** - Dependencies

### Log Files (Keep for now - can archive later)
- **`new_client_ingestion.log`** - Ingestion logs
- **`client_brief_generation.log`** - Brief generation logs
- **`upload_docs_to_vectara.log`** - Upload logs
- **`client_pipeline_log.json`** - Pipeline tracking

---

## ❌ REMOVE - Testing/One-Off Scripts

### Old/Duplicate Workflow Scripts (3 files)
1. **`run_workflow.py`** - OLD orchestrator (replaced by run_complete_workflow.py)
2. **`analysis_pipeline.py`** - OLD analysis (replaced by client_brief_generator.py)
3. **`ingestion_pipeline.py`** - OLD ingestion (replaced by new_client_ingestion.py)

### Testing/Debug Scripts (8 files)
4. **`demo_single_url.py`** - Demo script (not needed)
5. **`debug_brightdata.py`** - Debug script
6. **`test_integration.py`** - Integration test
7. **`test_metrics_preservation.py`** - Metrics test
8. **`test_brief_upload.sh`** - Upload test (keep for reference? or remove?)
9. **`check_full_markdown.py`** - Testing script
10. **`content_extractor.py`** - Old extractor (integrated into ingest_client_website.py)
11. **`local_llm_call.py`** - Local LLM testing

### Extract/Compare Utilities (3 files)
12. **`extract_compare.py`** - Comparison tool (one-off testing)
13. **`extract_g4d.py`** - G4D specific extraction (one-off)
14. **`extract_unique_content.py`** - Content extraction test

### Old Documentation/Scripts (3 files)
15. **`config.yaml`** - OLD config (run_workflow.py dependency)
16. **`suggested_workflow.md`** - OLD workflow docs
17. **`example_client_onboarding.sh`** - OLD example script
18. **`run.sh`** - OLD run script (if exists)

### Testing Data Directory
19. **`extraction_comparisons/`** - Testing data (can archive)

### Misc Files
20. **`vectara-agents-for-migration.txt`** - Migration notes (archive)

---

## 🗂️ Summary

**Keep**: 20-25 essential files + directories  
**Remove**: ~20 testing/old files  
**Archive**: Testing data and old logs (optional)

## Recommended Actions

### 1. Remove Old Workflow Scripts
These are replaced by the new unified workflow:
- `run_workflow.py`
- `analysis_pipeline.py`
- `ingestion_pipeline.py`
- `config.yaml`

### 2. Remove Testing/Debug Scripts
One-off testing scripts no longer needed:
- `demo_single_url.py`
- `debug_brightdata.py`
- `test_integration.py`
- `test_metrics_preservation.py`
- `check_full_markdown.py`
- `local_llm_call.py`
- `extract_compare.py`
- `extract_g4d.py`
- `extract_unique_content.py`

### 3. Remove Old Documentation
Replaced by new comprehensive docs:
- `suggested_workflow.md`
- `example_client_onboarding.sh`

### 4. Archive Testing Data
Move to archive folder or remove:
- `extraction_comparisons/`

### 5. Optional: Keep or Remove
Decide based on usage:
- `test_brief_upload.sh` - Could keep as example
- `run.sh` - Check if still used
- `content_extractor.py` - Old, but might have reference value

## Final Clean Structure

```
vectara/
├── Core Scripts (3)
│   ├── run_complete_workflow.py ⭐
│   ├── new_client_ingestion.py
│   └── client_brief_generator.py
│
├── Supporting Scripts (3)
│   ├── client_pipeline_tracker.py
│   ├── kb_querier.py
│   └── workspace_inspector.py
│
├── Configuration (4)
│   ├── service_account.json
│   ├── package.json
│   ├── package-lock.json
│   └── uv.lock
│
├── Documentation (10)
│   ├── README.md
│   ├── NEW_CLIENT_ONBOARDING.md
│   ├── COMPLETE_WORKFLOW_GUIDE.md
│   ├── WORKFLOW_QUICKSTART.md
│   ├── WORKFLOW_SUMMARY.md
│   ├── DRIVE_UPLOAD_GUIDE.md
│   ├── BRIEF_UPLOAD_QUICKSTART.md
│   ├── BRIEF_UPLOAD_CHANGELOG.md
│   ├── INTERFACE_IMPROVEMENTS.md
│   └── PDF_PROCESSOR_GUIDE.md
│
├── Directories
│   ├── ingestion/
│   ├── outputs/
│   ├── summarizers/
│   ├── vectara-documentation/
│   └── node_modules/
│
└── Logs (optional - can clean periodically)
    ├── *.log
    └── *.json
```

**Total**: ~20 files in root (down from ~40)

