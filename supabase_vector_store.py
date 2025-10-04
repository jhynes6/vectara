#!/usr/bin/env python3
"""
Supabase Vector Store

Handles all vector database operations using Supabase + pgvector.
Replaces Vectara for document storage and RAG retrieval.
"""

import os
import hashlib
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from uuid import UUID, uuid4
from dotenv import load_dotenv

# Database
import psycopg2
from psycopg2.extras import execute_values, Json
from psycopg2.pool import SimpleConnectionPool

# OpenAI for embeddings
import sys
sys.path.insert(0, '/home/ubuntu/.local/lib/python3.13/site-packages')
from openai import OpenAI

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SupabaseVectorStore:
    """
    Vector store client for Supabase + pgvector
    Handles document chunking, embedding generation, and similarity search
    """
    
    def __init__(self, 
                 connection_string: str = None,
                 openai_api_key: str = None,
                 embedding_model: str = "text-embedding-3-small",
                 chunk_size: int = 1000,
                 chunk_overlap: int = 200):
        """
        Initialize Supabase vector store
        
        Args:
            connection_string: PostgreSQL connection string
            openai_api_key: OpenAI API key for embeddings
            embedding_model: OpenAI embedding model to use
            chunk_size: Maximum tokens per chunk
            chunk_overlap: Token overlap between chunks
        """
        self.connection_string = connection_string or os.getenv('SUPABASE_VECTOR_DB_CONN')
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        self.embedding_model = embedding_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        if not self.connection_string:
            raise ValueError("SUPABASE_VECTOR_DB_CONN not found in environment")
        
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        
        # Initialize OpenAI client
        self.openai_client = OpenAI(api_key=self.openai_api_key)
        
        # Initialize connection pool
        self.pool = SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            dsn=self.connection_string
        )
        
        logger.info("✅ Supabase vector store initialized")
    
    def _get_connection(self):
        """Get a connection from the pool"""
        return self.pool.getconn()
    
    def _return_connection(self, conn):
        """Return a connection to the pool"""
        self.pool.putconn(conn)
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text using OpenAI
        
        Args:
            text: Text to embed
            
        Returns:
            List of floats representing the embedding
        """
        try:
            response = self.openai_client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into chunks for embedding
        
        Args:
            text: Text to chunk
            
        Returns:
            List of text chunks
        """
        # Simple chunking by words (approximate tokens)
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk_words = words[i:i + self.chunk_size]
            chunks.append(' '.join(chunk_words))
        
        return chunks if chunks else [text]
    
    def ensure_client_exists(self, client_id: str, primary_domain: str = None, 
                           drive_folder_id: str = None) -> UUID:
        """
        Ensure client exists in database, create if not
        
        Args:
            client_id: Client identifier (string)
            primary_domain: Client's primary domain
            drive_folder_id: Google Drive folder ID
            
        Returns:
            Client UUID
        """
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                # Check if client exists (using client_id as the UUID or converting)
                try:
                    # Try to use client_id as UUID if it's already one
                    client_uuid = UUID(client_id)
                except ValueError:
                    # Generate UUID from client_id string
                    client_uuid = uuid4()
                
                cur.execute(
                    "SELECT client_id FROM clients WHERE client_id = %s",
                    (client_uuid,)
                )
                
                result = cur.fetchone()
                
                if result:
                    logger.info(f"Client {client_id} already exists: {client_uuid}")
                    return client_uuid
                
                # Create new client
                cur.execute(
                    """
                    INSERT INTO clients (client_id, primary_domain, drive_folder_id)
                    VALUES (%s, %s, %s)
                    RETURNING client_id
                    """,
                    (client_uuid, primary_domain, drive_folder_id)
                )
                
                conn.commit()
                logger.info(f"✅ Created client {client_id}: {client_uuid}")
                return client_uuid
                
        except Exception as e:
            conn.rollback()
            logger.error(f"Error ensuring client exists: {e}")
            raise
        finally:
            self._return_connection(conn)
    
    def get_or_create_source_type(self, source_key: str) -> int:
        """Get or create source type ID"""
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id FROM source_types WHERE key = %s",
                    (source_key,)
                )
                result = cur.fetchone()
                
                if result:
                    return result[0]
                
                cur.execute(
                    "INSERT INTO source_types (key) VALUES (%s) RETURNING id",
                    (source_key,)
                )
                conn.commit()
                return cur.fetchone()[0]
        finally:
            self._return_connection(conn)
    
    def get_or_create_content_type(self, content_key: str) -> int:
        """Get or create content type ID"""
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id FROM content_types WHERE key = %s",
                    (content_key,)
                )
                result = cur.fetchone()
                
                if result:
                    return result[0]
                
                cur.execute(
                    "INSERT INTO content_types (key) VALUES (%s) RETURNING id",
                    (content_key,)
                )
                conn.commit()
                return cur.fetchone()[0]
        finally:
            self._return_connection(conn)
    
    def upload_document(self, 
                       client_id: str,
                       content: str,
                       title: str = None,
                       uri: str = None,
                       source_type: str = "website",
                       content_type: str = "other",
                       metadata: Dict[str, Any] = None,
                       mime_type: str = "text/markdown",
                       language: str = "eng") -> Tuple[UUID, int]:
        """
        Upload a document with automatic chunking and embedding
        
        Args:
            client_id: Client identifier
            content: Document content
            title: Document title
            uri: Document URI/URL
            source_type: Source type (website, client_materials, client_intake_form)
            content_type: Content type (case_studies, services_products, etc)
            metadata: Additional metadata
            mime_type: Document MIME type
            language: Document language code
            
        Returns:
            Tuple of (document_uuid, chunks_count)
        """
        conn = self._get_connection()
        try:
            # Ensure client exists
            client_uuid = self.ensure_client_exists(client_id)
            
            # Get type IDs
            source_type_id = self.get_or_create_source_type(source_type)
            content_type_id = self.get_or_create_content_type(content_type)
            
            # Calculate document hash
            doc_sha256 = hashlib.sha256(content.encode()).hexdigest()
            
            with conn.cursor() as cur:
                # Check if document already exists
                cur.execute(
                    "SELECT id FROM documents WHERE client_id = %s AND sha256 = %s",
                    (client_uuid, doc_sha256)
                )
                existing = cur.fetchone()
                
                if existing:
                    logger.info(f"Document already exists: {existing[0]}")
                    return existing[0], 0
                
                # Insert document
                cur.execute(
                    """
                    INSERT INTO documents 
                    (client_id, source_type_id, content_type_id, title, uri, 
                     sha256, mime_type, language, metadata)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (client_uuid, source_type_id, content_type_id, title, uri,
                     doc_sha256, mime_type, language, Json(metadata or {}))
                )
                
                document_id = cur.fetchone()[0]
                
                # Chunk the content
                chunks = self.chunk_text(content)
                
                # Generate embeddings and insert chunks
                chunk_data = []
                for idx, chunk in enumerate(chunks):
                    # Generate embedding
                    embedding = self.generate_embedding(chunk)
                    chunk_sha256 = hashlib.sha256(chunk.encode()).hexdigest()
                    
                    chunk_data.append((
                        document_id,
                        client_uuid,
                        idx,
                        chunk,
                        chunk_sha256,
                        len(chunk.split()),  # Approximate token count
                        embedding
                    ))
                
                # Batch insert chunks
                execute_values(
                    cur,
                    """
                    INSERT INTO document_chunks 
                    (document_id, client_id, chunk_index, content, content_sha256, 
                     token_count, embedding)
                    VALUES %s
                    """,
                    chunk_data
                )
                
                conn.commit()
                logger.info(f"✅ Uploaded document {document_id} with {len(chunks)} chunks")
                return document_id, len(chunks)
                
        except Exception as e:
            conn.rollback()
            logger.error(f"Error uploading document: {e}")
            raise
        finally:
            self._return_connection(conn)
    
    def query_documents(self, 
                       client_id: str,
                       query: str,
                       limit: int = 10,
                       content_type_filter: str = None,
                       source_type_filter: str = None,
                       similarity_threshold: float = 0.7) -> List[Dict[str, Any]]:
        """
        Query documents using semantic similarity search
        
        Args:
            client_id: Client identifier
            query: Query text
            limit: Maximum number of results
            content_type_filter: Filter by content type
            source_type_filter: Filter by source type
            similarity_threshold: Minimum similarity score
            
        Returns:
            List of matching chunks with metadata
        """
        conn = self._get_connection()
        try:
            # Get client UUID
            client_uuid = self.ensure_client_exists(client_id)
            
            # Generate query embedding
            query_embedding = self.generate_embedding(query)
            
            with conn.cursor() as cur:
                # Build query with filters
                query_sql = """
                    SELECT 
                        dc.id,
                        dc.content,
                        dc.chunk_index,
                        d.id as document_id,
                        d.title,
                        d.uri,
                        d.metadata,
                        st.key as source_type,
                        ct.key as content_type,
                        1 - (dc.embedding <=> %s::vector) as similarity
                    FROM document_chunks dc
                    JOIN documents d ON dc.document_id = d.id
                    JOIN source_types st ON d.source_type_id = st.id
                    JOIN content_types ct ON d.content_type_id = ct.id
                    WHERE dc.client_id = %s
                        AND 1 - (dc.embedding <=> %s::vector) > %s
                """
                
                params = [query_embedding, client_uuid, query_embedding, similarity_threshold]
                
                if content_type_filter:
                    query_sql += " AND ct.key = %s"
                    params.append(content_type_filter)
                
                if source_type_filter:
                    query_sql += " AND st.key = %s"
                    params.append(source_type_filter)
                
                query_sql += """
                    ORDER BY dc.embedding <=> %s::vector
                    LIMIT %s
                """
                params.extend([query_embedding, limit])
                
                cur.execute(query_sql, params)
                
                results = []
                for row in cur.fetchall():
                    results.append({
                        'chunk_id': str(row[0]),
                        'content': row[1],
                        'chunk_index': row[2],
                        'document_id': str(row[3]),
                        'title': row[4],
                        'uri': row[5],
                        'metadata': row[6],
                        'source_type': row[7],
                        'content_type': row[8],
                        'similarity': float(row[9])
                    })
                
                logger.info(f"Found {len(results)} matching chunks for query")
                return results
                
        except Exception as e:
            logger.error(f"Error querying documents: {e}")
            raise
        finally:
            self._return_connection(conn)
    
    def delete_client_documents(self, client_id: str) -> int:
        """
        Delete all documents for a client
        
        Args:
            client_id: Client identifier
            
        Returns:
            Number of documents deleted
        """
        conn = self._get_connection()
        try:
            client_uuid = self.ensure_client_exists(client_id)
            
            with conn.cursor() as cur:
                # Delete chunks first (cascading should handle this, but being explicit)
                cur.execute(
                    "DELETE FROM document_chunks WHERE client_id = %s",
                    (client_uuid,)
                )
                
                # Delete documents
                cur.execute(
                    "DELETE FROM documents WHERE client_id = %s RETURNING id",
                    (client_uuid,)
                )
                
                deleted_count = cur.rowcount
                conn.commit()
                
                logger.info(f"Deleted {deleted_count} documents for client {client_id}")
                return deleted_count
                
        except Exception as e:
            conn.rollback()
            logger.error(f"Error deleting client documents: {e}")
            raise
        finally:
            self._return_connection(conn)
    
    def get_client_stats(self, client_id: str) -> Dict[str, Any]:
        """
        Get statistics for a client
        
        Args:
            client_id: Client identifier
            
        Returns:
            Dictionary with client statistics
        """
        conn = self._get_connection()
        try:
            client_uuid = self.ensure_client_exists(client_id)
            
            with conn.cursor() as cur:
                # Get document and chunk counts
                cur.execute(
                    """
                    SELECT 
                        COUNT(DISTINCT d.id) as document_count,
                        COUNT(dc.id) as chunk_count,
                        SUM(dc.token_count) as total_tokens
                    FROM documents d
                    LEFT JOIN document_chunks dc ON d.id = dc.document_id
                    WHERE d.client_id = %s
                    """,
                    (client_uuid,)
                )
                
                row = cur.fetchone()
                
                return {
                    'client_id': client_id,
                    'client_uuid': str(client_uuid),
                    'document_count': row[0] or 0,
                    'chunk_count': row[1] or 0,
                    'total_tokens': row[2] or 0
                }
                
        except Exception as e:
            logger.error(f"Error getting client stats: {e}")
            raise
        finally:
            self._return_connection(conn)
    
    def close(self):
        """Close all connections in the pool"""
        if self.pool:
            self.pool.closeall()
            logger.info("Connection pool closed")


# Convenience function for getting a vector store instance
def get_vector_store() -> SupabaseVectorStore:
    """Get a configured SupabaseVectorStore instance"""
    return SupabaseVectorStore()
