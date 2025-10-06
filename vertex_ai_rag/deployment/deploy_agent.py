#!/usr/bin/env python3
"""
Deploy a single agent to Vertex AI Agent Engine

Usage:
    python deploy_agent.py --agent unique_mechanism_researcher
    python deploy_agent.py --agent client_materials_summarizer
    python deploy_agent.py --agent client_intake_summarizer
    python deploy_agent.py --agent case_study_summarizer
"""

import argparse
import logging
import sys
from pathlib import Path
import vertexai
from vertexai import agent_engines
from vertexai.preview.reasoning_engines import AdkApp
from dotenv import set_key

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from shared import config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


AGENT_MODULES = {
    'unique_mechanism_researcher': 'agents.unique_mechanism_researcher',
    'client_materials_summarizer': 'agents.client_materials_summarizer',
    'client_intake_summarizer': 'agents.client_intake_summarizer',
    'case_study_summarizer': 'agents.case_study_summarizer'
}

AGENT_ENV_VARS = {
    'unique_mechanism_researcher': 'AGENT_UNIQUE_MECHANISM_RESEARCHER',
    'client_materials_summarizer': 'AGENT_CLIENT_MATERIALS_SUMMARIZER',
    'client_intake_summarizer': 'AGENT_CLIENT_INTAKE_SUMMARIZER',
    'case_study_summarizer': 'AGENT_CASE_STUDY_SUMMARIZER'
}


def deploy_agent(agent_name: str) -> str:
    """
    Deploy an agent to Vertex AI Agent Engine
    
    Args:
        agent_name: Name of the agent to deploy
        
    Returns:
        Resource name of deployed agent
    """
    if agent_name not in AGENT_MODULES:
        raise ValueError(f"Unknown agent: {agent_name}. Valid options: {list(AGENT_MODULES.keys())}")
    
    logger.info(f"🚀 Deploying agent: {agent_name}")
    logger.info("=" * 80)
    
    # Validate configuration
    config.validate()
    
    # Initialize Vertex AI with staging bucket
    staging_bucket = f"gs://{config.PROJECT_ID}-staging-bucket"
    logger.info(f"📡 Initializing Vertex AI: {config.PROJECT_ID} ({config.LOCATION})")
    logger.info(f"📦 Staging bucket: {staging_bucket}")
    vertexai.init(
        project=config.PROJECT_ID,
        location=config.LOCATION,
        staging_bucket=staging_bucket
    )
    
    # Import the agent module
    logger.info(f"📦 Loading agent module: {AGENT_MODULES[agent_name]}")
    module_path = AGENT_MODULES[agent_name]
    module = __import__(module_path, fromlist=['root_agent'])
    root_agent = module.root_agent
    
    logger.info(f"🤖 Agent loaded: {root_agent.name}")
    logger.info(f"   Model: {root_agent.model}")
    logger.info(f"   Tools: {len(root_agent.tools)}")
    
    # Prepare environment variables for the agent (CRITICAL!)
    # ONLY include non-empty values - Vertex AI rejects empty strings
    env_vars = {}
    
    if config.RAG_CORPUS_MAIN:
        env_vars['RAG_CORPUS_MAIN'] = config.RAG_CORPUS_MAIN
    if config.RAG_CORPUS_CLIENT_MATERIALS:
        env_vars['RAG_CORPUS_CLIENT_MATERIALS'] = config.RAG_CORPUS_CLIENT_MATERIALS
    if config.RAG_CORPUS_CASE_STUDIES:
        env_vars['RAG_CORPUS_CASE_STUDIES'] = config.RAG_CORPUS_CASE_STUDIES
    if config.OPENAI_API_KEY:
        env_vars['OPENAI_API_KEY'] = config.OPENAI_API_KEY
    if config.GOOGLE_SEARCH_API_KEY:
        env_vars['GOOGLE_SEARCH_API_KEY'] = config.GOOGLE_SEARCH_API_KEY
    if config.GOOGLE_SEARCH_ENGINE_ID:
        env_vars['GOOGLE_SEARCH_ENGINE_ID'] = config.GOOGLE_SEARCH_ENGINE_ID
    
    logger.info("🔧 Environment variables for agent:")
    for key, value in env_vars.items():
        if 'KEY' in key or 'API' in key:
            logger.info(f"   {key}: ***hidden***")
        else:
            logger.info(f"   {key}: {value[:50]}..." if len(value) > 50 else f"   {key}: {value}")
    
    # Create ADK app with env_vars
    logger.info("📦 Creating ADK app with environment variables...")
    app = AdkApp(
        agent=root_agent,
        enable_tracing=config.ENABLE_TRACING,
        env_vars=env_vars,  # ← This was missing!
    )
    
    # Define requirements
    requirements = [
        "google-cloud-aiplatform[adk,agent-engines]==1.108.0",
        "google-adk==1.10.0",
        "python-dotenv",
        "google-auth",
        "google-api-python-client",
        "requests",
        "llama-index",
        "openai>=1.99.3"
    ]
    
    logger.info("☁️  Deploying to Vertex AI Agent Engine...")
    logger.info("   This may take several minutes...")
    
    try:
        remote_app = agent_engines.create(
            app,
            requirements=requirements,
            extra_packages=[
                "./agents",
                "./shared"
            ],
            env_vars=env_vars,  # Pass env_vars to create() as well!
        )
        
        resource_name = remote_app.resource_name
        
        logger.info("=" * 80)
        logger.info("✅ DEPLOYMENT SUCCESSFUL!")
        logger.info(f"📝 Resource name: {resource_name}")
        logger.info("=" * 80)
        
        # Save to .env file
        env_file = Path(__file__).parent.parent / '.env'
        env_var_name = AGENT_ENV_VARS[agent_name]
        set_key(str(env_file), env_var_name, resource_name)
        logger.info(f"💾 Saved {env_var_name} to .env file")
        
        logger.info("\n💡 Next steps:")
        logger.info(f"   1. Test the agent: python deployment/test_agent.py --agent {agent_name}")
        logger.info(f"   2. Query the agent: See deployment/query_agent.py for examples")
        
        return resource_name
        
    except Exception as e:
        logger.error(f"❌ Deployment failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Deploy an agent to Vertex AI Agent Engine',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        '--agent',
        required=True,
        choices=list(AGENT_MODULES.keys()),
        help='Agent to deploy'
    )
    
    args = parser.parse_args()
    
    try:
        resource_name = deploy_agent(args.agent)
        logger.info(f"\n✅ Deployment complete: {resource_name}")
        return 0
    except Exception as e:
        logger.error(f"\n❌ Deployment failed: {e}")
        return 1


if __name__ == "__main__":
    exit(main())

