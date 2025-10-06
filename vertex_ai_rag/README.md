# Vertex AI RAG Implementation

Complete replacement for Vectara using Google Vertex AI RAG Engine with 4 specialized AI agents.

## 📋 Overview

This implementation provides:
- **Vertex AI RAG Engine** for document storage and vector search
- **4 Specialized Agents** deployed to Vertex AI Agent Engine:
  1. **Unique Mechanism Researcher** - Researches marketing strategies (RAG + Web Search)
  2. **Client Materials Summarizer** - Analyzes capabilities and brochures
  3. **Client Intake Summarizer** - Extracts requirements from intake forms
  4. **Case Study Summarizer** - Structures case study information

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Vertex AI RAG Engine                      │
│  ┌──────────────┐  ┌───────────────┐  ┌──────────────────┐ │
│  │ Main Corpus  │  │ Client        │  │ Case Studies     │ │
│  │              │  │ Materials     │  │ Corpus           │ │
│  └──────────────┘  └───────────────┘  └──────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│               4 Agents (Vertex AI Agent Engine)              │
│  ┌──────────────┐  ┌───────────────┐  ┌──────────────────┐ │
│  │ Researcher   │  │ Materials     │  │ Intake           │ │
│  │ (RAG+Search) │  │ Summarizer    │  │ Summarizer       │ │
│  └──────────────┘  └───────────────┘  └──────────────────┘ │
│  ┌──────────────┐                                           │
│  │ Case Study   │                                           │
│  │ Summarizer   │                                           │
│  └──────────────┘                                           │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    GPT-5 (OpenAI API)
```

## 🚀 Quick Start

### Prerequisites

1. **Google Cloud Project** with:
   - Vertex AI API enabled
   - Agent Engine API enabled
   - Billing enabled
   
2. **API Keys**:
   - Google Cloud service account JSON
   - OpenAI API key (for GPT-5/GPT-4)
   - Google Search API key (for researcher agent)
   
3. **Python 3.10+** with Poetry

### Installation

```bash
cd vertex_ai_rag

# Install dependencies
poetry install

# Or use pip
pip install -r requirements.txt

# Copy environment template
cp .env.template .env

# Edit .env with your configuration
nano .env
```

### Required Environment Variables

```bash
# Google Cloud
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=../vertex-service-account.json

# OpenAI
OPENAI_API_KEY=your-openai-api-key

# Google Search (for researcher agent)
GOOGLE_SEARCH_API_KEY=your-search-api-key
GOOGLE_SEARCH_ENGINE_ID=your-search-engine-id
```

## 📦 Setup Process

### Step 1: Create RAG Corpora

```bash
# Create all corpora
python setup_corpus.py --create-all

# Or create individually
python setup_corpus.py --corpus-name main
python setup_corpus.py --corpus-name client_materials
python setup_corpus.py --corpus-name case_studies

# List existing corpora
python setup_corpus.py --list
```

This creates:
- `RAG_CORPUS_MAIN` - Main client knowledge base
- `RAG_CORPUS_CLIENT_MATERIALS` - Brochures, capabilities, presentations
- `RAG_CORPUS_CASE_STUDIES` - Case study documents

The corpus IDs are automatically saved to `.env`.

### Step 2: Upload Documents

```bash
# Upload existing ingestion output to Vertex AI
python ingestion/client_ingestion_adapter.py --client-id d2-creative

# This uploads:
# - Client intake forms
# - Client materials (brochures, capabilities)
# - Website content (markdown files)
```

### Step 3: Grant Permissions

```bash
# Grant RAG corpus access to Vertex AI agents
bash deployment/grant_permissions.sh
```

### Step 4: Deploy Agents

```bash
# Deploy all 4 agents (recommended)
python deployment/deploy_all_agents.py

# Or deploy individually
python deployment/deploy_agent.py --agent unique_mechanism_researcher
python deployment/deploy_agent.py --agent client_materials_summarizer
python deployment/deploy_agent.py --agent client_intake_summarizer
python deployment/deploy_agent.py --agent case_study_summarizer
```

⏱️ **Note**: Each agent deployment takes ~5-10 minutes. Total time: 20-40 minutes.

Agent resource names are automatically saved to `.env`.

## 🎯 Usage

### Query Agents

```bash
# Unique Mechanism Researcher
python deployment/query_agent.py \
  --agent unique_mechanism_researcher \
  --query "What are innovative lead generation strategies in B2B SaaS?"

# Client Materials Summarizer
python deployment/query_agent.py \
  --agent client_materials_summarizer \
  --query "What services does the client offer?"

# Client Intake Summarizer
python deployment/query_agent.py \
  --agent client_intake_summarizer \
  --query "Summarize the client requirements and timeline"

# Case Study Summarizer
python deployment/query_agent.py \
  --agent case_study_summarizer \
  --query "Summarize the Lawson case study with all metrics"
```

### Programmatic Usage

```python
from shared import config
import vertexai
from vertexai import agent_engines

# Initialize
vertexai.init(
    project=config.PROJECT_ID,
    location=config.LOCATION
)

# Get agent
agent = agent_engines.get(config.AGENT_UNIQUE_MECHANISM_RESEARCHER)

# Query
response = agent.query("What are the latest content marketing trends?")
print(response['response'])
```

## 📁 Project Structure

```
vertex_ai_rag/
├── agents/                    # Agent definitions
│   ├── unique_mechanism_researcher.py
│   ├── client_materials_summarizer.py
│   ├── client_intake_summarizer.py
│   ├── case_study_summarizer.py
│   ├── shared_prompts.py     # Agent instructions
│   └── tools/
│       └── google_search_tool.py
├── deployment/                # Deployment scripts
│   ├── deploy_agent.py
│   ├── deploy_all_agents.py
│   ├── grant_permissions.sh
│   └── query_agent.py
├── ingestion/                 # Document ingestion
│   └── client_ingestion_adapter.py
├── shared/                    # Shared utilities
│   ├── config.py
│   ├── vertex_rag_client.py
│   └── __init__.py
├── setup_corpus.py            # Corpus creation
├── pyproject.toml             # Dependencies
├── .env.template              # Environment template
└── README.md
```

## 🔧 Configuration

### Agent Parameters

All agents use GPT-5 (or GPT-4 fallback) with quality-optimized parameters:

- **Reasoning Effort**: Medium (balanced quality vs speed)
- **Temperature**: 0.2-0.7 (varies by agent for optimal output)
- **RAG Settings**: 
  - Chunk size: 512 tokens
  - Chunk overlap: 100 tokens
  - Top-k results: 10-15 (varies by agent)

### Corpus Settings

- **Embedding Model**: `text-embedding-004` (Google's latest)
- **Vector Distance**: Cosine similarity
- **Indexing**: Automatic by Vertex AI

## 🔍 Troubleshooting

### Quota Errors

If you hit quota limits during deployment:

```bash
# Check quotas
gcloud compute project-info describe --project=YOUR_PROJECT_ID

# Request quota increase:
# https://console.cloud.google.com/iam-admin/quotas
```

### Agent Not Found

```bash
# List deployed agents
gcloud ai reasoning-engines list \
  --location=us-central1 \
  --project=YOUR_PROJECT_ID

# Verify .env has agent resource names
cat .env | grep AGENT_
```

### Permission Errors

```bash
# Re-run permission grant
bash deployment/grant_permissions.sh

# Verify IAM roles
gcloud projects get-iam-policy YOUR_PROJECT_ID \
  --flatten="bindings[].members" \
  --filter="bindings.members:service-*@gcp-sa-aiplatform-re.iam.gserviceaccount.com"
```

### Import Errors

```bash
# Reinstall dependencies
poetry install

# Or with pip
pip install -r requirements.txt --force-reinstall
```

## 📊 Monitoring & Logging

### View Agent Logs

```bash
# View logs in Cloud Console
gcloud logging read "resource.type=aiplatform.googleapis.com/ReasoningEngine" \
  --limit=50 \
  --format=json
```

### Monitor Costs

- RAG Engine: ~$0.01 per 1K queries
- Agent Engine: ~$0.005 per agent call
- GPT-5 API: Variable by token usage
- Embeddings: ~$0.0001 per 1K tokens

## 🔐 Security

- Service account JSON is excluded from git (see `.gitignore`)
- API keys stored in `.env` (not committed)
- IAM permissions follow least-privilege principle
- All data encrypted at rest in Vertex AI

## 📈 Migration from Vectara

### Data Migration

```bash
# 1. Export from Vectara (use existing scripts)
# 2. Upload to Vertex AI
python ingestion/client_ingestion_adapter.py --client-id CLIENT_ID
```

### Agent Migration

The new agents are drop-in replacements for Vectara agents with equivalent functionality:

| Vectara Agent | Vertex AI Agent | Status |
|---------------|-----------------|--------|
| `agt_unique-mechanism-researcher` | `unique_mechanism_researcher` | ✅ Enhanced with web search |
| `client-materials-summarizer` | `client_materials_summarizer` | ✅ Equivalent |
| `client-intake-form-summarizer` | `client_intake_summarizer` | ✅ Equivalent |
| `case-study-summarizer` | `case_study_summarizer` | ✅ Equivalent |

## 🆘 Support

For issues or questions:
1. Check this README
2. Review logs: `gcloud logging read ...`
3. Verify `.env` configuration
4. Check Google Cloud Console for quota/billing

## 📝 License

Proprietary - Internal use only

