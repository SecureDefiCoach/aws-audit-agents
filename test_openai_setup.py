#!/usr/bin/env python3
"""Test OpenAI API setup and check available models."""

import os
from openai import OpenAI

def test_openai():
    """Test OpenAI API connection and model availability."""
    
    # Check for API key
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not set!")
        print("\nTo set it:")
        print("  export OPENAI_API_KEY='your-key-here'")
        print("\nOr add to ~/.zshrc:")
        print("  echo 'export OPENAI_API_KEY=\"your-key-here\"' >> ~/.zshrc")
        print("  source ~/.zshrc")
        return False
    
    print(f"✅ API key found: {api_key[:10]}...")
    
    # Test connection
    try:
        client = OpenAI(api_key=api_key)
        
        print("\n🧪 Testing API connection with GPT-5...")
        
        # Test with a simple audit question (GPT-5 works best with very simple, direct questions)
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "user", "content": "List 3 IAM risks in AWS."}
            ],
            max_completion_tokens=500
        )
        
        print("\n✅ API connection successful!")
        print(f"\n📊 Model used: {response.model}")
        print(f"💰 Tokens used: {response.usage.total_tokens} (input: {response.usage.prompt_tokens}, output: {response.usage.completion_tokens})")
        
        # Estimate cost (GPT-5 pricing)
        input_cost = response.usage.prompt_tokens * 0.015 / 1000  # $0.015 per 1K tokens
        output_cost = response.usage.completion_tokens * 0.045 / 1000  # $0.045 per 1K tokens
        total_cost = input_cost + output_cost
        print(f"💵 Estimated cost: ${total_cost:.4f}")
        
        print("\n🤖 GPT-5 Response:")
        print("-" * 80)
        content = response.choices[0].message.content
        print(content)
        print("-" * 80)
        
        # Check reasoning quality
        response_text = response.choices[0].message.content.lower()
        quality_indicators = ['mfa', 'least privilege', 'root', 'access key', 'policy', 'permission']
        found_indicators = [ind for ind in quality_indicators if ind in response_text]
        
        print(f"\n✅ Quality check: Found {len(found_indicators)} audit concepts: {', '.join(found_indicators)}")
        
        if len(found_indicators) >= 3:
            print("✅ Response quality: EXCELLENT - Shows strong audit knowledge")
        elif len(found_indicators) >= 2:
            print("⚠️  Response quality: GOOD - Shows basic audit knowledge")
        else:
            print("❌ Response quality: POOR - May need better prompting")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 80)
    print("OpenAI API Setup Test")
    print("=" * 80)
    
    success = test_openai()
    
    if success:
        print("\n" + "=" * 80)
        print("✅ READY TO BUILD LLM-BASED AGENTS!")
        print("=" * 80)
        print("\nNext steps:")
        print("  1. Implement base AuditAgent class")
        print("  2. Build Esther with GPT-4 reasoning")
        print("  3. Test against CloudRetail AWS account")
    else:
        print("\n" + "=" * 80)
        print("❌ SETUP INCOMPLETE")
        print("=" * 80)
        print("\nPlease set your OPENAI_API_KEY and try again.")
