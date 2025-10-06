"""
RAG Metadata Search Tool
========================
Tool for filtering and searching Vertex AI RAG corpus files based on metadata.

This tool enables targeted searches by filtering on:
- client_name
- source (client_materials, client_intake, website)
- content_type (pitch_decks, case_studies, capabilities_overview, etc.)
- corpus_id

Usage:
    from tools.rag_metadata_search import create_rag_metadata_search_function
    
    # Create the tool
    rag_search_tool = create_rag_metadata_search_function()
    
    # Use in agent
    agent = Agent(tools=[rag_search_tool, ...])
"""

import os
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any
from google.cloud import aiplatform
from vertexai.preview import rag
from google.oauth2 import service_account
from google.cloud import storage

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared import config


def search_rag_by_metadata(
    corpus_id: Optional[str] = None,
    client_name: Optional[str] = None,
    source: Optional[str] = None,
    content_type: Optional[str] = None,
    query_text: Optional[str] = None,
    similarity_top_k: int = 10
) -> Dict[str, Any]:
    """
    Search Vertex AI RAG corpus filtered by metadata. If client_name is provided,
    discover the client's dedicated bucket(s) (named like `<client_id>-vertex-rag`),
    list objects under `rag-uploads/`, and filter by object metadata. Optionally
    perform semantic retrieval on the matched RAG files.
    """
    
    # Initialize Vertex AI if not already initialized
    try:
        credentials = service_account.Credentials.from_service_account_file(
            config.CREDENTIALS_PATH,
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
        
        aiplatform.init(
            project=config.PROJECT_ID,
            location=config.LOCATION,
            credentials=credentials
        )
    except Exception as e:
        return {
            'success': False,
            'error': f'Failed to initialize Vertex AI: {e}',
            'results': []
        }
    
    # Determine corpus to search
    corpus_name = None
    
    if corpus_id:
        # Check if it's a display name or full resource name
        if corpus_id.startswith('projects/'):
            corpus_name = corpus_id
        else:
            # It's a display name, search for it
            try:
                corpora = list(rag.list_corpora())
                for corpus in corpora:
                    if corpus.display_name == corpus_id:
                        corpus_name = corpus.name
                        break
                
                if not corpus_name:
                    return {
                        'success': False,
                        'error': f'Corpus not found with display name: {corpus_id}',
                        'results': []
                    }
            except Exception as e:
                return {
                    'success': False,
                    'error': f'Failed to list corpora: {e}',
                    'results': []
                }
    else:
        # Use default corpus from config
        corpus_name = config.RAG_CORPUS_MAIN
        if not corpus_name:
            return {
                'success': False,
                'error': 'No corpus specified and RAG_CORPUS_MAIN not configured',
                'results': []
            }
    
    # Build mapping from GCS URI -> RagFile (for optional retrieval on matches)
    try:
        all_rag_files = list(rag.list_files(corpus_name=corpus_name))
        gcs_uri_to_rag = {}
        filename_to_rag = {}
        display_to_rag = {}
        # Support both potential attributes: gcs_uri and gcs_source
        for f in all_rag_files:
            uri = getattr(f, 'gcs_uri', '') or getattr(f, 'gcs_source', '')
            if uri:
                # Normalize to full gs:// form
                if not uri.startswith('gs://'):
                    uri = f"gs://{uri}"
                gcs_uri_to_rag[uri] = f
                # Also index by filename for fallback
                try:
                    filename = uri.split('/')[-1]
                    filename_to_rag[filename] = f
                except Exception:
                    pass
            # Index by display_name as additional fallback
            try:
                if getattr(f, 'display_name', None):
                    display_to_rag[f.display_name] = f
            except Exception:
                pass
    except Exception:
        all_rag_files = []
        gcs_uri_to_rag = {}
        filename_to_rag = {}
        display_to_rag = {}
    
    # If client_name provided, search per-client buckets; else fallback to corpus-wide scan
    try:
        storage_client = storage.Client(project=config.PROJECT_ID)
        matching_files: List[Dict[str, Any]] = []
        
        mapped_count = 0
        unmatched_count = 0
        
        if client_name:
            # Prefer exact bucket name match `<client_id>-vertex-rag`, fall back to substring
            prefer_bucket = f"{client_name}-vertex-rag"
            buckets_iter = storage_client.list_buckets(project=config.PROJECT_ID)
            all_buckets = list(buckets_iter)
            target_buckets = [b for b in all_buckets if b.name == prefer_bucket]
            if not target_buckets:
                target_buckets = [b for b in all_buckets if client_name.lower() in b.name.lower()]
            
            # Traverse each bucket's rag-uploads/ prefix and collect metadata
            for b in target_buckets:
                for blob in b.list_blobs(prefix='rag-uploads/'):
                    # Fetch metadata
                    blob = b.get_blob(blob.name)
                    if not blob or not blob.metadata:
                        continue
                    
                    # Apply filters
                    if source and blob.metadata.get('source') != source:
                        continue
                    if content_type and blob.metadata.get('content_type') != content_type:
                        continue
                    if client_name and blob.metadata.get('client_name') not in (client_name, client_name.lower(), client_name.upper()):
                        # If metadata has client_name, ensure it matches; otherwise allow if absent
                        if 'client_name' in blob.metadata:
                            continue
                    
                    gcs_uri = f"gs://{b.name}/{blob.name}"
                    rag_file = gcs_uri_to_rag.get(gcs_uri)
                    
                    # Fallback 1: by filename
                    if not rag_file:
                        try:
                            filename = blob.name.split('/')[-1]
                            rag_file = filename_to_rag.get(filename)
                        except Exception:
                            pass
                    
                    # Fallback 2: by display_name
                    if not rag_file:
                        try:
                            filename = blob.name.split('/')[-1]
                            rag_file = display_to_rag.get(filename)
                        except Exception:
                            pass
                    
                    if rag_file:
                        mapped_count += 1
                    else:
                        unmatched_count += 1
                    
                    matching_files.append({
                        'name': getattr(rag_file, 'name', None),
                        'display_name': getattr(rag_file, 'display_name', Path(blob.name).name),
                        'gcs_uri': gcs_uri,
                        'metadata': blob.metadata
                    })
        else:
            # Fallback: scan all files in the corpus and filter by blob metadata
            for rag_file in all_rag_files:
                try:
                    gcs_uri = getattr(rag_file, 'gcs_uri', '') or getattr(rag_file, 'gcs_source', '')
                    if not gcs_uri:
                        continue
                    # Normalize
                    if not gcs_uri.startswith('gs://'):
                        gcs_uri = f"gs://{gcs_uri}"
                    bucket_name, blob_name = gcs_uri.replace("gs://", "").split("/", 1)
                    bucket = storage_client.bucket(bucket_name)
                    blob = bucket.get_blob(blob_name)
                    if not blob or not blob.metadata:
                        continue
                    if source and blob.metadata.get('source') != source:
                        continue
                    if content_type and blob.metadata.get('content_type') != content_type:
                        continue
                    mapped_count += 1
                    matching_files.append({
                        'name': rag_file.name,
                        'display_name': rag_file.display_name,
                        'gcs_uri': gcs_uri,
                        'metadata': blob.metadata
                    })
                except Exception:
                    unmatched_count += 1
                    continue
        
        # Attach simple diagnostics
        diagnostics = {
            'mapped_count': mapped_count,
            'unmatched_count': unmatched_count,
            'total_matches': len(matching_files)
        }
        
        # If query_text provided, perform semantic search on matched RAG files
        if query_text:
            # Use only those matched files that have a RagFile resource name
            matched_rag_names = [f['name'] for f in matching_files if f.get('name')]
            if not matched_rag_names:
                return {
                    'success': True,
                    'corpus_name': corpus_name,
                    'filters': {
                        'client_name': client_name,
                        'source': source,
                        'content_type': content_type
                    },
                    'query': query_text,
                    'total_files': len(all_rag_files),
                    'matching_files': len(matching_files),
                    'diagnostics': diagnostics,
                    'contexts': [],
                    'results': []
                }
            
            rag_resources = [
                rag.RagResource(
                    rag_corpus=corpus_name,
                    rag_files=matched_rag_names
                )
            ]
            
            try:
                response = rag.retrieval_query(
                    rag_resources=rag_resources,
                    text=query_text,
                    similarity_top_k=similarity_top_k,
                )
                contexts = []
                if hasattr(response, 'contexts'):
                    for context in response.contexts.contexts:
                        contexts.append({
                            'text': getattr(context, 'text', None),
                            'source': getattr(context, 'source_uri', None),
                            'score': getattr(context, 'score', None)
                        })
                return {
                    'success': True,
                    'corpus_name': corpus_name,
                    'filters': {
                        'client_name': client_name,
                        'source': source,
                        'content_type': content_type
                    },
                    'query': query_text,
                    'total_files': len(all_rag_files),
                    'matching_files': len(matching_files),
                    'diagnostics': diagnostics,
                    'contexts': contexts,
                    'results': contexts
                }
            except Exception as e:
                return {
                    'success': False,
                    'error': f'RAG query failed: {e}',
                    'corpus_name': corpus_name,
                    'total_files': len(all_rag_files),
                    'matching_files': len(matching_files),
                    'diagnostics': diagnostics,
                    'results': []
                }
        else:
            return {
                'success': True,
                'corpus_name': corpus_name,
                'filters': {
                    'client_name': client_name,
                    'source': source,
                    'content_type': content_type
                },
                'total_files': len(all_rag_files),
                'matching_files': len(matching_files),
                'diagnostics': diagnostics,
                'files': matching_files,
                'results': matching_files
            }
    except Exception as e:
        return {
            'success': False,
            'error': f'Failed to search corpus: {e}',
            'results': []
        }


def create_rag_metadata_search_function():
    """
    Create a function tool for RAG metadata search
    
    Returns:
        Function that can be used as an agent tool
    """
    from google.adk.tools import function_tool
    
    @function_tool
    def search_client_documents(
        client_name: Optional[str] = None,
        source: Optional[str] = None,
        content_type: Optional[str] = None,
        query: Optional[str] = None
    ) -> str:
        """
        Search client documents in the RAG corpus with metadata filtering.
        
        Use this to find specific types of client documents based on:
        - client_name: Which client's documents to search
        - source: Type of source (client_materials, client_intake, website)
        - content_type: Content category (pitch_decks, case_studies, capabilities_overview, etc.)
        - query: Optional text to search within filtered documents
        
        Examples:
        - Find all pitch decks: source="client_materials", content_type="pitch_decks"
        - Find client intake form: source="client_intake"
        - Find case studies: content_type="case_studies"
        - Search website content: source="website", query="pricing"
        
        Args:
            client_name: Client identifier (e.g., 'mintleads', 'prospex')
            source: Document source type
            content_type: Content category
            query: Text to search for
            
        Returns:
            String with search results and relevant document excerpts
        """
        
        result = search_rag_by_metadata(
            client_name=client_name,
            source=source,
            content_type=content_type,
            query_text=query,
            similarity_top_k=10
        )
        
        if not result['success']:
            return f"Error searching documents: {result.get('error', 'Unknown error')}"
        
        # Format results as string
        output = []
        output.append(f"🔍 Search Results from RAG Corpus")
        output.append(f"=" * 60)
        output.append(f"Corpus: {result.get('corpus_name', 'Unknown')}")
        output.append(f"Filters: {result.get('filters', 'None')}")
        output.append(f"Total files in corpus: {result.get('total_files', 0)}")
        output.append(f"Matching files: {result.get('matching_files', 0)}")
        output.append("")
        
        if 'contexts' in result and result['contexts']:
            output.append(f"📄 Retrieved Contexts ({len(result['contexts'])}):")
            output.append("")
            for i, ctx in enumerate(result['contexts'][:5], 1):  # Show top 5
                output.append(f"{i}. Score: {ctx.get('score', 'N/A')}")
                output.append(f"   Source: {ctx.get('source', 'N/A')}")
                output.append(f"   Text: {ctx.get('text', '')[:200]}...")
                output.append("")
        elif 'files' in result:
            output.append(f"📁 Files ({len(result['files'])}):")
            for i, file in enumerate(result['files'][:10], 1):  # Show top 10
                output.append(f"{i}. {file.get('display_name', 'Unknown')}")
        
        return '\n'.join(output)
    
    return search_client_documents


# Standalone usage
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Search RAG corpus by metadata')
    parser.add_argument('--corpus-id', help='Corpus ID or display name')
    parser.add_argument('--client-name', help='Filter by client name')
    parser.add_argument('--source', choices=['client_materials', 'client_intake', 'website'],
                       help='Filter by source type')
    parser.add_argument('--content-type', help='Filter by content type')
    parser.add_argument('--query', help='Text query for semantic search')
    parser.add_argument('--top-k', type=int, default=10, help='Number of results')
    
    args = parser.parse_args()
    
    result = search_rag_by_metadata(
        corpus_id=args.corpus_id,
        client_name=args.client_name,
        source=args.source,
        content_type=args.content_type,
        query_text=args.query,
        similarity_top_k=args.top_k
    )
    
    import json
    print(json.dumps(result, indent=2, default=str))
