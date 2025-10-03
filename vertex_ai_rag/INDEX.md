# Vertex AI RAG - File Index

## Quick Navigation

### 📘 Documentation
- [`README.md`](README.md) - Main documentation and usage guide
- [`SETUP_GUIDE.md`](SETUP_GUIDE.md) - Step-by-step setup instructions  
- [`AGENT_REFERENCE.md`](AGENT_REFERENCE.md) - Agent-specific usage guide
- [`../VERTEX_AI_MIGRATION.md`](../VERTEX_AI_MIGRATION.md) - Migration overview
- [`../agents.txt`](../agents.txt) - Agent definitions and prompts
- [`../IMPLEMENTATION_COMPLETE.md`](../IMPLEMENTATION_COMPLETE.md) - Implementation summary

### 🛠️ Setup & Configuration
- [`.env.template`](.env.template) - Environment variables template
- [`pyproject.toml`](pyproject.toml) - Poetry dependencies
- [`requirements.txt`](requirements.txt) - Pip dependencies
- [`setup_corpus.py`](setup_corpus.py) - Create RAG corpora
- [`../quick_setup_vertex_ai.sh`](../quick_setup_vertex_ai.sh) - Quick setup script

### 🤖 Agents
- [`agents/unique_mechanism_researcher.py`](agents/unique_mechanism_researcher.py) - Agent 1: Research strategies
- [`agents/client_materials_summarizer.py`](agents/client_materials_summarizer.py) - Agent 2: Analyze materials  
- [`agents/client_intake_summarizer.py`](agents/client_intake_summarizer.py) - Agent 3: Extract requirements
- [`agents/case_study_summarizer.py`](agents/case_study_summarizer.py) - Agent 4: Structure case studies
- [`agents/shared_prompts.py`](agents/shared_prompts.py) - Agent instructions

### 🔧 Tools
- [`agents/tools/google_search_tool.py`](agents/tools/google_search_tool.py) - Web search for researcher agent
- [`agents/tools/__init__.py`](agents/tools/__init__.py) - Tools package

### 🚀 Deployment
- [`deployment/deploy_agent.py`](deployment/deploy_agent.py) - Deploy single agent
- [`deployment/deploy_all_agents.py`](deployment/deploy_all_agents.py) - Deploy all 4 agents
- [`deployment/grant_permissions.sh`](deployment/grant_permissions.sh) - Grant RAG access
- [`deployment/query_agent.py`](deployment/query_agent.py) - Query deployed agents

### 📦 Ingestion
- [`ingestion/client_ingestion_adapter.py`](ingestion/client_ingestion_adapter.py) - Upload Vectara docs to Vertex AI

### 🔌 Shared Infrastructure
- [`shared/config.py`](shared/config.py) - Configuration management
- [`shared/vertex_rag_client.py`](shared/vertex_rag_client.py) - RAG corpus client
- [`shared/__init__.py`](shared/__init__.py) - Shared package

## File Count by Type

- **Documentation**: 6 files (README, guides, reference)
- **Python Scripts**: 13 files (agents, tools, deployment, ingestion)
- **Configuration**: 4 files (.env, pyproject, requirements, .gitignore)
- **Shell Scripts**: 2 files (permissions, setup)

**Total: 25 files**

## Execution Order

### First-Time Setup
1. Copy `.env.template` → `.env` and configure
2. Run `pip install -r requirements.txt`
3. Run `python setup_corpus.py --create-all`
4. Run `python ingestion/client_ingestion_adapter.py --client-id CLIENT_ID`
5. Run `bash deployment/grant_permissions.sh`
6. Run `python deployment/deploy_all_agents.py`
7. Test with `python deployment/query_agent.py --agent AGENT_NAME --query "test"`

### Regular Usage
1. Query agents: `python deployment/query_agent.py`
2. Upload new docs: `python ingestion/client_ingestion_adapter.py`
3. View corpora: `python setup_corpus.py --list`

## Dependencies

### External APIs Required
- Google Cloud (Vertex AI + Agent Engine)
- OpenAI API (GPT-5)
- Google Search API (for researcher agent)

### Python Packages Required
- `google-cloud-aiplatform[adk,agent-engines]>=1.108.0`
- `google-adk>=1.10.0`
- `openai>=1.99.3`
- `llama-index>=0.13.3`
- See `requirements.txt` for complete list

## Related Files (Outside vertex_ai_rag/)

- `/workspace/agents.txt` - Agent definitions
- `/workspace/VERTEX_AI_MIGRATION.md` - Migration guide
- `/workspace/IMPLEMENTATION_COMPLETE.md` - Implementation summary
- `/workspace/vertex-service-account.json` - Google Cloud credentials (not in git)
- `/workspace/quick_setup_vertex_ai.sh` - Quick setup helper

---

**Last Updated**: 2025-10-03
**Version**: 1.0.0
**Status**: Complete and ready for deployment
