#!/usr/bin/env python3
"""
Setup Vertex AI RAG Corpora

This script creates RAG corpora for individual clients in the knowledge management system.
Each client gets their own corpus, with files tagged by metadata (source, content_type, etc.)

Usage:
    python setup_corpus.py --client-id CLIENT_ID [--list] [--list-clients]
"""

import argparse
import logging
from pathlib import Path
from dotenv import set_key
from shared import config, VertexRAGClient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CorpusSetup:
    """Manages RAG corpus setup"""
    
    def __init__(self):
        """Initialize corpus setup"""
        self.client = VertexRAGClient()
        self.env_file = Path(__file__).parent / '.env'
        self.client_outputs_dir = Path(__file__).parent.parent / 'ingestion' / 'client_ingestion_outputs'
    
    def create_client_corpus(self, client_id: str) -> str:
        """
        Create a corpus for a specific client
        
        Args:
            client_id: The client identifier (e.g., 'd2-creative')
            
        Returns:
            Corpus resource name
        """
        logger.info(f"🏗️  Creating corpus for client: {client_id}")
        
        corpus = self.client.create_corpus(
            display_name=f"client-{client_id}",
            description=f"Knowledge base for client {client_id}: contains website data, capabilities, case studies, and intake forms"
        )
        
        # Save corpus ID to .env using sanitized key name
        env_key = f"RAG_CORPUS_{client_id.upper().replace('-', '_')}"
        self._save_corpus_to_env(env_key, corpus.name)
        
        logger.info(f"✅ Corpus created for {client_id}: {corpus.name}")
        logger.info(f"   Saved as: {env_key}")
        return corpus.name
    
    def get_available_clients(self) -> list[str]:
        """
        Get list of clients from client_ingestion_outputs directory
        
        Returns:
            List of client IDs
        """
        if not self.client_outputs_dir.exists():
            logger.warning(f"⚠️  Client outputs directory not found: {self.client_outputs_dir}")
            return []
        
        clients = [
            d.name for d in self.client_outputs_dir.iterdir() 
            if d.is_dir() and not d.name.startswith('.')
        ]
        return sorted(clients)
    
    def _save_corpus_to_env(self, key: str, value: str):
        """Save corpus ID to .env file"""
        if not self.env_file.exists():
            # Copy template
            template = Path(__file__).parent / '.env.template'
            if template.exists():
                import shutil
                shutil.copy(template, self.env_file)
                logger.info(f"📋 Created .env file from template")
        
        set_key(str(self.env_file), key, value)
        logger.info(f"💾 Saved {key} to .env file")
    
    def list_all_corpora(self):
        """List all existing corpora"""
        logger.info("📚 Listing all RAG corpora...")
        
        corpora = self.client.list_corpora()
        
        if not corpora:
            logger.info("   No corpora found")
            return
        
        logger.info(f"   Found {len(corpora)} corpora:")
        for i, corpus in enumerate(corpora, 1):
            stats = self.client.get_corpus_stats(corpus.name)
            logger.info(f"\n   {i}. {corpus.display_name}")
            logger.info(f"      Resource name: {corpus.name}")
            logger.info(f"      Description: {corpus.description}")
            logger.info(f"      Files: {stats.get('file_count', 0)}")
            logger.info(f"      Embedding model: {stats.get('embedding_model', 'N/A')}")
    
    def list_available_clients(self):
        """List all available clients from client_ingestion_outputs"""
        clients = self.get_available_clients()
        
        if not clients:
            logger.info("📂 No clients found in client_ingestion_outputs/")
            return
        
        logger.info(f"📂 Available clients ({len(clients)}):")
        for client_id in clients:
            client_dir = self.client_outputs_dir / client_id
            file_count = len(list(client_dir.glob('**/*.md')))
            logger.info(f"   • {client_id} ({file_count} markdown files)")
    
    def create_all_client_corpora(self):
        """Create corpora for all available clients"""
        clients = self.get_available_clients()
        
        if not clients:
            logger.error("❌ No clients found in client_ingestion_outputs/")
            return {}
        
        logger.info(f"🚀 Creating corpora for {len(clients)} clients...")
        logger.info("=" * 80)
        
        corpora = {}
        for client_id in clients:
            try:
                corpus_name = self.create_client_corpus(client_id)
                corpora[client_id] = corpus_name
            except Exception as e:
                logger.error(f"❌ Failed to create corpus for {client_id}: {e}")
        
        logger.info("\n" + "=" * 80)
        logger.info("✅ Corpus setup complete!")
        logger.info(f"   Created {len(corpora)} corpora")
        logger.info("\n📋 Corpus Resource Names:")
        for client_id, resource_name in corpora.items():
            logger.info(f"   {client_id}: {resource_name}")
        
        logger.info("\n💡 Next steps:")
        logger.info("   1. Check your .env file for saved corpus IDs")
        logger.info("   2. Run ingestion script to upload documents:")
        logger.info("      python ingestion/client_ingestion_adapter.py --client-id CLIENT_ID")
        logger.info("   3. Deploy agents using the deployment scripts")
        
        return corpora


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Setup Vertex AI RAG Corpora for Clients',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List available clients from client_ingestion_outputs/
  python setup_corpus.py --list-clients
  
  # Create corpus for a specific client
  python setup_corpus.py --client-id d2-creative
  
  # Create corpora for all clients
  python setup_corpus.py --create-all
  
  # List all existing corpora in Vertex AI
  python setup_corpus.py --list
"""
    )
    
    parser.add_argument(
        '--client-id',
        help='Client ID to create corpus for (e.g., d2-creative)'
    )
    
    parser.add_argument(
        '--create-all',
        action='store_true',
        help='Create corpora for all clients in client_ingestion_outputs/'
    )
    
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all existing corpora in Vertex AI'
    )
    
    parser.add_argument(
        '--list-clients',
        action='store_true',
        help='List available clients from client_ingestion_outputs/'
    )
    
    args = parser.parse_args()
    
    # Validate configuration
    try:
        config.validate()
    except ValueError as e:
        logger.error(f"❌ Configuration error: {e}")
        logger.error("💡 Please check your .env file")
        return 1
    
    setup = CorpusSetup()
    
    # Handle list-clients first (doesn't need Vertex AI connection)
    if args.list_clients:
        setup.list_available_clients()
        return 0
    
    # List existing corpora in Vertex AI
    if args.list:
        setup.list_all_corpora()
        return 0
    
    # Create corpora for all clients
    if args.create_all:
        setup.create_all_client_corpora()
        return 0
    
    # Create corpus for specific client
    if args.client_id:
        try:
            setup.create_client_corpus(args.client_id)
            return 0
        except Exception as e:
            logger.error(f"❌ Failed to create corpus: {e}")
            return 1
    
    # No arguments provided, show help
    parser.print_help()
    return 0


if __name__ == "__main__":
    exit(main())

