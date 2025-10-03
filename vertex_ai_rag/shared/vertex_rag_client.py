"""
Vertex AI RAG Engine client for corpus and document management
"""
import os
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import vertexai
from vertexai.preview import rag
from vertexai.preview.rag import RagCorpus, RagFile
from google.cloud import storage
from google.api_core import retry
import time

from .config import config

logging.basicConfig(level=getattr(logging, config.LOG_LEVEL))
logger = logging.getLogger(__name__)


class VertexRAGClient:
    """Client for interacting with Vertex AI RAG Engine"""
    
    def __init__(self):
        """Initialize Vertex AI RAG client"""
        # Set credentials
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config.CREDENTIALS_PATH
        
        # Initialize Vertex AI
        vertexai.init(
            project=config.PROJECT_ID,
            location=config.LOCATION
        )
        
        logger.info(f"✅ Initialized Vertex AI RAG client for project: {config.PROJECT_ID}")
    
    def create_corpus(
        self,
        display_name: str,
        description: str = ""
    ) -> RagCorpus:
        """
        Create a new RAG corpus
        
        Args:
            display_name: Human-readable name for the corpus
            description: Description of the corpus purpose
            
        Returns:
            Created RagCorpus object
        """
        logger.info(f"🏗️  Creating RAG corpus: {display_name}")
        
        try:
            # Create corpus with embedding model configuration
            corpus = rag.create_corpus(
                display_name=display_name,
                description=description,
                embedding_model_config=rag.EmbeddingModelConfig(
                    publisher_model=f"publishers/google/models/{config.get_embedding_model()}"
                )
            )
            
            logger.info(f"✅ Created corpus: {corpus.name}")
            logger.info(f"   Display name: {display_name}")
            logger.info(f"   Embedding model: {config.get_embedding_model()}")
            
            return corpus
            
        except Exception as e:
            logger.error(f"❌ Failed to create corpus: {e}")
            raise
    
    def get_corpus(self, corpus_name: str) -> Optional[RagCorpus]:
        """
        Get an existing RAG corpus by name
        
        Args:
            corpus_name: Full resource name of the corpus
            
        Returns:
            RagCorpus object or None if not found
        """
        try:
            corpus = rag.get_corpus(name=corpus_name)
            logger.info(f"✅ Retrieved corpus: {corpus.display_name}")
            return corpus
        except Exception as e:
            logger.warning(f"⚠️  Corpus not found: {corpus_name} - {e}")
            return None
    
    def list_corpora(self) -> List[RagCorpus]:
        """
        List all RAG corpora in the project
        
        Returns:
            List of RagCorpus objects
        """
        try:
            corpora = rag.list_corpora()
            logger.info(f"📚 Found {len(corpora)} corpora")
            return corpora
        except Exception as e:
            logger.error(f"❌ Failed to list corpora: {e}")
            return []
    
    @retry.Retry(predicate=retry.if_exception_type(Exception), maximum=3, initial=2.0)
    def upload_file(
        self,
        corpus_name: str,
        file_path: str,
        display_name: Optional[str] = None,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> RagFile:
        """
        Upload a file to a RAG corpus
        
        Args:
            corpus_name: Full resource name of the corpus
            file_path: Local path to the file
            display_name: Display name for the file in RAG
            description: Description of the file
            metadata: Additional metadata as key-value pairs
            
        Returns:
            RagFile object
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_name = os.path.basename(file_path)
        display_name = display_name or file_name
        
        logger.info(f"⬆️  Uploading file: {file_name} to corpus")
        
        try:
            # Import the file into RAG corpus
            rag_file = rag.import_files(
                corpus_name=corpus_name,
                paths=[file_path],
                chunk_size=512,  # Optimal chunk size for retrieval
                chunk_overlap=100,  # Overlap for context continuity
                max_embedding_requests_per_min=900  # Rate limiting
            )
            
            logger.info(f"✅ Uploaded file: {file_name}")
            logger.info(f"   RAG File name: {rag_file[0].name if rag_file else 'N/A'}")
            
            return rag_file[0] if rag_file else None
            
        except Exception as e:
            logger.error(f"❌ Failed to upload file {file_name}: {e}")
            raise
    
    def upload_files_batch(
        self,
        corpus_name: str,
        file_paths: List[str],
        metadata_list: Optional[List[Dict[str, Any]]] = None
    ) -> List[RagFile]:
        """
        Upload multiple files to a RAG corpus in batch
        
        Args:
            corpus_name: Full resource name of the corpus
            file_paths: List of local file paths
            metadata_list: Optional list of metadata dicts (one per file)
            
        Returns:
            List of RagFile objects
        """
        logger.info(f"⬆️  Uploading {len(file_paths)} files in batch...")
        
        rag_files = []
        for i, file_path in enumerate(file_paths):
            try:
                metadata = metadata_list[i] if metadata_list and i < len(metadata_list) else None
                rag_file = self.upload_file(
                    corpus_name=corpus_name,
                    file_path=file_path,
                    metadata=metadata
                )
                rag_files.append(rag_file)
                
                # Rate limiting: Vertex AI has quota limits
                if (i + 1) % 10 == 0:
                    logger.info(f"   Progress: {i + 1}/{len(file_paths)} files uploaded")
                    time.sleep(1)  # Brief pause to avoid rate limits
                    
            except Exception as e:
                logger.error(f"❌ Failed to upload {file_path}: {e}")
                continue
        
        logger.info(f"✅ Batch upload complete: {len(rag_files)}/{len(file_paths)} successful")
        return rag_files
    
    def delete_file(self, file_name: str) -> bool:
        """
        Delete a file from a RAG corpus
        
        Args:
            file_name: Full resource name of the file
            
        Returns:
            True if successful
        """
        try:
            rag.delete_file(name=file_name)
            logger.info(f"✅ Deleted file: {file_name}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to delete file: {e}")
            return False
    
    def list_files(self, corpus_name: str) -> List[RagFile]:
        """
        List all files in a RAG corpus
        
        Args:
            corpus_name: Full resource name of the corpus
            
        Returns:
            List of RagFile objects
        """
        try:
            files = rag.list_files(corpus_name=corpus_name)
            logger.info(f"📄 Found {len(files)} files in corpus")
            return files
        except Exception as e:
            logger.error(f"❌ Failed to list files: {e}")
            return []
    
    def get_corpus_stats(self, corpus_name: str) -> Dict[str, Any]:
        """
        Get statistics about a RAG corpus
        
        Args:
            corpus_name: Full resource name of the corpus
            
        Returns:
            Dictionary with corpus statistics
        """
        try:
            corpus = self.get_corpus(corpus_name)
            files = self.list_files(corpus_name)
            
            stats = {
                "corpus_name": corpus.name if corpus else "N/A",
                "display_name": corpus.display_name if corpus else "N/A",
                "description": corpus.description if corpus else "N/A",
                "file_count": len(files),
                "embedding_model": config.get_embedding_model()
            }
            
            logger.info(f"📊 Corpus stats: {stats['file_count']} files")
            return stats
            
        except Exception as e:
            logger.error(f"❌ Failed to get corpus stats: {e}")
            return {}
