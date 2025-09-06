#!/usr/bin/env python3
"""
Website Summarizer Agent - Custom Website Content Analysis

This script analyzes website content to extract services and target industries.
It queries files where source = 'website' and content_type != 'case_studies'.

Usage:
    python website_summarizer.py --summarize
    python website_summarizer.py --query "What services are offered?"
    python website_summarizer.py --list-agents  # List all available agents
"""

import argparse
import asyncio
import os
import sys
import json
import requests
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional

# Add the vectara-agentic directory to the Python path
vectara_agentic_path = Path(__file__).parent.parent / "vectara-documentation" / "vectara-agentic"
sys.path.insert(0, str(vectara_agentic_path))

try:
    from vectara_agentic import Agent, AgentConfig, ModelProvider
    from vectara_agentic.tools import VectaraToolFactory
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Please ensure you have the vectara-agentic library installed and configured.")
    sys.exit(1)

# Load environment variables
load_dotenv(override=True)


class VectaraWorkspaceClient:
    """Client for interacting with Vectara workspace agents via API"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.vectara.io"):
        """
        Initialize the Vectara workspace client
        
        Args:
            api_key: Vectara API key
            base_url: Vectara API base URL
        """
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def list_agents(self, filter_pattern: str = None, enabled_only: bool = True, limit: int = 100) -> Dict[str, Any]:
        """
        List all agents in the workspace
        
        Args:
            filter_pattern: Optional regex pattern to filter agents by name/description
            enabled_only: Only return enabled agents
            limit: Maximum number of agents to return
            
        Returns:
            Dict containing agents list and metadata
        """
        url = f"{self.base_url}/v2/agents"
        params = {"limit": limit}
        
        if filter_pattern:
            params["filter"] = filter_pattern
        if enabled_only:
            params["enabled"] = "true"
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Failed to list agents: {e}")
    
    def get_agent(self, agent_id: str) -> Dict[str, Any]:
        """
        Get detailed configuration for a specific agent
        
        Args:
            agent_id: The agent ID
            
        Returns:
            Dict containing complete agent configuration
        """
        url = f"{self.base_url}/v2/agents/{agent_id}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Failed to get agent {agent_id}: {e}")
    
    def find_agent_by_name(self, name_pattern: str) -> Optional[Dict[str, Any]]:
        """
        Find an agent by name pattern
        
        Args:
            name_pattern: Pattern to match against agent names
            
        Returns:
            First matching agent or None
        """
        try:
            result = self.list_agents(filter_pattern=name_pattern)
            agents = result.get("agents", [])
            return agents[0] if agents else None
        except Exception:
            return None


class WebsiteQueryArgs(BaseModel):
    """Schema for website query arguments with content type filtering"""
    content_type_filter: str = Field(
        default="homepage", 
        description="The doc.content_type value to filter for specific website content types."
    )


class WebsiteSummarizer:
    """Website Summarizer for extracting services and target industries"""
    
    def __init__(self, api_key: str = None, agent_id: str = None, corpus_key: str = None):
        """
        Initialize the Website Summarizer
        
        Args:
            api_key: Vectara API key (defaults to VECTARA_API_KEY env var)
            agent_id: Specific agent ID to use (optional, will create custom agent if not provided)
            corpus_key: Vectara corpus key (defaults to VECTARA_CORPUS_KEY env var)
        """
        self.api_key = api_key or os.environ.get('VECTARA_API_KEY')
        self.corpus_key = corpus_key or os.environ.get('VECTARA_CORPUS_KEY')
        
        if not self.api_key:
            raise ValueError(
                "Missing Vectara API key. Please set VECTARA_API_KEY environment variable or pass as argument."
            )
        
        self.workspace_client = VectaraWorkspaceClient(self.api_key)
        self.agent_config = None
        self.agent_id = agent_id
        
        # Load existing agent if specified, otherwise create custom agent
        if self.agent_id:
            self.agent_config = self._load_existing_agent()
        
        # Create local agent for querying
        if self.corpus_key:
            self.agent = self._create_local_agent_from_config()
        else:
            self.agent = None
    
    def _load_existing_agent(self) -> Dict[str, Any]:
        """Load existing agent configuration from Vectara workspace"""
        try:
            # Use specific agent ID
            agent_config = self.workspace_client.get_agent(self.agent_id)
            print(f"✅ Loaded agent: {agent_config.get('name', 'Unknown')} ({self.agent_id})")
            return agent_config
            
        except Exception as e:
            raise Exception(f"Failed to load existing agent: {e}")
    
    def _create_local_agent_from_config(self) -> Agent:
        """Create a local agent instance for website content analysis"""
        
        # Use the corpus key from initialization
        if not self.corpus_key:
            raise ValueError("VECTARA_CORPUS_KEY is required (set as environment variable or --corpus-key argument)")
        
        # Create Vectara tool factory
        vec_factory = VectaraToolFactory(
            vectara_corpus_key=self.corpus_key,
            vectara_api_key=self.api_key
        )
        
        # Create RAG tool with content type filtering
        website_tool = vec_factory.create_rag_tool(
            tool_name="query_website_documents",
            tool_description=(
                "Query website documents by content type to extract services and target industries. "
                "Filters for specific doc.content_type values like homepage, services_products, etc."
            ),
            tool_args_schema=WebsiteQueryArgs,
            tool_args_type={
                "content_type_filter": {
                    "type": "doc", 
                    "is_list": False, 
                    "filter_name": "content_type"  # Maps to doc.content_type in Vectara
                }
            },
            summary_num_results=25,  # Results per content type
            lambda_val=0.005,
            vhc_eligible=True,
            include_citations=True,
            vectara_summarizer="vectara-summary-ext-24-05-med-omni"
        )
        
        # Extract model configuration from workspace agent or use default
        if self.agent_config:
            model_config = self.agent_config.get("model", {})
            model_name = model_config.get("name", "gpt-4o-mini")
        else:
            model_name = "gpt-4o-mini"
        
        # Create agent configuration
        agent_config = AgentConfig(
            main_llm_provider=ModelProvider.OPENAI,
            main_llm_model_name=model_name,
        )
        
        # Extract instructions from workspace agent if available, or use custom instructions
        workspace_instructions = ""
        if self.agent_config:
            first_step = self.agent_config.get("first_step", {})
            instructions_list = first_step.get("instructions", [])
            
            for instruction in instructions_list:
                if instruction.get("type") == "inline":
                    template = instruction.get("template", "")
                    if template:
                        workspace_instructions += template + "\n\n"
        
        # Use custom instructions for website analysis
        if not workspace_instructions:
            workspace_instructions = """
            When asked to analyze website content by content type, provide a focused analysis in the following format:

            ## SERVICES OFFERED
            Based on this specific content type, list all services mentioned:
            - List each service name clearly
            - Include any sub-services or specializations
            - Note unique approaches or methodologies
            - Be comprehensive and specific to this content type

            ## TARGET INDUSTRIES  
            Based on this specific content type, list all target industries mentioned:
            - Industries explicitly mentioned as target markets
            - Industries implied by context or descriptions
            - Vertical markets or specialized sectors
            - Geographic focus or market segments
            - Be comprehensive and specific to this content type

            ## CONTENT TYPE NOTES
            - Focus specifically on the content type being analyzed
            - Extract ALL services and industries mentioned in this content type
            - Be thorough and complete for this specific content section
            - If no services or industries are mentioned, state "None found in this content type"

            Provide a clean, focused analysis for the specific content type being queried.
            """
        
        # Create the agent with custom instructions
        agent = Agent(
            tools=[website_tool],
            topic="Website Content Analysis",
            custom_instructions=workspace_instructions,
            general_instructions="",  # Remove framework default instructions
            agent_config=agent_config,
        )
        
        # Override the system prompt if no workspace agent was used
        if not self.agent_config:
            print("🔧 Using custom instructions for website analysis...")
            try:
                if hasattr(agent, '_agent') and agent._agent is not None:
                    # For lazy-loaded agents, force creation first
                    _ = agent.agent
                
                if hasattr(agent.agent, 'system_prompt'):
                    agent.agent.system_prompt = workspace_instructions.strip()
                    print("✅ Custom system prompt applied successfully")
                elif hasattr(agent.agent, '_system_prompt'):
                    agent.agent._system_prompt = workspace_instructions.strip()
                    print("✅ Custom system prompt applied successfully")
            except Exception as e:
                print(f"⚠️  Warning: Could not override system prompt: {e}")
        
        return agent
    
    def list_agent_attributes(self) -> Dict[str, Any]:
        """
        List all attributes of the loaded agent configuration
        
        Returns:
            Dict containing all agent attributes and their values
        """
        if not self.agent_config:
            return {"message": "Using custom agent configuration for website analysis"}
        
        return {
            "agent_key": self.agent_id,
            "name": self.agent_config.get("name"),
            "description": self.agent_config.get("description"),
            "enabled": self.agent_config.get("enabled"),
            "created_at": self.agent_config.get("created_at"),
            "updated_at": self.agent_config.get("updated_at"),
            "model": self.agent_config.get("model", {}),
            "tool_configurations": self.agent_config.get("tool_configurations", {}),
            "first_step": self.agent_config.get("first_step", {}),
            "metadata": self.agent_config.get("metadata", {}),
        }
    
    def print_agent_attributes(self):
        """Print a formatted display of all agent attributes"""
        attributes = self.list_agent_attributes()
        
        print("=" * 80)
        print("🤖 AGENT CONFIGURATION")
        print("=" * 80)
        
        if "message" in attributes:
            print(f"📝 {attributes['message']}")
            print("🎯 Custom configuration for comprehensive website analysis")
            print("🔍 Method: Sequential analysis of 5 content types")
            print("📋 Output: Compiled services offered + Target industries")
            print("=" * 80)
            return
        
        print(f"🆔 Agent Key: {attributes.get('agent_key', 'N/A')}")
        print(f"📛 Name: {attributes.get('name', 'N/A')}")
        print(f"📝 Description: {attributes.get('description', 'N/A')}")
        print(f"✅ Enabled: {attributes.get('enabled', 'N/A')}")
        print(f"📅 Created: {attributes.get('created_at', 'N/A')}")
        print(f"🔄 Updated: {attributes.get('updated_at', 'N/A')}")
        
        print("\n🧠 MODEL CONFIGURATION:")
        model = attributes.get('model', {})
        print(f"  Model Name: {model.get('name', 'N/A')}")
        print(f"  Parameters: {json.dumps(model.get('parameters', {}), indent=4)}")
        
        print("=" * 80)
    
    def analyze_content_type(self, content_type: str, custom_query: str = None) -> str:
        """
        Analyze a specific content type for services and target industries
        
        Args:
            content_type: The content type to analyze (e.g., 'homepage', 'services_products')
            custom_query: Optional custom query to focus the analysis
            
        Returns:
            Generated analysis for the specific content type
        """
        if custom_query:
            query = f"{custom_query}"
        else:
            query = (
                f"Analyze the {content_type} content to extract services offered "
                "and target industries mentioned. Use your analysis format."
            )
        
        if not self.agent:
            return f"Error: VECTARA_CORPUS_KEY is required to generate analysis."
        
        # Create enhanced query for specific content type
        enhanced_query = f"{query}\n\nPlease use the query_website_documents tool with content_type_filter='{content_type}' to search for this specific content type."
        
        print(f"🔍 Analyzing content_type = '{content_type}'")
        
        try:
            # Enable minimal debug logging
            import logging
            logging.basicConfig(level=logging.WARNING)
            logging.getLogger('aiosqlite').setLevel(logging.WARNING)
            logging.getLogger('asyncio').setLevel(logging.WARNING)
            logging.getLogger('httpcore').setLevel(logging.WARNING)
            
            response = self.agent.chat(enhanced_query)
                
            return response.response
        except Exception as e:
            return f"Error analyzing {content_type}: {str(e)}"

    def generate_comprehensive_website_analysis(self, custom_query: str = None) -> str:
        """
        Generate a comprehensive website analysis by querying 5 different content types
        and compiling the results into master lists
        
        Args:
            custom_query: Optional custom query to focus the analysis
            
        Returns:
            Comprehensive compiled analysis across all content types
        """
        if not self.agent:
            return f"Error: VECTARA_CORPUS_KEY is required to generate analysis (set as environment variable or --corpus-key argument)."
        
        # Define the 5 content types to analyze
        content_types = [
            "services_products",
            "industry_markets", 
            "blogs_resources",
            "testimonials",
            "homepage"
        ]
        
        # Initialize master lists
        all_services = set()
        all_industries = set()
        
        print("🔍 Analyzing website content across 5 different content types...")
        print("=" * 80)
        
        # Analyze each content type
        for i, content_type in enumerate(content_types, 1):
            print(f"\n📋 [{i}/5] Analyzing content_type = '{content_type}'")
            print("-" * 60)
            
            analysis = self.analyze_content_type(content_type, custom_query)
            
            # Extract services and industries from the analysis
            services_from_content, industries_from_content = self._extract_lists_from_analysis(analysis)
            
            # Add to master lists
            all_services.update(services_from_content)
            all_industries.update(industries_from_content)
            
            # Show what was found for this content type
            print(f"✅ Found {len(services_from_content)} services, {len(industries_from_content)} industries")
            if services_from_content:
                print(f"   Services: {', '.join(list(services_from_content)[:3])}{'...' if len(services_from_content) > 3 else ''}")
            if industries_from_content:
                print(f"   Industries: {', '.join(list(industries_from_content)[:3])}{'...' if len(industries_from_content) > 3 else ''}")
        
        # Compile final comprehensive analysis
        print("\n" + "=" * 80)
        print("📊 COMPILING COMPREHENSIVE ANALYSIS")
        print("=" * 80)
        
        final_analysis = self._compile_final_analysis(all_services, all_industries, content_types)
        
        return final_analysis
    
    def _extract_lists_from_analysis(self, analysis: str) -> tuple:
        """
        Extract services and industries lists from analysis text
        
        Args:
            analysis: The analysis text from the agent
            
        Returns:
            Tuple of (services_set, industries_set)
        """
        services = set()
        industries = set()
        
        lines = analysis.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            # Detect sections
            if '## SERVICES OFFERED' in line:
                current_section = 'services'
                continue
            elif '## TARGET INDUSTRIES' in line:
                current_section = 'industries'
                continue
            elif line.startswith('## '):
                current_section = None
                continue
            
            # Extract items from lists
            if current_section and line.startswith('-'):
                # Remove bullet point and clean up
                item = line[1:].strip()
                if item.startswith('**') and item.endswith('**'):
                    item = item[2:-2]  # Remove bold formatting
                
                # Remove additional descriptions after parentheses or colons
                if '(' in item:
                    item = item.split('(')[0].strip()
                if ':' in item:
                    item = item.split(':')[0].strip()
                
                # Skip empty items or notes
                if item and not item.lower().startswith(('none', 'no ', 'not ')):
                    if current_section == 'services':
                        services.add(item)
                    elif current_section == 'industries':
                        industries.add(item)
        
        return services, industries
    
    def _compile_final_analysis(self, all_services: set, all_industries: set, content_types: list) -> str:
        """
        Compile the final comprehensive analysis from all content types
        
        Args:
            all_services: Set of all unique services found
            all_industries: Set of all unique industries found
            content_types: List of content types analyzed
            
        Returns:
            Formatted final analysis
        """
        analysis = f"""
## COMPREHENSIVE SERVICES ANALYSIS
**Total Unique Services Found: {len(all_services)}**

"""
        
        # Sort services alphabetically for better presentation
        sorted_services = sorted(list(all_services))
        for i, service in enumerate(sorted_services, 1):
            analysis += f"{i:2d}. {service}\n"
        
        analysis += f"""
## COMPREHENSIVE TARGET INDUSTRIES ANALYSIS  
**Total Unique Industries Found: {len(all_industries)}**

"""
        
        # Sort industries alphabetically
        sorted_industries = sorted(list(all_industries))
        for i, industry in enumerate(sorted_industries, 1):
            analysis += f"{i:2d}. {industry}\n"
        
        analysis += f"""
## ANALYSIS METHODOLOGY
- **Content Types Analyzed:** {len(content_types)}
  - {', '.join(content_types)}
- **Total Services Extracted:** {len(all_services)} unique services
- **Total Industries Extracted:** {len(all_industries)} unique industries
- **Approach:** Sequential analysis of each content type with deduplication

## COVERAGE NOTES
- This analysis covers all major website content types
- Services and industries are deduplicated across content types
- Each content type contributed unique insights to the comprehensive lists
- Results represent the full scope of services offered and markets targeted
        """
        
        return analysis.strip()
    


def list_workspace_corpora(api_key: str = None):
    """List all corpora in the Vectara workspace"""
    api_key = api_key or os.environ.get('VECTARA_API_KEY')
    if not api_key:
        print("❌ Missing VECTARA_API_KEY environment variable")
        return
    
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        url = "https://api.vectara.io/v2/corpora"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        corpora = result.get("corpora", [])
        
        print("=" * 80)
        print("📚 VECTARA CORPORA (Document Collections)")
        print("=" * 80)
        print(f"Found {len(corpora)} corpus/corpora")
        print("=" * 80)
        
        for i, corpus in enumerate(corpora, 1):
            print(f"\n{i}. 📖 {corpus.get('name', 'Unnamed Corpus')}")
            print(f"   🆔 Key: {corpus.get('key', 'N/A')}")
            print(f"   📝 Description: {corpus.get('description', 'No description')[:100]}{'...' if len(corpus.get('description', '')) > 100 else ''}")
            print(f"   ✅ Enabled: {corpus.get('enabled', 'N/A')}")
            print(f"   📅 Created: {corpus.get('created_at', 'N/A')}")
        
        print("\n" + "=" * 80)
        print("💡 Copy the 'Key' value and set it as VECTARA_CORPUS_KEY")
        print("💡 Example: export VECTARA_CORPUS_KEY=\"your_corpus_key_here\"")
        
    except Exception as e:
        print(f"❌ Error listing corpora: {e}")


def list_workspace_agents(api_key: str = None):
    """List all agents in the Vectara workspace"""
    api_key = api_key or os.environ.get('VECTARA_API_KEY')
    if not api_key:
        print("❌ Missing VECTARA_API_KEY environment variable")
        return
    
    try:
        client = VectaraWorkspaceClient(api_key)
        result = client.list_agents()
        agents = result.get("agents", [])
        
        print("=" * 80)
        print("🏢 VECTARA WORKSPACE AGENTS")
        print("=" * 80)
        print(f"Found {len(agents)} agent(s)")
        print("=" * 80)
        
        for i, agent in enumerate(agents, 1):
            print(f"\n{i}. 🤖 {agent.get('name', 'Unnamed Agent')}")
            print(f"   🆔 ID: {agent.get('key', 'N/A')}")
            print(f"   📝 Description: {agent.get('description', 'No description')[:100]}{'...' if len(agent.get('description', '')) > 100 else ''}")
            print(f"   ✅ Enabled: {agent.get('enabled', 'N/A')}")
            print(f"   📅 Created: {agent.get('created_at', 'N/A')}")
            print(f"   🔄 Updated: {agent.get('updated_at', 'N/A')}")
        
        print("\n" + "=" * 80)
        print("💡 Use --agent-id <ID> to work with a specific agent")
        print("🔍 Use --summarize to generate website analysis")
        
    except Exception as e:
        print(f"❌ Error listing agents: {e}")


def main():
    """Main function for command line interface"""
    parser = argparse.ArgumentParser(
        description="Website content analyzer for extracting services and target industries",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --list-agents                                          # List all workspace agents
  %(prog)s --list-corpora                                         # List all document collections 
  %(prog)s --summarize --corpus-key "corpus_123"                  # Analyze website content
  %(prog)s --query "What services are mentioned?" --corpus-key "corpus_123"  # Custom analysis
  %(prog)s --agent-id "agt_xyz" --show-attributes                 # Show agent attributes
  %(prog)s --summarize --async --corpus-key "corpus_123"          # Use async processing
        """
    )
    
    # Action arguments (mutually exclusive)
    action_group = parser.add_mutually_exclusive_group(required=False)
    action_group.add_argument(
        "--list-agents",
        action="store_true",
        help="List all agents in the Vectara workspace"
    )
    action_group.add_argument(
        "--list-corpora",
        action="store_true",
        help="List all corpora (document collections) in the Vectara workspace"
    )
    action_group.add_argument(
        "--summarize",
        action="store_true",
        help="Analyze website content across 5 content types: services_products, industry_markets, blogs_resources, testimonials, homepage"
    )
    
    # Configuration arguments
    parser.add_argument(
        "--agent-id",
        help="Specific agent ID to use (optional, will create custom agent if not provided)"
    )
    
    parser.add_argument(
        "--show-attributes",
        action="store_true",
        help="Show all attributes of the agent configuration"
    )
    
    parser.add_argument(
        "--query",
        help="Custom query to focus the website analysis"
    )
    
    parser.add_argument(
        "--api-key",
        help="Vectara API key (defaults to VECTARA_API_KEY env var)"
    )
    
    parser.add_argument(
        "--corpus-key",
        help="Vectara corpus key (defaults to VECTARA_CORPUS_KEY env var)"
    )
    
    parser.add_argument(
        "--async",
        dest="use_async",
        action="store_true",
        help="Use async processing"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    try:
        # Handle list agents request
        if args.list_agents:
            list_workspace_agents(args.api_key)
            return
        
        # Handle list corpora request
        if args.list_corpora:
            list_workspace_corpora(args.api_key)
            return
        
        # Check if we need to load an agent (for attributes or analysis)
        if args.show_attributes or args.summarize or args.query:
            # Create the website summarizer
            print("🔄 Initializing website content analyzer...")
            summarizer = WebsiteSummarizer(
                api_key=args.api_key,
                agent_id=args.agent_id,
                corpus_key=args.corpus_key
            )
            
            # Show agent attributes if requested
            if args.show_attributes:
                summarizer.print_agent_attributes()
                if not args.summarize and not args.query:  # Only show attributes if no analysis requested
                    return
                print("\n")  # Add spacing before analysis
        else:
            # No action specified, show help
            parser.print_help()
            return
        
        # Generate the analysis
        if args.summarize or args.query:
            print("🚀 Starting comprehensive website analysis across 5 content types...")
            analysis = summarizer.generate_comprehensive_website_analysis(
                custom_query=args.query
            )
            
            print("\n" + "=" * 80)
            print("🌐 COMPREHENSIVE WEBSITE CONTENT ANALYSIS")
            print("=" * 80)
            print("Method: Sequential analysis of 5 content types")
            if args.query:
                print(f"Custom Query: {args.query}")
            print("=" * 80)
            print(analysis)
            print("=" * 80)
            
            if args.verbose:
                print(f"\n🔍 Content Types Analyzed: services_products, industry_markets, blogs_resources, testimonials, homepage")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
