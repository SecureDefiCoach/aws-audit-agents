#!/usr/bin/env python3
"""
Quick test to verify OpenAI API key is working.
"""

import os
import sys

def test_api_key():
    """Test if OpenAI API key is set and working."""
    
    print("\n" + "=" * 80)
    print("TESTING OPENAI API KEY")
    print("=" * 80)
    print()
    
    # Check if key is set
    api_key = os.environ.get('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ OPENAI_API_KEY environment variable is NOT set")
        print()
        print("To set it:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        print()
        return False
    
    print(f"✓ OPENAI_API_KEY is set (length: {len(api_key)} characters)")
    print(f"  Starts with: {api_key[:10]}...")
    print()
    
    # Try to import OpenAI
    try:
        from openai import OpenAI
        print("✓ OpenAI library imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import OpenAI library: {e}")
        print()
        print("Install it with:")
        print("  pip install openai")
        return False
    
    # Try to make a simple API call
    print()
    print("Testing API call...")
    try:
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "user", "content": "Say 'API test successful' and nothing else."}
            ],
            max_tokens=10
        )
        
        result = response.choices[0].message.content
        print(f"✓ API call successful!")
        print(f"  Response: {result}")
        print()
        print("=" * 80)
        print("✅ ALL TESTS PASSED - Your API key is working!")
        print("=" * 80)
        return True
        
    except Exception as e:
        print(f"❌ API call failed: {e}")
        print()
        print("This could mean:")
        print("  1. Invalid API key")
        print("  2. Network connectivity issue")
        print("  3. OpenAI service issue")
        return False


if __name__ == "__main__":
    success = test_api_key()
    sys.exit(0 if success else 1)
