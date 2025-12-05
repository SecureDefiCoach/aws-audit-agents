"""
Test the chat feature in the dashboard.

This script verifies that:
1. The dashboard loads successfully
2. Agents are created and available
3. The chat API endpoint works
"""

import os
import sys
import requests
import json

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.agents.agent_factory import AgentFactory


def test_chat_api():
    """Test the chat API endpoint."""
    
    print("\n" + "=" * 80)
    print("TESTING CHAT FEATURE")
    print("=" * 80)
    print()
    
    # Check if dashboard is running
    dashboard_url = "http://127.0.0.1:5000"
    
    try:
        response = requests.get(f"{dashboard_url}/api/agents", timeout=2)
        if response.status_code != 200:
            print("❌ Dashboard is not running or not responding correctly")
            print(f"   Status code: {response.status_code}")
            print()
            print("Please start the dashboard first:")
            print("   python3 examples/launch_dashboard.py")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Dashboard is not running")
        print()
        print("Please start the dashboard first:")
        print("   python3 examples/launch_dashboard.py")
        return False
    
    print("✓ Dashboard is running")
    
    # Get list of agents
    agents = response.json()
    print(f"✓ Found {len(agents)} agents")
    
    if len(agents) == 0:
        print("❌ No agents available to test")
        return False
    
    # Test chat with Neil (GPT-4 Turbo - confirmed working)
    test_agent = "neil"
    test_message = "Hello Neil, can you briefly introduce yourself?"
    
    print(f"\n📤 Sending test message to {test_agent}:")
    print(f"   '{test_message}'")
    print()
    
    try:
        chat_response = requests.post(
            f"{dashboard_url}/api/agents/{test_agent}/chat",
            json={"message": test_message},
            timeout=30
        )
        
        if chat_response.status_code != 200:
            print(f"❌ Chat API returned error: {chat_response.status_code}")
            print(f"   Response: {chat_response.text}")
            return False
        
        data = chat_response.json()
        
        if "error" in data:
            print(f"❌ Chat API returned error: {data['error']}")
            return False
        
        print("✓ Chat API responded successfully")
        print()
        print("📥 Agent Response:")
        print("-" * 80)
        print(data.get("response", "No response"))
        print("-" * 80)
        print()
        print(f"📊 Stats:")
        print(f"   Tokens used: {data.get('tokens_used', 0)}")
        print(f"   Cost: ${data.get('cost', 0):.6f}")
        print()
        
        return True
    
    except requests.exceptions.Timeout:
        print("❌ Request timed out (agent took too long to respond)")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Run the test."""
    
    # Check for API key
    if not os.environ.get('OPENAI_API_KEY'):
        print("\n⚠️  OPENAI_API_KEY not set")
        print("   Please set your OpenAI API key:")
        print("   export OPENAI_API_KEY='your-key-here'")
        print()
        return
    
    success = test_chat_api()
    
    if success:
        print("=" * 80)
        print("✅ CHAT FEATURE TEST PASSED")
        print("=" * 80)
        print()
        print("You can now use the chat feature in the dashboard:")
        print("1. Open http://127.0.0.1:5000 in your browser")
        print("2. Click on any agent card")
        print("3. Click the 'Chat' tab")
        print("4. Start chatting with the agent!")
        print()
    else:
        print("=" * 80)
        print("❌ CHAT FEATURE TEST FAILED")
        print("=" * 80)
        print()


if __name__ == "__main__":
    main()
