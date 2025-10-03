#!/usr/bin/env python3
"""
Setup Vertex AI RAG Corpora

This script creates the necessary RAG corpora for the client knowledge management system.
It creates separate corpora for:
1. Main client corpus (all client data)
2. Client materials corpus (capabilities, brochures, etc.)
3. Case studies corpus (case study documents)

Usage:
    python setup_corpus.py [--create-all] [--corpus-name NAME]
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
    
    def create_main_corpus(self) -> str:
        """Create main client corpus for all client data"""
        logger.info("🏗️  Creating main client corpus...")
        
        corpus = self.client.create_corpus(
            display_name="client-knowledge-base-main",
            description="Main corpus containing all client data: websites, materials, case studies, and intake forms"
        )
        
        # Save corpus ID to .env
        self._save_corpus_to_env('RAG_CORPUS_MAIN', corpus.name)
        
        logger.info(f"✅ Main corpus created: {corpus.name}")
        return corpus.name
    
    def create_client_materials_corpus(self) -> str:
        """Create corpus specifically for client materials"""
        logger.info("🏗️  Creating client materials corpus...")
        
        corpus = self.client.create_corpus(
            display_name="client-materials",
            description="Corpus for client brochures, capabilities decks, presentations, and marketing materials"
        )
        
        # Save corpus ID to .env
        self._save_corpus_to_env('RAG_CORPUS_CLIENT_MATERIALS', corpus.name)
        
        logger.info(f"✅ Client materials corpus created: {corpus.name}")
        return corpus.name
    
    def create_case_studies_corpus(self) -> str:
        """Create corpus specifically for case studies"""
        logger.info("🏗️  Creating case studies corpus...")
        
        corpus = self.client.create_corpus(
            display_name="case-studies",
            description="Corpus containing client case studies and success stories"
        )
        
        # Save corpus ID to .env
        self._save_corpus_to_env('RAG_CORPUS_CASE_STUDIES', corpus.name)
        
        logger.info(f"✅ Case studies corpus created: {corpus.name}")
        return corpus.name
    
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
    
    def create_all_corpora(self):
        """Create all required corpora"""
        logger.info("🚀 Creating all RAG corpora...")
        logger.info("=" * 80)
        
        corpora = {}
        
        # Create main corpus
        try:
            corpora['main'] = self.create_main_corpus()
        except Exception as e:
            logger.error(f"❌ Failed to create main corpus: {e}")
        
        # Create client materials corpus
        try:
            corpora['client_materials'] = self.create_client_materials_corpus()
        except Exception as e:
            logger.error(f"❌ Failed to create client materials corpus: {e}")
        
        # Create case studies corpus
        try:
            corpora['case_studies'] = self.create_case_studies_corpus()
        except Exception as e:
            logger.error(f"❌ Failed to create case studies corpus: {e}")
        
        logger.info("\n" + "=" * 80)
        logger.info("✅ Corpus setup complete!")
        logger.info(f"   Created {len(corpora)} corpora")
        logger.info("\n📋 Corpus Resource Names:")
        for name, resource_name in corpora.items():
            logger.info(f"   {name}: {resource_name}")
        
        logger.info("\n💡 Next steps:")
        logger.info("   1. Check your .env file for saved corpus IDs")
        logger.info("   2. Run ingestion scripts to upload documents")
        logger.info("   3. Deploy agents using the deployment scripts")
        
        return corpora


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Setup Vertex AI RAG Corpora',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        '--create-all',
        action='store_true',
        help='Create all corpora (main, client_materials, case_studies)'
    )
    
    parser.add_argument(
        '--corpus-name',
        choices=['main', 'client_materials', 'case_studies'],
        help='Create a specific corpus'
    )
    
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all existing corpora'
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
    
    if args.list:
        setup.list_all_corpora()
        return 0
    
    if args.create_all:
        setup.create_all_corpora()
        return 0
    
    if args.corpus_name:
        if args.corpus_name == 'main':
            setup.create_main_corpus()
        elif args.corpus_name == 'client_materials':
            setup.create_client_materials_corpus()
        elif args.corpus_name == 'case_studies':
            setup.create_case_studies_corpus()
        return 0
    
    # No arguments provided, show help
    parser.print_help()
    return 0


if __name__ == "__main__":
    exit(main())
