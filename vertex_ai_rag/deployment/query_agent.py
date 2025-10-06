#!/usr/bin/env python3
"""
Query a deployed Vertex AI agent

Usage:
    python query_agent.py --agent unique_mechanism_researcher --query "What are innovative lead generation strategies?"
    python query_agent.py --agent client_materials_summarizer --query "What services does the client offer?"
    python query_agent.py --agent client_intake_summarizer --query "Summarize the client intake form"
    python query_agent.py --agent case_study_summarizer --query "Summarize the Lawson case study"
"""

import argparse
import logging
import sys
from pathlib import Path
import vertexai
from vertexai import agent_engines
from google.adk.sessions import VertexAiSessionService
import asyncio

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from shared import config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


AGENT_ENV_VARS = {
    'unique_mechanism_researcher': 'AGENT_UNIQUE_MECHANISM_RESEARCHER',
    'client_materials_summarizer': 'AGENT_CLIENT_MATERIALS_SUMMARIZER',
    'client_intake_summarizer': 'AGENT_CLIENT_INTAKE_SUMMARIZER',
    'case_study_summarizer': 'AGENT_CASE_STUDY_SUMMARIZER'
}


async def query_agent_async(agent_name: str, query: str, verbose: bool = False):
    """
    Query a deployed agent using async stream API
    
    Args:
        agent_name: Name of the agent
        query: Query string
        verbose: If True, show detailed output
    """
    if agent_name not in AGENT_ENV_VARS:
        raise ValueError(f"Unknown agent: {agent_name}")
    
    # Get agent resource name from config
    resource_name = getattr(config, AGENT_ENV_VARS[agent_name], None)
    
    if not resource_name:
        raise ValueError(
            f"Agent {agent_name} not deployed. "
            f"Please deploy first: python deployment/deploy_agent.py --agent {agent_name}"
        )
    
    logger.info(f"🤖 Querying agent: {agent_name}")
    logger.info(f"📝 Query: {query}")
    logger.info(f"🔗 Resource: {resource_name}")
    logger.info("=" * 80)
    
    # Initialize Vertex AI
    vertexai.init(
        project=config.PROJECT_ID,
        location=config.LOCATION
    )
    
    # Get the remote agent
    try:
        remote_agent = agent_engines.get(resource_name)
        logger.info("✅ Connected to remote agent")
    except Exception as e:
        logger.error(f"❌ Failed to get agent: {e}")
        raise
    
    # Create session service
    session_service = VertexAiSessionService(
        project=config.PROJECT_ID,
        location=config.LOCATION
    )
    
    # Create a session
    try:
        session = await session_service.create_session(
            app_name=resource_name,
            user_id="user-001"
        )
        logger.info(f"📌 Session created: {session.id}")
    except Exception as e:
        logger.error(f"❌ Failed to create session: {e}")
        raise
    
    # Query the agent using stream_query
    try:
        logger.info("\n🔄 Processing query...")
        logger.info("   (This may take 30-60 seconds depending on query complexity)\n")
        
        logger.info("=" * 80)
        logger.info("📄 AGENT RESPONSE")
        logger.info("=" * 80)
        
        full_response = []
        event_count = 0
        
        # Use stream_query for real-time response
        for event in remote_agent.stream_query(
            user_id="user-001",
            session_id=session.id,
            message=query
        ):
            event_count += 1
            
            # Debug: Show all events
            if verbose:
                logger.info(f"📦 Event #{event_count}: {event}")
            
            # Extract and display text content from various possible formats
            if isinstance(event, dict):
                # Try different event structures
                if "content" in event:
                    parts = event["content"].get("parts", [])
                    for part in parts:
                        if "text" in part:
                            text = part["text"]
                            print(text, end='', flush=True)
                            full_response.append(text)
                
                # Also check for direct text field
                elif "text" in event:
                    text = event["text"]
                    print(text, end='', flush=True)
                    full_response.append(text)
                
                # Check for model response
                elif "model_response" in event:
                    text = str(event["model_response"])
                    print(text, end='', flush=True)
                    full_response.append(text)
        
        print()  # New line after response
        logger.info("=" * 80)
        logger.info(f"📊 Received {event_count} events, extracted {len(full_response)} text parts")
        
        if not full_response:
            logger.warning("⚠️  No text response extracted from events")
            logger.warning("   This might mean:")
            logger.warning("   1. The RAG corpus has no data for this query")
            logger.warning("   2. The agent couldn't find relevant information")
            logger.warning("   3. Use --verbose to see raw events")
        
        return ''.join(full_response) if full_response else "[No response generated]"
        
        logger.info("=" * 80)
        logger.info("📄 AGENT RESPONSE")
        
    except Exception as e:
        logger.error(f"❌ Query failed: {e}")
        logger.error(f"\n💡 Troubleshooting:")
        logger.error(f"   1. Verify agent is deployed: cat .env | grep AGENT_CLIENT_INTAKE")
        logger.error(f"   2. Check permissions: bash deployment/grant_permissions.sh")
        logger.error(f"   3. Verify corpus exists: cat .env | grep RAG_CORPUS")
        raise


async def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Query a deployed Vertex AI agent',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        '--agent',
        required=True,
        choices=list(AGENT_ENV_VARS.keys()),
        help='Agent to query'
    )
    
    parser.add_argument(
        '--query',
        required=True,
        help='Query string'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed response'
    )
    
    args = parser.parse_args()
    
    try:
        config.validate()
        await query_agent_async(args.agent, args.query, args.verbose)
        return 0
    except Exception as e:
        logger.error(f"\n❌ Error: {e}")
        if args.verbose:
            import traceback
            logger.error(traceback.format_exc())
        return 1


if __name__ == "__main__":
    exit(asyncio.run(main()))

