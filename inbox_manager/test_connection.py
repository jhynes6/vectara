#!/usr/bin/env python3
"""
Test script to verify Supabase connection and database setup
"""
import sys
from dotenv import load_dotenv

load_dotenv()

from vector_store import VectorStore
from config import SUPABASE_VECTOR_DB_CONN

def test_connection():
    """Test database connection and table structure"""
    print("🧪 Testing Inbox Manager Setup\n")
    
    # Test 1: Connection string
    print("1️⃣ Checking connection string...")
    if SUPABASE_VECTOR_DB_CONN:
        print("   ✅ Connection string configured")
    else:
        print("   ❌ Connection string not found in .env")
        return False
    
    # Test 2: Database connection
    print("\n2️⃣ Testing database connection...")
    try:
        vector_store = VectorStore()
        conn = vector_store.get_connection()
        print("   ✅ Successfully connected to database")
        conn.close()
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        return False
    
    # Test 3: Table structure
    print("\n3️⃣ Checking documents table...")
    try:
        with vector_store.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'documents'
                    ORDER BY ordinal_position;
                """)
                columns = cur.fetchall()
                
                if columns:
                    print("   ✅ Documents table exists")
                    print("   📋 Columns:")
                    for col in columns:
                        print(f"      - {col['column_name']}: {col['data_type']}")
                else:
                    print("   ⚠️  Documents table not found")
                    print("   📝 You need to create the documents table:")
                    print("""
                    CREATE TABLE documents (
                        id SERIAL PRIMARY KEY,
                        content TEXT NOT NULL,
                        embedding vector(1536),
                        metadata JSONB NOT NULL,
                        created_at TIMESTAMP DEFAULT NOW()
                    );
                    """)
                    return False
    except Exception as e:
        print(f"   ❌ Error checking table: {e}")
        return False
    
    # Test 4: Check for data
    print("\n4️⃣ Checking for documents...")
    try:
        with vector_store.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) as count FROM documents;")
                result = cur.fetchone()
                count = result['count'] if result else 0
                
                if count > 0:
                    print(f"   ✅ Found {count} documents in database")
                else:
                    print("   ⚠️  No documents found")
                    print("   📝 You need to ingest some documents first")
    except Exception as e:
        print(f"   ❌ Error checking documents: {e}")
        return False
    
    # Test 5: List clients
    print("\n5️⃣ Listing available clients...")
    try:
        clients = vector_store.list_available_clients()
        if clients:
            print(f"   ✅ Found {len(clients)} client(s):")
            for client_id in clients:
                doc_count = vector_store.get_client_documents_count(client_id)
                print(f"      - {client_id}: {doc_count} documents")
        else:
            print("   ⚠️  No clients found")
            print("   📝 Make sure documents have 'client_id' in metadata")
    except Exception as e:
        print(f"   ❌ Error listing clients: {e}")
        return False
    
    # Test 6: Test embedding generation
    print("\n6️⃣ Testing embedding generation...")
    try:
        embedding = vector_store.get_embedding("test query")
        print(f"   ✅ Successfully generated embedding (dimension: {len(embedding)})")
    except Exception as e:
        print(f"   ❌ Error generating embedding: {e}")
        print("   📝 Check your OPENAI_API_KEY in .env")
        return False
    
    print("\n" + "="*60)
    print("✨ All tests passed! Inbox Manager is ready to use.")
    print("="*60)
    print("\n🚀 Run the application with: python app.py")
    print("📱 Then open http://localhost:5000 in your browser\n")
    
    return True

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
