#!/usr/bin/env python3
"""
Comprehensive Agent Debugging Script
=====================================
Diagnoses why Vertex AI agents aren't responding with events.
"""

import os
import sys
import asyncio
import time
import vertexai
from vertexai import agent_engines
from google.adk.sessions import VertexAiSessionService
from dotenv import load_dotenv
import json

# Add to path
sys.path.insert(0, os.path.dirname(__file__))
from shared import config

load_dotenv()

async def test_agent_comprehensive():
    """Comprehensive agent testing with detailed diagnostics"""
    
    print("🔍 COMPREHENSIVE AGENT DIAGNOSTICS")
    print("=" * 80)
    
    # Step 1: Verify configuration
    print("\n📋 Step 1: Configuration Check")
    print("-" * 80)
    print(f"Project: {config.PROJECT_ID}")
    print(f"Location: {config.LOCATION}")
    print(f"RAG_CORPUS_MAIN: {config.RAG_CORPUS_MAIN}")
    print(f"Service Account: {config.CREDENTIALS_PATH}")
    
    # Step 2: Initialize Vertex AI
    print("\n📡 Step 2: Initialize Vertex AI")
    print("-" * 80)
    vertexai.init(
        project=config.PROJECT_ID,
        location=config.LOCATION,
    )
    print("✅ Vertex AI initialized")
    
    # Step 3: Test with newly deployed agent
    AGENT_ID = config.AGENT_CLIENT_MATERIALS_SUMMARIZER
    print(f"\n🤖 Step 3: Testing Agent")
    print("-" * 80)
    print(f"Agent ID: {AGENT_ID}")
    
    # Step 4: Get agent and check configuration
    print("\n📦 Step 4: Get Agent")
    print("-" * 80)
    try:
        agent = agent_engines.get(AGENT_ID)
        print(f"✅ Agent retrieved")
        print(f"   Display name: {agent.display_name or 'N/A'}")
        
        # Check operation schemas
        schemas = agent.operation_schemas()
        print(f"   Available operations: {len(schemas)}")
        print(f"   Operations: {[s.get('name') for s in schemas[:5]]}")
        
        # Check if stream_query is available
        has_stream_query = any(s.get('name') == 'stream_query' for s in schemas)
        print(f"   Has stream_query: {has_stream_query}")
        
    except Exception as e:
        print(f"❌ Failed to get agent: {e}")
        return
    
    # Step 5: Create session
    print("\n📌 Step 5: Create Session")
    print("-" * 80)
    session_service = VertexAiSessionService(
        project=config.PROJECT_ID,
        location=config.LOCATION
    )
    
    try:
        session = await session_service.create_session(
            app_name=AGENT_ID,
            user_id="debug-user-001"
        )
        print(f"✅ Session created: {session.id}")
    except Exception as e:
        print(f"❌ Session creation failed: {e}")
        return
    
    # Step 6: Send query with detailed event monitoring
    print("\n📨 Step 6: Send Query and Monitor Events")
    print("-" * 80)
    
    test_queries = [
        "Hello, can you hear me?",
        "List the documents you have access to",
        "What is in your knowledge base?"
    ]
    
    for query_num, query in enumerate(test_queries, 1):
        print(f"\n🔍 Query {query_num}: '{query}'")
        print("   Waiting for response...")
        
        event_count = 0
        start_time = time.time()
        timeout = 60  # 60 second timeout
        
        try:
            # Create a list to collect all events
            all_events = []
            
            print("   Streaming events:")
            for event in agent.stream_query(
                user_id="debug-user-001",
                session_id=session.id,
                message=query,
            ):
                event_count += 1
                elapsed = time.time() - start_time
                
                print(f"   📦 Event #{event_count} (at {elapsed:.1f}s)")
                print(f"      Type: {type(event)}")
                print(f"      Keys: {list(event.keys()) if isinstance(event, dict) else 'Not a dict'}")
                print(f"      Content: {json.dumps(event, indent=6, default=str)[:500]}")
                
                all_events.append(event)
                
                # Timeout check
                if elapsed > timeout:
                    print(f"   ⏱️  Timeout reached ({timeout}s)")
                    break
            
            elapsed = time.time() - start_time
            print(f"\n   ✅ Stream complete: {event_count} events in {elapsed:.1f}s")
            
            if event_count == 0:
                print("   ❌ NO EVENTS RECEIVED")
                print("   This indicates:")
                print("      1. Agent is not processing the query")
                print("      2. Agent crashed or errored silently")
                print("      3. Configuration issue preventing execution")
            
            # Try to extract any text
            text_parts = []
            for event in all_events:
                if isinstance(event, dict):
                    if "content" in event:
                        parts = event["content"].get("parts", [])
                        for part in parts:
                            if "text" in part:
                                text_parts.append(part["text"])
            
            if text_parts:
                print(f"\n   📄 Extracted text:")
                print("   " + "".join(text_parts))
            
        except Exception as e:
            print(f"   ❌ Query failed: {e}")
            import traceback
            traceback.print_exc()
        
        # Brief pause between queries
        if query_num < len(test_queries):
            await asyncio.sleep(2)
    
    # Step 7: Check corpus access directly
    print("\n📚 Step 7: Direct RAG Corpus Check")
    print("-" * 80)
    try:
        from vertexai.preview import rag
        
        if config.RAG_CORPUS_MAIN:
            files = list(rag.list_files(corpus_name=config.RAG_CORPUS_MAIN))
            print(f"✅ Corpus accessible: {len(files)} files")
            
            # Try direct RAG query
            if files:
                print("\n   Testing direct RAG query (without agent)...")
                response = rag.retrieval_query(
                    rag_resources=[
                        rag.RagResource(rag_corpus=config.RAG_CORPUS_MAIN)
                    ],
                    text="What services does the client offer?",
                    similarity_top_k=5,
                )
                
                if hasattr(response, 'contexts'):
                    contexts = response.contexts.contexts
                    print(f"   ✅ Direct RAG query works: {len(contexts)} contexts retrieved")
                    if contexts:
                        print(f"   First context: {contexts[0].text[:200]}...")
                else:
                    print(f"   ⚠️  Response: {response}")
        else:
            print("❌ RAG_CORPUS_MAIN not configured")
            
    except Exception as e:
        print(f"❌ Direct RAG query failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 80)
    print("🔍 DIAGNOSTIC COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(test_agent_comprehensive())
