#!/usr/bin/env python3
"""
Client Ingestion Adapter for Vertex AI RAG

This script adapts the existing Vectara ingestion workflow to work with Vertex AI RAG Engine.
It processes the markdown files from the existing ingestion pipeline and uploads them to Vertex AI.

The script automatically searches for a corpus with the display name "client-{CLIENT_ID}" in 
the RAG Engine. Make sure to create the corpus first using setup_corpus.py.

Usage:
    python client_ingestion_adapter.py --client-id CLIENT_ID [--input-dir DIR]
"""

import os
import sys
import json
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

# Add parent directory to path for shared imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from shared import config, VertexRAGClient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ClientIngestionAdapter:
    """Adapts existing ingestion workflow to upload to Vertex AI RAG"""
    
    def __init__(self, client_id: str, input_dir: Optional[str] = None):
        """
        Initialize the adapter
        
        Args:
            client_id: The client identifier
            input_dir: Optional path to client's ingestion output directory
        """
        self.client_id = client_id
        if input_dir:
            self.client_output_dir = Path(input_dir)
        
        # Default to the existing ingestion output directory
        if input_dir is None:
            workspace_root = Path(__file__).parent.parent.parent
            self.client_output_dir = workspace_root / 'ingestion' / 'client_ingestion_outputs' / client_id
        
        self.rag_client = VertexRAGClient()
        
        logger.info(f"📁 Client: {client_id}")
        logger.info(f"📂 Input directory: {self.client_output_dir}")
    
    def discover_files(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Discover all markdown files from ingestion output
        
        Returns:
            Dictionary categorizing files by source type
        """
        logger.info("🔍 Discovering files from ingestion output...")
        
        files_by_source = {
            'client_intake_form': [],
            'client_materials': [],
            'website': []
        }
        
        # Process client intake form files
        intake_dir = self.client_output_dir / 'client_intake_form'
        if intake_dir.exists():
            for md_file in intake_dir.glob('*.md'):
                if md_file.name.endswith('.metadata.json'):
                    continue
                
                metadata_file = Path(str(md_file) + '.metadata.json')
                metadata = self._load_metadata(metadata_file)
                
                files_by_source['client_intake_form'].append({
                    'path': md_file,
                    'filename': md_file.name,
                    'source': 'client_intake_form',
                    'content_type': 'client_intake_form',
                    'metadata': metadata
                })
        
        # Process client materials files
        materials_dir = self.client_output_dir / 'client_materials'
        if materials_dir.exists():
            for md_file in materials_dir.glob('*.md'):
                if md_file.name.endswith('.metadata.json'):
                    continue
                
                metadata_file = Path(str(md_file) + '.metadata.json')
                metadata = self._load_metadata(metadata_file)
                
                files_by_source['client_materials'].append({
                    'path': md_file,
                    'filename': md_file.name,
                    'source': 'client_materials',
                    'content_type': metadata.get('content_type', 'other'),
                    'metadata': metadata
                })
        
        # Process website files
        website_dir = self.client_output_dir / 'website'
        if website_dir.exists():
            for md_file in website_dir.glob('*.md'):
                metadata = self._extract_frontmatter(md_file)
                
                files_by_source['website'].append({
                    'path': md_file,
                    'filename': md_file.name,
                    'source': 'website',
                    'content_type': metadata.get('content_type', 'other'),
                    'metadata': metadata
                })
        
        # Log summary
        total_files = sum(len(files) for files in files_by_source.values())
        logger.info(f"✅ Discovered {total_files} files:")
        for source, files in files_by_source.items():
            logger.info(f"   • {source}: {len(files)} files")
        
        return files_by_source
    
    def _load_metadata(self, metadata_file: Path) -> Dict[str, Any]:
        """Load metadata from JSON file"""
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"⚠️  Failed to load metadata from {metadata_file}: {e}")
        return {}
    
    def _extract_frontmatter(self, md_file: Path) -> Dict[str, Any]:
        """Extract metadata from markdown frontmatter"""
        metadata = {}
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if content.startswith('---\n'):
                parts = content.split('---\n', 2)
                if len(parts) >= 2:
                    frontmatter_lines = parts[1].strip().split('\n')
                    for line in frontmatter_lines:
                        if ':' in line:
                            key, value = line.split(':', 1)
                            metadata[key.strip()] = value.strip().strip('"')
        except Exception as e:
            logger.warning(f"⚠️  Failed to extract frontmatter from {md_file}: {e}")
        
        return metadata
    
    def run(self, corpus_name: str, client_id: str):
        """
        Run the full ingestion and upload process
        This method is now deprecated in favor of upload_to_vertex_rag
        """
        files_by_source = self.discover_files()
        return self.upload_to_vertex_rag(files_by_source, corpus_name, client_id)

    def upload_to_vertex_rag(self, files_by_source: Dict[str, List], corpus_name: str, client_id: str) -> Dict[str, int]:
        """
        Upload discovered files to Vertex AI RAG corpus.
        
        Args:
            files_by_source: Dictionary of files categorized by source
            corpus_name: The resource name of the corpus to upload to
            client_id: The client ID for folder creation in GCS
            
        Returns:
            Dictionary with upload statistics
        """
        if corpus_name is None:
            # Search for corpus by display name: "client-{client_id}"
            corpus_display_name = f"client-{self.client_id}"
            logger.info(f"🔍 Searching for corpus with display name: {corpus_display_name}")
            
            corpus = self.rag_client.find_corpus_by_display_name(corpus_display_name)
            if not corpus:
                raise ValueError(
                    f"No corpus found with display name '{corpus_display_name}'. "
                    f"Run: python setup_corpus.py --client-id {self.client_id}"
                )
            corpus_name = corpus.name
        
        logger.info(f"⬆️  Uploading to Vertex AI RAG corpus: {corpus_name}")
        
        stats = {
            'total_files': 0,
            'successful': 0,
            'failed': 0,
            'by_source': {}
        }
        
        for source_type, files in files_by_source.items():
            if not files:
                continue

            logger.info(f"\n📤 Uploading {source_type} files...")
            
            # Use upload_files_batch and pass the client_id
            uploaded = self.rag_client.upload_files_batch(
                corpus_name=corpus_name,
                file_paths=[str(f['path']) for f in files],
                metadata_list=[f['metadata'] for f in files],
                client_id=client_id # Pass client_id here
            )
            
            stats['successful'] += len(uploaded)
            stats['failed'] += len(files) - len(uploaded)
            
            stats['by_source'][source_type] = {
                'successful': len(uploaded),
                'failed': len(files) - len(uploaded)
            }
            stats['total_files'] += len(files)
            
            logger.info(f"   ✅ {source_type}: {len(uploaded)}/{len(files)} uploaded")
        
        # Log final summary
        logger.info("\n" + "=" * 80)
        logger.info("📊 UPLOAD SUMMARY")
        logger.info("=" * 80)
        logger.info(f"Total files: {stats['total_files']}")
        logger.info(f"Successful: {stats['successful']}")
        logger.info(f"Failed: {stats['failed']}")
        logger.info(f"Success rate: {stats['successful']/stats['total_files']*100:.1f}%")
        
        logger.info("\nBy source:")
        for source, source_stats in stats['by_source'].items():
            logger.info(f"  {source}:")
            logger.info(f"    Successful: {source_stats['successful']}")
            logger.info(f"    Failed: {source_stats['failed']}")
        
        return stats
    
    def run(self, corpus_name: str = None) -> Dict[str, Any]:
        """
        Run the complete ingestion adapter workflow
        
        Args:
            corpus_name: Optional specific corpus to upload to
            
        Returns:
            Upload statistics
        """
        logger.info("🚀 Starting Client Ingestion Adapter")
        logger.info("=" * 80)
        
        # Validate configuration
        config.validate()
        
        # Discover files
        files_by_source = self.discover_files()
        
        if not any(files_by_source.values()):
            logger.warning("⚠️  No files found to upload")
            return {'total_files': 0, 'successful': 0, 'failed': 0}
        
        # Upload to Vertex AI RAG
        stats = self.upload_to_vertex_rag(files_by_source, corpus_name)
        
        logger.info("\n✅ Ingestion adapter complete!")
        return stats


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Adapt existing ingestion output for Vertex AI RAG',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        '--client-id',
        required=True,
        help='Client identifier (matches directory name in ingestion output)'
    )
    
    parser.add_argument(
        '--input-dir',
        help='Input directory containing ingestion outputs (default: ingestion/client_ingestion_outputs/CLIENT_ID)'
    )
    
    parser.add_argument(
        '--corpus-name',
        help='Specific RAG corpus resource name to upload to (default: searches for "client-{CLIENT_ID}")'
    )
    
    args = parser.parse_args()
    
    try:
        adapter = ClientIngestionAdapter(
            client_id=args.client_id,
            input_dir=args.input_dir
        )
        
        stats = adapter.run(corpus_name=args.corpus_name)
        
        # Exit with error code if uploads failed
        if stats['failed'] > 0:
            logger.warning(f"⚠️  {stats['failed']} files failed to upload")
            return 1
        
        return 0
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return 1


if __name__ == "__main__":
    exit(main())

