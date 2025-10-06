#!/usr/bin/env python3
"""
Vertex AI Uploader - Easy integration helper for existing ingestion workflow

This script can be called from the main vectara workflow to upload client data
to Vertex AI RAG after ingestion is complete.

Usage from main workflow:
    from vertex_ai_rag.vertex_ai_uploader import upload_client_to_vertex_ai
    
    upload_client_to_vertex_ai(
        client_id="mintleads",
        create_corpus=True,  # Create if doesn't exist
        verbose=True
    )

Or standalone:
    python vertex_ai_rag/vertex_ai_uploader.py --client-id mintleads --create-corpus
"""

import sys
import logging
from pathlib import Path
from typing import Optional, Dict, Any

# Add vertex_ai_rag to path
sys.path.insert(0, str(Path(__file__).parent))

from setup_corpus import CorpusSetup
from ingestion.client_ingestion_adapter import ClientIngestionAdapter

logger = logging.getLogger(__name__)


def upload_client_to_vertex_ai(
    client_id: str,
    create_corpus: bool = True,
    input_dir: Optional[str] = None,
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Upload a client's ingested content to Vertex AI RAG
    
    Args:
        client_id: Client identifier
        create_corpus: Whether to create corpus if it doesn't exist
        input_dir: Custom input directory (optional)
        verbose: Enable verbose logging
        
    Returns:
        Dictionary with upload statistics
    """
    if verbose:
        logging.basicConfig(level=logging.INFO)
    
    logger.info(f"🚀 Starting Vertex AI upload for client: {client_id}")
    
    results = {
        'client_id': client_id,
        'corpus_created': False,
        'corpus_name': None,
        'total_files': 0,
        'successful_uploads': 0,
        'failed_uploads': 0
    }
    
    try:
        # Step 1: Initialize adapter with the client_id
        adapter = ClientIngestionAdapter(client_id=client_id, input_dir=input_dir)
        
        # Step 2: Discover files and their metadata
        discovered_files = adapter.discover_files()
        
        # Step 3: Ensure corpus exists
        if create_corpus:
            logger.info(f"📋 Checking corpus for client: {client_id}")
            setup = CorpusSetup()
            
            # Check if corpus already exists
            corpus_display_name = f"client-{client_id}"
            existing_corpus = setup.client.find_corpus_by_display_name(corpus_display_name)
            
            if existing_corpus:
                logger.info(f"✅ Corpus already exists: {corpus_display_name}")
                results['corpus_existed'] = True
            else:
                logger.info(f"🏗️  Creating new corpus: {corpus_display_name}")
                setup.create_client_corpus(client_id)
                results['corpus_created'] = True
                logger.info(f"✅ Corpus created successfully")
        
        # Step 4: Upload files
        logger.info(f"📤 Uploading files for client: {client_id}")
        stats = adapter.run()
        results['upload_stats'] = stats
        
        # Check success
        if stats['failed'] == 0 and stats['successful'] > 0:
            results['success'] = True
            logger.info(f"✅ Upload complete: {stats['successful']}/{stats['total_files']} files uploaded")
        elif stats['failed'] > 0:
            logger.warning(f"⚠️  Partial success: {stats['successful']}/{stats['total_files']} files uploaded, {stats['failed']} failed")
            results['success'] = False
        else:
            logger.warning(f"⚠️  No files uploaded")
            results['success'] = False
        
        return results
        
    except Exception as e:
        error_msg = f"Failed to upload to Vertex AI: {e}"
        logger.error(f"❌ {error_msg}")
        results['error'] = str(e)
        results['success'] = False
        return results


def main():
    """CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Upload client content to Vertex AI RAG'
    )
    
    parser.add_argument(
        '--client-id',
        required=True,
        help='Client identifier'
    )
    
    parser.add_argument(
        '--create-corpus',
        action='store_true',
        help='Create corpus if it doesn\'t exist'
    )
    
    parser.add_argument(
        '--input-dir',
        help='Custom input directory (default: ingestion/client_ingestion_outputs/CLIENT_ID)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    results = upload_client_to_vertex_ai(
        client_id=args.client_id,
        create_corpus=args.create_corpus,
        input_dir=args.input_dir,
        verbose=args.verbose
    )
    
    # Exit with error code if upload failed
    if not results['success']:
        sys.exit(1)
    
    return 0


if __name__ == "__main__":
    exit(main())

