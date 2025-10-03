"""
Agent 2: Client Materials Summarizer
Analyzes client capabilities, brochures, and marketing materials
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
from .shared_prompts import CLIENT_MATERIALS_SUMMARIZER_INSTRUCTIONS

load_dotenv()


# Create RAG retrieval tool configured for client materials
rag_retrieval_tool = VertexAiRagRetrieval(
    name='retrieve_client_materials',
    description=(
        'Search client materials including brochures, capabilities decks, presentations, and marketing collateral. '
        'This corpus contains information about services, capabilities, and differentiators.'
    ),
    rag_resources=[
        rag.RagResource(
            rag_corpus=os.environ.get("RAG_CORPUS_CLIENT_MATERIALS") or os.environ.get("RAG_CORPUS_MAIN")
        )
    ],
    similarity_top_k=15,  # More results for comprehensive extraction
    vector_distance_threshold=0.4,  # Lower threshold for more inclusive results
)

# Create the agent
client_materials_summarizer_agent = Agent(
    model='gpt-5',
    name='client_materials_summarizer',
    instruction=CLIENT_MATERIALS_SUMMARIZER_INSTRUCTIONS,
    tools=[
        rag_retrieval_tool
    ],
    # Model parameters from agents.txt
    model_kwargs={
        'reasoning_effort': 'medium',
        'temperature': 0.3  # Lower temperature for more consistent extraction
    }
)

# Export for deployment
root_agent = client_materials_summarizer_agent
