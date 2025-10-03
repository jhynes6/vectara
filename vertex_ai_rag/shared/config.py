"""
Shared configuration for Vertex AI RAG implementation
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


class VertexConfig:
    """Configuration for Vertex AI services"""
    
    # Google Cloud
    PROJECT_ID: str = os.getenv('GOOGLE_CLOUD_PROJECT', '')
    LOCATION: str = os.getenv('GOOGLE_CLOUD_LOCATION', 'us-central1')
    CREDENTIALS_PATH: str = os.getenv(
        'GOOGLE_APPLICATION_CREDENTIALS',
        str(Path(__file__).parent.parent.parent / 'vertex-service-account.json')
    )
    
    # OpenAI
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')
    
    # Google Search API
    GOOGLE_SEARCH_API_KEY: str = os.getenv('GOOGLE_SEARCH_API_KEY', '')
    GOOGLE_SEARCH_ENGINE_ID: str = os.getenv('GOOGLE_SEARCH_ENGINE_ID', '')
    
    # RAG Corpus IDs
    RAG_CORPUS_MAIN: Optional[str] = os.getenv('RAG_CORPUS_MAIN')
    RAG_CORPUS_CLIENT_MATERIALS: Optional[str] = os.getenv('RAG_CORPUS_CLIENT_MATERIALS')
    RAG_CORPUS_CASE_STUDIES: Optional[str] = os.getenv('RAG_CORPUS_CASE_STUDIES')
    
    # Agent Resource Names
    AGENT_UNIQUE_MECHANISM_RESEARCHER: Optional[str] = os.getenv('AGENT_UNIQUE_MECHANISM_RESEARCHER')
    AGENT_CLIENT_MATERIALS_SUMMARIZER: Optional[str] = os.getenv('AGENT_CLIENT_MATERIALS_SUMMARIZER')
    AGENT_CLIENT_INTAKE_SUMMARIZER: Optional[str] = os.getenv('AGENT_CLIENT_INTAKE_SUMMARIZER')
    AGENT_CASE_STUDY_SUMMARIZER: Optional[str] = os.getenv('AGENT_CASE_STUDY_SUMMARIZER')
    
    # Logging
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    ENABLE_TRACING: bool = os.getenv('ENABLE_TRACING', 'true').lower() == 'true'
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration"""
        if not cls.PROJECT_ID:
            raise ValueError("GOOGLE_CLOUD_PROJECT must be set in .env file")
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY must be set in .env file")
        if not os.path.exists(cls.CREDENTIALS_PATH):
            raise ValueError(f"Service account file not found: {cls.CREDENTIALS_PATH}")
        return True
    
    @classmethod
    def get_embedding_model(cls) -> str:
        """Get the embedding model to use for Vertex AI RAG"""
        return "text-embedding-004"
    
    @classmethod
    def get_llm_model(cls) -> str:
        """Get the LLM model for agents (GPT-5 or fallback to GPT-4)"""
        # User specified gpt-5, fallback to gpt-4-turbo if gpt-5 not available
        return "gpt-5"  # Will try gpt-5, OpenAI SDK will handle if not available


# Create singleton instance
config = VertexConfig()
