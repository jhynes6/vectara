"""
Agent: Website Summarizer
Analyzes website content to extract services and target industries
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

load_dotenv()

# Create RAG retrieval tool configured for website content (main corpus)
rag_retrieval_tool = VertexAiRagRetrieval(
    name='retrieve_website_content',
    description=(
        'Search website documents to extract services offered and target industries. '
        'Use this tool to access structured website content grouped by content types '
        '(services_products, industry_markets, blogs_resources, testimonials, homepage).'
    ),
    rag_resources=[
        rag.RagResource(
            rag_corpus=os.environ.get("RAG_CORPUS_MAIN")
        )
    ],
    similarity_top_k=15,
    vector_distance_threshold=0.4,
)

# Create the agent
website_summarizer_agent = Agent(
    model='gemini-2.5-pro',
    name='website_summarizer',
    instruction=(
        'Analyze website documents to extract: 1) services offered and 2) target industries. '
        'Focus your analysis on the provided content types and produce a concise, structured summary.'
    ),
    tools=[
        rag_retrieval_tool
    ]
)

# Export for deployment
root_agent = website_summarizer_agent
