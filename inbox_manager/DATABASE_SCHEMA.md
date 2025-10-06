# Database Schema Reference

## Supabase Tables Used

### `document_chunks` Table

This is the primary table used by the Inbox Manager for RAG retrieval.

```sql
CREATE TABLE document_chunks (
    id UUID PRIMARY KEY,
    document_id UUID NOT NULL,
    client_id TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    content_sha256 TEXT,
    token_count INTEGER,
    embedding VECTOR(1536),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Important indexes for performance
CREATE INDEX ON document_chunks (client_id);
CREATE INDEX ON document_chunks USING ivfflat (embedding vector_cosine_ops);
```

### Key Fields

- **`id`**: Unique identifier for each chunk
- **`document_id`**: Reference to parent document in `documents` table
- **`client_id`**: Client identifier (used for filtering)
- **`chunk_index`**: Order of this chunk within the parent document
- **`content`**: The actual text content (with metadata frontmatter)
- **`token_count`**: Number of tokens in this chunk
- **`embedding`**: 1536-dimensional vector from OpenAI text-embedding-3-small
- **`created_at`**: Timestamp when chunk was created

## Content Format

The `content` field includes YAML frontmatter with metadata:

```markdown
--- 
source: "website" 
content_type: "case_studies" 
url: "https://example.com/page" 
title: "Page Title" 
domain: "example.com" 
path: "/page" 
scraped_time: "2025-10-04T14:12:38.035685" 
url_depth: 2 
word_count: 590 
client_name: "client-name" 
--- 

### Heading

Actual content text here...
```

## How Inbox Manager Uses This

1. **Client Filtering**: `WHERE client_id = 'dodeka-digital-supa'`
2. **Vector Search**: `ORDER BY embedding <=> query_embedding::vector`
3. **Similarity Threshold**: `WHERE 1 - (embedding <=> query) > 0.7`
4. **Top-K Results**: `LIMIT 5`

## Example Query

```sql
SELECT 
    id,
    document_id,
    client_id,
    chunk_index,
    content,
    token_count,
    1 - (embedding <=> '[...]'::vector) as similarity
FROM document_chunks
WHERE client_id = 'dodeka-digital-supa'
    AND 1 - (embedding <=> '[...]'::vector) > 0.7
ORDER BY embedding <=> '[...]'::vector
LIMIT 5;
```

This returns the top 5 most relevant chunks for the client with similarity > 70%.

