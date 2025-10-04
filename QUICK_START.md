# Quick Start: Agentic Workflow

Get up and running with the OpenAI agent-based client onboarding workflow in 5 minutes.

## Prerequisites

- Python 3.8+
- OpenAI API key
- Vertex AI/Vectara API key
- Google Drive service account (for Drive ingestion)

## Installation

### 1. Install Dependencies

```bash
cd /workspace
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file:

```bash
# Required
OPENAI_API_KEY=sk-...your-key-here
VECTARA_API_KEY=your-vectara-key

# Optional
BRIGHTDATA_API_TOKEN=your-token-if-using-brightdata
```

### 3. Verify Installation

```bash
python3 test_agentic_workflow.py
```

Expected output:
```
================================================================================
AGENTIC WORKFLOW TEST SUITE
================================================================================

Testing imports...
  ✅ OpenAI SDK imported successfully
  ✅ python-dotenv imported successfully
  ✅ asyncio available

Testing workflow files...
  ✅ agentic_workflow.py exists
  ✅ ingestion/reprocess_failed_pdfs.py exists
  ...

🎉 ALL TESTS PASSED!
```

## Usage

### Option 1: Interactive Mode (Recommended)

```bash
python3 agentic_workflow.py
```

Follow the prompts:
- Enter client ID
- Enter Google Drive folder ID
- Enter client homepage URL
- Confirm and run

### Option 2: Batch Mode

```bash
python3 agentic_workflow.py \
  --client-id "acme-corp" \
  --drive-folder-id "1ABC123..." \
  --client-homepage-url "https://acme-corp.com" \
  --batch-mode
```

### Option 3: With Custom Options

```bash
python3 agentic_workflow.py \
  --client-id "tech-startup" \
  --drive-folder-id "1XYZ789..." \
  --client-homepage-url "https://techstartup.io" \
  --pdf-processor markitdown \
  --workers 8 \
  --batch-mode
```

## What Happens?

The coordinator agent will:

1. **🔄 Run Ingestion**
   - Scrape client website
   - Download Google Drive files
   - Process and categorize content

2. **📄 Reprocess PDFs**
   - Find failed PDF extractions
   - Retry with alternative methods
   - Validate successful extractions

3. **☁️  Upload to Vertex AI**
   - Upload all processed files
   - Create RAG corpus
   - Generate upload report

4. **📝 Generate Brief**
   - Query RAG corpus
   - Generate comprehensive brief
   - Upload to Google Drive

## Example Output

```
🚀🚀🚀🚀🚀 ... 🚀🚀🚀🚀🚀
AGENTIC CLIENT ONBOARDING WORKFLOW (OpenAI Assistants)
🚀🚀🚀🚀🚀 ... 🚀🚀🚀🚀🚀
Client: acme-corp
Started: 2025-10-04 10:30:00

✅ Created coordinator agent: asst_abc123...
🤖 Coordinator agent is now orchestrating the workflow...

Agent status: requires_action (iteration 1)
  📞 Tool call: run_ingestion
  🛠️  Executing tool: run_ingestion
  ✅ Tool run_ingestion completed: True

Agent status: requires_action (iteration 2)
  📞 Tool call: reprocess_pdfs
  🛠️  Executing tool: reprocess_pdfs
  ✅ Tool reprocess_pdfs completed: True

...

================================================================================
🎉 AGENTIC WORKFLOW FINISHED
================================================================================
Client: acme-corp
Duration: 245.3 seconds (4.1 minutes)

Results:
  ✅ Ingestion: Complete
  ✅ PDF Reprocessing: Complete
  ✅ Vertex Upload: Complete
  ✅ Brief Generation: Complete
================================================================================
```

## Output Files

After completion, check:

```
/workspace/
├── ingestion/client_ingestion_outputs/acme-corp/
│   ├── website/                    # Website content
│   ├── client_materials/           # Drive files
│   ├── onboarding_report.json      # Upload stats
│   └── ...
└── outputs/
    └── acme-corp_client_brief_20251004.md  # Generated brief
```

## Common Issues

### Issue: "Module not found"

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "OPENAI_API_KEY not set"

**Solution:**
Create `.env` file:
```bash
echo "OPENAI_API_KEY=sk-your-key" > .env
echo "VECTARA_API_KEY=your-key" >> .env
```

### Issue: "Agent creation failed"

**Solution:**
- Verify API key is valid
- Check OpenAI account has credit
- Ensure internet connection works

### Issue: "Drive folder access denied"

**Solution:**
- Verify service account credentials
- Ensure Drive folder is shared ("Anyone with link can view")
- Check folder ID is correct

## Cost Estimate

Typical workflow costs:

| Component | Cost |
|-----------|------|
| Agent orchestration | ~$0.10-0.30 |
| Website scraping | Free |
| PDF processing | Variable |
| Brief generation | ~$0.05-0.20 |
| **Total per run** | **~$0.15-0.50** |

## Next Steps

1. ✅ Run your first workflow
2. 📖 Read [AGENTIC_WORKFLOW_GUIDE.md](AGENTIC_WORKFLOW_GUIDE.md) for details
3. 🔍 Compare with [AGENT_VS_TRADITIONAL_COMPARISON.md](AGENT_VS_TRADITIONAL_COMPARISON.md)
4. 🛠️  Customize agent behavior (see guide)
5. 🚀 Deploy to production

## Need Help?

- Check logs in console output
- Review `test_agentic_workflow.py` output
- Read the comprehensive guide: `AGENTIC_WORKFLOW_GUIDE.md`
- Verify all environment variables are set

## Key Files

- **agentic_workflow.py** - Main agent orchestrator
- **ingestion/reprocess_failed_pdfs.py** - PDF reprocessing
- **new_client_ingestion.py** - Core ingestion logic
- **client_brief_generator.py** - Brief generation
- **test_agentic_workflow.py** - Test suite

Happy agent orchestration! 🤖✨
