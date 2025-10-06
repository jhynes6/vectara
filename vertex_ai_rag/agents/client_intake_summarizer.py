"""
Agent 3: Client Intake Form Summarizer
Extracts requirements and project details from intake forms
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
from .shared_prompts import CLIENT_INTAKE_FORM_SUMMARIZER_INSTRUCTIONS

load_dotenv()


# Create RAG retrieval tool configured for intake forms
rag_retrieval_tool = VertexAiRagRetrieval(
    name='retrieve_intake_forms',
    description=(
        'Search client intake forms to find project requirements, preferences, timelines, and constraints. '
        'Use this tool to access detailed information from client intake documentation.'
    ),
    rag_resources=[
        rag.RagResource(
            rag_corpus=os.environ.get("RAG_CORPUS_MAIN")
        )
    ],
    similarity_top_k=10,
    vector_distance_threshold=0.3,  # Low threshold for maximum recall
)

# Create the agent
client_intake_summarizer_agent = Agent(
    model='gemini-2.5-pro',
    name='client_intake_summarizer',
    instruction=CLIENT_INTAKE_FORM_SUMMARIZER_INSTRUCTIONS,
    tools=[
        rag_retrieval_tool
    ]
)

# Export for deployment
root_agent = client_intake_summarizer_agent

