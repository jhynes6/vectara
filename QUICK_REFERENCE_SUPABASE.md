# Supabase Quick Reference

## Environment Setup

```bash
# Copy example config
cp .env.supabase.example .env

# Edit with your values
nano .env
```

Required variables:
```bash
SUPABASE_VECTOR_DB_CONN=postgresql://postgres:password@host:5432/postgres
OPENAI_API_KEY=sk-your-key
```

## Common Commands

### 1. Run Complete Workflow

```bash
python agentic_workflow.py \
  --client-id "client-name" \
  --drive-folder-id "1ABC123..." \
  --client-homepage-url "https://example.com" \
  --batch-mode
```

### 2. Manual Ingestion

```bash
python supabase_client_ingestion.py \
  --client-id "client-name" \
  --drive-folder-id "1ABC..." \
  --client-homepage-url "https://example.com" \
  --batch-mode
```

### 3. Generate Brief

```bash
python supabase_brief_generator.py \
  --client-id "client-name" \
  --output "brief.md"
```

### 4. Test Migration

```bash
python test_supabase_migration.py
```

## Python API

### Initialize Vector Store

```python
from supabase_vector_store import SupabaseVectorStore

vs = SupabaseVectorStore()
```

### Upload Document

```python
doc_id, chunks = vs.upload_document(
    client_id="acme-corp",
    content="Document text here...",
    title="Document Title",
    uri="https://example.com/doc",
    source_type="website",
    content_type="services_products",
    metadata={"custom": "data"}
)
```

### Query Documents

```python
results = vs.query_documents(
    client_id="acme-corp",
    query="What services do they offer?",
    limit=10,
    content_type_filter="services_products",
    similarity_threshold=0.7
)

for result in results:
    print(f"{result['title']}: {result['similarity']:.3f}")
    print(result['content'][:200])
```

### Get Stats

```python
stats = vs.get_client_stats("acme-corp")
print(f"Documents: {stats['document_count']}")
print(f"Chunks: {stats['chunk_count']}")
print(f"Tokens: {stats['total_tokens']}")
```

## Database Queries

### Direct SQL Access

```python
import psycopg2

conn = psycopg2.connect(os.getenv('SUPABASE_VECTOR_DB_CONN'))
cur = conn.cursor()

# Get all clients
cur.execute("SELECT client_id, primary_domain FROM clients")
for row in cur.fetchall():
    print(row)

# Get document count per client
cur.execute("""
    SELECT c.client_id, COUNT(d.id) as doc_count
    FROM clients c
    LEFT JOIN documents d ON c.client_id = d.client_id
    GROUP BY c.client_id
""")
```

### Similarity Search (Raw SQL)

```python
from openai import OpenAI

# Generate embedding
client = OpenAI()
response = client.embeddings.create(
    model="text-embedding-3-small",
    input="your query here"
)
embedding = response.data[0].embedding

# Search
cur.execute("""
    SELECT 
        content,
        1 - (embedding <=> %s::vector) as similarity
    FROM document_chunks
    WHERE client_id = %s
    ORDER BY embedding <=> %s::vector
    LIMIT 10
""", (embedding, client_uuid, embedding))
```

## Content Types

Available content types:
- `case_studies` - Client case studies and success stories
- `services_products` - Services and product offerings
- `blogs_resources` - Blog posts and resources
- `industries_markets` - Industry and market information
- `client_intake_form` - Client intake forms
- `other` - General content

## Source Types

Available source types:
- `website` - Website content
- `client_materials` - Google Drive materials
- `client_intake_form` - Intake form data

## Troubleshooting

### Connection Error

```python
# Test connection
import psycopg2
conn = psycopg2.connect(os.getenv('SUPABASE_VECTOR_DB_CONN'))
print("✅ Connected!")
```

### pgvector Extension

```sql
-- Check if installed
SELECT * FROM pg_extension WHERE extname = 'vector';

-- Install if needed (requires superuser)
CREATE EXTENSION vector;
```

### Embedding Errors

```python
# Test OpenAI embeddings
from openai import OpenAI
client = OpenAI()
response = client.embeddings.create(
    model="text-embedding-3-small",
    input="test"
)
print(f"✅ {len(response.data[0].embedding)} dimensions")
```

## Performance Tips

1. **Use Connection Pooling**
   - Already implemented in `SupabaseVectorStore`
   - Pool size: 1-10 connections

2. **Batch Operations**
   - Upload multiple documents in sequence
   - Use batch insert for chunks

3. **Index Optimization**
   ```sql
   -- Create index on embeddings (if not exists)
   CREATE INDEX ON document_chunks 
   USING ivfflat (embedding vector_cosine_ops);
   ```

4. **Query Optimization**
   - Adjust `similarity_threshold` (lower = more results)
   - Use metadata filters to narrow search
   - Limit results appropriately

## Cost Estimates

### OpenAI Embeddings
- Model: `text-embedding-3-small`
- Cost: $0.02 per 1M tokens
- Average: ~500 tokens per document
- **$0.01 per 1,000 documents**

### Supabase
- Free tier: 500MB database
- Pro: $25/month for 8GB
- Unlimited queries included

### Total Cost
- **~$0.02-0.05 per 1,000 operations**
- 95% cheaper than Vectara!

## Migration from Vectara

### Old Code
```python
from vectara import Vectara
vectara = Vectara(api_key="...")
vectara.upload_document(corpus_key="client", ...)
results = vectara.query(corpus_key="client", query="...")
```

### New Code
```python
from supabase_vector_store import SupabaseVectorStore
vs = SupabaseVectorStore()
vs.upload_document(client_id="client", ...)
results = vs.query_documents(client_id="client", query="...")
```

## Additional Resources

- **SUPABASE_MIGRATION_COMPLETE.md** - Full migration guide
- **test_supabase_migration.py** - Test suite
- **supabase_vector_store.py** - Full API documentation (docstrings)
