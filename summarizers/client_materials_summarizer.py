#!/usr/bin/env python3
"""
Client Materials Summarizer Agent - Using Existing Workspace Agent

This script allows you to interact with an existing client-materials-summarizer agent from
your Vectara workspace that generates summaries of client materials based on document IDs.

Usage:
    python client_materials_summarizer.py --doc-id "doc_123.md" --client-id "corpus_123"
    python client_materials_summarizer.py --doc-id "your-doc-id" --query "What are the key services mentioned?"
    python client_materials_summarizer.py --list-agents  # List all available agents
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
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def list_agents(self, filter_pattern: str = None, enabled_only: bool = True, limit: int = 100) -> Dict[str, Any]:
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
        url = f"{self.base_url}/v2/agents/{agent_id}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Failed to get agent {agent_id}: {e}")
    
    def find_agent_by_name(self, name_pattern: str) -> Optional[Dict[str, Any]]:
        try:
            result = self.list_agents(filter_pattern=name_pattern)
            agents = result.get("agents", [])
            return agents[0] if agents else None
        except Exception:
            return None


class ClientMaterialsQueryArgs(BaseModel):
    """Schema for client materials query arguments with doc.id filtering"""
    doc_id: str = Field(
        ..., 
        description="The document ID to query for client materials information. This should be the full document identifier."
    )


class ClientMaterialsSummarizer:
    """Client Materials Summarizer using existing Vectara workspace agent"""
    
    def __init__(self, api_key: str = None, agent_id: str = None, corpus_key: str = None):
        self.api_key = api_key or os.environ.get('VECTARA_API_KEY')
        self.corpus_key = corpus_key or os.environ.get('VECTARA_CORPUS_KEY')
        
        if not self.api_key:
            raise ValueError("Missing Vectara API key.")
        
        self.workspace_client = VectaraWorkspaceClient(self.api_key)
        self.agent_config = None
        self.agent_id = agent_id
        
        self.agent_config = self._load_existing_agent()
        
        if self.corpus_key:
            self.agent = self._create_local_agent_from_config()
        else:
            self.agent = None
    
    def _load_existing_agent(self) -> Dict[str, Any]:
        """Load existing agent configuration from Vectara workspace"""
        try:
            if self.agent_id:
                agent_config = self.workspace_client.get_agent(self.agent_id)
                print(f"✅ Loaded agent: {agent_config.get('name', 'Unknown')} ({self.agent_id})")
            else:
                agent_config = self.workspace_client.find_agent_by_name("client.*materials.*summarizer")
                if not agent_config:
                    raise Exception("No client-materials-summarizer agent found in workspace")
                self.agent_id = agent_config["key"]
                print(f"✅ Found agent: {agent_config.get('name', 'Unknown')} ({self.agent_id})")
            return agent_config
        except Exception as e:
            raise Exception(f"Failed to load existing agent: {e}")
    
    def _create_local_agent_from_config(self) -> Agent:
        """Create a local agent instance based on workspace agent configuration"""
        if not self.agent_config:
            raise ValueError("No agent configuration loaded")
        
        if not self.corpus_key:
            raise ValueError("VECTARA_CORPUS_KEY is required")
        
        vec_factory = VectaraToolFactory(
            vectara_corpus_key=self.corpus_key,
            vectara_api_key=self.api_key
        )
        
        materials_tool = vec_factory.create_rag_tool(
            tool_name="query_client_materials_documents",
            tool_description="Query client material documents by document ID to extract key information about their services, capabilities, and offerings.",
            tool_args_schema=ClientMaterialsQueryArgs,
            tool_args_type={"doc_id": {"type": "doc", "is_list": False, "filter_name": "id"}},
            summary_num_results=25,
            lambda_val=0.005,
            vhc_eligible=True,
            include_citations=True,
            vectara_summarizer="vectara-summary-ext-24-05-med-omni"
        )
        
        model_config = self.agent_config.get("model", {})
        model_name = model_config.get("name", "gpt-4o-mini")
        
        agent_config = AgentConfig(
            main_llm_provider=ModelProvider.OPENAI,
            main_llm_model_name=model_name,
        )
        
        first_step = self.agent_config.get("first_step", {})
        instructions_list = first_step.get("instructions", [])
        
        workspace_instructions = ""
        for instruction in instructions_list:
            if instruction.get("type") == "inline":
                template = instruction.get("template", "")
                if template:
                    workspace_instructions += template + "\n\n"
        
        if not workspace_instructions:
            workspace_instructions = "Summarize the provided client materials, focusing on their core services and capabilities. Be concise and clear."

        agent = Agent(
            tools=[materials_tool],
            topic="Client Materials Analysis",
            custom_instructions=workspace_instructions,
            general_instructions="",
            agent_config=agent_config,
        )
        
        return agent
    
    def generate_client_materials_summary(self, doc_id: str, custom_query: str = None) -> str:
        if not self.agent:
            return "Error: VECTARA_CORPUS_KEY is required to generate summaries."
        
        query = custom_query or "Summarize the key information from this client material."
        enhanced_query = f"{query}\n\nPlease use the query_client_materials_documents tool with doc_id='{doc_id}' to search for this specific document."
        
        print(f"🔍 Querying document: {doc_id}")
        print("🤖 Generating client materials summary...\n")
        
        try:
            response = self.agent.chat(enhanced_query)
            return response.response
        except Exception as e:
            return f"Error generating summary: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="Interact with a client-materials-summarizer agent.")
    
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument("--list-agents", action="store_true", help="List all agents.")
    action_group.add_argument("--doc-id", help="Document ID to summarize.")
    
    parser.add_argument("--client-id", help="Vectara corpus key.")
    parser.add_argument("--api-key", help="Vectara API key.")
    parser.add_argument("--agent-id", help="Specific agent ID to use.")
    parser.add_argument("--query", help="Custom query for the summary.")
    
    args = parser.parse_args()
    
    try:
        if args.list_agents:
            client = VectaraWorkspaceClient(api_key=args.api_key or os.environ.get('VECTARA_API_KEY'))
            agents = client.list_agents()
            print(json.dumps(agents, indent=2))
            return

        if args.doc_id:
            summarizer = ClientMaterialsSummarizer(
                api_key=args.api_key,
                agent_id=args.agent_id,
                corpus_key=args.client_id
            )
            summary = summarizer.generate_client_materials_summary(
                doc_id=args.doc_id,
                custom_query=args.query
            )
            print("=" * 80)
            print("📄 CLIENT MATERIALS SUMMARY")
            print("=" * 80)
            print(f"Document ID: {args.doc_id}")
            if args.query:
                print(f"Custom Query: {args.query}")
            print("=" * 80)
            print(summary)
            print("=" * 80)

    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
