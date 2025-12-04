"""
Test script to verify dashboard agent initialization.

This simulates what launch_dashboard.py does and checks agent memory.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.agents.agent_factory import AgentFactory


def main():
    """Test dashboard agent initialization."""
    
    print("\n" + "=" * 80)
    print("SIMULATING DASHBOARD LAUNCH")
    print("=" * 80)
    print()
    
    # This is what launch_dashboard.py does
    factory = AgentFactory("config/agent_models.yaml")
    team = factory.create_audit_team()
    
    print("\n" + "=" * 80)
    print("CHECKING TEAM DICTIONARY")
    print("=" * 80)
    print()
    
    for agent_name, agent in team.items():
        print(f"\nAgent key: '{agent_name}'")
        print(f"  Agent object: {agent}")
        print(f"  Agent.name: {agent.name}")
        print(f"  Agent.role: {agent.role}")
        print(f"  Memory address: {id(agent.memory)}")
        print(f"  Memory length: {len(agent.memory)}")
        if agent.memory:
            system_msg = agent.memory[0].get('content', '')
            first_line = system_msg.split('\n')[0] if system_msg else ''
            print(f"  First line of system message: {first_line}")
    
    print("\n" + "=" * 80)
    print("CHECKING FOR SHARED MEMORY")
    print("=" * 80)
    print()
    
    agents_list = list(team.values())
    for i in range(len(agents_list)):
        for j in range(i + 1, len(agents_list)):
            agent1 = agents_list[i]
            agent2 = agents_list[j]
            if agent1.memory is agent2.memory:
                print(f"⚠️  WARNING: {agent1.name} and {agent2.name} SHARE MEMORY!")
            else:
                print(f"✓ {agent1.name} and {agent2.name} have separate memory")


if __name__ == "__main__":
    main()
