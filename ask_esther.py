#!/usr/bin/env python3
"""
Quick script to ask Esther a single question and get her response.
"""

import sys
from src.agents.agent_factory import AgentFactory


def ask_esther(question: str):
    """Ask Esther a question and print her response."""
    print("\n" + "=" * 80)
    print("ASKING ESTHER")
    print("=" * 80)
    print("\nInitializing Esther...")
    
    # Create Esther
    factory = AgentFactory()
    esther = factory.create_agent("esther")
    
    print("✓ Esther initialized\n")
    print("-" * 80)
    print(f"\nYou: {question}\n")
    print("-" * 80)
    print("\nEsther: ", end="", flush=True)
    
    # Get response
    try:
        # Add the question to Esther's memory as a user message
        esther.memory.append({"role": "user", "content": question})
        
        print("Calling LLM API...")
        print(f"Model: {esther.llm.model}")
        print(f"Provider: {esther.llm.provider}")
        print(f"Messages in memory: {len(esther.memory)}")
        print()
        
        # Get LLM response
        response = esther.llm.chat(esther.memory)
        
        print(f"✓ API call successful")
        print(f"  Tokens used: {response.tokens_used}")
        print(f"  Cost: ${response.cost:.4f}")
        print(f"  Response length: {len(response.content)} characters")
        print()
        
        # Add response to memory
        esther.memory.append({"role": "assistant", "content": response.content})
        
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
    question = "Esther, welcome to the audit team. Your first task will be to perform a risk assessment, do you know how to proceed, when the task starts?"
    
    # Allow question from command line
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
    
    ask_esther(question)
