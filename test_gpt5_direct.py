#!/usr/bin/env python3
"""
Direct test of GPT-5 API to see if we have access.
"""

import os
from openai import OpenAI

def test_gpt5():
    """Test GPT-5 API directly."""
    
    print("\n" + "=" * 80)
    print("TESTING GPT-5 API ACCESS")
    print("=" * 80)
    print()
    
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not set")
        return False
    
    print(f"✓ API key found")
    print()
    
    client = OpenAI(api_key=api_key)
    
    # Try different GPT-5 model names
    model_names = [
        "gpt-5",
        "gpt-5-preview",
        "gpt-5-turbo",
        "o1",
        "o1-preview",
        "o1-mini"
    ]
    
    for model_name in model_names:
        print(f"Testing model: {model_name}")
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "user", "content": "Say 'test successful' and nothing else."}
                ],
                max_completion_tokens=10
            )
            
            result = response.choices[0].message.content
            print(f"  ✅ SUCCESS! Model works: {model_name}")
            print(f"  Response: {result}")
            print(f"  Tokens: {response.usage.total_tokens}")
            print()
            return True
            
        except Exception as e:
            error_msg = str(e)
            if "does not exist" in error_msg or "model_not_found" in error_msg:
                print(f"  ❌ Model not found: {model_name}")
            elif "access" in error_msg.lower() or "permission" in error_msg.lower():
                print(f"  ❌ No access to: {model_name}")
            else:
                print(f"  ❌ Error: {error_msg[:100]}")
            print()
    
    print("=" * 80)
    print("❌ None of the GPT-5 model names worked")
    print()
    print("This means either:")
    print("  1. Your API key doesn't have GPT-5 access yet")
    print("  2. GPT-5 uses a different model name")
    print("  3. GPT-5 isn't publicly available yet")
    print()
    print("RECOMMENDATION: Use GPT-4 Turbo for all agents for now")
    print("=" * 80)
    return False


if __name__ == "__main__":
    test_gpt5()
