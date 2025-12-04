"""
Test script to verify agent memory isolation.

This script creates multiple agents and checks if they have separate memory.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.agents.agent_factory import AgentFactory


def main():
    """Test agent memory isolation."""
    
    print("\n" + "=" * 80)
    print("TESTING AGENT MEMORY ISOLATION")
    print("=" * 80)
    print()
    
    # Create factory
    factory = AgentFactory("config/agent_models.yaml")
    
    # Create a few agents
    print("Creating agents...")
    maurice = factory.create_agent("maurice")
    esther = factory.create_agent("esther")
    chuck = factory.create_agent("chuck")
    
    print("\n" + "=" * 80)
    print("CHECKING MEMORY ISOLATION")
    print("=" * 80)
    print()
    
    # Check memory for each agent
    print(f"Maurice memory address: {id(maurice.memory)}")
    print(f"Maurice memory length: {len(maurice.memory)}")
    if maurice.memory:
        print(f"Maurice system message starts with: {maurice.memory[0]['content'][:100]}...")
    print()
    
    print(f"Esther memory address: {id(esther.memory)}")
    print(f"Esther memory length: {len(esther.memory)}")
    if esther.memory:
        print(f"Esther system message starts with: {esther.memory[0]['content'][:100]}...")
    print()
    
    print(f"Chuck memory address: {id(chuck.memory)}")
    print(f"Chuck memory length: {len(chuck.memory)}")
    if chuck.memory:
        print(f"Chuck system message starts with: {chuck.memory[0]['content'][:100]}...")
    print()
    
    # Check if they're the same object
    print("=" * 80)
    print("MEMORY OBJECT COMPARISON")
    print("=" * 80)
    print()
    print(f"Maurice and Esther share memory: {maurice.memory is esther.memory}")
    print(f"Maurice and Chuck share memory: {maurice.memory is chuck.memory}")
    print(f"Esther and Chuck share memory: {esther.memory is chuck.memory}")
    print()
    
    # Check names and roles
    print("=" * 80)
    print("AGENT IDENTITIES")
    print("=" * 80)
    print()
    print(f"Maurice: {maurice.name} - {maurice.role}")
    print(f"Esther: {esther.name} - {esther.role}")
    print(f"Chuck: {chuck.name} - {chuck.role}")
    print()
    
    # Check knowledge
    print("=" * 80)
    print("KNOWLEDGE LOADED")
    print("=" * 80)
    print()
    print(f"Maurice knowledge keys: {list(maurice.knowledge.keys())}")
    print()
    print(f"Esther knowledge keys: {list(esther.knowledge.keys())}")
    print()
    print(f"Chuck knowledge keys: {list(chuck.knowledge.keys())}")
    print()


if __name__ == "__main__":
    main()
