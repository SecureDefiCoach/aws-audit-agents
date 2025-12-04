"""
Example: Using different LLM models for different agent levels.

This demonstrates how to configure:
- GPT-5 for senior auditors (Esther, Chuck, Victor) - more sophisticated reasoning
- GPT-4 Turbo for staff auditors (Hillel, Neil, Juman) - cost-effective for routine tasks
- GPT-4 Turbo for Maurice (Audit Manager) - reviews and approvals

This mirrors real-world audit teams where senior staff have more expertise.

Two approaches are shown:
1. Using AgentFactory with YAML configuration (recommended)
2. Manual agent creation (for custom scenarios)
"""

import os
from src.agents.agent_factory import AgentFactory, create_agent_with_model


def demo_factory_approach():
    """Demonstrate using AgentFactory with YAML configuration."""
    print("\n" + "=" * 80)
    print("APPROACH 1: Using AgentFactory (Recommended)")
    print("=" * 80)
    print()
    print("Loading agent configuration from config/agent_models.yaml")
    print()
    
    # Create factory
    factory = AgentFactory("config/agent_models.yaml")
    
    # Print configuration summary
    factory.print_team_summary()
    
    # Create entire team
    team = factory.create_audit_team()
    
    return team


def demo_manual_approach():
    """Demonstrate manual agent creation."""
    print("\n" + "=" * 80)
    print("APPROACH 2: Manual Agent Creation")
    print("=" * 80)
    print()
    print("Creating agents manually with specific models:")
    print()
    
    team = {}
    
    # Create Senior Auditors with GPT-5
    print("--- SENIOR AUDITORS (GPT-5) ---")
    team['esther'] = create_agent_with_model(
        name="Esther",
        role="Senior Auditor - IAM & Logical Access",
        model="gpt-5"
    )
    
    team['chuck'] = create_agent_with_model(
        name="Chuck",
        role="Senior Auditor - Data Encryption & Network",
        model="gpt-5"
    )
    
    team['victor'] = create_agent_with_model(
        name="Victor",
        role="Senior Auditor - Logging & Monitoring",
        model="gpt-5"
    )
    
    # Create Staff Auditors with GPT-4 Turbo
    print("\n--- STAFF AUDITORS (GPT-4 Turbo) ---")
    team['hillel'] = create_agent_with_model(
        name="Hillel",
        role="Staff Auditor - IAM Support",
        model="gpt-4-turbo"
    )
    
    team['neil'] = create_agent_with_model(
        name="Neil",
        role="Staff Auditor - Encryption & Network Support",
        model="gpt-4-turbo"
    )
    
    team['juman'] = create_agent_with_model(
        name="Juman",
        role="Staff Auditor - Logging Support",
        model="gpt-4-turbo"
    )
    
    # Create Audit Manager with GPT-4 Turbo
    print("\n--- AUDIT MANAGER (GPT-4 Turbo) ---")
    team['maurice'] = create_agent_with_model(
        name="Maurice",
        role="Audit Manager",
        model="gpt-4-turbo"
    )
    
    print()
    return team


def main():
    """Demonstrate multi-model agent configuration."""
    
    # Check for API key
    if not os.environ.get('OPENAI_API_KEY'):
        print("\n⚠️  OPENAI_API_KEY not set. Please set it to run this example.")
        return
    
    # Demonstrate both approaches
    print("\n" + "=" * 80)
    print("MULTI-MODEL AGENT CONFIGURATION DEMO")
    print("=" * 80)
    
    # Approach 1: Factory (recommended)
    team_factory = demo_factory_approach()
    
    # Approach 2: Manual (for comparison)
    # team_manual = demo_manual_approach()
    
    # Use the factory-created team for the rest of the demo
    team = team_factory
    esther = team['esther']
    hillel = team['hillel']
    maurice = team['maurice']
    
    # Show cost comparison
    print("\n" + "=" * 80)
    print("COST COMPARISON")
    print("=" * 80)
    print()
    print("PRICING (per 1M tokens):")
    print()
    print("GPT-5:")
    print("  Input:  $15.00")
    print("  Output: $45.00")
    print()
    print("GPT-4 Turbo:")
    print("  Input:  $10.00")
    print("  Output: $30.00")
    print()
    print("TEAM COMPOSITION:")
    print("  3 Senior Auditors (GPT-5)")
    print("  3 Staff Auditors (GPT-4 Turbo)")
    print("  1 Audit Manager (GPT-4 Turbo)")
    print()
    print("ESTIMATED SAVINGS:")
    print("  vs All GPT-5: ~33% cost reduction")
    print("  vs All GPT-4 Turbo: +20% cost for better senior reasoning")
    print()
    
    # Demonstrate usage
    print("=" * 80)
    print("DEMONSTRATION: Senior vs Staff Auditor Reasoning")
    print("=" * 80)
    print()
    
    # Senior auditor (GPT-5) - complex judgment
    print("--- Esther (Senior Auditor with GPT-5) ---")
    print("Goal: Assess IAM risks and determine testing approach")
    print()
    esther.set_goal(
        "Assess IAM risks for CloudRetail Inc. Determine which controls "
        "require the most attention and create a testing strategy."
    )
    print("✓ Goal set. Esther will use GPT-5 for sophisticated risk analysis.")
    print()
    
    # Staff auditor (GPT-4 Turbo) - routine task
    print("--- Hillel (Staff Auditor with GPT-4 Turbo) ---")
    print("Goal: Collect IAM user list and check MFA status")
    print()
    hillel.set_goal(
        "Collect the list of IAM users and check which ones have MFA enabled. "
        "Store the evidence for Esther to review."
    )
    print("✓ Goal set. Hillel will use GPT-4 Turbo for routine evidence collection.")
    print()
    
    print("=" * 80)
    print("KEY BENEFITS")
    print("=" * 80)
    print()
    print("1. COST OPTIMIZATION")
    print("   - Senior auditors (GPT-5): Complex reasoning, risk assessment, judgment calls")
    print("   - Staff auditors (GPT-4 Turbo): Routine tasks, evidence collection, data gathering")
    print("   - Estimated 30-40% cost savings vs all GPT-5")
    print()
    print("2. REALISTIC TEAM STRUCTURE")
    print("   - Mirrors real audit teams where seniors have more expertise")
    print("   - Staff auditors handle routine work under senior supervision")
    print("   - Manager reviews and approves (doesn't need most advanced model)")
    print()
    print("3. QUALITY WHERE IT MATTERS")
    print("   - GPT-5 for risk assessment and complex analysis")
    print("   - GPT-4 Turbo is still highly capable for structured tasks")
    print("   - Best balance of quality and cost")
    print()
    
    # Show how to track costs separately
    print("=" * 80)
    print("COST TRACKING BY AGENT")
    print("=" * 80)
    print()
    print("Each agent tracks its own LLM costs:")
    print()
    for name, agent in team.items():
        model = agent.llm.model
        cost = agent.llm.cost_tracker.total_cost
        print(f"{agent.name:10} ({model:15}): ${cost:.4f}")
    print()
    print("This allows you to see exactly where your LLM budget is going.")
    print()
    
    # Calculate total
    total_cost = sum(agent.llm.cost_tracker.total_cost for agent in team.values())
    print(f"Total cost so far: ${total_cost:.4f}")
    print()


if __name__ == "__main__":
    main()
