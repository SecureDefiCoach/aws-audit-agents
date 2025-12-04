"""
Launch dashboard with pre-created agents.

This script creates the audit team and launches the web dashboard
so you can see and monitor the agents.
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.agent_factory import AgentFactory
from src.web.agent_dashboard import run_dashboard


def main():
    """Create agents and launch dashboard."""
    
    print("\n" + "=" * 80)
    print("CREATING AUDIT TEAM")
    print("=" * 80)
    print()
    
    # Check for API key
    if not os.environ.get('OPENAI_API_KEY'):
        print("⚠️  OPENAI_API_KEY not set.")
        print("   Agents will be created but won't be able to use LLMs.")
        print("   Set it with: export OPENAI_API_KEY='your-key-here'")
        print()
    
    try:
        # Create the audit team
        factory = AgentFactory("config/agent_models.yaml")
        
        print("Creating agents from configuration...")
        print()
        
        team = factory.create_audit_team()
        
        print()
        print(f"✓ Successfully created {len(team)} agents!")
        print()
        print("Agents created:")
        for name, agent in team.items():
            print(f"  • {agent.name} ({agent.role}) - {agent.llm.model}")
        print()
        
        # Optionally set some goals to make it more interesting
        print("Setting example goals for demonstration...")
        team['esther'].set_goal("Assess IAM risks for CloudRetail Inc")
        team['chuck'].set_goal("Evaluate data encryption controls")
        team['victor'].set_goal("Review logging and monitoring configuration")
        print("✓ Goals set for senior auditors")
        print()
        
        # Launch dashboard
        print("=" * 80)
        print("LAUNCHING WEB DASHBOARD")
        print("=" * 80)
        print()
        print("Dashboard will open at: http://127.0.0.1:5000")
        print()
        print("Features:")
        print("  • Click any agent card to see detailed configuration")
        print("  • View agent attributes, tools, and settings")
        print("  • Monitor LLM usage and costs")
        print("  • Inspect agent memory and actions")
        print()
        print("Press Ctrl+C to stop the server")
        print("=" * 80)
        print()
        
        run_dashboard(
            agent_team=team,
            config_path="config/agent_models.yaml",
            host='127.0.0.1',
            port=5000,
            debug=True
        )
    
    except FileNotFoundError as e:
        print(f"\n❌ Error: Configuration file not found")
        print(f"   {e}")
        print()
        print("Make sure you're running from the project root directory:")
        print("  cd /path/to/aws-audit-agents")
        print("  python examples/dashboard_with_agents.py")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ Error creating agents: {e}")
        print()
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
