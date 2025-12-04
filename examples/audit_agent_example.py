"""
Example demonstrating the base AuditAgent class with LLM reasoning.

This example shows how an agent:
1. Receives a goal
2. Reasons about how to achieve it
3. Uses tools to collect information
4. Documents findings
5. Completes the goal

Run with: python examples/audit_agent_example.py
"""

import os
import sys
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.agents.audit_agent import AuditAgent, Tool
from src.agents.llm_client import LLMClient


class SimpleAuditorAgent(AuditAgent):
    """Simple auditor agent for demonstration"""
    
    def create_workpaper(self):
        """Create a simple workpaper"""
        return {
            "agent": self.name,
            "goal": self.current_goal,
            "actions": len(self.action_history),
            "status": self.goal_status
        }


def create_mock_iam_tool():
    """Create a mock IAM tool for demonstration"""
    
    def list_users(**kwargs):
        """Mock IAM user listing"""
        return {
            "users": [
                {"UserName": "admin-john", "MFA": False, "Policies": ["AdministratorAccess"]},
                {"UserName": "developer-sarah", "MFA": True, "Policies": ["DeveloperAccess"]},
                {"UserName": "auditor-mike", "MFA": True, "Policies": ["ReadOnlyAccess"]}
            ],
            "count": 3
        }
    
    return Tool(
        name="list_iam_users",
        description="Lists all IAM users with their MFA status and policies",
        parameters={
            "type": "object",
            "properties": {
                "include_mfa": {"type": "boolean", "description": "Include MFA status"},
                "include_policies": {"type": "boolean", "description": "Include policy info"}
            }
        },
        execute=list_users
    )


def create_mock_workpaper_tool(agent):
    """Create a mock workpaper tool"""
    
    def create_workpaper(title, findings, risk_rating, **kwargs):
        """Mock workpaper creation"""
        workpaper = {
            "reference": f"WP-{agent.name.upper()}-001",
            "title": title,
            "findings": findings,
            "risk_rating": risk_rating,
            "created_by": agent.name,
            "created_at": datetime.now().isoformat()
        }
        
        print(f"\n📄 Workpaper Created: {workpaper['reference']}")
        print(f"   Title: {title}")
        print(f"   Risk: {risk_rating}")
        
        return workpaper
    
    return Tool(
        name="create_workpaper",
        description="Creates a professional audit workpaper documenting findings",
        parameters={
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Workpaper title"},
                "findings": {"type": "string", "description": "Audit findings"},
                "risk_rating": {"type": "string", "description": "Risk rating (HIGH/MEDIUM/LOW)"}
            },
            "required": ["title", "findings", "risk_rating"]
        },
        execute=create_workpaper
    )


def main():
    """Run the example"""
    
    print("=" * 70)
    print("AuditAgent Example - LLM-Based Autonomous Agent")
    print("=" * 70)
    
    # Check for API key
    if not os.environ.get('OPENAI_API_KEY'):
        print("\n⚠️  Warning: OPENAI_API_KEY not set")
        print("   Set it with: export OPENAI_API_KEY='your-key-here'")
        print("\n   For this demo, we'll simulate the agent behavior")
        print("   In production, the agent would use real LLM reasoning\n")
        return
    
    # Initialize LLM client
    print("\n1. Initializing LLM client...")
    llm = LLMClient(
        provider='openai',
        model='gpt-4o',  # Using GPT-4o for cost efficiency
        rate_limit=10,
        temperature=0.7
    )
    print("   ✅ LLM client ready")
    
    # Create agent
    print("\n2. Creating audit agent...")
    agent = SimpleAuditorAgent(
        name="Esther",
        role="Senior Auditor - IAM",
        llm_client=llm
    )
    print(f"   ✅ Agent created: {agent.name} ({agent.role})")
    
    # Register tools
    print("\n3. Registering tools...")
    agent.register_tool(create_mock_iam_tool())
    agent.register_tool(create_mock_workpaper_tool(agent))
    print(f"   ✅ {len(agent.tools)} tools registered")
    
    # Set goal
    print("\n4. Setting goal...")
    goal = """Assess IAM security for the AWS account. 
    
Your tasks:
1. List all IAM users
2. Identify users without MFA
3. Document your findings in a workpaper
4. Rate the overall IAM risk

Be thorough and professional in your analysis."""
    
    agent.set_goal(goal)
    
    # Run agent autonomously
    print("\n5. Running agent autonomously...")
    print("   (Agent will reason and act until goal is complete)")
    print()
    
    result = agent.run_autonomously(max_iterations=10)
    
    # Print results
    print("\n" + "=" * 70)
    print("Execution Complete")
    print("=" * 70)
    print(f"Status: {result['status']}")
    print(f"Iterations: {result['iterations']}")
    print(f"Actions taken: {result['actions_taken']}")
    
    # Print action history
    print("\n" + "=" * 70)
    print("Action History")
    print("=" * 70)
    for i, action in enumerate(agent.get_action_history(), 1):
        print(f"\n{i}. {action.action_type.upper()}")
        print(f"   Time: {action.timestamp.strftime('%H:%M:%S')}")
        print(f"   Description: {action.description}")
        if action.details:
            print(f"   Details: {action.details}")
    
    # Print cost summary
    print()
    llm.print_cost_summary()
    
    print("\n✅ Example complete!")


if __name__ == "__main__":
    main()
