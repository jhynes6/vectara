# Supabase Migration Plan

## Overview
Migrate from Vectara RAG to Supabase Vector Database (pgvector)

## Current Architecture (Vectara-based)

### Files Using Vectara
1. **new_client_ingestion.py** - VectaraClientOnboarder class
2. **agentic_workflow.py** - References Vectara in tools
3. **client_brief_generator.py** - Uses Vectara for RAG queries
4. **summarizers/case_study_summarizer.py** - Vectara queries
5. **summarizers/client_intake_summarizer.py** - Vectara queries
6. **summarizers/website_summarizer.py** - Vectara queries

### Current Vectara Operations

#### 1. Document Storage
```python
# Creating corpus
corpus_config = {
    "key": client_id,
    "name": client_id,
    "filter_attributes": [...]
}
vectara_client.create_corpus(corpus_config)

# Uploading documents
vectara_client.upload_document(
    corpus_key=client_id,
    document_id=doc_id,
    content=content,
    metadata={...}
)
```

#### 2. RAG Retrieval
```python
# Query for context
response = vectara_client.query(
    corpus_key=client_id,
    query_text=query,
    num_results=10,
    metadata_filter="content_type:case_studies"
)
```

## Target Architecture (Supabase-based)

### Required Components

#### 1. Supabase Client Setup
```python
from supabase import create_client
import openai  # for embeddings

class SupabaseVectorStore:
    def __init__(self, supabase_url, supabase_key, openai_key):
        self.client = create_client(supabase_url, supabase_key)
        self.openai = openai.OpenAI(api_key=openai_key)
```

#### 2. Database Schema (pgvector)
```sql
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Documents table
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id TEXT NOT NULL,
    document_id TEXT NOT NULL,
    content TEXT NOT NULL,
    embedding vector(1536),  -- OpenAI embedding dimension
    metadata JSONB,
    content_type TEXT,
    source TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create index for similarity search
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops);

-- Create index for client lookups
CREATE INDEX ON documents (client_id);
CREATE INDEX ON documents (content_type);
```

#### 3. Embedding Generation
```python
def generate_embedding(text: str) -> List[float]:
    """Generate OpenAI embedding for text"""
    response = openai.embeddings.create(
        model="text-embedding-3-small",  # or text-embedding-ada-002
        input=text
    )
    return response.data[0].embedding
```

#### 4. Document Upload
```python
def upload_document(client_id, document_id, content, metadata):
    """Upload document to Supabase with embedding"""
    # Generate embedding
    embedding = generate_embedding(content)
    
    # Insert into Supabase
    data = {
        'client_id': client_id,
        'document_id': document_id,
        'content': content,
        'embedding': embedding,
        'metadata': metadata,
        'content_type': metadata.get('content_type'),
        'source': metadata.get('source')
    }
    
    result = supabase.table('documents').insert(data).execute()
    return result
```

#### 5. RAG Retrieval
```python
def query_documents(client_id, query, limit=10, content_type_filter=None):
    """Query documents using similarity search"""
    # Generate query embedding
    query_embedding = generate_embedding(query)
    
    # RPC call to pgvector similarity search
    results = supabase.rpc(
        'match_documents',
        {
            'query_embedding': query_embedding,
            'match_client_id': client_id,
            'match_content_type': content_type_filter,
            'match_threshold': 0.7,
            'match_count': limit
        }
    ).execute()
    
    return results.data
```

#### 6. Similarity Search Function (PostgreSQL)
```sql
CREATE OR REPLACE FUNCTION match_documents(
    query_embedding vector(1536),
    match_client_id text,
    match_content_type text DEFAULT NULL,
    match_threshold float DEFAULT 0.7,
    match_count int DEFAULT 10
)
RETURNS TABLE (
    id uuid,
    document_id text,
    content text,
    metadata jsonb,
    similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        d.id,
        d.document_id,
        d.content,
        d.metadata,
        1 - (d.embedding <=> query_embedding) as similarity
    FROM documents d
    WHERE d.client_id = match_client_id
        AND (match_content_type IS NULL OR d.content_type = match_content_type)
        AND 1 - (d.embedding <=> query_embedding) > match_threshold
    ORDER BY d.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;
```

## Migration Steps

### Phase 1: Create Supabase Infrastructure
1. ✅ Set up Supabase project
2. ✅ Create database schema with pgvector
3. ✅ Create similarity search functions
4. ✅ Create SupabaseVectorStore class
5. ✅ Test basic operations

### Phase 2: Migrate Ingestion Pipeline
1. Replace `VectaraClientOnboarder` with `SupabaseClientOnboarder`
2. Modify `create_vectara_corpus()` → `create_client_collection()`
3. Modify `upload_files_to_vectara()` → `upload_files_to_supabase()`
4. Add embedding generation for all documents
5. Update metadata structure

### Phase 3: Migrate RAG Retrieval
1. Replace all Vectara query calls with Supabase queries
2. Update `client_brief_generator.py`
3. Update all summarizer scripts
4. Ensure metadata filtering works correctly

### Phase 4: Update Agentic Workflow
1. Modify `agentic_workflow.py` tools
2. Update `upload_to_vertex()` → `upload_to_supabase()`
3. Test agent workflow with Supabase

### Phase 5: Testing & Validation
1. Test document upload
2. Test similarity search
3. Test metadata filtering
4. Compare results with Vectara baseline
5. Performance testing

## Cost Comparison

### Vectara
- API-based pricing
- Pay per query/document
- ~$0.50-2.00 per 1000 queries

### Supabase + OpenAI Embeddings
- Supabase: Free tier (500MB) or ~$25/month
- OpenAI embeddings: $0.13 per 1M tokens (text-embedding-3-small)
- More cost-effective at scale

## Configuration Changes

### Environment Variables
```bash
# Remove
VECTARA_API_KEY=...

# Add
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
OPENAI_API_KEY=sk-...  # For embeddings
```

### Dependencies
```bash
# Remove
vectara>=0.1.0

# Add
supabase>=2.0.0
pgvector>=0.2.0
```

## Files to Create

1. **supabase_vector_store.py** - Main Supabase client
2. **supabase_client_onboarder.py** - Replace VectaraClientOnboarder
3. **supabase_query.py** - RAG query utilities
4. **supabase_schema.sql** - Database schema
5. **test_supabase_migration.py** - Test suite

## Files to Modify

1. **new_client_ingestion.py** - Use SupabaseClientOnboarder
2. **agentic_workflow.py** - Update tools
3. **client_brief_generator.py** - Use Supabase queries
4. **summarizers/*.py** - Use Supabase queries
5. **requirements.txt** - Update dependencies
6. **README.md** - Update setup instructions

## Backward Compatibility

Option 1: **Clean migration** - Remove Vectara entirely
Option 2: **Dual support** - Support both Vectara and Supabase with flag
Option 3: **Migration tool** - Script to migrate existing Vectara data

## Next Steps

**Please confirm:**
1. Do you have an existing Supabase project set up?
2. Should I create the complete Supabase infrastructure?
3. Do you want dual support or clean migration?
4. Should I migrate existing Vectara data or start fresh?
