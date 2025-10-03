"""
Agent 1: Unique Mechanism Researcher
Researches advanced marketing strategies using RAG corpus + web search
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from shared import config

from google.adk.agents import Agent
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag
from dotenv import load_dotenv
from .shared_prompts import UNIQUE_MECHANISM_RESEARCHER_INSTRUCTIONS
from .tools.google_search_tool import create_google_search_function

load_dotenv()


# Create RAG retrieval tool
rag_retrieval_tool = VertexAiRagRetrieval(
    name='retrieve_from_knowledge_base',
    description=(
        'Search the client knowledge base for case studies, documented strategies, and proven mechanisms. '
        'Use this tool to find existing examples and documented approaches from the corpus.'
    ),
    rag_resources=[
        rag.RagResource(
            rag_corpus=os.environ.get("RAG_CORPUS_MAIN")
        )
    ],
    similarity_top_k=10,
    vector_distance_threshold=0.5,
)

# Create Google Search tool
web_search_tool = create_google_search_function()

# Create the agent
unique_mechanism_researcher_agent = Agent(
    model='gpt-5',
    name='unique_mechanism_researcher',
    instruction=UNIQUE_MECHANISM_RESEARCHER_INSTRUCTIONS,
    tools=[
        rag_retrieval_tool,
        web_search_tool
    ],
    # Model parameters from agents.txt
    model_kwargs={
        'reasoning_effort': 'medium',
        'temperature': 0.7
    }
)

# Export for deployment
root_agent = unique_mechanism_researcher_agent
