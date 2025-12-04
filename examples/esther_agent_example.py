"""
Example: Esther Agent - IAM Risk Assessment

This example demonstrates Esther, an autonomous LLM-powered agent who
assesses IAM risks for AWS accounts.

Esther will:
1. Query IAM to understand the account structure
2. Collect evidence about users, roles, and policies
3. Analyze access controls and identify risks
4. Document findings in a professional workpaper
5. Adapt her approach based on what she discovers
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.esther_agent import EstherAgent
from src.agents.llm_client import LLMClient
from src.aws.iam_client import IAMClient


def main():
    """Run Esther to assess IAM risks."""
    
    print("\n" + "=" * 80)
    print("ESTHER - IAM RISK ASSESSMENT")
    print("=" * 80)
    print()
    
    # Check for API key
    if not os.environ.get('OPENAI_API_KEY'):
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print()
        print("Please set your OpenAI API key:")
        print("  export OPENAI_API_KEY='your-key-here'")
        print()
        print("Or use Ollama for local development:")
        print("  See LLM_AGENTS_QUICKSTART.md for setup instructions")
        sys.exit(1)
    
    try:
        # Create LLM client
        print("Initializing Esther...")
        llm = LLMClient(
            provider="openai",
            model="gpt-4-turbo",  # Use GPT-4 Turbo for cost-effective testing
            temperature=0.7
        )
        
        # Create IAM client (read-only)
        iam_client = IAMClient(read_only=True)
        
        # Create Esther
        esther = EstherAgent(
            llm_client=llm,
            iam_client=iam_client,
            output_dir="output"
        )
        
        print(f"✓ {esther.name} initialized")
        print(f"  Role: {esther.role}")
        print(f"  LLM: {esther.llm.model}")
        print(f"  Tools: {', '.join(esther.tools.keys())}")
        print()
        
        # Set goal
        print("=" * 80)
        print("SETTING GOAL")
        print("=" * 80)
        print()
        
        goal = "Assess IAM risks for CloudRetail Inc and document findings in a workpaper"
        esther.set_goal(goal)
        
        print()
        print("=" * 80)
        print("AUTONOMOUS EXECUTION")
        print("=" * 80)
        print()
        print("Esther will now work autonomously to achieve her goal.")
        print("She will reason about what to do, collect evidence, and document findings.")
        print()
        
        # Run autonomously
        result = esther.run_autonomously(max_iterations=15)
        
        print()
        print("=" * 80)
        print("EXECUTION COMPLETE")
        print("=" * 80)
        print()
        print(f"Status: {result['status']}")
        print(f"Iterations: {result['iterations']}")
        print(f"Actions taken: {result['actions_taken']}")
        print()
        
        # Show summary
        summary = esther.get_summary()
        print("=" * 80)
        print("ESTHER'S WORK SUMMARY")
        print("=" * 80)
        print()
        print(f"Goal: {summary['current_goal']}")
        print(f"Status: {summary['goal_status']}")
        print(f"Workpapers created: {summary['workpapers_created']}")
        print(f"Evidence collected: {summary['evidence_collected']}")
        print(f"Total actions: {summary['actions_taken']}")
        print()
        
        # Show action history
        if esther.action_history:
            print("=" * 80)
            print("ACTION HISTORY")
            print("=" * 80)
            print()
            for i, action in enumerate(esther.action_history[-10:], 1):  # Last 10 actions
                print(f"{i}. [{action.action_type}] {action.description}")
                if action.action_type == "reason" and action.result:
                    print(f"   Reasoning: {action.result[:100]}...")
            print()
        
        # Show workpapers created
        if esther.workpapers_created:
            print("=" * 80)
            print("WORKPAPERS CREATED")
            print("=" * 80)
            print()
            for wp in esther.workpapers_created:
                print(f"  • {wp}")
                print(f"    Location: output/workpapers/{wp.replace(' ', '_')}.md")
            print()
        
        # Show evidence collected
        if esther.evidence_collected:
            print("=" * 80)
            print("EVIDENCE COLLECTED")
            print("=" * 80)
            print()
            for ev in esther.evidence_collected:
                print(f"  • {ev}")
                print(f"    Location: output/evidence/{ev.replace(' ', '_')}.json")
            print()
        
        print("=" * 80)
        print("NEXT STEPS")
        print("=" * 80)
        print()
        print("1. Review the workpaper in output/workpapers/")
        print("2. Examine the evidence in output/evidence/")
        print("3. Check Esther's reasoning in the action history above")
        print("4. Run the dashboard to see Esther's state:")
        print("   python examples/dashboard_with_agents.py")
        print()
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
