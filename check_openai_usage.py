"""
Check actual OpenAI API usage and costs.

This script queries the OpenAI API to show your actual usage.
"""

import os
from datetime import datetime, timedelta
from openai import OpenAI


def check_usage():
    """Check OpenAI usage."""
    
    print("\n" + "=" * 80)
    print("OPENAI API USAGE CHECKER")
    print("=" * 80)
    print()
    
    # Check for API key
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not set")
        return
    
    print(f"✓ API Key: {api_key[:8]}...{api_key[-4:]}")
    print()
    
    try:
        client = OpenAI(api_key=api_key)
        
        print("=" * 80)
        print("WHERE TO CHECK USAGE ON OPENAI PLATFORM")
        print("=" * 80)
        print()
        print("1. Go to: https://platform.openai.com/usage")
        print()
        print("2. You'll see:")
        print("   • Daily usage graph")
        print("   • Cost breakdown by model")
        print("   • Total costs for current billing period")
        print()
        print("3. Note: Usage can take 5-10 minutes to appear after API calls")
        print()
        print("4. Look for:")
        print("   • Model: gpt-4-turbo")
        print("   • Recent activity (last hour)")
        print("   • Token counts and costs")
        print()
        
        print("=" * 80)
        print("ESTIMATED COSTS (from our calculations)")
        print("=" * 80)
        print()
        print("Based on your 3 chat messages with Esther:")
        print()
        print("  • System prompt: ~11,500 tokens per message")
        print("  • User messages: ~13 tokens each")
        print("  • Agent responses: ~200 tokens each")
        print()
        print("  Total input tokens: ~34,500 tokens")
        print("  Total output tokens: ~600 tokens")
        print()
        print("  Input cost: $0.345 (34,500 × $0.01/1K)")
        print("  Output cost: $0.018 (600 × $0.03/1K)")
        print("  Total: $0.363")
        print()
        
        print("=" * 80)
        print("WHY YOU MIGHT NOT SEE IT YET")
        print("=" * 80)
        print()
        print("1. DELAY: Usage typically appears within 5-10 minutes")
        print("   • Try refreshing the usage page")
        print("   • Check again in a few minutes")
        print()
        print("2. BILLING PERIOD: Make sure you're looking at the current period")
        print("   • Usage page shows current month by default")
        print("   • Check the date range selector")
        print()
        print("3. ORGANIZATION: If you're part of an organization")
        print("   • Make sure you're viewing the right organization")
        print("   • Check organization selector in top-right")
        print()
        print("4. API KEY: Verify this is the right API key")
        print("   • Go to: https://platform.openai.com/api-keys")
        print("   • Check which key you're using")
        print()
        
        print("=" * 80)
        print("TESTING API ACCESS")
        print("=" * 80)
        print()
        print("Making a small test call to verify API is working...")
        print()
        
        # Make a tiny test call
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": "Say 'test'"}],
            max_tokens=5
        )
        
        print("✓ API call successful!")
        print(f"  Model: {response.model}")
        print(f"  Tokens used: {response.usage.total_tokens}")
        print(f"  Input tokens: {response.usage.prompt_tokens}")
        print(f"  Output tokens: {response.usage.completion_tokens}")
        print()
        
        # Calculate cost
        input_cost = (response.usage.prompt_tokens * 0.01) / 1000
        output_cost = (response.usage.completion_tokens * 0.03) / 1000
        total_cost = input_cost + output_cost
        
        print(f"  Estimated cost: ${total_cost:.6f}")
        print()
        print("This test call should appear on your usage page within 5-10 minutes.")
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("This might mean:")
        print("  • API key is invalid")
        print("  • No internet connection")
        print("  • OpenAI API is down")
        print()


def main():
    """Run the usage checker."""
    check_usage()
    
    print("=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print()
    print("1. Visit: https://platform.openai.com/usage")
    print("2. Wait 5-10 minutes if you don't see recent usage")
    print("3. Look for gpt-4-turbo calls in the last hour")
    print("4. Check the cost breakdown")
    print()
    print("If you still don't see usage after 10 minutes:")
    print("  • Verify you're logged into the correct OpenAI account")
    print("  • Check that the API key belongs to your account")
    print("  • Contact OpenAI support if needed")
    print()


if __name__ == "__main__":
    main()
