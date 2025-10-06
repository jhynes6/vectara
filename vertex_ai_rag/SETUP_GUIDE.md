## Complete Setup Guide: Vectara to Vertex AI Migration

This guide walks you through the complete setup process step-by-step.

## ⏱️ Estimated Time: 1-2 hours

- Corpus setup: 10 minutes
- Document upload: 10-30 minutes (depending on document count)
- Permission grant: 5 minutes  
- Agent deployment: 30-60 minutes (4 agents × 7-15 min each)

---

## Prerequisites Checklist

Before you begin, ensure you have:

- [ ] Google Cloud Project with billing enabled
- [ ] Vertex AI API enabled
- [ ] Agent Engine API enabled
- [ ] Service account JSON file (`vertex-service-account.json`)
- [ ] OpenAI API key (for GPT-5/GPT-4)
- [ ] Google Search API key + Search Engine ID (for researcher agent)
- [ ] Python 3.10+ installed
- [ ] `gcloud` CLI installed and authenticated

---

## Step-by-Step Setup

### 1. Enable Required APIs

```bash
# Set your project ID
export PROJECT_ID="your-project-id"
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable aiplatform.googleapis.com
gcloud services enable agentengine.googleapis.com
gcloud services enable customsearch.googleapis.com

# Verify APIs are enabled
gcloud services list --enabled | grep -E "aiplatform|agentengine"
```

### 2. Create Service Account (if needed)

```bash
# Create service account
gcloud iam service-accounts create vertex-ai-rag \
    --display-name="Vertex AI RAG Service Account"

# Grant necessary roles
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:vertex-ai-rag@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:vertex-ai-rag@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/storage.objectAdmin"

# Create and download key
gcloud iam service-accounts keys create vertex-service-account.json \
    --iam-account=vertex-ai-rag@${PROJECT_ID}.iam.gserviceaccount.com

# Move to project root
mv vertex-service-account.json ../
```

### 3. Get Google Search API Credentials

1. Go to [Google Cloud Console > APIs & Services > Credentials](https://console.cloud.google.com/apis/credentials)
2. Click "Create Credentials" → "API Key"
3. Copy the API key
4. Create a Custom Search Engine:
   - Go to [Programmable Search Engine](https://programmablesearchengine.google.com/controlpanel/create)
   - Set "Search the entire web" option
   - Create and copy the Search Engine ID

### 4. Install Dependencies

```bash
cd vertex_ai_rag

# Option 1: Using Poetry (recommended)
poetry install

# Option 2: Using pip
pip install google-cloud-aiplatform[adk,agent-engines]==1.108.0 \
            google-adk==1.10.0 \
            google-auth==2.35.0 \
            google-api-python-client==2.154.0 \
            python-dotenv==1.0.1 \
            requests==2.32.3 \
            tqdm==4.67.1 \
            llama-index==0.13.3 \
            openai>=1.99.3
```

### 5. Configure Environment

```bash
# Copy template
cp .env.template .env

# Edit .env file
nano .env
```

Fill in these values:

```bash
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=../vertex-service-account.json

OPENAI_API_KEY=sk-...your-openai-key...

GOOGLE_SEARCH_API_KEY=...your-google-search-key...
GOOGLE_SEARCH_ENGINE_ID=...your-search-engine-id...
```

### 6. Create RAG Corpora

```bash
# Create all 3 corpora
python setup_corpus.py --create-all
```

**Expected output:**
```
🏗️ Creating RAG corpus: client-knowledge-base-main
✅ Main corpus created: projects/.../ragCorpora/...
💾 Saved RAG_CORPUS_MAIN to .env file

🏗️ Creating RAG corpus: client-materials
✅ Client materials corpus created: projects/.../ragCorpora/...
💾 Saved RAG_CORPUS_CLIENT_MATERIALS to .env file

🏗️ Creating RAG corpus: case-studies
✅ Case studies corpus created: projects/.../ragCorpora/...
💾 Saved RAG_CORPUS_CASE_STUDIES to .env file

✅ Corpus setup complete!
```

**Verify:** Check `.env` file now has corpus IDs:
```bash
cat .env | grep RAG_CORPUS
```

### 7. Upload Documents

Upload your existing client data to Vertex AI RAG:

```bash
# For client from existing Vectara ingestion output
python ingestion/client_ingestion_adapter.py --client-id d2-creative

# For custom directory
python ingestion/client_ingestion_adapter.py \
    --client-id CLIENT_ID \
    --input-dir /path/to/documents
```

**Expected output:**
```
🔍 Discovering files from ingestion output...
✅ Discovered 152 files:
   • client_intake_form: 1 files
   • client_materials: 4 files
   • website: 147 files

⬆️ Uploading to Vertex AI RAG corpus: projects/.../ragCorpora/...
   ✅ client_intake_form: 1/1 uploaded
   ✅ client_materials: 4/4 uploaded
   ✅ website: 147/147 uploaded

📊 UPLOAD SUMMARY
Total files: 152
Successful: 152
Failed: 0
Success rate: 100.0%
```

### 8. Grant Permissions

```bash
# Grant RAG corpus access to Vertex AI agents
bash deployment/grant_permissions.sh
```

**Expected output:**
```
🔐 Granting RAG Corpus permissions...
Project: your-project-id
Project Number: 123456789012

📝 Creating custom IAM role (if not exists)...
✅ Created custom role: ragCorpusQueryRole

🔗 Binding role to service account...
✅ Permissions granted successfully!
```

### 9. Deploy Agents

**Option A: Deploy All (Recommended)**

```bash
python deployment/deploy_all_agents.py
```

This deploys all 4 agents sequentially (~30-60 minutes total).

**Option B: Deploy Individually**

```bash
# Deploy one at a time (useful for testing)
python deployment/deploy_agent.py --agent unique_mechanism_researcher
python deployment/deploy_agent.py --agent client_materials_summarizer
python deployment/deploy_agent.py --agent client_intake_summarizer
python deployment/deploy_agent.py --agent case_study_summarizer
```

**Expected output (per agent):**
```
🚀 Deploying agent: unique_mechanism_researcher
📦 Loading agent module: agents.unique_mechanism_researcher
🤖 Agent loaded: unique_mechanism_researcher
   Model: gpt-5
   Tools: 2
☁️ Deploying to Vertex AI Agent Engine...
   This may take several minutes...

✅ DEPLOYMENT SUCCESSFUL!
📝 Resource name: projects/.../reasoningEngines/...
💾 Saved AGENT_UNIQUE_MECHANISM_RESEARCHER to .env file
```

**Verify deployments:**
```bash
cat .env | grep AGENT_
```

---

## Testing Your Setup

### Test 1: Query the Researcher Agent

```bash
python deployment/query_agent.py \
  --agent unique_mechanism_researcher \
  --query "What are the top 3 innovative lead generation strategies for B2B SaaS companies in 2024?"
```

### Test 2: Query the Materials Summarizer

```bash
python deployment/query_agent.py \
  --agent client_materials_summarizer \
  --query "What services and capabilities does the client offer?"
```

### Test 3: Query the Intake Summarizer

```bash
python deployment/query_agent.py \
  --agent client_intake_summarizer \
  --query "Summarize the client intake form requirements and timeline"
```

### Test 4: Query the Case Study Summarizer

```bash
python deployment/query_agent.py \
  --agent case_study_summarizer \
  --query "Summarize all case studies with quantitative results"
```

---

## Verification Checklist

After setup, verify:

- [ ] `.env` file has all corpus IDs (RAG_CORPUS_*)
- [ ] `.env` file has all agent resource names (AGENT_*)
- [ ] All 4 agents respond to test queries
- [ ] RAG retrieval returns relevant documents
- [ ] Web search works for researcher agent
- [ ] No permission errors in agent responses

---

## Common Issues & Solutions

### Issue: "API not enabled"

**Solution:**
```bash
gcloud services enable aiplatform.googleapis.com agentengine.googleapis.com
```

### Issue: "Quota exceeded"

**Solution:**
- Check quotas: [Cloud Console > IAM > Quotas](https://console.cloud.google.com/iam-admin/quotas)
- Request increase for:
  - Vertex AI API requests
  - Agent Engine deployments
  - Embedding API calls

### Issue: "Permission denied" during deployment

**Solution:**
```bash
# Re-run permission script
bash deployment/grant_permissions.sh

# Or manually grant role
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:service-PROJECT_NUMBER@gcp-sa-aiplatform-re.iam.gserviceaccount.com" \
    --role="projects/$PROJECT_ID/roles/ragCorpusQueryRole"
```

### Issue: Agent returns empty/no results

**Solutions:**
1. Verify documents were uploaded:
   ```bash
   python setup_corpus.py --list
   ```
2. Check corpus has files in Cloud Console
3. Lower `vector_distance_threshold` in agent code
4. Check query phrasing matches document content

### Issue: "gpt-5" model not available

**Solution:**
The code will automatically fallback to `gpt-4-turbo`. Or manually edit agent files to use `gpt-4-turbo-preview`.

---

## Next Steps

1. **Production Setup**:
   - Set up monitoring/alerting
   - Configure backup/disaster recovery
   - Establish deployment pipeline

2. **Integration**:
   - Integrate agents into your applications
   - Create API wrappers if needed
   - Build UI for agent interactions

3. **Optimization**:
   - Fine-tune similarity thresholds
   - Adjust chunk sizes for better retrieval
   - Monitor and optimize costs

4. **Data Migration**:
   - Migrate remaining Vectara data
   - Deprecate Vectara infrastructure
   - Update documentation

---

## Success Criteria

✅ Your setup is complete when:

1. All 4 agents deployed successfully
2. Each agent returns relevant responses to test queries
3. RAG retrieval finds appropriate documents
4. Web search works for researcher agent
5. No errors in `.env` configuration
6. All resource names saved in `.env`

**Estimated total cost (first month):**
- Vertex AI RAG: ~$10-50 (depending on query volume)
- Agent Engine: ~$20-100 (depending on usage)
- OpenAI API: ~$50-200 (depending on token usage)
- Google Search API: ~$5-25 (100 free queries/day, then $5/1K queries)

**Total: ~$85-375/month** (scales with usage)

