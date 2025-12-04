"""
Test Enhanced Dashboard with Knowledge and Tasks

This script creates agents with knowledge and tasks, then launches
the enhanced dashboard to view all capabilities.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.agent_factory import AgentFactory
from src.agents.tools import TaskManagementTool
from src.web.agent_dashboard import run_dashboard


def setup_test_data():
    """Create test agents with knowledge and tasks"""
    print("Setting up test data...")
    
    # Create agent factory
    factory = AgentFactory("config/agent_models.yaml")
    
    # Create agents with knowledge
    print("\n📚 Creating agents with knowledge...")
    maurice = factory.create_agent("maurice", load_knowledge=True)
    esther = factory.create_agent("esther", load_knowledge=True)
    chuck = factory.create_agent("chuck", load_knowledge=True)
    hillel = factory.create_agent("hillel", load_knowledge=True)
    victor = factory.create_agent("victor", load_knowledge=True)
    neil = factory.create_agent("neil", load_knowledge=True)
    juman = factory.create_agent("juman", load_knowledge=True)
    
    # Add task management tool to all agents
    task_tool = TaskManagementTool()
    maurice.register_tool(task_tool)
    esther.register_tool(task_tool)
    hillel.register_tool(task_tool)
    victor.register_tool(task_tool)
    neil.register_tool(task_tool)
    juman.register_tool(task_tool)
    
    print("✅ All 7 agents created with knowledge and tasks")
    
    return {
        "maurice": maurice,
        "esther": esther,
        "chuck": chuck,
        "hillel": hillel,
        "victor": victor,
        "neil": neil,
        "juman": juman
    }


def main():
    print("=" * 80)
    print("ENHANCED AGENT DASHBOARD TEST")
    print("=" * 80)
    
    # Setup test data
    team = setup_test_data()
    
    print("\n" + "=" * 80)
    print("LAUNCHING DASHBOARD")
    print("=" * 80)
    print()
    print("The dashboard now includes:")
    print("  ✅ Info - Basic agent information")
    print("  ✅ Capabilities - Tools and AWS access")
    print("  ✅ Knowledge - Loaded procedures")
    print("  ✅ Tasks - Current, completed, delegated")
    print("  ✅ Actions - Action history")
    print("  ✅ Memory - Conversation memory")
    print()
    print("Click on any agent card to see detailed information!")
    print()
    
    # Run dashboard
    run_dashboard(
        agent_team=team,
        config_path="config/agent_models.yaml",
        host='127.0.0.1',
        port=5000,
        debug=True
    )


if __name__ == "__main__":
    main()
