#!/usr/bin/env python3
"""
Document Uploader with Upsert Logic

Handles uploading documents to the documents table with unique constraint
on (client_id, uri). If a document already exists, it updates it.
"""
import psycopg2
from psycopg2.extras import RealDictCursor, execute_values
from typing import Dict, List, Optional
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv("/Users/hynes/dev/vectara/.env")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SUPABASE_VECTOR_DB_CONN = os.getenv("SUPABASE_VECTOR_DB_CONN")


class DocumentUploader:
    """Handles document uploads with upsert logic"""
    
    def __init__(self):
        self.conn_string = SUPABASE_VECTOR_DB_CONN
        
    def get_connection(self):
        """Get database connection"""
        return psycopg2.connect(self.conn_string, cursor_factory=RealDictCursor)
    
    def ensure_unique_constraint(self):
        """
        Ensure unique constraint exists on (client_id, uri)
        This allows upsert operations
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    # Check if constraint exists
                    cur.execute("""
                        SELECT constraint_name 
                        FROM information_schema.table_constraints 
                        WHERE table_name = 'documents' 
                        AND constraint_name = 'documents_client_id_uri_key';
                    """)
                    
                    if not cur.fetchone():
                        logger.info("Creating unique constraint on (client_id, uri)...")
                        cur.execute("""
                            ALTER TABLE documents 
                            ADD CONSTRAINT documents_client_id_uri_key 
                            UNIQUE (client_id, uri);
                        """)
                        conn.commit()
                        logger.info("✅ Unique constraint created")
                    else:
                        logger.info("✅ Unique constraint already exists")
                        
        except Exception as e:
            logger.error(f"Error ensuring unique constraint: {e}")
            raise
    
    def upsert_document(
        self,
        client_id: str,
        uri: str,
        title: Optional[str] = None,
        sha256: Optional[str] = None,
        mime_type: Optional[str] = None,
        language: Optional[str] = None,
        metadata: Optional[Dict] = None,
        source_type: Optional[str] = None,
        content_type: Optional[str] = None
    ) -> str:
        """
        Insert or update a document
        
        Args:
            client_id: Client identifier (required)
            uri: Document URI/URL (required)
            title: Document title
            sha256: Content hash
            mime_type: MIME type
            language: Language code
            metadata: JSONB metadata
            source_type: Source type (website, gdrive, etc.)
            content_type: Content category
            
        Returns:
            Document ID (UUID)
        """
        try:
            if metadata is None:
                metadata = {}
            
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    # Upsert using ON CONFLICT
                    sql = """
                        INSERT INTO documents (
                            client_id, 
                            uri, 
                            title, 
                            sha256, 
                            mime_type, 
                            language, 
                            metadata, 
                            source_type, 
                            content_type,
                            ingested_at
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (client_id, uri) 
                        DO UPDATE SET
                            title = EXCLUDED.title,
                            sha256 = EXCLUDED.sha256,
                            mime_type = EXCLUDED.mime_type,
                            language = EXCLUDED.language,
                            metadata = EXCLUDED.metadata,
                            source_type = EXCLUDED.source_type,
                            content_type = EXCLUDED.content_type,
                            ingested_at = EXCLUDED.ingested_at
                        RETURNING id;
                    """
                    
                    cur.execute(sql, (
                        client_id,
                        uri,
                        title,
                        sha256,
                        mime_type,
                        language,
                        json.dumps(metadata),
                        source_type,
                        content_type,
                        datetime.now()
                    ))
                    
                    result = cur.fetchone()
                    doc_id = result['id']
                    
                    conn.commit()
                    logger.info(f"✅ Upserted document: {doc_id} for {uri}")
                    return doc_id
                    
        except Exception as e:
            logger.error(f"Error upserting document: {e}")
            raise
    
    def upsert_documents_batch(self, documents: List[Dict]) -> List[str]:
        """
        Batch upsert multiple documents
        
        Args:
            documents: List of document dicts with required fields:
                - client_id (required)
                - uri (required)
                - title (optional)
                - sha256 (optional)
                - mime_type (optional)
                - language (optional)
                - metadata (optional)
                - source_type (optional)
                - content_type (optional)
                
        Returns:
            List of document IDs
        """
        doc_ids = []
        
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    for doc in documents:
                        # Validate required fields
                        if 'client_id' not in doc or 'uri' not in doc:
                            logger.warning(f"Skipping document - missing client_id or uri: {doc}")
                            continue
                        
                        # Prepare values
                        values = (
                            doc['client_id'],
                            doc['uri'],
                            doc.get('title'),
                            doc.get('sha256'),
                            doc.get('mime_type'),
                            doc.get('language'),
                            json.dumps(doc.get('metadata', {})),
                            doc.get('source_type'),
                            doc.get('content_type'),
                            datetime.now()
                        )
                        
                        # Upsert
                        sql = """
                            INSERT INTO documents (
                                client_id, uri, title, sha256, mime_type, 
                                language, metadata, source_type, content_type, ingested_at
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (client_id, uri) 
                            DO UPDATE SET
                                title = EXCLUDED.title,
                                sha256 = EXCLUDED.sha256,
                                mime_type = EXCLUDED.mime_type,
                                language = EXCLUDED.language,
                                metadata = EXCLUDED.metadata,
                                source_type = EXCLUDED.source_type,
                                content_type = EXCLUDED.content_type,
                                ingested_at = EXCLUDED.ingested_at
                            RETURNING id;
                        """
                        
                        cur.execute(sql, values)
                        result = cur.fetchone()
                        doc_ids.append(result['id'])
                    
                    conn.commit()
                    logger.info(f"✅ Batch upserted {len(doc_ids)} documents")
                    
        except Exception as e:
            logger.error(f"Error in batch upsert: {e}")
            raise
        
        return doc_ids
    
    def get_document_by_uri(self, client_id: str, uri: str) -> Optional[Dict]:
        """Get a document by client_id and uri"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT * FROM documents 
                        WHERE client_id = %s AND uri = %s;
                    """, (client_id, uri))
                    
                    result = cur.fetchone()
                    return dict(result) if result else None
                    
        except Exception as e:
            logger.error(f"Error fetching document: {e}")
            return None
    
    def delete_document(self, client_id: str, uri: str) -> bool:
        """Delete a document by client_id and uri"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        DELETE FROM documents 
                        WHERE client_id = %s AND uri = %s
                        RETURNING id;
                    """, (client_id, uri))
                    
                    result = cur.fetchone()
                    conn.commit()
                    
                    if result:
                        logger.info(f"✅ Deleted document: {result['id']}")
                        return True
                    else:
                        logger.warning(f"No document found to delete: {uri}")
                        return False
                        
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            return False


def main():
    """Example usage and testing"""
    print("📤 Document Uploader - Testing\n")
    
    uploader = DocumentUploader()
    
    # 1. Ensure unique constraint
    print("1️⃣ Ensuring unique constraint...")
    uploader.ensure_unique_constraint()
    
    # 2. Test single upsert (using existing client)
    test_client = "dodeka-digital-supa"  # Use existing client
    
    print("\n2️⃣ Testing single document upsert...")
    doc_id = uploader.upsert_document(
        client_id=test_client,
        uri="https://example.com/test-page-script",
        title="Test Page",
        content_type="test",
        source_type="manual",
        metadata={
            "test": True,
            "created_by": "script"
        }
    )
    print(f"   Created/Updated: {doc_id}")
    
    # 3. Update the same document
    print("\n3️⃣ Updating same document with new title...")
    doc_id2 = uploader.upsert_document(
        client_id=test_client,
        uri="https://example.com/test-page-script",
        title="Test Page - Updated",
        content_type="test",
        source_type="manual",
        metadata={
            "test": True,
            "updated": True
        }
    )
    print(f"   Updated: {doc_id2}")
    print(f"   Same ID: {doc_id == doc_id2} ✅")
    
    # 4. Retrieve document
    print("\n4️⃣ Retrieving document...")
    doc = uploader.get_document_by_uri(test_client, "https://example.com/test-page-script")
    if doc:
        print(f"   Title: {doc['title']}")
        print(f"   Metadata: {doc['metadata']}")
    
    # 5. Batch upsert
    print("\n5️⃣ Testing batch upsert...")
    docs = [
        {
            "client_id": test_client,
            "uri": "https://example.com/page1-script",
            "title": "Page 1",
            "content_type": "test"
        },
        {
            "client_id": test_client,
            "uri": "https://example.com/page2-script",
            "title": "Page 2",
            "content_type": "test"
        }
    ]
    ids = uploader.upsert_documents_batch(docs)
    print(f"   Created/Updated {len(ids)} documents")
    
    # 6. Clean up test data
    print("\n6️⃣ Cleaning up test documents...")
    uploader.delete_document(test_client, "https://example.com/test-page-script")
    uploader.delete_document(test_client, "https://example.com/page1-script")
    uploader.delete_document(test_client, "https://example.com/page2-script")
    
    print("\n✅ All tests completed!")


if __name__ == "__main__":
    main()

