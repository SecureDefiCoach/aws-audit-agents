"""
Example: Monitoring and inspecting agent attributes.

This demonstrates how to use the AgentMonitor to:
- View agent configuration and state
- Track agent progress
- Inspect memory and actions
- Monitor LLM costs
- Export agent state
"""

import os
from src.agents.agent_factory import AgentFactory
from src.agents.agent_monitor import AgentMonitor


def main():
    """Demonstrate agent monitoring capabilities."""
    
    # Check for API key
    if not os.environ.get('OPENAI_API_KEY'):
        print("\n⚠️  OPENAI_API_KEY not set. Please set it to run this example.")
        return
    
    print("\n" + "=" * 80)
    print("AGENT MONITORING DEMO")
    print("=" * 80)
    print()
    
    # Create audit team
    print("Creating audit team...")
    factory = AgentFactory("config/agent_models.yaml")
    team = factory.create_audit_team()
    
    # Create monitor
    monitor = AgentMonitor(team)
    
    print("\n" + "=" * 80)
    print("MONITORING CAPABILITIES")
    print("=" * 80)
    print()
    
    # 1. Team Summary
    print("1. TEAM SUMMARY")
    print("   View all agents at a glance")
    print()
    monitor.print_team_summary()
    
    # 2. Individual Agent Info
    print("\n" + "=" * 80)
    print("2. INDIVIDUAL AGENT DETAILS")
    print("   Deep dive into a specific agent")
    print()
    monitor.print_agent_info("esther")
    
    # 3. Set a goal and monitor progress
    print("\n" + "=" * 80)
    print("3. MONITORING AGENT PROGRESS")
    print("   Track what an agent is doing")
    print()
    
    esther = team['esther']
    print("Setting goal for Esther...")
    esther.set_goal("Assess IAM risks for CloudRetail Inc")
    
    print("\nAgent info after setting goal:")
    monitor.print_agent_info("esther")
    
    # 4. View agent memory
    print("\n" + "=" * 80)
    print("4. AGENT MEMORY")
    print("   See the conversation history with the LLM")
    print()
    monitor.print_agent_memory("esther", last_n=3)
    
    # 5. View agent actions
    print("\n" + "=" * 80)
    print("5. AGENT ACTIONS")
    print("   See what actions the agent has taken")
    print()
    monitor.print_agent_actions("esther", last_n=5)
    
    # 6. Cost breakdown
    print("\n" + "=" * 80)
    print("6. COST BREAKDOWN")
    print("   Track LLM costs by agent and model")
    print()
    monitor.print_cost_breakdown()
    
    # 7. Export agent state
    print("\n" + "=" * 80)
    print("7. EXPORT AGENT STATE")
    print("   Save agent state to JSON for analysis")
    print()
    monitor.export_agent_state("esther", "output/esther_state.json")
    
    # 8. Interactive mode
    print("\n" + "=" * 80)
    print("8. INTERACTIVE MONITORING")
    print("=" * 80)
    print()
    print("You can also use interactive mode for real-time monitoring:")
    print()
    print("  monitor = AgentMonitor(team)")
    print("  monitor.interactive_monitor()")
    print()
    print("This provides a CLI interface for inspecting agents during execution.")
    print()
    
    # Demonstrate programmatic access
    print("\n" + "=" * 80)
    print("PROGRAMMATIC ACCESS")
    print("=" * 80)
    print()
    print("You can also access agent attributes programmatically:")
    print()
    
    # Get agent info as dict
    info = monitor.get_agent_info("esther")
    print(f"Esther's current goal: {info['current_goal']}")
    print(f"Esther's status: {info['goal_status']}")
    print(f"Esther's LLM cost: ${info['llm_cost']:.4f}")
    print()
    
    # Get cost breakdown
    breakdown = monitor.get_cost_breakdown()
    print(f"Total team cost: ${breakdown['total_cost']:.4f}")
    print(f"GPT-5 cost: ${breakdown['by_model'].get('gpt-5', {}).get('total_cost', 0):.4f}")
    print(f"GPT-4 Turbo cost: ${breakdown['by_model'].get('gpt-4-turbo', {}).get('total_cost', 0):.4f}")
    print()
    
    print("=" * 80)
    print("KEY BENEFITS")
    print("=" * 80)
    print()
    print("1. VISIBILITY")
    print("   - See exactly what each agent is doing")
    print("   - Track progress toward goals")
    print("   - Inspect reasoning process")
    print()
    print("2. DEBUGGING")
    print("   - View agent memory to understand decisions")
    print("   - See action history to trace behavior")
    print("   - Export state for detailed analysis")
    print()
    print("3. COST CONTROL")
    print("   - Monitor LLM costs in real-time")
    print("   - Break down costs by agent and model")
    print("   - Identify expensive operations")
    print()
    print("4. AUDIT TRAIL")
    print("   - Complete record of agent actions")
    print("   - Timestamps for all activities")
    print("   - Export for compliance/review")
    print()


if __name__ == "__main__":
    main()
