#!/usr/bin/env python3
"""
Test Supabase Migration

Validates that the Supabase vector store is working correctly
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, '/home/ubuntu/.local/lib/python3.13/site-packages')


def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from supabase_vector_store import SupabaseVectorStore
        print("  ✅ supabase_vector_store imported")
    except ImportError as e:
        print(f"  ❌ Failed to import supabase_vector_store: {e}")
        return False
    
    try:
        from supabase_client_ingestion import SupabaseClientOnboarder
        print("  ✅ supabase_client_ingestion imported")
    except ImportError as e:
        print(f"  ❌ Failed to import supabase_client_ingestion: {e}")
        return False
    
    try:
        from supabase_brief_generator import SupabaseClientBriefGenerator
        print("  ✅ supabase_brief_generator imported")
    except ImportError as e:
        print(f"  ❌ Failed to import supabase_brief_generator: {e}")
        return False
    
    return True


def test_connection():
    """Test database connection"""
    print("\nTesting database connection...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    conn_string = os.getenv('SUPABASE_VECTOR_DB_CONN')
    if not conn_string:
        print("  ⚠️  SUPABASE_VECTOR_DB_CONN not set in environment")
        return False
    
    try:
        import psycopg2
        conn = psycopg2.connect(conn_string)
        print("  ✅ Database connection successful")
        
        # Test pgvector extension
        with conn.cursor() as cur:
            cur.execute("SELECT extname FROM pg_extension WHERE extname = 'vector'")
            result = cur.fetchone()
            if result:
                print("  ✅ pgvector extension installed")
            else:
                print("  ⚠️  pgvector extension not found")
                print("     Run: CREATE EXTENSION vector;")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"  ❌ Database connection failed: {e}")
        return False


def test_vector_store():
    """Test SupabaseVectorStore initialization"""
    print("\nTesting SupabaseVectorStore...")
    
    try:
        from supabase_vector_store import SupabaseVectorStore
        from dotenv import load_dotenv
        load_dotenv()
        
        if not os.getenv('OPENAI_API_KEY'):
            print("  ⚠️  OPENAI_API_KEY not set")
            return False
        
        vs = SupabaseVectorStore()
        print("  ✅ SupabaseVectorStore initialized")
        
        # Test embedding generation
        embedding = vs.generate_embedding("test text")
        print(f"  ✅ Embedding generated: {len(embedding)} dimensions")
        
        # Test client creation
        test_client_id = "test-client-migration"
        client_uuid = vs.ensure_client_exists(
            client_id=test_client_id,
            primary_domain="test.example.com"
        )
        print(f"  ✅ Client ensured: {client_uuid}")
        
        # Test stats
        stats = vs.get_client_stats(test_client_id)
        print(f"  ✅ Stats retrieved: {stats['document_count']} documents")
        
        return True
        
    except Exception as e:
        print(f"  ❌ SupabaseVectorStore test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_document_upload():
    """Test document upload"""
    print("\nTesting document upload...")
    
    try:
        from supabase_vector_store import SupabaseVectorStore
        from dotenv import load_dotenv
        load_dotenv()
        
        vs = SupabaseVectorStore()
        
        # Upload test document
        doc_id, chunks = vs.upload_document(
            client_id="test-client-migration",
            content="This is a test document for Supabase migration. It tests the document upload and chunking functionality.",
            title="Test Document",
            uri="test://document",
            source_type="website",
            content_type="other",
            metadata={"test": True}
        )
        
        print(f"  ✅ Document uploaded: {doc_id}")
        print(f"  ✅ Chunks created: {chunks}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Document upload failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_query():
    """Test semantic search query"""
    print("\nTesting semantic search...")
    
    try:
        from supabase_vector_store import SupabaseVectorStore
        from dotenv import load_dotenv
        load_dotenv()
        
        vs = SupabaseVectorStore()
        
        # Query documents
        results = vs.query_documents(
            client_id="test-client-migration",
            query="test document migration",
            limit=5,
            similarity_threshold=0.5
        )
        
        print(f"  ✅ Query successful: {len(results)} results")
        
        if results:
            print(f"  ✅ Top result similarity: {results[0]['similarity']:.3f}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Query failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("=" * 80)
    print("SUPABASE MIGRATION TEST SUITE")
    print("=" * 80)
    print()
    
    results = {
        'imports': test_imports(),
        'connection': test_connection(),
        'vector_store': test_vector_store(),
        'document_upload': test_document_upload(),
        'query': test_query()
    }
    
    print("\n" + "=" * 80)
    print("TEST RESULTS")
    print("=" * 80)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 80)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("The Supabase migration is working correctly.")
    else:
        print("⚠️  SOME TESTS FAILED")
        print("Review the errors above and fix any issues.")
        print("\nCommon issues:")
        print("  • Missing SUPABASE_VECTOR_DB_CONN in .env")
        print("  • Missing OPENAI_API_KEY in .env")
        print("  • pgvector extension not installed")
        print("  • Connection string incorrect")
    print("=" * 80)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
