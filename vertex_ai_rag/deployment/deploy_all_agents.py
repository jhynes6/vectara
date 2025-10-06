#!/usr/bin/env python3
"""
Deploy all 4 agents to Vertex AI Agent Engine

This script deploys all agents in sequence:
1. unique_mechanism_researcher
2. client_materials_summarizer
3. client_intake_summarizer
4. case_study_summarizer

Usage:
    python deploy_all_agents.py
    python deploy_all_agents.py --yes  # Auto-confirm (non-interactive)
"""

import argparse
import logging
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from deployment.deploy_agent import deploy_agent, AGENT_MODULES

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def deploy_all(auto_confirm: bool = False) -> dict:
    """
    Deploy all agents
    
    Args:
        auto_confirm: If True, skip confirmation prompts
    
    Returns:
        Dictionary mapping agent names to resource names
    """
    logger.info("🚀 DEPLOYING ALL AGENTS")
    logger.info("=" * 80)
    logger.info("This will deploy 4 agents sequentially:")
    for i, agent_name in enumerate(AGENT_MODULES.keys(), 1):
        logger.info(f"   {i}. {agent_name}")
    logger.info("=" * 80)
    logger.info("\n⚠️  This process will take approximately 15-30 minutes total")
    logger.info("    Each agent deployment takes ~5-10 minutes\n")
    
    # Ask for confirmation unless auto-confirmed
    if not auto_confirm:
        try:
            confirmation = input("Do you want to proceed? [y/N]: ").strip().lower()
            if confirmation not in ['y', 'yes']:
                logger.info("❌ Deployment cancelled by user")
                return {}
        except EOFError:
            logger.info("❌ No input available - use --yes flag for non-interactive mode")
            return {}
    
    deployed_agents = {}
    failed_agents = []
    
    for i, agent_name in enumerate(AGENT_MODULES.keys(), 1):
        logger.info(f"\n{'=' * 80}")
        logger.info(f"DEPLOYING AGENT {i}/4: {agent_name}")
        logger.info("=" * 80)
        
        try:
            resource_name = deploy_agent(agent_name)
            deployed_agents[agent_name] = resource_name
            logger.info(f"✅ Agent {i}/4 deployed successfully")
        except Exception as e:
            logger.error(f"❌ Failed to deploy {agent_name}: {e}")
            failed_agents.append(agent_name)
            
            # Ask if we should continue (unless auto-confirmed)
            if i < len(AGENT_MODULES) and not auto_confirm:
                try:
                    continue_prompt = input("\nContinue with remaining agents? [y/N]: ").strip().lower()
                    if continue_prompt not in ['y', 'yes']:
                        logger.info("❌ Deployment process stopped")
                        break
                except EOFError:
                    logger.info("⚠️  Auto-continuing (non-interactive mode)")
                    continue
    
    # Final summary
    logger.info("\n" + "=" * 80)
    logger.info("DEPLOYMENT SUMMARY")
    logger.info("=" * 80)
    logger.info(f"✅ Successfully deployed: {len(deployed_agents)}/4 agents")
    
    if deployed_agents:
        logger.info("\nDeployed agents:")
        for agent_name, resource_name in deployed_agents.items():
            logger.info(f"   ✅ {agent_name}")
            logger.info(f"      {resource_name}")
    
    if failed_agents:
        logger.info(f"\n❌ Failed deployments: {len(failed_agents)} agents")
        for agent_name in failed_agents:
            logger.info(f"   ❌ {agent_name}")
    
    logger.info("\n💡 Next steps:")
    logger.info("   1. Check your .env file for agent resource names")
    logger.info("   2. Grant RAG corpus permissions: bash deployment/grant_permissions.sh")
    logger.info("   3. Test agents: python deployment/test_all_agents.py")
    
    return deployed_agents


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Deploy all Vertex AI agents')
    parser.add_argument('--yes', '-y', action='store_true',
                       help='Auto-confirm deployment (non-interactive mode)')
    
    args = parser.parse_args()
    
    try:
        deployed = deploy_all(auto_confirm=args.yes)
        
        if len(deployed) == len(AGENT_MODULES):
            logger.info("\n🎉 ALL AGENTS DEPLOYED SUCCESSFULLY!")
            return 0
        else:
            logger.warning(f"\n⚠️  Partial deployment: {len(deployed)}/{len(AGENT_MODULES)} agents")
            return 1
            
    except KeyboardInterrupt:
        logger.info("\n🛑 Deployment interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"\n❌ Deployment failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return 1


if __name__ == "__main__":
    exit(main())

