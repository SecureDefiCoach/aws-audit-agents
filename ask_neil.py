#!/usr/bin/env python3
"""
Quick script to ask Neil a single question and get his response.
Neil uses GPT-4 Turbo (not GPT-5) so this is a good test.
"""

import sys
from src.agents.agent_factory import AgentFactory


def ask_neil(question: str):
    """Ask Neil a question and print his response."""
    print("\n" + "=" * 80)
    print("ASKING NEIL (GPT-4 Turbo)")
    print("=" * 80)
    print("\nInitializing Neil...")
    
    # Create Neil
    factory = AgentFactory()
    neil = factory.create_agent("neil")
    
    print("✓ Neil initialized\n")
    print("-" * 80)
    print(f"\nYou: {question}\n")
    print("-" * 80)
    print("\nNeil: ", end="", flush=True)
    
    # Get response
    try:
        # Add the question to Neil's memory as a user message
        neil.memory.append({"role": "user", "content": question})
        
        print("Calling LLM API...")
        print(f"Model: {neil.llm.model}")
        print(f"Provider: {neil.llm.provider}")
        print(f"Messages in memory: {len(neil.memory)}")
        print()
        
        # Get LLM response
        response = neil.llm.chat(neil.memory)
        
        print(f"✓ API call successful")
        print(f"  Tokens used: {response.tokens_used}")
        print(f"  Cost: ${response.cost:.4f}")
        print(f"  Response length: {len(response.content)} characters")
        print()
        
        # Add response to memory
        neil.memory.append({"role": "assistant", "content": response.content})
        
        if not response.content or response.content.strip() == "":
            print("[WARNING: Response is empty!]")
            print()
        
        print(response.content)
        print("\n" + "=" * 80)
        return response.content
    except Exception as e:
        print(f"\n[Error: {str(e)}]")
        print("\nMake sure you have:")
        print("  1. Set OPENAI_API_KEY environment variable")
        print("  2. Installed requirements: pip install -r requirements.txt")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    # Default question
    question = "Neil, welcome to the audit team. Can you briefly introduce yourself and tell me what your role is?"
    
    # Allow question from command line
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
    
    ask_neil(question)
