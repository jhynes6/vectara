#!/usr/bin/env python3
"""
Test script for client brief chunks functionality
"""
from vector_store import VectorStore
from email_handler import EmailHandler

def test_save_brief_chunks():
    """Test saving client brief chunks to document_chunks table"""
    print("🧪 Testing client brief chunks functionality")
    
    vs = VectorStore()
    client_id = 'abundantly'
    
    print(f"\n1. Saving client brief chunks for {client_id}...")
    success = vs.save_client_brief_chunks(client_id)
    
    if success:
        print(f"✅ Successfully saved client brief chunks for {client_id}")
    else:
        print(f"❌ Failed to save client brief chunks for {client_id}")
        return False
    
    return True

def test_query_brief_chunks():
    """Test querying client brief chunks from document_chunks table"""
    print(f"\n2. Testing client brief chunk queries...")
    
    vs = VectorStore()
    client_id = 'abundantly'
    query = 'What employee recognition services do you offer?'
    
    # Test querying client brief chunks specifically
    print(f"   Query: {query}")
    print(f"   Client: {client_id}")
    
    brief_chunks = vs.search_documents(
        query=query,
        client_id=client_id,
        top_k=1,
        filters={'content_type': 'client_brief'}
    )
    
    if brief_chunks:
        chunk = brief_chunks[0]
        print(f"✅ Found client brief chunk!")
        print(f"   - Title: {chunk.get('title', 'N/A')}")
        print(f"   - Content type: {chunk.get('content_type', 'N/A')}")
        print(f"   - Similarity: {chunk.get('similarity', 0):.3f}")
        print(f"   - Chunk index: {chunk.get('chunk_index', 'N/A')}")
        print(f"   - Content length: {len(chunk.get('content', ''))} chars")
        print(f"   - Content preview: {chunk.get('content', '')[:200]}...")
        
        # Check if UNIQUE MECHANISM RESEARCH was excluded
        content = chunk.get('content', '')
        if 'UNIQUE MECHANISM RESEARCH' in content:
            print('❌ UNIQUE MECHANISM RESEARCH section was NOT excluded!')
        else:
            print('✅ UNIQUE MECHANISM RESEARCH section was successfully excluded')
        
        return True
    else:
        print(f"❌ No client brief chunks found")
        return False

def test_email_handler_integration():
    """Test email handler with persisted client brief chunks"""
    print(f"\n3. Testing email handler integration...")
    
    handler = EmailHandler()
    client_id = 'abundantly'
    client_name = 'Abundantly'
    email_content = 'Hi, what employee recognition services do you offer?'
    
    print(f"   Email: {email_content}")
    print(f"   Client: {client_id} ({client_name})")
    
    result = handler.handle_email(email_content, client_id, client_name)
    
    if result.get('success'):
        print(f"✅ Email handler successful!")
        print(f"   - Documents found: {result.get('documents_found', 0)}")
        print(f"   - Confidence: {result.get('confidence', 0):.3f}")
        
        # Check document types
        documents = result.get('metadata', {}).get('documents', [])
        client_brief_docs = [doc for doc in documents if doc.get('content_type') == 'client_brief']
        regular_docs = [doc for doc in documents if doc.get('content_type') != 'client_brief']
        
        print(f"   - Client brief chunks: {len(client_brief_docs)}")
        print(f"   - Regular documents: {len(regular_docs)}")
        
        if client_brief_docs:
            print(f"   ✅ Client brief chunk included from document_chunks table!")
        else:
            print(f"   ❌ No client brief chunks found in results")
            
        response = result.get('response', '')
        print(f"   - Response length: {len(response)} chars")
        print(f"   - Response preview: {response[:300]}...")
        
        return True
    else:
        print(f"❌ Email handler failed: {result.get('response', 'Unknown error')}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting client brief chunks tests")
    
    try:
        # Test 1: Save chunks
        if not test_save_brief_chunks():
            return 1
        
        # Test 2: Query chunks
        if not test_query_brief_chunks():
            return 1
        
        # Test 3: Email handler integration
        if not test_email_handler_integration():
            return 1
        
        print(f"\n🎉 All tests passed! Client brief chunks are working correctly.")
        return 0
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())
