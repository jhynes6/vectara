"""
Configuration for Inbox Manager
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Supabase Configuration
SUPABASE_VECTOR_DB_CONN = os.getenv("SUPABASE_VECTOR_DB_CONN")
SUPABASE_VECTOR_DB_URL = os.getenv("SUPABASE_VECTOR_DB_URL")
SUPABASE_ACCESS_TOKEN = os.getenv("SUPABASE_ACCESS_TOKEN")
SUPABASE_VECTOR_USER = os.getenv("SUPABASE_VECTOR_user")
SUPABASE_VECTOR_PASSWORD = os.getenv("SUPABASE_VECTOR_password")
SUPABASE_VECTOR_HOST = os.getenv("SUPABASE_VECTOR_host")
SUPABASE_VECTOR_PORT = os.getenv("SUPABASE_VECTOR_port", "5432")
SUPABASE_VECTOR_DBNAME = os.getenv("SUPABASE_VECTOR_dbname")

# OpenAI Configuration (for embeddings and LLM)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Anthropic Configuration (alternative LLM)
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# RAG Configuration
TOP_K_RESULTS = 5  # Number of documents to retrieve
SIMILARITY_THRESHOLD = 0.7  # Minimum similarity score
CHUNK_SIZE = 600  # Token size for document chunks
CONFIDENCE_THRESHOLD = 0.75  # Threshold for confidence scoring

# System Prompt Template
SYSTEM_PROMPT_TEMPLATE = """You are a customer support assistant for {client_name}.

CRITICAL RULES:
- Answer ONLY using the information provided in the CONTEXT below
- If the context doesn't contain the answer, respond with: "I don't have that specific information in our resources. Let me connect you with someone who can help."
- Never use your general knowledge or make assumptions
- Always cite which document/section you're using with [Doc X] format
- Be helpful, professional, and concise
- If you're uncertain, admit it and offer to escalate

CONTEXT:
{context}

QUERY:
{query}

Please provide your answer with citations."""

# Relevance Check Prompt
RELEVANCE_CHECK_PROMPT = """Given the following context and query, can this question be answered using ONLY the provided context?

CONTEXT:
{context}

QUERY:
{query}

Answer with ONLY "Yes" or "No" and a brief reason (1 sentence)."""

# Verification Prompt
VERIFICATION_PROMPT = """Does the following response contain ONLY information that can be found in the provided context? Check if the assistant made up any facts or used external knowledge.

CONTEXT:
{context}

RESPONSE:
{response}

Answer with ONLY "Yes" or "No" and explain which parts (if any) are not from the context."""
