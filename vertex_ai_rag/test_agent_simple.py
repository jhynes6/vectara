#!/usr/bin/env python3
"""Simple agent test based on working RAG example"""

import os
import sys
import asyncio
import vertexai
from vertexai import agent_engines
from google.adk.sessions import VertexAiSessionService
from dotenv import load_dotenv

# Add to path
sys.path.insert(0, os.path.dirname(__file__))
from shared import config

load_dotenv()

async def test_agent():
    # Initialize Vertex AI
    vertexai.init(
        project=config.PROJECT_ID,
        location=config.LOCATION,
    )
    
    # Create session service
    session_service = VertexAiSessionService(
        project=config.PROJECT_ID,
        location=config.LOCATION
    )
    
    # Use client intake summarizer
    AGENT_ID = config.AGENT_CLIENT_INTAKE_SUMMARIZER
    print(f"🤖 Testing Agent: {AGENT_ID}")
    print("=" * 80)
    
    # Create session
    session = await session_service.create_session(
        app_name=AGENT_ID,
        user_id="test-user-123",
    )
    print(f"✅ Session created: {session.id}")
    
    # Get agent
    agent_engine = agent_engines.get(AGENT_ID)
    print(f"✅ Agent connected")
    
    # Test query
    query = "What are the main goals from the mintleads client intake form?"
    print(f"\n📝 Query: {query}")
    print("\n📄 Response:")
    print("-" * 80)
    
    # Stream the response
    for event in agent_engine.stream_query(
        user_id="test-user-123",
        session_id=session.id,
        message=query,
    ):
        print(f"EVENT: {event}")
        
        if "content" in event:
            parts = event["content"].get("parts", [])
            for part in parts:
                if "text" in part:
                    print(part["text"], end='', flush=True)
    
    print("\n" + "-" * 80)
    print("✅ Test complete")

if __name__ == "__main__":
    asyncio.run(test_agent())
