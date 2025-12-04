"""
Demo: Agent Knowledge and Task Management

This script demonstrates:
1. Agents loading their own knowledge/procedures
2. Agents creating and assigning tasks to each other
3. Task delegation workflow
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.llm_client import LLMClient
from src.agents.audit_agent import AuditAgent
from src.agents.tools import TaskManagementTool


class DemoAgent(AuditAgent):
    """Simple agent for demonstration"""
    
    def create_workpaper(self):
        return {"status": "demo"}


def main():
    print("=" * 80)
    print("AGENT KNOWLEDGE AND TASK MANAGEMENT DEMO")
    print("=" * 80)
    
    # Create LLM client (using Ollama for demo)
    llm = LLMClient(
        provider="ollama",
        model="llama3.2:3b",
        temperature=0.7
    )
    
    # Create task management tool
    task_tool = TaskManagementTool()
    
    print("\n" + "=" * 80)
    print("PART 1: AGENT KNOWLEDGE SYSTEM")
    print("=" * 80)
    
    # Create Maurice with his knowledge
    print("\n📚 Creating Maurice (Audit Manager) with knowledge...")
    maurice = DemoAgent(
        name="Maurice",
        role="Audit Manager",
        llm_client=llm,
        tools=[task_tool],
        knowledge_path="knowledge/maurice"
    )
    
    print(f"\n✅ Maurice loaded {len(maurice.knowledge)} procedures:")
    for procedure_name in maurice.knowledge.keys():
        print(f"   - {procedure_name}")
    
    # Create Esther with her knowledge
    print("\n📚 Creating Esther (Senior Auditor) with knowledge...")
    esther = DemoAgent(
        name="Esther",
        role="Senior Auditor",
        llm_client=llm,
        tools=[task_tool],
        knowledge_path="knowledge/esther"
    )
    
    print(f"\n✅ Esther loaded {len(esther.knowledge)} procedures:")
    for procedure_name in esther.knowledge.keys():
        print(f"   - {procedure_name}")
    
    # Create Hillel with his knowledge
    print("\n📚 Creating Hillel (Staff Auditor) with knowledge...")
    hillel = DemoAgent(
        name="Hillel",
        role="Staff Auditor",
        llm_client=llm,
        tools=[task_tool],
        knowledge_path="knowledge/hillel"
    )
    
    print(f"\n✅ Hillel loaded {len(hillel.knowledge)} procedures:")
    for procedure_name in hillel.knowledge.keys():
        print(f"   - {procedure_name}")
    
    print("\n" + "=" * 80)
    print("PART 2: TASK MANAGEMENT SYSTEM")
    print("=" * 80)
    
    # Maurice creates a task for himself
    print("\n📝 Maurice creates a task for himself...")
    result = task_tool.execute(
        action="create_task",
        agent_name="Maurice",
        task_description="Perform risk assessment for CloudRetail AWS environment",
        priority="high"
    )
    print(f"✅ {result['message']}")
    
    # Maurice assigns a task to Esther
    print("\n📝 Maurice assigns a task to Esther...")
    result = task_tool.execute(
        action="assign_task",
        agent_name="Maurice",
        assignee="Esther",
        task_description="Test Control: Securing Root Account Access (ISACA 1.1)",
        priority="high",
        due_date="2025-12-06"
    )
    print(f"✅ {result['message']}")
    
    # Esther reads her tasks
    print("\n📋 Esther checks her task list...")
    result = task_tool.execute(
        action="read_my_tasks",
        agent_name="Esther"
    )
    print(f"✅ Esther has {len(result['current_tasks'])} current task(s)")
    for task in result['current_tasks']:
        print(f"   - {task}")
    
    # Esther assigns a subtask to Hillel
    print("\n📝 Esther delegates evidence collection to Hillel...")
    result = task_tool.execute(
        action="assign_task",
        agent_name="Esther",
        assignee="Hillel",
        task_description="Collect IAM user list with MFA status for root account control testing",
        priority="high",
        due_date="2025-12-05"
    )
    print(f"✅ {result['message']}")
    
    # Hillel reads his tasks
    print("\n📋 Hillel checks his task list...")
    result = task_tool.execute(
        action="read_my_tasks",
        agent_name="Hillel"
    )
    print(f"✅ Hillel has {len(result['current_tasks'])} current task(s)")
    for task in result['current_tasks']:
        print(f"   - {task}")
    
    # Hillel completes his task
    print("\n✅ Hillel completes his task...")
    result = task_tool.execute(
        action="complete_task",
        agent_name="Hillel",
        task_index=0
    )
    print(f"✅ {result['message']}")
    
    # List all tasks
    print("\n📊 Task summary across all agents...")
    result = task_tool.execute(
        action="list_all_tasks",
        agent_name="Maurice"  # agent_name required but not used for this action
    )
    print("\nTask counts by agent:")
    for agent, counts in result['all_tasks'].items():
        print(f"   {agent}:")
        print(f"      Current: {counts['current']}")
        print(f"      Completed: {counts['completed']}")
        print(f"      Delegated: {counts['delegated']}")
    
    print("\n" + "=" * 80)
    print("PART 3: KNOWLEDGE IN ACTION")
    print("=" * 80)
    
    # Show how knowledge appears in agent context
    print("\n📚 Maurice's knowledge context (first 500 chars):")
    print("-" * 80)
    knowledge_context = maurice.get_knowledge_context()
    print(knowledge_context[:500] + "...")
    print("-" * 80)
    
    print("\n" + "=" * 80)
    print("DEMO COMPLETE")
    print("=" * 80)
    
    print("\n✅ Successfully demonstrated:")
    print("   1. Agent knowledge loading (procedures specific to each role)")
    print("   2. Task creation and self-assignment")
    print("   3. Task delegation between agents")
    print("   4. Task completion tracking")
    print("   5. Task visibility across team")
    
    print("\n📁 Check these locations:")
    print("   - knowledge/maurice/ - Maurice's procedures")
    print("   - knowledge/esther/ - Esther's procedures")
    print("   - knowledge/hillel/ - Hillel's procedures")
    print("   - tasks/maurice-tasks.md - Maurice's task list")
    print("   - tasks/esther-tasks.md - Esther's task list")
    print("   - tasks/hillel-tasks.md - Hillel's task list")
    
    print("\n🎯 Next Steps:")
    print("   - Add more knowledge files for each agent")
    print("   - Integrate task management into dashboard")
    print("   - Let agents autonomously create and assign tasks")
    print("   - Document which procedures were used in workpapers")


if __name__ == "__main__":
    main()
