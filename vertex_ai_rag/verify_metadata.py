#!/usr/bin/env python3
"""
Verify metadata extraction from client ingestion outputs

Tests that:
1. Website files - YAML frontmatter is extracted correctly
2. Client materials - .metadata.json files are loaded correctly
3. Metadata is preserved through the upload process
"""
import sys
import json
from pathlib import Path
from typing import Dict, Any

sys.path.insert(0, str(Path(__file__).parent))
from ingestion.client_ingestion_adapter import ClientIngestionAdapter


def test_frontmatter_extraction(adapter: ClientIngestionAdapter, test_file: Path) -> bool:
    """Test YAML frontmatter extraction from a website file"""
    print(f"\n📄 Testing frontmatter extraction: {test_file.name}")
    
    if not test_file.exists():
        print(f"   ⚠️  File not found: {test_file}")
        return False
    
    metadata = adapter._extract_frontmatter(test_file)
    
    expected_fields = ['source', 'content_type', 'url', 'title', 'domain']
    found_fields = [f for f in expected_fields if f in metadata]
    
    print(f"   Extracted fields: {len(metadata)} total")
    for key, value in list(metadata.items())[:5]:
        print(f"      {key}: {value}")
    
    if len(found_fields) >= 3:
        print(f"   ✅ Found {len(found_fields)}/{len(expected_fields)} expected fields")
        return True
    else:
        print(f"   ❌ Only found {len(found_fields)}/{len(expected_fields)} expected fields")
        return False


def test_json_metadata_loading(adapter: ClientIngestionAdapter, test_file: Path) -> bool:
    """Test JSON metadata loading for client materials"""
    print(f"\n📄 Testing JSON metadata: {test_file.name}")
    
    if not test_file.exists():
        print(f"   ⚠️  File not found: {test_file}")
        return False
    
    metadata_file = Path(str(test_file) + '.metadata.json')
    
    if not metadata_file.exists():
        print(f"   ⚠️  Metadata file not found: {metadata_file.name}")
        return False
    
    metadata = adapter._load_metadata(metadata_file)
    
    print(f"   Extracted fields: {len(metadata)} total")
    for key, value in metadata.items():
        print(f"      {key}: {value}")
    
    if metadata:
        print(f"   ✅ Successfully loaded metadata")
        return True
    else:
        print(f"   ❌ No metadata loaded")
        return False


def verify_client_metadata(client_id: str):
    """
    Verify metadata extraction for a client
    
    Args:
        client_id: Client identifier (e.g., 'mintleads')
    """
    print("=" * 80)
    print(f"METADATA VERIFICATION: {client_id}")
    print("=" * 80)
    
    # Initialize adapter
    workspace_root = Path(__file__).parent.parent
    client_dir = workspace_root / 'ingestion' / 'client_ingestion_outputs' / client_id
    
    if not client_dir.exists():
        print(f"❌ Client directory not found: {client_dir}")
        return
    
    print(f"\n📁 Client directory: {client_dir}")
    
    adapter = ClientIngestionAdapter(client_id=client_id)
    
    results = {
        'website_frontmatter': False,
        'materials_json': False,
        'discovery': False
    }
    
    # Test 1: Website frontmatter extraction
    website_dir = client_dir / 'website'
    if website_dir.exists():
        website_files = list(website_dir.glob('*.md'))[:1]  # Test first file
        if website_files:
            results['website_frontmatter'] = test_frontmatter_extraction(
                adapter, website_files[0]
            )
    else:
        print(f"\n⚠️  No website directory found")
    
    # Test 2: Client materials JSON metadata
    materials_dir = client_dir / 'client_materials'
    if materials_dir.exists():
        materials_files = [f for f in materials_dir.glob('*.md') 
                          if not f.name.endswith('.metadata.json')][:1]
        if materials_files:
            results['materials_json'] = test_json_metadata_loading(
                adapter, materials_files[0]
            )
    else:
        print(f"\n⚠️  No client_materials directory found")
    
    # Test 3: Full discovery process
    print(f"\n📋 Testing full file discovery...")
    try:
        files_by_source = adapter.discover_files()
        
        total_files = sum(len(files) for files in files_by_source.values())
        print(f"   ✅ Discovered {total_files} files:")
        
        for source, files in files_by_source.items():
            if files:
                print(f"\n   {source}: {len(files)} files")
                # Show metadata sample from first file
                sample = files[0]
                print(f"      Sample: {sample['filename']}")
                print(f"      Source: {sample['source']}")
                print(f"      Type: {sample['content_type']}")
                print(f"      Metadata fields: {len(sample['metadata'])}")
                if sample['metadata']:
                    for key in list(sample['metadata'].keys())[:3]:
                        print(f"         {key}: {sample['metadata'][key]}")
        
        results['discovery'] = True
        
    except Exception as e:
        print(f"   ❌ Discovery failed: {e}")
    
    # Summary
    print("\n" + "=" * 80)
    print("VERIFICATION RESULTS")
    print("=" * 80)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✅ PASS" if passed_test else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All metadata extraction working correctly!")
    else:
        print("⚠️  Some metadata extraction issues found")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Verify metadata extraction for client ingestion'
    )
    
    parser.add_argument(
        '--client-id',
        required=True,
        help='Client identifier (e.g., mintleads)'
    )
    
    args = parser.parse_args()
    
    verify_client_metadata(args.client_id)


if __name__ == "__main__":
    main()

