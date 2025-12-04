"""
Test API routing to verify agents are correctly accessed.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.agents.agent_factory import AgentFactory
from src.agents.agent_monitor import AgentMonitor


def main():
    """Test API routing."""
    
    print("\n" + "=" * 80)
    print("TESTING API ROUTING")
    print("=" * 80)
    print()
    
    # Create factory and team
    factory = AgentFactory("config/agent_models.yaml")
    team = factory.create_audit_team()
    
    # Create monitor
    monitor = AgentMonitor(team)
    
    print("\n" + "=" * 80)
    print("TESTING get_team_summary()")
    print("=" * 80)
    print()
    
    summaries = monitor.get_team_summary()
    for summary in summaries:
        print(f"Key: '{summary['key']}' → Name: '{summary['name']}'")
    
    print("\n" + "=" * 80)
    print("TESTING get_agent_info()")
    print("=" * 80)
    print()
    
    # Test with lowercase keys
    test_keys = ['maurice', 'esther', 'chuck']
    
    for key in test_keys:
        print(f"\nTesting key: '{key}'")
        info = monitor.get_agent_info(key)
        if 'error' in info:
            print(f"  ❌ ERROR: {info['error']}")
        else:
            print(f"  ✓ Name: {info['name']}")
            print(f"  ✓ Role: {info['role']}")
    
    print("\n" + "=" * 80)
    print("TESTING get_agent_memory()")
    print("=" * 80)
    print()
    
    for key in test_keys:
        print(f"\nTesting key: '{key}'")
        memory = monitor.get_agent_memory(key, last_n=1)
        if not memory:
            print(f"  ❌ No memory found")
        else:
            first_msg = memory[0].get('content', '')
            first_line = first_msg.split('\n')[0] if first_msg else ''
            print(f"  ✓ First line: {first_line}")


if __name__ == "__main__":
    main()
