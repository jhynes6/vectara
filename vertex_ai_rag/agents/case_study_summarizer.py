"""
Agent 4: Case Study Summarizer
Analyzes case studies to extract structured information
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
from .shared_prompts import CASE_STUDY_SUMMARIZER_INSTRUCTIONS

load_dotenv()


# Create RAG retrieval tool configured for case studies
rag_retrieval_tool = VertexAiRagRetrieval(
    name='retrieve_case_studies',
    description=(
        'Use the instructions provided to summarize the case study.'
    ),
    rag_resources=[
        rag.RagResource(
            rag_corpus=os.environ.get("RAG_CORPUS_CASE_STUDIES") or os.environ.get("RAG_CORPUS_MAIN")
        )
    ],
    similarity_top_k=12,
    vector_distance_threshold=0.4,
)

# Create the agent
case_study_summarizer_agent = Agent(
    model='gemini-2.5-pro',
    name='case_study_summarizer',
    instruction=CASE_STUDY_SUMMARIZER_INSTRUCTIONS,
    tools=[
        rag_retrieval_tool
    ]
)

# Export for deployment
root_agent = case_study_summarizer_agent

