#!/usr/bin/env python3
"""
Test script to demonstrate query extraction enhancement
"""
import sys
from dotenv import load_dotenv

load_dotenv("../.env")

from email_handler import EmailHandler

# Example customer emails
test_emails = [
    {
        "name": "Simple question",
        "email": """
Hi there,

I hope this email finds you well. I'm reaching out because I'm curious about what 
services your agency offers. We're a B2B SaaS company looking to scale our 
marketing efforts.

Could you help me understand what you specialize in?

Best regards,
Sarah Johnson
sarah@acmesaas.com
        """
    },
    {
        "name": "Multiple questions",
        "email": """
Hello,

We're currently evaluating marketing agencies and I have a few questions:

1. Do you have experience with demand generation campaigns?
2. What are your pricing models?
3. Can you help with both paid ads and SEO?
4. What results have you achieved for similar B2B clients?

Looking forward to hearing from you.

Thanks,
Mike Chen
Head of Marketing
TechCorp Inc.
mike@techcorp.com
(555) 123-4567
        """
    },
    {
        "name": "Specific request with context",
        "email": """
Hi team,

I visited your website and was impressed by your Clutch case study. We're a healthcare 
technology company launching a new patient engagement platform, and we need help with 
website design and a go-to-market strategy.

Our target audience is hospital administrators and we need to launch in Q2. Do you have 
experience in healthcare marketing and can you work within our timeline?

Please let me know your availability for a call this week.

Best,
Dr. Emily Rodriguez
Chief Marketing Officer
HealthTech Solutions
emily@healthtech.com
        """
    }
]

def main():
    print("🧪 Testing LLM-Enhanced Query Extraction\n")
    print("=" * 80)
    
    # Test with both OpenAI and Anthropic
    for provider in ["openai"]:  # Add "anthropic" if you have the key
        print(f"\n🤖 Testing with {provider.upper()}\n")
        
        try:
            handler = EmailHandler(llm_provider=provider)
            
            for i, test_case in enumerate(test_emails, 1):
                print(f"\n📧 Test {i}: {test_case['name']}")
                print("-" * 80)
                print("ORIGINAL EMAIL:")
                print(test_case['email'].strip())
                print("\n🔍 EXTRACTED QUERY:")
                
                extracted = handler.extract_query(test_case['email'])
                print(f"   {extracted}")
                print("-" * 80)
                
                # Show the difference
                print(f"\n   ✨ Improved for search: {len(extracted)} chars vs {len(test_case['email'])} chars")
                print(f"   💡 Removed {len(test_case['email']) - len(extracted)} chars of fluff\n")
                
        except Exception as e:
            print(f"   ❌ Error with {provider}: {e}\n")
            continue
    
    print("\n" + "=" * 80)
    print("✅ Query extraction test complete!")
    print("\nBenefits:")
    print("  • More focused semantic search")
    print("  • Better retrieval accuracy")
    print("  • Removes noise and signatures")
    print("  • Combines multiple questions intelligently")

if __name__ == "__main__":
    main()

