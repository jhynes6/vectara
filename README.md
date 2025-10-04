# Client Onboarding & RAG Workflow System

A comprehensive AI-powered client onboarding system featuring:
- 🤖 **Agentic Workflow** using OpenAI Assistants
- 📚 Website & Google Drive content ingestion
- 📄 Intelligent PDF processing with fallback methods
- 🗄️ **Supabase Vector DB** with pgvector for RAG (NEW!)
- 📝 Automated client brief generation

## 🚀 Quick Start

### New Agentic Workflow (Recommended)

Run the AI-powered orchestrator:

```bash
# Interactive mode
python3 agentic_workflow.py

# Batch mode
python3 agentic_workflow.py \
  --client-id "client-name" \
  --drive-folder-id "1ABC123..." \
  --client-homepage-url "https://example.com" \
  --batch-mode
```

**See [QUICK_START.md](QUICK_START.md) for detailed setup.**

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file with your API keys:

```bash
# Required for agentic workflow
OPENAI_API_KEY=sk-your-openai-key-here

# Required for Supabase Vector DB
SUPABASE_VECTOR_DB_CONN=postgresql://postgres:password@host:5432/postgres
SUPABASE_ACCESS_TOKEN=your-supabase-token

# Optional
BRIGHTDATA_API_TOKEN=your-brightdata-token
```

### 3. Google Drive Credentials

Place your service account JSON file:

```bash
cp /path/to/your-service-account.json ./service_account.json
```

## Usage

### 🤖 Agentic Workflow (NEW - Recommended)

The intelligent AI-orchestrated workflow:

```bash
# Interactive - guides you through setup
python3 agentic_workflow.py

# Automated batch processing
python3 agentic_workflow.py \
  --client-id "acme-corp" \
  --drive-folder-id "1ABC..." \
  --client-homepage-url "https://acme.com" \
  --batch-mode
```

**Benefits:**
- ✅ Intelligent error handling
- ✅ Adaptive workflow execution  
- ✅ Self-documenting process
- ✅ Easy to extend and modify

### 📚 Traditional Workflow Components

Individual scripts for manual orchestration:

```bash
# 1. Client ingestion
python3 new_client_ingestion.py --client-id "client" \
  --drive-folder-id "1ABC..." --client-homepage-url "https://..."

# 2. PDF reprocessing (if needed)
python3 ingestion/reprocess_failed_pdfs.py \
  --output-dir "ingestion/client_ingestion_outputs/client"

# 3. Brief generation
python3 client_brief_generator.py --corpus-key "client"
```

## Output

The script will display:

1. **Agents**: Currently, agents are managed through the vectara-agentic library and may not be available via REST API yet.

2. **Corpora**: A table showing:
   - Corpus name
   - Corpus key
   - Description
   - Creation date

3. **Documents**: For each corpus, a table showing:
   - Document ID
   - Document title
   - Source URL
   - Creation date

## Features

### Agentic Workflow
- 🤖 **AI Orchestration**: OpenAI Assistants coordinate entire workflow
- 🧠 **Intelligent Decisions**: Adapts to errors and makes smart choices
- 🔄 **Automatic Retry**: Smart retry logic for failed operations
- 📝 **Self-Documenting**: Agent explains its reasoning

### Content Processing
- 🌐 **Website Scraping**: Intelligent content extraction from sitemaps
- 📁 **Google Drive Integration**: Automated file download and processing
- 📄 **Advanced PDF Processing**: Multiple extraction methods (GPT-4, MarkItDown, PDFPlumber)
- 🏷️ **LLM Categorization**: Automatic content type classification

### RAG & Search
- 🗄️ **Supabase Vector DB**: PostgreSQL + pgvector for vector storage
- 🔍 **Semantic Search**: OpenAI embeddings + cosine similarity
- 📊 **Rich Metadata**: Comprehensive document tagging
- 💰 **Cost Effective**: 95% cheaper than SaaS alternatives

### Brief Generation
- 📝 **Automated Briefs**: AI-generated comprehensive client summaries
- 📤 **Drive Upload**: Automatic upload to client folders
- 🎯 **Multi-Source**: Combines website, docs, and intake forms

## Troubleshooting

### Authentication Errors

If you get authentication errors:
1. Verify your API key is correct
2. Make sure your API key has the necessary permissions
3. Check that you're using the correct Vectara endpoint

### No Data Found

If no corpora or documents are found:
1. Verify you're using the correct Vectara account
2. Check that your API key has read permissions
3. Ensure you have corpora created in your Vectara workspace

## Documentation

📖 **Start Here:**
- [QUICK_START.md](QUICK_START.md) - Get running in 5 minutes
- [AGENTIC_WORKFLOW_GUIDE.md](AGENTIC_WORKFLOW_GUIDE.md) - Complete guide to agent workflow
- [AGENT_VS_TRADITIONAL_COMPARISON.md](AGENT_VS_TRADITIONAL_COMPARISON.md) - Detailed comparison

📚 **Additional Guides:**
- [NEW_CLIENT_ONBOARDING.md](NEW_CLIENT_ONBOARDING.md) - Traditional workflow guide
- [pdf_processing_docs.md](pdf_processing_docs.md) - PDF processing details

## Architecture

```
┌─────────────────────────────────────────────────────┐
│          OpenAI Coordinator Agent                   │
│  (Intelligent workflow orchestration)               │
└────────────┬────────────────────────────────────────┘
             │
    ┌────────┴────────┬──────────┬──────────┐
    │                 │          │          │
    ▼                 ▼          ▼          ▼
┌────────┐    ┌─────────┐  ┌────────┐  ┌────────┐
│Ingest  │    │PDF      │  │Vertex  │  │Brief   │
│Website │    │Process  │  │AI RAG  │  │Generate│
│& Drive │    │         │  │Upload  │  │        │
└────────┘    └─────────┘  └────────┘  └────────┘
```

## Testing

Run the test suite to verify installation:

```bash
python3 test_agentic_workflow.py
```

Expected output:
```
================================================================================
🎉 ALL TESTS PASSED!
The agentic workflow is ready to use.
================================================================================
```

## Dependencies

**Core:**
- `openai>=2.1.0` - OpenAI SDK with Assistants API
- `psycopg2-binary>=2.9.9` - PostgreSQL adapter
- `supabase>=2.0.0` - Supabase client
- `llama-index` - LLM application framework

**Processing:**
- `beautifulsoup4` - Web scraping
- `pdfplumber` - PDF extraction
- `markitdown` - Advanced PDF processing
- `python-slugify` - Filename sanitization

**Infrastructure:**
- `python-dotenv` - Environment management
- `google-api-python-client` - Google Drive API
