#!/usr/bin/env python3
"""
Client Metadata Validation Script
---------------------------------
Validates that all .metadata.json files in a client directory have the required 'client_name' field.
This ensures data integrity before uploading to Vertex AI RAG corpus.

Usage:
    python validate_client_metadata.py --client-id prospex
    python validate_client_metadata.py --output-dir ./ingestion/client_ingestion_outputs/prospex
"""

import json
import argparse
import sys
from pathlib import Path
from typing import List, Dict, Tuple

def validate_metadata_files(base_dir: str, expected_client_name: str = None) -> Tuple[List[Dict], List[Dict]]:
    """
    Validate all .metadata.json files in a client directory
    
    Args:
        base_dir: Base directory to scan (e.g., ./ingestion/client_ingestion_outputs/prospex)
        expected_client_name: Expected client name (optional validation)
        
    Returns:
        Tuple of (valid_files, invalid_files)
    """
    base_path = Path(base_dir)
    if not base_path.exists():
        print(f"❌ Directory not found: {base_dir}")
        return [], []
    
    print(f"🔍 Scanning for .metadata.json files in: {base_dir}")
    
    # Find all .metadata.json files
    metadata_files = list(base_path.glob("**/*.metadata.json"))
    
    if not metadata_files:
        print("⚠️  No .metadata.json files found")
        return [], []
    
    print(f"📄 Found {len(metadata_files)} metadata files")
    
    valid_files = []
    invalid_files = []
    
    for metadata_file in metadata_files:
        try:
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            
            # Check if client_name field exists
            if 'client_name' not in metadata:
                invalid_files.append({
                    'file': str(metadata_file.relative_to(base_path)),
                    'issue': 'Missing client_name field',
                    'metadata': metadata
                })
            elif expected_client_name and metadata['client_name'] != expected_client_name:
                invalid_files.append({
                    'file': str(metadata_file.relative_to(base_path)),
                    'issue': f'Wrong client_name: expected "{expected_client_name}", got "{metadata["client_name"]}"',
                    'metadata': metadata
                })
            else:
                valid_files.append({
                    'file': str(metadata_file.relative_to(base_path)),
                    'client_name': metadata['client_name'],
                    'source': metadata.get('source', 'unknown'),
                    'content_type': metadata.get('content_type', 'unknown'),
                    'word_count': metadata.get('word_count', 0)
                })
                
        except json.JSONDecodeError:
            invalid_files.append({
                'file': str(metadata_file.relative_to(base_path)),
                'issue': 'Invalid JSON format',
                'metadata': None
            })
        except Exception as e:
            invalid_files.append({
                'file': str(metadata_file.relative_to(base_path)),
                'issue': f'Error reading file: {e}',
                'metadata': None
            })
    
    return valid_files, invalid_files

def main():
    parser = argparse.ArgumentParser(
        description='Validate client metadata files for client_name field',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--client-id', 
                       help='Client ID to validate (looks in ingestion/client_ingestion_outputs/CLIENT_ID)')
    group.add_argument('--output-dir', 
                       help='Specific output directory to validate')
    
    args = parser.parse_args()
    
    # Determine directory to scan
    if args.client_id:
        base_dir = f"./ingestion/client_ingestion_outputs/{args.client_id}"
        expected_client_name = args.client_id
    else:
        base_dir = args.output_dir
        expected_client_name = None
    
    print("🔍 CLIENT METADATA VALIDATION")
    print("=" * 80)
    print(f"Directory: {base_dir}")
    if expected_client_name:
        print(f"Expected client_name: {expected_client_name}")
    print("=" * 80)
    
    # Run validation
    valid_files, invalid_files = validate_metadata_files(base_dir, expected_client_name)
    
    # Report results
    print(f"\n📊 VALIDATION RESULTS:")
    print(f"   ✅ Valid files: {len(valid_files)}")
    print(f"   ❌ Invalid files: {len(invalid_files)}")
    
    if valid_files:
        print(f"\n✅ Valid Files ({len(valid_files)}):")
        
        # Group by source type
        by_source = {}
        for file_info in valid_files:
            source = file_info['source']
            if source not in by_source:
                by_source[source] = []
            by_source[source].append(file_info)
        
        for source, files in by_source.items():
            print(f"\n   📁 {source.upper()} ({len(files)} files):")
            for file_info in files[:3]:  # Show first 3
                print(f"      • {file_info['file']}")
                print(f"        Client: {file_info['client_name']}, Type: {file_info['content_type']}, Words: {file_info['word_count']}")
            
            if len(files) > 3:
                print(f"      ... and {len(files) - 3} more files")
    
    if invalid_files:
        print(f"\n❌ Invalid Files ({len(invalid_files)}):")
        for file_info in invalid_files:
            print(f"   • {file_info['file']}")
            print(f"     Issue: {file_info['issue']}")
    
    print("\n" + "=" * 80)
    
    if invalid_files:
        print("❌ VALIDATION FAILED - Some files are missing client_name metadata")
        print("   These files should not be uploaded to the corpus until fixed")
        return 1
    else:
        print("✅ VALIDATION PASSED - All files have proper client_name metadata")
        print("   Safe to upload to Vertex AI RAG corpus")
        return 0


if __name__ == "__main__":
    sys.exit(main())
