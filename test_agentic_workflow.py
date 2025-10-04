#!/usr/bin/env python3
"""
Test script for the agentic workflow

This validates that:
1. OpenAI SDK is properly installed
2. All dependencies can be imported
3. Agent creation works
4. Tool definitions are valid
"""

import sys
import os
from pathlib import Path

# Add OpenAI to path
sys.path.insert(0, '/home/ubuntu/.local/lib/python3.13/site-packages')

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        from openai import OpenAI, AsyncOpenAI
        print("  ✅ OpenAI SDK imported successfully")
    except ImportError as e:
        print(f"  ❌ Failed to import OpenAI SDK: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("  ✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"  ❌ Failed to import dotenv: {e}")
        return False
    
    try:
        import asyncio
        print("  ✅ asyncio available")
    except ImportError as e:
        print(f"  ❌ Failed to import asyncio: {e}")
        return False
    
    return True


def test_openai_client():
    """Test OpenAI client initialization"""
    print("\nTesting OpenAI client...")
    
    from openai import OpenAI
    from dotenv import load_dotenv
    
    load_dotenv()
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("  ⚠️  OPENAI_API_KEY not set in environment")
        print("     Set this in your .env file to test agent creation")
        return False
    
    try:
        client = OpenAI(api_key=api_key)
        print("  ✅ OpenAI client initialized")
        
        # Test API access by listing models (lightweight call)
        models = client.models.list()
        print(f"  ✅ API access verified ({len(list(models.data))} models available)")
        
        return True
    except Exception as e:
        print(f"  ❌ Failed to initialize OpenAI client: {e}")
        return False


def test_agent_creation():
    """Test creating a simple test agent"""
    print("\nTesting agent creation...")
    
    from openai import OpenAI
    from dotenv import load_dotenv
    
    load_dotenv()
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("  ⚠️  Skipping agent creation (no API key)")
        return False
    
    try:
        client = OpenAI(api_key=api_key)
        
        # Create a test assistant
        assistant = client.beta.assistants.create(
            name="Test Agent",
            instructions="You are a test agent for validation purposes.",
            model="gpt-4o-2024-11-20",
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "test_tool",
                        "description": "A test tool",
                        "parameters": {
                            "type": "object",
                            "properties": {},
                            "required": []
                        }
                    }
                }
            ]
        )
        
        print(f"  ✅ Test agent created: {assistant.id}")
        
        # Clean up
        client.beta.assistants.delete(assistant.id)
        print(f"  ✅ Test agent deleted: {assistant.id}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Failed to create test agent: {e}")
        return False


def test_workflow_files():
    """Test that workflow files exist and are valid"""
    print("\nTesting workflow files...")
    
    files_to_check = [
        'agentic_workflow.py',
        'ingestion/reprocess_failed_pdfs.py',
        'new_client_ingestion.py',
        'client_brief_generator.py'
    ]
    
    all_exist = True
    for file_path in files_to_check:
        path = Path(file_path)
        if path.exists():
            print(f"  ✅ {file_path} exists")
        else:
            print(f"  ❌ {file_path} not found")
            all_exist = False
    
    return all_exist


def test_syntax():
    """Test Python syntax of workflow files"""
    print("\nTesting Python syntax...")
    
    import py_compile
    
    files_to_check = [
        'agentic_workflow.py',
        'ingestion/reprocess_failed_pdfs.py'
    ]
    
    all_valid = True
    for file_path in files_to_check:
        try:
            py_compile.compile(file_path, doraise=True)
            print(f"  ✅ {file_path} syntax valid")
        except py_compile.PyCompileError as e:
            print(f"  ❌ {file_path} syntax error: {e}")
            all_valid = False
    
    return all_valid


def main():
    """Run all tests"""
    print("=" * 80)
    print("AGENTIC WORKFLOW TEST SUITE")
    print("=" * 80)
    print()
    
    results = {
        'imports': test_imports(),
        'workflow_files': test_workflow_files(),
        'syntax': test_syntax(),
        'openai_client': test_openai_client(),
        'agent_creation': test_agent_creation()
    }
    
    print("\n" + "=" * 80)
    print("TEST RESULTS")
    print("=" * 80)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 80)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("The agentic workflow is ready to use.")
    else:
        print("⚠️  SOME TESTS FAILED")
        print("Review the errors above and fix any issues.")
        print("\nCommon issues:")
        print("  • Missing OPENAI_API_KEY in .env file")
        print("  • OpenAI SDK not installed (pip install openai)")
        print("  • python-dotenv not installed (pip install python-dotenv)")
    print("=" * 80)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
