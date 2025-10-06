# Inbox Manager - AI Customer Service Email Handler

A RAG-powered chatbot system for handling customer service emails with strong grounding and hallucination prevention.

## Features

✨ **RAG Architecture with Client Filtering**
- Retrieves relevant documents from Supabase vector database
- Filters by client ID to ensure responses use only client-specific knowledge
- Semantic search using OpenAI embeddings

🛡️ **Hallucination Prevention**
- Strong system prompts emphasizing grounding in context
- Pre-generation relevance checking
- Post-generation response verification
- Citation requirements with [Doc X] format
- Confidence scoring based on similarity thresholds

🤖 **Multi-LLM Support**
- OpenAI GPT-4o
- Anthropic Claude 3.5 Sonnet

🎨 **Modern Web UI**
- Clean, responsive interface
- Real-time document search
- Metadata display with confidence scores
- Copy-to-clipboard functionality

## Architecture

```
┌─────────────────┐
│ Customer Email  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Extract Query   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│ Vector Search with Filters  │
│ - Client ID filtering       │
│ - Similarity threshold      │
│ - Top-K results             │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────┐
│ Relevance Check         │
│ (Can context answer?)   │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ Generate Response       │
│ - Strong grounding      │
│ - Citation required     │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ Verification (Optional) │
│ (Is response grounded?) │
└────────┬────────────────┘
         │
         ▼
┌─────────────────┐
│ Return Response │
└─────────────────┘
```

## Setup

### 1. Install Dependencies

```bash
cd inbox_manager
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the `inbox_manager` directory (or use the root `.env`):

```bash
# Supabase Configuration
SUPABASE_VECTOR_DB_CONN=postgresql://postgres:Testpa$$123@db.zepjgxxwrnapxldywsbh.supabase.co:5432/postgres
SUPABASE_VECTOR_DB_URL=https://zepjgxxwrnapxldywsbh.supabase.co
SUPABASE_ACCESS_TOKEN=your_token_here
SUPABASE_VECTOR_user=postgres
SUPABASE_VECTOR_password=your_password
SUPABASE_VECTOR_host=db.zepjgxxwrnapxldywsbh.supabase.co
SUPABASE_VECTOR_port=5432
SUPABASE_VECTOR_dbname=postgres

# LLM API Keys
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
```

### 3. Database Setup

Your Supabase database should have a `documents` table with this structure:

```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding vector(1536),  -- For OpenAI text-embedding-3-small
    metadata JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create index for vector similarity search
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops);

-- Create index for client_id filtering
CREATE INDEX ON documents ((metadata->>'client_id'));
```

The `metadata` JSONB field should contain at minimum:
```json
{
    "client_id": "client-name",
    "source": "website|document|etc",
    "content_type": "documentation|faq|etc"
}
```

### 4. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## Usage

### Web UI

1. **Select a Client**: Choose from the dropdown of available clients
2. **Configure Settings**:
   - Choose LLM provider (OpenAI or Anthropic)
   - Enable/disable response verification
3. **Enter Email**: Paste the customer's email content
4. **Process**: Click "Process Email" to generate response
5. **Review**: See the AI response with confidence scores and source documents

### API Endpoints

#### Handle Email
```bash
POST /api/handle-email
Content-Type: application/json

{
    "email_content": "Customer's email text...",
    "client_id": "client-name",
    "client_name": "Client Display Name",
    "llm_provider": "openai",  # or "anthropic"
    "enable_verification": true
}
```

Response:
```json
{
    "success": true,
    "response": "AI-generated response with [Doc X] citations",
    "documents_found": 5,
    "confidence": 0.85,
    "metadata": {
        "query": "extracted query",
        "documents": [...],
        "relevance_check": "Yes - context is relevant",
        "verification": "Yes - response is grounded",
        "is_grounded": true
    }
}
```

#### Search Documents
```bash
POST /api/search-documents
Content-Type: application/json

{
    "query": "search query",
    "client_id": "client-name",
    "top_k": 5
}
```

#### List Clients
```bash
GET /api/clients
```

## Configuration

Edit `config.py` to customize:

- `TOP_K_RESULTS`: Number of documents to retrieve (default: 5)
- `SIMILARITY_THRESHOLD`: Minimum similarity score (default: 0.7)
- `CONFIDENCE_THRESHOLD`: Confidence threshold for responses (default: 0.75)
- System prompts and verification prompts

## Key Components

### `vector_store.py`
- Handles Supabase pgvector queries
- Generates embeddings using OpenAI
- Filters documents by client_id
- Returns similarity scores

### `email_handler.py`
- Core RAG logic
- Relevance checking
- Response generation with grounding
- Post-generation verification
- Confidence scoring

### `app.py`
- Flask web server
- API endpoints
- Request handling

### `templates/index.html` + `static/`
- Modern, responsive UI
- Real-time interaction
- Metadata visualization

## Best Practices

1. **Always filter by client_id** to ensure responses use only client-specific knowledge
2. **Set appropriate similarity thresholds** (0.7-0.8 recommended)
3. **Enable verification** for high-stakes customer interactions
4. **Review low-confidence responses** before sending to customers
5. **Monitor and log** all interactions for continuous improvement
6. **Update knowledge base regularly** with new documentation
7. **Test with real customer emails** before production deployment

## Troubleshooting

**No clients showing up?**
- Check database connection in `.env`
- Ensure documents table has data with `client_id` in metadata
- Run: `SELECT DISTINCT metadata->>'client_id' FROM documents;`

**Low similarity scores?**
- Documents may not be well-chunked
- Try adjusting chunk size in ingestion
- Consider hybrid search (keyword + vector)

**Responses not grounded?**
- Increase similarity threshold
- Enable verification
- Review and improve system prompts

## Future Enhancements

- [ ] Email queue management
- [ ] Human-in-loop approval workflow
- [ ] A/B testing different prompts
- [ ] Analytics dashboard
- [ ] Automated response sending
- [ ] Multi-language support
- [ ] Integration with email providers (Gmail, Outlook)
- [ ] Feedback loop for continuous learning
