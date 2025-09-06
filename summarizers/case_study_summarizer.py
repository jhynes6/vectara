#!/usr/bin/env python3
"""
Case Study Summarizer Agent - Using Existing Workspace Agent

This script allows you to interact with an existing case-study-summarizer agent from
your Vectara workspace that generates case study summaries based on document IDs.

Usage:
    python case_study_summarizer.py --doc-id "clients_rapid-pos.md" 
    python case_study_summarizer.py --doc-id "your-doc-id" --query "What are the key achievements?"
    python case_study_summarizer.py --list-agents  # List all available agents
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
            agent_id: The agent ID (e.g., 'agt_case_study_summarizer')
            
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


class CaseStudyQueryArgs(BaseModel):
    """Schema for case study query arguments with doc.id filtering"""
    doc_id: str = Field(
        ..., 
        description="The document ID to query for case study information. This should be the full document identifier."
    )


class CaseStudySummarizer:
    """Case Study Summarizer using existing Vectara workspace agent"""
    
    def __init__(self, api_key: str = None, agent_id: str = None, corpus_key: str = None):
        """
        Initialize the Case Study Summarizer with existing workspace agent
        
        Args:
            api_key: Vectara API key (defaults to VECTARA_API_KEY env var)
            agent_id: Specific agent ID to use (if not provided, searches for case-study-summarizer)
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
        
        # Load the existing agent from workspace
        self.agent_config = self._load_existing_agent()
        
        # Only create local agent if we have corpus key (for actual querying)
        if self.corpus_key:
            # For now, we'll create a local agent with similar configuration
            # In future versions, this could use the Vectara Agent API directly
            self.agent = self._create_local_agent_from_config()
        else:
            self.agent = None
    
    def _load_existing_agent(self) -> Dict[str, Any]:
        """Load existing agent configuration from Vectara workspace"""
        try:
            if self.agent_id:
                # Use specific agent ID
                agent_config = self.workspace_client.get_agent(self.agent_id)
                print(f"✅ Loaded agent: {agent_config.get('name', 'Unknown')} ({self.agent_id})")
            else:
                # Search for case-study-summarizer agent
                agent_config = self.workspace_client.find_agent_by_name("case.*study.*summarizer")
                if not agent_config:
                    agent_config = self.workspace_client.find_agent_by_name("case.study")
                
                if not agent_config:
                    raise Exception("No case-study-summarizer agent found in workspace")
                
                self.agent_id = agent_config["key"]
                print(f"✅ Found agent: {agent_config.get('name', 'Unknown')} ({self.agent_id})")
            
            return agent_config
            
        except Exception as e:
            raise Exception(f"Failed to load existing agent: {e}")
    
    def _create_local_agent_from_config(self) -> Agent:
        """Create a local agent instance based on workspace agent configuration"""
        if not self.agent_config:
            raise ValueError("No agent configuration loaded")
        
        # Use the corpus key from initialization
        if not self.corpus_key:
            raise ValueError("VECTARA_CORPUS_KEY is required (set as environment variable or --corpus-key argument)")
        
        # Create Vectara tool factory
        vec_factory = VectaraToolFactory(
            vectara_corpus_key=self.corpus_key,
            vectara_api_key=self.api_key
        )
        
        # Create RAG tool with doc.id filtering
        case_study_tool = vec_factory.create_rag_tool(
            tool_name="query_case_study_documents",
            tool_description=(
                "Query case study documents by document ID to extract key information, "
                "achievements, challenges, solutions, and outcomes for case study summarization. "
                "Always include document metadata (especially URL) in the response for source attribution."
            ),
            tool_args_schema=CaseStudyQueryArgs,
            tool_args_type={
                "doc_id": {
                    "type": "doc", 
                    "is_list": False, 
                    "filter_name": "id"  # Maps to doc.id in Vectara
                }
            },
            summary_num_results=25,
            lambda_val=0.005,
            vhc_eligible=True,
            include_citations=True,
            vectara_summarizer="vectara-summary-ext-24-05-med-omni"
        )
        
        # Extract model configuration from workspace agent
        model_config = self.agent_config.get("model", {})
        model_name = model_config.get("name", "gpt-4o-mini")
        model_parameters = model_config.get("parameters", {})
        
        print(f"🧠 Using workspace model parameters: {model_parameters}")
        
        # Create agent configuration
        agent_config = AgentConfig(
            main_llm_provider=ModelProvider.OPENAI,
            main_llm_model_name=model_name,
        )
        
        # Extract instructions from workspace agent if available
        first_step = self.agent_config.get("first_step", {})
        instructions_list = first_step.get("instructions", [])
        
        # Use workspace instructions or fallback to default
        workspace_instructions = ""
        for instruction in instructions_list:
            if instruction.get("type") == "inline":
                template = instruction.get("template", "")
                if template:
                    workspace_instructions += template + "\n\n"
        
        if not workspace_instructions:
            workspace_instructions = """
            when asked to summarize case studies, format the response as follows:

            0. CLIENT: the name of the client in the case study
            1. INDUSTRY: the industry category of the CLIENT (rather than the subject of the case) in the case study.
            2. SERVICES: the service(s) that were rendered (bullet point list). Be as specific as possible when defining the service — ex: return "paid ads" instead of "marketing services."
            3. RESULTS: extract and list **all quantitative results** and **all qualitative results** found in the case study. Do not summarize or condense into a smaller set of representative points. Only combine if exact duplicates are present. Completeness takes priority over brevity. If no quantitative or qualitative results are provided, explicitly state: "No quantitative results provided" or "No qualitative results provided."
            4. MECHANISM: the specific mechanism(s) by which the results were achieved. This should answer the question: "How did [service, ex: paid ads] [result, ex: 4x revenue]."
            5. SOURCE: Include the source URL from the document metadata. Look for a "url" field in the document metadata and include it as "Source: [URL]". If no URL is found in the metadata, state "Source: Not available".

            When summarizing a **single case study**, you output this result as a clean, bulleted list. 
            """
        
        # Create a minimal custom prompt template with only workspace instructions
        minimal_prompt_template = """{custom_instructions}"""
        
        # Create the agent with minimal prompting - only workspace instructions
        agent = Agent(
            tools=[case_study_tool],
            topic="",  # Empty topic to avoid "expertise in X" text
            custom_instructions=workspace_instructions,
            general_instructions="",  # Remove all framework default instructions
            agent_config=agent_config,
        )
        
        # Apply workspace model parameters to the underlying agent
        if model_parameters:
            print("🔧 Applying workspace model parameters to underlying agent...")
            try:
                # Force creation of the underlying agent if lazy-loaded
                if hasattr(agent, '_agent') and agent._agent is not None:
                    _ = agent.agent
                
                # Apply model parameters to the underlying LLM
                if hasattr(agent.agent, '_llm') and hasattr(agent.agent._llm, '_model_kwargs'):
                    agent.agent._llm._model_kwargs.update(model_parameters)
                    print(f"✅ Applied model parameters to _llm._model_kwargs: {model_parameters}")
                elif hasattr(agent.agent, 'llm') and hasattr(agent.agent.llm, '_model_kwargs'):
                    agent.agent.llm._model_kwargs.update(model_parameters)
                    print(f"✅ Applied model parameters to llm._model_kwargs: {model_parameters}")
                elif hasattr(agent.agent, '_llm'):
                    # Try to set attributes directly on the LLM
                    llm = agent.agent._llm
                    for key, value in model_parameters.items():
                        if hasattr(llm, key):
                            setattr(llm, key, value)
                            print(f"✅ Set {key} = {value} on LLM")
                        else:
                            print(f"⚠️  LLM doesn't have attribute: {key}")
                else:
                    print("⚠️  Could not find LLM object to apply parameters")
            except Exception as e:
                print(f"⚠️  Warning: Could not apply model parameters: {e}")
        
        # Override the system prompt directly to bypass framework templates
        # Access the underlying agent and replace its system prompt
        print("🔧 Overriding system prompt to use only workspace instructions...")
        try:
            if hasattr(agent, '_agent') and agent._agent is not None:
                # For lazy-loaded agents, force creation first
                _ = agent.agent
            
            if hasattr(agent.agent, 'system_prompt'):
                # Replace with only workspace instructions
                agent.agent.system_prompt = workspace_instructions.strip()
                print("✅ System prompt overridden successfully (system_prompt)")
            elif hasattr(agent.agent, '_system_prompt'):
                agent.agent._system_prompt = workspace_instructions.strip()
                print("✅ System prompt overridden successfully (_system_prompt)")
            else:
                print("⚠️  Could not find system_prompt attribute to override")
        except Exception as e:
            print(f"⚠️  Warning: Could not override system prompt: {e}")
            print("   (Agent will use minimal framework prompts instead)")
        
        # Store model parameters for later application
        self.model_parameters = model_parameters
        
        return agent
    
    def _apply_model_parameters_if_needed(self):
        """Apply model parameters to the underlying LLM if not already done"""
        if not hasattr(self, 'model_parameters') or not self.model_parameters:
            return
        
        if hasattr(self, '_model_params_applied') and self._model_params_applied:
            return  # Already applied
        
        try:
            print("🔧 Applying workspace model parameters to active LLM...")
            # Force agent creation by accessing it
            _ = self.agent.agent
            
            # Try multiple possible LLM locations
            llm = None
            if hasattr(self.agent.agent, '_llm'):
                llm = self.agent.agent._llm
                print(f"✅ Found LLM at agent.agent._llm")
            elif hasattr(self.agent.agent, 'llm'):
                llm = self.agent.agent.llm
                print(f"✅ Found LLM at agent.agent.llm")
            elif hasattr(self.agent.agent, '_query_engine') and hasattr(self.agent.agent._query_engine, '_llm'):
                llm = self.agent.agent._query_engine._llm
                print(f"✅ Found LLM at agent.agent._query_engine._llm")
            
            if llm:
                applied_params = []
                llm_type = type(llm).__name__
                print(f"🔧 Applying parameters to {llm_type}")
                
                # Handle different LLM types
                if 'OpenAI' in llm_type:
                    # Map workspace parameters to valid OpenAI parameters
                    openai_params = {}
                    for key, value in self.model_parameters.items():
                        if key == 'effort':
                            # Map 'effort' to 'reasoning_effort' for OpenAI reasoning models
                            openai_params['reasoning_effort'] = value
                        elif key == 'verbosity':
                            # Skip verbosity as it's not a standard OpenAI parameter
                            print(f"ℹ️  Skipping 'verbosity' parameter (not supported by OpenAI API)")
                            continue
                        else:
                            # Pass through other parameters as-is
                            openai_params[key] = value
                    
                    print(f"🔄 Mapped parameters: {self.model_parameters} → {openai_params}")
                    
                    # For OpenAI LLMs, update additional_kwargs or model_kwargs
                    if openai_params and hasattr(llm, 'additional_kwargs'):
                        if llm.additional_kwargs is None:
                            llm.additional_kwargs = {}
                        llm.additional_kwargs.update(openai_params)
                        applied_params.append(f"additional_kwargs: {openai_params}")
                    
                    if openai_params and hasattr(llm, 'model_kwargs'):
                        if llm.model_kwargs is None:
                            llm.model_kwargs = {}
                        llm.model_kwargs.update(openai_params)
                        applied_params.append(f"model_kwargs: {openai_params}")
                    
                    # Try _model_kwargs as backup
                    if openai_params and hasattr(llm, '_model_kwargs'):
                        if llm._model_kwargs is None:
                            llm._model_kwargs = {}
                        llm._model_kwargs.update(openai_params)
                        applied_params.append(f"_model_kwargs: {openai_params}")
                
                else:
                    # Generic approach for other LLM types
                    if hasattr(llm, '_model_kwargs'):
                        if llm._model_kwargs is None:
                            llm._model_kwargs = {}
                        llm._model_kwargs.update(self.model_parameters)
                        applied_params.append(f"_model_kwargs: {self.model_parameters}")
                
                # Try to set parameters as direct attributes (fallback)
                for key, value in self.model_parameters.items():
                    if hasattr(llm, key):
                        setattr(llm, key, value)
                        applied_params.append(f"{key} = {value}")
                
                if applied_params:
                    print(f"✅ Applied model parameters: {', '.join(applied_params)}")
                    self._model_params_applied = True
                else:
                    print(f"⚠️  Could not apply parameters to LLM type: {type(llm)}")
                    print(f"   Available attributes: {[attr for attr in dir(llm) if 'kwargs' in attr.lower() or 'param' in attr.lower()]}")
            else:
                print("⚠️  Could not find LLM object to apply parameters to")
                
        except Exception as e:
            print(f"⚠️  Error applying model parameters: {e}")
    
    def list_agent_attributes(self) -> Dict[str, Any]:
        """
        List all attributes of the loaded agent configuration
        
        Returns:
            Dict containing all agent attributes and their values
        """
        if not self.agent_config:
            return {"error": "No agent configuration loaded"}
        
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
            "full_config": self.agent_config  # Include complete config for debugging
        }
    
    def print_agent_attributes(self):
        """Print a formatted display of all agent attributes"""
        attributes = self.list_agent_attributes()
        
        print("=" * 80)
        print("🤖 WORKSPACE AGENT ATTRIBUTES")
        print("=" * 80)
        
        if "error" in attributes:
            print(f"❌ {attributes['error']}")
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
        
        print("\n🛠️  TOOL CONFIGURATIONS:")
        tool_configs = attributes.get('tool_configurations', {})
        print(f"  Available Tools: {len(tool_configs)}")
        for i, (tool_id, config) in enumerate(tool_configs.items(), 1):
            print(f"    {i}. Tool ID: {tool_id}")
            print(f"       Type: {config.get('type', 'N/A')}")
            if 'argument_override' in config:
                print(f"       Argument Override: {json.dumps(config['argument_override'], indent=8)}")
        
        print("\n📋 FIRST STEP CONFIGURATION:")
        first_step = attributes.get('first_step', {})
        print(f"  Type: {first_step.get('type', 'N/A')}")
        instructions = first_step.get('instructions', [])
        print(f"  Instructions: {len(instructions)} instruction(s)")
        for i, instruction in enumerate(instructions, 1):
            print(f"    {i}. Type: {instruction.get('type', 'N/A')}")
            if instruction.get('type') == 'reference':
                print(f"       ID: {instruction.get('id', 'N/A')}")
                print(f"       Version: {instruction.get('version', 'N/A')}")
            elif instruction.get('type') == 'inline':
                print(f"       Name: {instruction.get('name', 'N/A')}")
                template = instruction.get('template', '')
                print(f"       Template: {template[:200]}{'...' if len(template) > 200 else ''}")
        
        print("\n🏷️  METADATA:")
        metadata = attributes.get('metadata', {})
        if metadata:
            for key, value in metadata.items():
                print(f"  {key}: {value}")
        else:
            print("  No metadata available")
        
        print("=" * 80)
    
    def generate_case_study_summary(self, doc_id: str, custom_query: str = None) -> str:
        """
        Generate a case study summary for the given document ID
        
        Args:
            doc_id: The document ID to summarize
            custom_query: Optional custom query to focus the summary
            
        Returns:
            Generated case study summary
        """
        if custom_query:
            query = f"{custom_query}"
        else:
            query = (
                "generate the case study summary using your instructions."
            )
        
        if not self.agent:
            return f"Error: VECTARA_CORPUS_KEY is required to generate summaries (set as environment variable or --corpus-key argument). Agent attributes can still be viewed with --show-attributes."
        
        # Create enhanced query that instructs the agent to use the doc_id filter and include metadata
        enhanced_query = f"{query}\n\nPlease use the query_case_study_documents tool with doc_id='{doc_id}' to search for this specific document. Make sure to examine the document metadata for source URL information to include in the SOURCE section of your summary."
        
        print(f"🔍 Querying document: {doc_id}")
        print(f"📝 Enhanced Query: {enhanced_query}")
        print("🤖 Generating case study summary...\n")
        
        try:
            # Enable minimal debug logging (disable noisy database logs)
            import logging
            logging.basicConfig(level=logging.WARNING)  # Only show warnings and errors
            # Specifically disable the noisy aiosqlite logs
            logging.getLogger('aiosqlite').setLevel(logging.WARNING)
            logging.getLogger('asyncio').setLevel(logging.WARNING)
            logging.getLogger('httpcore').setLevel(logging.WARNING)
            
            # Capture the agent's memory and system instructions
            print("\n" + "=" * 80)
            print("🧠 FULL LLM PROMPT DETAILS")
            print("=" * 80)
            
            # Display the agent's system instructions
            print("\n📋 AGENT SYSTEM INSTRUCTIONS:")
            print("-" * 50)
            workspace_instructions = ""
            first_step = self.agent_config.get("first_step", {})
            instructions_list = first_step.get("instructions", [])
            
            for instruction in instructions_list:
                if instruction.get("type") == "inline":
                    template = instruction.get("template", "")
                    if template:
                        workspace_instructions += template + "\n\n"
                        print(template)
            
            # Display the tool descriptions
            print("\n🛠️ TOOL DESCRIPTIONS:")
            print("-" * 50)
            for tool in self.agent.tools:
                print(f"Tool Name: {tool.metadata.name}")
                print(f"Description: {tool.metadata.description}")
                if hasattr(tool.metadata, 'fn_schema') and tool.metadata.fn_schema:
                    try:
                        schema = tool.metadata.fn_schema.model_json_schema()
                        print(f"Parameters: {json.dumps(schema.get('properties', {}), indent=2)}")
                    except:
                        print("Parameters: Unable to display schema")
                print()
            
            # Display the enhanced query being sent
            print("\n💬 USER QUERY:")
            print("-" * 50)
            print(enhanced_query)
            
            print("\n⚡ SENDING TO LLM...")
            print("=" * 80)
            
            # Apply model parameters before first use
            self._apply_model_parameters_if_needed()
            
            # Use the agent to generate the summary with specific doc_id filtering
            response = self.agent.chat(enhanced_query)
            
            # Display what the agent actually did
            print("\n🔍 AGENT EXECUTION TRACE:")
            print("-" * 50)
            if hasattr(response, 'source_nodes') and response.source_nodes:
                print(f"Retrieved {len(response.source_nodes)} source nodes from RAG")
                for i, node in enumerate(response.source_nodes[:3]):  # Show first 3
                    print(f"  {i+1}. Score: {node.score:.3f}, Source: {node.node.metadata}")
            
            if hasattr(response, 'metadata') and response.metadata:
                print(f"Response metadata: {json.dumps(response.metadata, indent=2)}")
                
            return response.response
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    async def generate_case_study_summary_async(self, doc_id: str, custom_query: str = None) -> str:
        """Async version of generate_case_study_summary"""
        if custom_query:
            query = f"{custom_query}"
        else:
            query = (
                "Generate the case study summary using your instructions."
            )
        
        if not self.agent:
            return f"Error: VECTARA_CORPUS_KEY is required to generate summaries (set as environment variable or --corpus-key argument). Agent attributes can still be viewed with --show-attributes."
        
        # Create enhanced query that instructs the agent to use the doc_id filter and include metadata
        enhanced_query = f"{query}\n\nPlease use the query_case_study_documents tool with doc_id='{doc_id}' to search for this specific document. Make sure to examine the document metadata for source URL information to include in the SOURCE section of your summary."
        
        print(f"🔍 Querying document: {doc_id}")
        print(f"📝 Enhanced Query: {enhanced_query}")
        print("🤖 Generating case study summary...\n")
        
        try:
            # Enable minimal debug logging (disable noisy database logs)
            import logging
            logging.basicConfig(level=logging.WARNING)  # Only show warnings and errors
            # Specifically disable the noisy aiosqlite logs
            logging.getLogger('aiosqlite').setLevel(logging.WARNING)
            logging.getLogger('asyncio').setLevel(logging.WARNING)
            logging.getLogger('httpcore').setLevel(logging.WARNING)
            
            # Capture the agent's memory and system instructions
            print("\n" + "=" * 80)
            print("🧠 FULL LLM PROMPT DETAILS (ASYNC)")
            print("=" * 80)
            
            # Display the agent's system instructions
            print("\n📋 AGENT SYSTEM INSTRUCTIONS:")
            print("-" * 50)
            workspace_instructions = ""
            first_step = self.agent_config.get("first_step", {})
            instructions_list = first_step.get("instructions", [])
            
            for instruction in instructions_list:
                if instruction.get("type") == "inline":
                    template = instruction.get("template", "")
                    if template:
                        workspace_instructions += template + "\n\n"
                        print(template)
            
            # Display the tool descriptions
            print("\n🛠️ TOOL DESCRIPTIONS:")
            print("-" * 50)
            for tool in self.agent.tools:
                print(f"Tool Name: {tool.metadata.name}")
                print(f"Description: {tool.metadata.description}")
                if hasattr(tool.metadata, 'fn_schema') and tool.metadata.fn_schema:
                    try:
                        schema = tool.metadata.fn_schema.model_json_schema()
                        print(f"Parameters: {json.dumps(schema.get('properties', {}), indent=2)}")
                    except:
                        print("Parameters: Unable to display schema")
                print()
            
            # Display the enhanced query being sent
            print("\n💬 USER QUERY:")
            print("-" * 50)
            print(enhanced_query)
            
            print("\n⚡ SENDING TO LLM (ASYNC)...")
            print("=" * 80)
            
            # Apply model parameters before first use
            self._apply_model_parameters_if_needed()
            
            # Use the agent to generate the summary with specific doc_id filtering
            response = await self.agent.achat(enhanced_query)
            
            # Display what the agent actually did
            print("\n🔍 AGENT EXECUTION TRACE:")
            print("-" * 50)
            if hasattr(response, 'source_nodes') and response.source_nodes:
                print(f"Retrieved {len(response.source_nodes)} source nodes from RAG")
                for i, node in enumerate(response.source_nodes[:3]):  # Show first 3
                    print(f"  {i+1}. Score: {node.score:.3f}, Source: {node.node.metadata}")
            
            if hasattr(response, 'metadata') and response.metadata:
                print(f"Response metadata: {json.dumps(response.metadata, indent=2)}")
                
            return response.response
        except Exception as e:
            return f"Error generating summary: {str(e)}"


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
        
        # List corpora endpoint
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
            
            # Show available tools
            tool_configs = agent.get('tool_configurations', {})
            if tool_configs:
                tool_types = [config.get('type', 'unknown') for config in tool_configs.values()]
                print(f"   🛠️  Tools: {', '.join(tool_types)}")
            
            # Show instructions
            first_step = agent.get('first_step', {})
            instructions = first_step.get('instructions', [])
            if instructions:
                print(f"   📋 Instructions ({len(instructions)}):")
                for idx, instruction in enumerate(instructions, 1):
                    inst_type = instruction.get('type', 'unknown')
                    inst_name = instruction.get('name', 'Unnamed')
                    print(f"      {idx}. Type: {inst_type}, Name: {inst_name}")
                    
                    if inst_type == 'inline':
                        template = instruction.get('template', '')
                        # Show first 150 characters of template
                        if template:
                            template_preview = template.replace('\n', ' ').strip()[:150]
                            if len(template) > 150:
                                template_preview += "..."
                            print(f"         📄 Template: {template_preview}")
                    elif inst_type == 'reference':
                        ref_id = instruction.get('id', 'N/A')
                        version = instruction.get('version', 'N/A')
                        print(f"         🔗 Reference ID: {ref_id}, Version: {version}")
            else:
                print(f"   📋 Instructions: None")
        
        print("\n" + "=" * 80)
        print("💡 Use --agent-id <ID> to work with a specific agent")
        print("🔍 Use --doc-id <ID> to generate case study summaries")
        
    except Exception as e:
        print(f"❌ Error listing agents: {e}")


def main():
    """Main function for command line interface"""
    parser = argparse.ArgumentParser(
        description="Interact with existing case-study-summarizer agent from Vectara workspace",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --list-agents                                      # List all workspace agents
  %(prog)s --list-corpora                                     # List all document collections 
  %(prog)s --doc-id "clients_rapid-pos.md" --corpus-key "corpus_123"  # Generate case study summary
  %(prog)s --doc-id "project.pdf" --query "What challenges?" # Custom focused summary
  %(prog)s --agent-id "agt_xyz" --show-attributes             # Show agent attributes
  %(prog)s --doc-id "client.md" --async --corpus-key "corpus_123"     # Use async processing
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
        "--doc-id",
        help="Document ID to generate case study summary for (e.g., 'clients_rapid-pos.md')"
    )
    
    # Configuration arguments
    parser.add_argument(
        "--agent-id",
        help="Specific agent ID to use (if not provided, searches for case-study-summarizer)"
    )
    
    parser.add_argument(
        "--show-attributes",
        action="store_true",
        help="Show all attributes of the loaded agent"
    )
    
    parser.add_argument(
        "--query",
        help="Custom query to focus the case study summary"
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
        
        # Check if we need to load an agent (for attributes or doc processing)
        if args.show_attributes or args.doc_id:
            # Create the case study summarizer with existing agent
            print("🔄 Loading existing case-study-summarizer agent from workspace...")
            summarizer = CaseStudySummarizer(
                api_key=args.api_key,
                agent_id=args.agent_id,
                corpus_key=args.corpus_key
            )
            
            # Show agent attributes if requested
            if args.show_attributes:
                summarizer.print_agent_attributes()
                if not args.doc_id:  # Only show attributes if no doc_id provided
                    return
                print("\n")  # Add spacing before summary
        else:
            # No action specified, show help
            parser.print_help()
            return
        
        # Generate the summary
        if args.doc_id:
            if args.use_async:
                summary = asyncio.run(
                    summarizer.generate_case_study_summary_async(
                        doc_id=args.doc_id,
                        custom_query=args.query
                    )
                )
            else:
                summary = summarizer.generate_case_study_summary(
                    doc_id=args.doc_id,
                    custom_query=args.query
                )
            
            print("=" * 80)
            print("📊 CASE STUDY SUMMARY")
            print("=" * 80)
            print(f"Document ID: {args.doc_id}")
            if args.query:
                print(f"Custom Query: {args.query}")
            print("=" * 80)
            print(summary)
            print("=" * 80)
            
            if args.verbose:
                print(f"\n🔍 Metadata Filter Applied: doc.id = '{args.doc_id}'")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
