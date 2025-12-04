#!/usr/bin/env python3
"""Test the LLM client with GPT-4"""

from src.agents.llm_client import LLMClient

def test_llm_client():
    """Test LLM client with a simple audit question"""
    
    print("=" * 80)
    print("Testing LLM Client with GPT-4")
    print("=" * 80)
    
    # Initialize client with GPT-4
    print("\n🔧 Initializing LLM client...")
    print(f"   Provider: OpenAI")
    print(f"   Model: gpt-4-turbo")
    print(f"   Rate limit: 10 calls/minute")
    
    llm = LLMClient(
        provider='openai',
        model='gpt-4-turbo',
        rate_limit=10,
        temperature=0.7
    )
    
    # Test with Esther's persona
    print("\n🧪 Testing with Esther's persona...")
    
    messages = [
        {
            'role': 'system',
            'content': '''You are Esther, a senior auditor with 15 years of experience 
            specializing in Identity and Access Management (IAM). You are professional, 
            thorough, and always document your reasoning.'''
        },
        {
            'role': 'user',
            'content': '''You've been assigned to audit CloudRetail Inc's AWS account.
            
Your goal: Assess IAM risks and document findings.

You have these tools available:
- list_iam_users: Lists all IAM users with MFA status
- check_policies: Reviews IAM policies for excessive permissions
- create_workpaper: Documents your findings

What should you do first? Explain your reasoning in 2-3 sentences.'''
        }
    ]
    
    response = llm.chat(messages, max_tokens=200)
    
    print("\n✅ Response received!")
    print(f"\n📊 Model: {response.model}")
    print(f"💰 Tokens: {response.tokens_used}")
    print(f"💵 Cost: ${response.cost:.4f}")
    
    print(f"\n🤖 Esther's response:")
    print("-" * 80)
    print(response.content)
    print("-" * 80)
    
    # Test rate limiting with multiple calls
    print("\n🧪 Testing rate limiting with 3 quick calls...")
    
    for i in range(3):
        print(f"\n   Call {i+1}/3...")
        response = llm.chat([
            {'role': 'user', 'content': f'Say "Test {i+1}" and nothing else.'}
        ], max_tokens=10)
        print(f"   Response: {response.content}")
        print(f"   Cost: ${response.cost:.4f}")
    
    # Print cost summary
    llm.print_cost_summary()
    
    print("\n" + "=" * 80)
    print("✅ LLM Client Test Complete!")
    print("=" * 80)
    print("\nNext steps:")
    print("  1. Implement base AuditAgent class")
    print("  2. Create Tool interface")
    print("  3. Build Esther agent")

if __name__ == '__main__':
    test_llm_client()
