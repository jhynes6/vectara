#!/usr/bin/env python3
"""
Query Vertex AI Agents using REST API
======================================
Directly uses the REST API endpoints for querying agents.

Usage:
    python query_agent_rest.py --agent client_intake_summarizer --query "Summarize the intake form"
    python query_agent_rest.py --agent client_materials_summarizer --query "What services?"
    python query_agent_rest.py --stream --agent case_study_summarizer --query "Summarize case study"
"""

import argparse
import logging
import sys
import json
from pathlib import Path
import requests
from google.auth.transport.requests import Request
from google.oauth2 import service_account

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


def get_access_token():
    """Get access token from service account"""
    try:
        credentials = service_account.Credentials.from_service_account_file(
            config.CREDENTIALS_PATH,
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
        credentials.refresh(Request())
        return credentials.token
    except Exception as e:
        logger.error(f"Failed to get access token: {e}")
        raise


def query_agent_rest(agent_name: str, query_text: str, stream: bool = False):
    """
    Query agent using REST API
    
    Args:
        agent_name: Name of the agent
        query_text: Query string
        stream: If True, use streaming API
    """
    if agent_name not in AGENT_ENV_VARS:
        raise ValueError(f"Unknown agent: {agent_name}")
    
    # Get agent resource name
    resource_name = getattr(config, AGENT_ENV_VARS[agent_name], None)
    
    if not resource_name:
        raise ValueError(
            f"Agent {agent_name} not deployed. "
            f"Resource name not found in .env: {AGENT_ENV_VARS[agent_name]}"
        )
    
    # Extract engine ID from resource name
    # Format: projects/730752998321/locations/us-east4/reasoningEngines/5830789326933327872
    engine_id = resource_name.split('/')[-1]
    
    logger.info(f"🤖 Querying agent: {agent_name}")
    logger.info(f"📝 Query: {query_text}")
    logger.info(f"🔗 Engine ID: {engine_id}")
    logger.info("=" * 80)
    
    # Get access token
    access_token = get_access_token()
    
    # Build API URL
    base_url = f"https://{config.LOCATION}-aiplatform.googleapis.com/v1/{resource_name}"
    
    # Prepare request headers
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Step 1: Create a session
    create_session_url = f"{base_url}:create_session"
    session_body = {
        'user_id': 'user-001'
    }
    
    logger.info(f"🌐 Creating session...")
    session_response = requests.post(
        create_session_url,
        headers=headers,
        json=session_body
    )
    
    if session_response.status_code != 200:
        logger.error(f"❌ Session creation failed: {session_response.text}")
        return None
    
    session_data = session_response.json()
    session_id = session_data.get('session', {}).get('id', session_data.get('id'))
    logger.info(f"✅ Session created: {session_id}")
    
    # Step 2: Send query to the session
    if stream:
        url = f"{base_url}:stream_query?alt=sse"
        logger.info(f"🌐 Stream Query URL: {url}")
    else:
        # Use the agent's query functionality through sessions
        url = f"{base_url}:query"
        logger.info(f"🌐 Query URL: {url}")
    
    # Build request body for query with session info
    request_body = {
        'user_id': 'user-001',
        'session_id': session_id,
        'message': query_text
    }
    
    logger.info("\n🔄 Sending request...")
    logger.info(f"   Method: POST")
    logger.info(f"   Streaming: {stream}")
    
    try:
        if stream:
            # Streaming request
            response = requests.post(
                url,
                headers=headers,
                json=request_body,
                stream=True
            )
            
            logger.info(f"   Status: {response.status_code}")
            
            if response.status_code != 200:
                logger.error(f"❌ Request failed: {response.text}")
                return None
            
            logger.info("\n" + "=" * 80)
            logger.info("📄 AGENT RESPONSE (Streaming)")
            logger.info("=" * 80)
            
            # Process Server-Sent Events
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data: '):
                        data_str = line_str[6:]  # Remove 'data: ' prefix
                        try:
                            data = json.loads(data_str)
                            # Extract text from response
                            if 'candidates' in data:
                                for candidate in data['candidates']:
                                    if 'content' in candidate:
                                        parts = candidate['content'].get('parts', [])
                                        for part in parts:
                                            if 'text' in part:
                                                print(part['text'], end='', flush=True)
                        except json.JSONDecodeError:
                            pass
            
            print()  # New line
            logger.info("=" * 80)
            
        else:
            # Non-streaming request
            response = requests.post(
                url,
                headers=headers,
                json=request_body
            )
            
            logger.info(f"   Status: {response.status_code}")
            
            if response.status_code != 200:
                logger.error(f"❌ Request failed: {response.text}")
                return None
            
            result = response.json()
            
            logger.info("\n" + "=" * 80)
            logger.info("📄 AGENT RESPONSE")
            logger.info("=" * 80)
            
            # Extract response text
            if 'output' in result:
                print(result['output'])
            elif 'response' in result:
                print(result['response'])
            else:
                print(json.dumps(result, indent=2))
            
            logger.info("=" * 80)
            
            return result
            
    except Exception as e:
        logger.error(f"❌ Query failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise


def main():
    parser = argparse.ArgumentParser(
        description='Query Vertex AI agents using REST API',
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
        '--stream',
        action='store_true',
        help='Use streaming API'
    )
    
    args = parser.parse_args()
    
    try:
        config.validate()
        query_agent_rest(args.agent, args.query, args.stream)
        return 0
    except Exception as e:
        logger.error(f"\n❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
