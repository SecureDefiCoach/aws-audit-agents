"""
Quick test to verify Esther can be created and viewed in dashboard.

This script creates just Esther and shows her in the dashboard.
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.agent_factory import AgentFactory
from src.web.agent_dashboard import run_dashboard


def main():
    """Create Esther and launch dashboard."""
    
    print("\n" + "=" * 80)
    print("CREATING ESTHER")
    print("=" * 80)
    print()
    
    # Check for API key
    if not os.environ.get('OPENAI_API_KEY'):
        print("⚠️  OPENAI_API_KEY not set.")
        print("   Esther will be created but won't be able to use LLMs.")
        print("   Set it with: export OPENAI_API_KEY='your-key-here'")
        print()
    
    try:
        # Create the agent factory
        factory = AgentFactory("config/agent_models.yaml")
        
        print("Creating Esther from configuration...")
        print()
        
        # Create just Esther
        esther = factory.create_agent("esther")
        
        print()
        print(f"✓ Successfully created Esther!")
        print()
        print("Agent details:")
        print(f"  • Name: {esther.name}")
        print(f"  • Role: {esther.role}")
        print(f"  • LLM Model: {esther.llm.model}")
        print(f"  • Control Domains: {', '.join(esther.control_domains)}")
        print(f"  • Staff Auditor: {esther.staff_auditor}")
        print(f"  • Tools: {', '.join(esther.tools.keys())}")
        print()
        
        # Set a goal to make it interesting
        print("Setting example goal for demonstration...")
        esther.set_goal("Assess IAM risks for CloudRetail Inc")
        print("✓ Goal set")
        print()
        
        # Create team dict with just Esther
        team = {"esther": esther}
        
        # Launch dashboard
        print("=" * 80)
        print("LAUNCHING WEB DASHBOARD")
        print("=" * 80)
        print()
        print("Dashboard will open at: http://127.0.0.1:5000")
        print()
        print("Features:")
        print("  • Click Esther's card to see detailed configuration")
        print("  • View her tools (query_iam, create_workpaper, store_evidence)")
        print("  • See her current goal and status")
        print("  • Inspect her attributes and settings")
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
        print("  python3 examples/test_esther_in_dashboard.py")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ Error creating Esther: {e}")
        print()
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
