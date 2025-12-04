# Agent Knowledge & Task Management Design

## Overview

Two powerful features that make agents more autonomous and showcase their thought process:

1. **Agent Knowledge Folders** - Each agent has their own procedures and knowledge
2. **Agent Task Management** - Agents create and assign tasks to each other

## Feature 1: Agent Knowledge Folders

### Concept

Each agent has a personal knowledge folder containing procedures, guidelines, and reference materials. This knowledge is loaded into the agent's context and guides their decision-making.

### Folder Structure

```
knowledge/
├── maurice/                          # Audit Manager
│   ├── risk-assessment-procedure.md
│   ├── audit-planning-guide.md
│   ├── workpaper-review-checklist.md
│   ├── team-management-guidelines.md
│   └── approval-criteria.md
│
├── esther/                           # Senior Auditor
│   ├── control-testing-procedures.md
│   ├── interview-techniques.md
│   ├── evidence-collection-guide.md
│   └── workpaper-standards.md
│
├── chuck/                            # Senior Auditor
│   ├── control-testing-procedures.md
│   ├── interview-techniques.md
│   ├── evidence-collection-guide.md
│   └── workpaper-standards.md
│
├── victor/                           # Senior Auditor
│   ├── control-testing-procedures.md
│   ├── interview-techniques.md
│   ├── evidence-collection-guide.md
│   └── workpaper-standards.md
│
├── hillel/                           # Staff Auditor
│   ├── evidence-gathering-basics.md
│   ├── documentation-standards.md
│   └── escalation-procedures.md
│
├── neil/                             # Staff Auditor
│   ├── evidence-gathering-basics.md
│   ├── documentation-standards.md
│   └── escalation-procedures.md
│
├── juman/                            # Staff Auditor
│   ├── evidence-gathering-basics.md
│   ├── documentation-standards.md
│   └── escalation-procedures.md
│
└── shared/                           # Accessible to all agents
    ├── isaca-audit-program/
    ├── company-policies.md
    ├── aws-best-practices.md
    └── audit-methodology.md
```

### Implementation

```python
class AuditAgent:
    def __init__(self, name, role, llm_client, knowledge_path=None):
        self.name = name
        self.role = role
        self.llm = llm_client
        self.knowledge = {}
        
        # Load agent-specific knowledge
        if knowledge_path:
            self.load_knowledge(knowledge_path)
        
        # Load shared knowledge
        self.load_knowledge("knowledge/shared")
    
    def load_knowledge(self, path):
        """Load all markdown files from knowledge folder"""
        knowledge_dir = Path(path)
        if not knowledge_dir.exists():
            return
        
        for file in knowledge_dir.glob("*.md"):
            procedure_name = file.stem
            procedure_content = file.read_text()
            self.knowledge[procedure_name] = procedure_content
            print(f"📚 {self.name}: Loaded knowledge '{procedure_name}'")
    
    def get_relevant_knowledge(self, task_description):
        """Retrieve knowledge relevant to current task"""
        # Simple approach: return all knowledge
        # Advanced: use embeddings to find relevant procedures
        return "\n\n".join([
            f"## {name}\n{content}" 
            for name, content in self.knowledge.items()
        ])
```

### Usage Example

**Maurice performing risk assessment:**
```python
maurice = AuditAgent(
    name="Maurice",
    role="Audit Manager",
    llm_client=llm,
    knowledge_path="knowledge/maurice"
)

# Maurice's knowledge includes risk-assessment-procedure.md
maurice.set_goal("Perform risk assessment for CloudRetail")

# When Maurice reasons, his LLM context includes:
# - risk-assessment-procedure.md (step-by-step guide)
# - risk-scoring-matrix.md (how to score risks)
# - audit-planning-guide.md (how to create audit plan)

# Maurice follows the procedures from his knowledge folder
```

### Benefits

✅ **Realistic role separation** - Maurice knows risk assessment, staff auditors don't  
✅ **Procedural compliance** - Agents follow documented procedures  
✅ **Easy to update** - Change procedures without changing code  
✅ **Auditable** - Can see exactly what procedures agents followed  
✅ **Scalable** - Add new knowledge without retraining  

---

## Feature 2: Agent Task Management

### Concept

Agents manage their own task lists and can create/assign tasks to each other. This enables autonomous delegation and showcases agent decision-making.

### Folder Structure

```
tasks/
├── maurice-tasks.md          # Maurice's personal task list
├── esther-tasks.md           # Esther's personal task list
├── chuck-tasks.md            # Chuck's personal task list
├── victor-tasks.md           # Victor's personal task list
├── hillel-tasks.md           # Hillel's personal task list
├── neil-tasks.md             # Neil's personal task list
├── juman-tasks.md            # Juman's personal task list
└── team-backlog.md           # Shared team task backlog
```

### Task File Format

```markdown
# Esther's Tasks

## Current Tasks
- [ ] Test Control: Securing Root Account Access (ISACA 1.1)
  - Assigned by: Maurice
  - Assigned on: 2025-12-04
  - Priority: High
  - Due: 2025-12-06
  - Status: In Progress

- [ ] Review Hillel's evidence collection for IAM users
  - Assigned by: Self
  - Assigned on: 2025-12-04
  - Priority: Medium
  - Due: 2025-12-05

## Completed Tasks
- [x] Perform initial IAM risk assessment
  - Assigned by: Maurice
  - Completed on: 2025-12-03
  - Workpaper: WP-IAM-001

## Delegated Tasks (Waiting on Others)
- [ ] Collect IAM user list with MFA status
  - Assigned to: Hillel
  - Assigned on: 2025-12-04
  - Status: In Progress
```

### Implementation

```python
class TaskManagementTool(Tool):
    """Tool for agents to manage tasks"""
    
    def __init__(self, tasks_dir="tasks"):
        super().__init__(
            name="manage_tasks",
            description="Create, read, assign, and complete tasks"
        )
        self.tasks_dir = Path(tasks_dir)
        self.tasks_dir.mkdir(exist_ok=True)
        
        # Define parameters
        self.add_parameter("action", "string", 
            "Action: 'read_my_tasks', 'create_task', 'assign_task', 'complete_task'")
        self.add_parameter("task_description", "string", 
            "Description of the task", required=False)
        self.add_parameter("assignee", "string", 
            "Agent to assign task to", required=False)
        self.add_parameter("priority", "string", 
            "Priority: high, medium, low", required=False)
    
    def execute(self, action, agent_name, **kwargs):
        if action == "read_my_tasks":
            return self.read_tasks(agent_name)
        
        elif action == "create_task":
            return self.create_task(
                agent_name=agent_name,
                task=kwargs['task_description'],
                priority=kwargs.get('priority', 'medium')
            )
        
        elif action == "assign_task":
            return self.assign_task(
                from_agent=agent_name,
                to_agent=kwargs['assignee'],
                task=kwargs['task_description'],
                priority=kwargs.get('priority', 'medium')
            )
        
        elif action == "complete_task":
            return self.complete_task(
                agent_name=agent_name,
                task_id=kwargs['task_id']
            )
    
    def read_tasks(self, agent_name):
        """Read agent's task list"""
        task_file = self.tasks_dir / f"{agent_name.lower()}-tasks.md"
        if task_file.exists():
            return {"tasks": task_file.read_text()}
        return {"tasks": "No tasks yet"}
    
    def assign_task(self, from_agent, to_agent, task, priority):
        """Assign a task to another agent"""
        task_file = self.tasks_dir / f"{to_agent.lower()}-tasks.md"
        
        # Create task entry
        task_entry = f"""
- [ ] {task}
  - Assigned by: {from_agent}
  - Assigned on: {datetime.now().strftime('%Y-%m-%d')}
  - Priority: {priority}
  - Status: Not Started
"""
        
        # Append to agent's task file
        with open(task_file, 'a') as f:
            f.write(task_entry)
        
        return {
            "status": "success",
            "message": f"Task assigned to {to_agent}",
            "task": task
        }
```

### Workflow Example

**1. Maurice performs risk assessment:**
```python
# Maurice identifies high-risk controls
maurice.reason()  # LLM decides: "I should create tasks for testing these controls"

# Maurice uses task management tool
maurice.act({
    "action": "use_tool",
    "tool": "manage_tasks",
    "parameters": {
        "action": "assign_task",
        "assignee": "esther",
        "task_description": "Test Control: Securing Root Account Access (ISACA 1.1)",
        "priority": "high"
    }
})
```

**2. Esther checks her tasks:**
```python
# Esther starts her day
esther.act({
    "action": "use_tool",
    "tool": "manage_tasks",
    "parameters": {
        "action": "read_my_tasks"
    }
})

# Esther sees: "I have a new high-priority task from Maurice"
# Esther reasons: "I should start with the highest priority task"
```

**3. Esther delegates to Hillel:**
```python
# Esther breaks down the task
esther.act({
    "action": "use_tool",
    "tool": "manage_tasks",
    "parameters": {
        "action": "assign_task",
        "assignee": "hillel",
        "task_description": "Collect IAM user list with MFA status",
        "priority": "high"
    }
})
```

**4. Esther completes her task:**
```python
# After finishing the control test
esther.act({
    "action": "use_tool",
    "tool": "manage_tasks",
    "parameters": {
        "action": "complete_task",
        "task_id": "1"
    }
})
```

### Dashboard Integration

Add task visibility to the web dashboard:

```python
@app.route('/api/agents/<agent_name>/tasks')
def get_agent_tasks(agent_name):
    """Get agent's task list"""
    task_file = Path(f"tasks/{agent_name.lower()}-tasks.md")
    if task_file.exists():
        tasks = parse_task_file(task_file)
        return jsonify(tasks)
    return jsonify([])

@app.route('/api/tasks/all')
def get_all_tasks():
    """Get all tasks across all agents"""
    all_tasks = {}
    for task_file in Path("tasks").glob("*-tasks.md"):
        agent_name = task_file.stem.replace("-tasks", "")
        all_tasks[agent_name] = parse_task_file(task_file)
    return jsonify(all_tasks)
```

### Benefits

✅ **Autonomous delegation** - Agents manage their own work  
✅ **Transparent** - All task assignments are documented  
✅ **Realistic workflow** - Mimics real audit team dynamics  
✅ **Visible thought process** - Can see agent decision-making  
✅ **Auditable** - Complete history of who assigned what to whom  
✅ **Flexible** - Agents can reprioritize and reassign  

---

## Integration with Audit Workflow

### Risk Assessment Phase
```
Maurice:
1. Performs risk assessment
2. Identifies 10 high-risk controls
3. Creates 10 tasks in team-backlog.md
4. Assigns tasks to Esther, Chuck, Victor based on availability
```

### Control Testing Phase
```
Esther:
1. Checks her tasks (sees 4 assignments from Maurice)
2. Reads her knowledge: control-testing-procedures.md
3. Starts highest priority task
4. Delegates evidence collection to Hillel
5. Completes task, creates workpaper
6. Marks task complete
```

### Review Phase
```
Maurice:
1. Checks team-backlog.md (sees completed tasks)
2. Creates review tasks for himself
3. Reviews workpapers
4. Assigns follow-up tasks if needed
```

---

## Implementation Plan

### Task 5.5: Agent Knowledge System
1. Create `knowledge/` folder structure
2. Add `load_knowledge()` method to AuditAgent
3. Create sample procedures for each agent
4. Update agent initialization to load knowledge
5. Add knowledge to LLM context
6. Document which procedures were used in workpapers

### Task 5.6: Agent Task Management
1. Create `tasks/` folder structure
2. Implement TaskManagementTool
3. Add task operations (read, create, assign, complete)
4. Update dashboard to show tasks
5. Create task visualization
6. Test task delegation workflow

---

## Example Procedures to Create

### Maurice's Knowledge
- `risk-assessment-procedure.md` - Step-by-step risk assessment
- `audit-planning-guide.md` - How to create audit plan
- `workpaper-review-checklist.md` - What to check in workpapers
- `team-management-guidelines.md` - How to assign work

### Senior Auditor Knowledge
- `control-testing-procedures.md` - How to test controls
- `interview-techniques.md` - How to conduct interviews
- `evidence-collection-guide.md` - What evidence to collect
- `workpaper-standards.md` - How to document findings

### Staff Auditor Knowledge
- `evidence-gathering-basics.md` - Basic evidence collection
- `documentation-standards.md` - How to document work
- `escalation-procedures.md` - When to escalate to senior

---

## Success Criteria

✅ Each agent has their own knowledge folder  
✅ Agents load procedures on initialization  
✅ Agents reference procedures in their reasoning  
✅ Each agent has their own task file  
✅ Agents can create tasks for themselves  
✅ Agents can assign tasks to others  
✅ Dashboard shows all agent tasks  
✅ Task history is auditable  

This design showcases agent autonomy, decision-making, and realistic team dynamics!
