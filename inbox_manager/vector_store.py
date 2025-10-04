"""
Vector Store Handler for Supabase pgvector
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Optional
import numpy as np
from openai import OpenAI
import logging

from config import (
    SUPABASE_VECTOR_DB_CONN,
    OPENAI_API_KEY,
    TOP_K_RESULTS,
    SIMILARITY_THRESHOLD
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VectorStore:
    """Interface for querying Supabase vector database"""
    
    def __init__(self):
        self.conn_string = SUPABASE_VECTOR_DB_CONN
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY)
        
    def get_connection(self):
        """Get database connection"""
        return psycopg2.connect(self.conn_string, cursor_factory=RealDictCursor)
    
    def get_embedding(self, text: str, model: str = "text-embedding-3-small") -> List[float]:
        """Generate embedding for text using OpenAI"""
        try:
            response = self.openai_client.embeddings.create(
                input=text,
                model=model
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise
    
    def search_documents(
        self,
        query: str,
        client_id: str,
        top_k: int = TOP_K_RESULTS,
        similarity_threshold: float = SIMILARITY_THRESHOLD,
        filters: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Search for relevant documents in the vector database
        
        Args:
            query: The search query
            client_id: Client identifier for filtering
            top_k: Number of results to return
            similarity_threshold: Minimum similarity score
            filters: Additional metadata filters
            
        Returns:
            List of documents with content, metadata, and similarity scores
        """
        try:
            # Generate embedding for query
            query_embedding = self.get_embedding(query)
            
            # Build the query
            # Assuming table structure: documents(id, content, embedding, metadata jsonb)
            # metadata should contain client_id field
            
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    # Check if the table exists and get its structure
                    cur.execute("""
                        SELECT column_name, data_type 
                        FROM information_schema.columns 
                        WHERE table_name = 'documents'
                        ORDER BY ordinal_position;
                    """)
                    columns = cur.fetchall()
                    
                    if not columns:
                        logger.warning("Documents table not found. Returning empty results.")
                        return []
                    
                    # Build query with client_id filter
                    sql = """
                        SELECT 
                            id,
                            content,
                            metadata,
                            1 - (embedding <=> %s::vector) as similarity
                        FROM documents
                        WHERE metadata->>'client_id' = %s
                            AND 1 - (embedding <=> %s::vector) > %s
                        ORDER BY embedding <=> %s::vector
                        LIMIT %s;
                    """
                    
                    # Execute search
                    cur.execute(
                        sql,
                        (query_embedding, client_id, query_embedding, similarity_threshold, query_embedding, top_k)
                    )
                    
                    results = cur.fetchall()
                    
                    logger.info(f"Found {len(results)} documents for client_id={client_id} with similarity > {similarity_threshold}")
                    
                    return [dict(row) for row in results]
                    
        except Exception as e:
            logger.error(f"Error searching documents: {e}")
            # Return empty results rather than failing
            return []
    
    def get_client_documents_count(self, client_id: str) -> int:
        """Get count of documents for a specific client"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT COUNT(*) as count
                        FROM documents
                        WHERE metadata->>'client_id' = %s;
                    """, (client_id,))
                    
                    result = cur.fetchone()
                    return result['count'] if result else 0
                    
        except Exception as e:
            logger.error(f"Error getting document count: {e}")
            return 0
    
    def list_available_clients(self) -> List[str]:
        """List all unique client IDs in the database"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT DISTINCT metadata->>'client_id' as client_id
                        FROM documents
                        WHERE metadata->>'client_id' IS NOT NULL
                        ORDER BY client_id;
                    """)
                    
                    results = cur.fetchall()
                    return [row['client_id'] for row in results if row['client_id']]
                    
        except Exception as e:
            logger.error(f"Error listing clients: {e}")
            return []
