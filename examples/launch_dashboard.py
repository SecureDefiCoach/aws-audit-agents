"""
Launch the Agent Dashboard web interface.

This starts a Flask web server that provides a visual interface for:
- Monitoring agent status and progress
- Viewing agent configuration
- Tracking LLM costs
- Inspecting agent memory and actions
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.agent_factory import AgentFactory
from src.web.agent_dashboard import run_dashboard


def main():
    """Launch the agent dashboard."""
    
    print("\n" + "=" * 80)
    print("AGENT DASHBOARD LAUNCHER")
    print("=" * 80)
    print()
    
    # Check for API key
    if not os.environ.get('OPENAI_API_KEY'):
        print("⚠️  OPENAI_API_KEY not set.")
        print("   The dashboard will work, but agents won't be able to use LLMs.")
        print()
    
    # Option 1: Launch with existing agents
    print("Option 1: Launch with pre-created agents")
    print("   This creates the audit team and starts monitoring them")
    print()
    
    try:
        factory = AgentFactory("config/agent_models.yaml")
        team = factory.create_audit_team()
        
        print("\n✓ Audit team created successfully")
        print(f"  {len(team)} agents ready to monitor")
        print()
        
        # Launch dashboard
        run_dashboard(
            agent_team=team,
            config_path="config/agent_models.yaml",
            host='127.0.0.1',
            port=5000,
            debug=True
        )
    
    except FileNotFoundError:
        print("\n⚠️  Configuration file not found: config/agent_models.yaml")
        print("   Launching dashboard without agents...")
        print()
        
        # Launch empty dashboard
        run_dashboard(
            agent_team={},
            config_path="config/agent_models.yaml",
            host='127.0.0.1',
            port=5000,
            debug=True
        )
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("   Launching dashboard in minimal mode...")
        print()
        
        # Launch empty dashboard
        run_dashboard(
            agent_team={},
            config_path="config/agent_models.yaml",
            host='127.0.0.1',
            port=5000,
            debug=True
        )


if __name__ == "__main__":
    main()
