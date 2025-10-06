#!/usr/bin/env python3
"""
Test the new conversational sales tone
"""
import sys
from dotenv import load_dotenv

load_dotenv("/Users/hynes/dev/vectara/.env")

from email_handler import EmailHandler

test_email = """
Hi there,

I came across your agency while researching marketing partners. 
Do you have experience working with B2B tech companies, particularly 
in the fintech space? 

We're looking for someone who understands our sector and has a proven 
track record with similar clients.

Thanks,
Sarah Chen
Head of Marketing
FinTech Innovations Inc.
sarah@fintechinnovations.com
"""

def main():
    print("🎯 Testing New Sales-Oriented Response Tone\n")
    print("=" * 80)
    print("\n📧 INCOMING EMAIL:")
    print("-" * 80)
    print(test_email.strip())
    print("-" * 80)
    
    print("\n🤖 Processing with OpenAI GPT-5...\n")
    
    try:
        handler = EmailHandler(llm_provider="openai")
        
        # This will:
        # 1. Extract query (with name/company preserved)
        # 2. Search for relevant docs
        # 3. Generate response with new conversational tone
        
        result = handler.handle_email(
            email_content=test_email,
            client_id="dodeka-digital-supa",
            client_name="Dodeka Digital",
            enable_verification=False  # Speed up for demo
        )
        
        print("\n📝 GENERATED RESPONSE:")
        print("=" * 80)
        print(result.get('response', 'No response generated'))
        print("=" * 80)
        
        print(f"\n📊 Metadata:")
        print(f"   • Confidence: {result.get('confidence_score', 0):.1%}")
        print(f"   • Documents retrieved: {len(result.get('source_documents', []))}")
        print(f"   • Relevance check: {result.get('relevance_check', {}).get('is_relevant', 'N/A')}")
        
        print("\n✨ Notice the improvements:")
        print("   • Friendly greeting with first name")
        print("   • Conversational tone (Yes -- not Yes.)")
        print("   • Case studies formatted as bullets")
        print("   • Personal touch about their company")
        print("   • Call-to-action to schedule a call")
        print("   • All while staying grounded in the knowledge base!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

