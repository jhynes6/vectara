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


def query_agent(agent_name: str, query: str, verbose: bool = False):
    """
    Query a deployed agent
    
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
    
    # Query the agent
    try:
        logger.info("\n🔄 Processing query...")
        logger.info("   (This may take 30-60 seconds depending on query complexity)\n")
        
        response = remote_agent.query(query)
        
        logger.info("=" * 80)
        logger.info("📄 AGENT RESPONSE")
        logger.info("=" * 80)
        print(response.get('response', 'No response'))
        logger.info("=" * 80)
        
        if verbose:
            logger.info("\n📊 Full Response Object:")
            import json
            print(json.dumps(response, indent=2, default=str))
        
        return response
        
    except Exception as e:
        logger.error(f"❌ Query failed: {e}")
        raise


def main():
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
        query_agent(args.agent, args.query, args.verbose)
        return 0
    except Exception as e:
        logger.error(f"\n❌ Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
