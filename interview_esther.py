#!/usr/bin/env python3
"""
Interactive interview with Esther - Senior Auditor

This script allows you to have a conversation with Esther to understand
her capabilities, ask questions, and test her responses.
"""

from src.agents.agent_factory import AgentFactory


def interview_esther():
    """Interactive interview session with Esther."""
    print("\n" + "=" * 80)
    print("INTERVIEW WITH ESTHER - SENIOR AUDITOR")
    print("=" * 80)
    print("\nInitializing Esther...")
    
    # Create agent factory and instantiate Esther
    factory = AgentFactory()
    esther = factory.create_agent("esther")
    
    print("\n✓ Esther is ready for interview")
    print("\nYou can ask Esther questions about:")
    print("  - Her role and capabilities")
    print("  - How she approaches audit work")
    print("  - What tools she has access to")
    print("  - Her knowledge base")
    print("  - Anything else related to auditing")
    print("\nType 'exit' or 'quit' to end the interview")
    print("=" * 80)
    
    # Interview loop
    while True:
        print("\n" + "-" * 80)
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'q']:
            print("\n✓ Interview ended. Thank you!")
            break
        
        if not user_input:
            continue
        
        # Send message to Esther
        print("\nEsther: ", end="", flush=True)
        try:
            response = esther.process_message(user_input)
            print(response)
        except Exception as e:
            print(f"\n[Error: {str(e)}]")
            print("Esther encountered an issue. Please try rephrasing your question.")


if __name__ == "__main__":
    try:
        interview_esther()
    except KeyboardInterrupt:
        print("\n\n✓ Interview interrupted. Goodbye!")
    except Exception as e:
        print(f"\n\n✗ Error: {str(e)}")
        print("\nMake sure you have:")
        print("  1. Set up your OpenAI API key")
        print("  2. Installed all requirements (pip install -r requirements.txt)")
