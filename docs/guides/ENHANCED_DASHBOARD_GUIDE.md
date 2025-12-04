# Enhanced Agent Dashboard Guide

## Overview

The enhanced dashboard provides comprehensive oversight of all agent capabilities, knowledge, and activities. You can now drill down into each agent to see:

- **Tools & Capabilities** - What tools they have access to
- **AWS Access** - What AWS services they can query
- **Knowledge Base** - What procedures they've loaded
- **Tasks** - Current, completed, and delegated tasks
- **Actions** - Detailed history of everything they've done
- **Memory** - Their conversation history with the LLM

## New Features

### 1. Capabilities Tab

Shows detailed information about what each agent can do:

**Tools**:
- Tool name and description
- Parameters each tool accepts
- Whether parameters are required

**AWS Capabilities**:
- Which AWS services the agent can access
- Available operations (e.g., list_users, get_role)
- Service descriptions

**Summary**:
- Total number of tools
- Number of knowledge procedures loaded
- Number of AWS services accessible
- Whether agent can delegate tasks

### 2. Knowledge Tab

Shows all procedures and knowledge loaded by the agent:

**For Each Procedure**:
- Procedure name (formatted title)
- Preview of first 5 lines
- Total number of lines
- Full content available on hover

**Example Knowledge**:
- Maurice: risk-assessment-procedure, audit-planning-guide, workpaper-review-checklist
- Esther: control-testing-procedures
- Hillel: evidence-gathering-basics

### 3. Tasks Tab

Shows complete task management view:

**Current Tasks**:
- Task description
- Priority level (high, medium, low)
- Who assigned it
- When it was assigned
- Due date (if set)

**Completed Tasks**:
- Task description
- Completion date
- Slightly faded to show completed status

**Delegated Tasks**:
- Tasks this agent assigned to others
- Who it was assigned to
- Current status
- Assignment date

### 4. Enhanced Info Tab

Now includes:
- All basic information (name, role, model, provider)
- Current goal and status
- **Complete list of tools** (not just count)
- Memory size
- Action count
- LLM usage statistics
- Cost tracking

## API Endpoints

### New Endpoints

#### GET `/api/agents/<agent_name>/capabilities`
Returns agent's tools and AWS capabilities.

**Response**:
```json
{
  "tools": [
    {
      "name": "create_workpaper",
      "description": "Create an audit workpaper...",
      "parameters": [
        {
          "name": "reference_number",
          "type": "string",
          "description": "Unique workpaper reference",
          "required": true
        }
      ]
    }
  ],
  "aws_capabilities": [
    {
      "service": "IAM",
      "description": "Identity and Access Management",
      "operations": ["list_users", "list_roles", ...]
    }
  ],
  "knowledge_count": 3,
  "can_delegate_tasks": true
}
```

#### GET `/api/agents/<agent_name>/knowledge`
Returns agent's loaded knowledge/procedures.

**Response**:
```json
{
  "count": 3,
  "procedures": [
    {
      "name": "risk-assessment-procedure",
      "title": "Risk Assessment Procedure",
      "preview": "# Risk Assessment Procedure\n\n## Purpose...",
      "size": 5234,
      "lines": 285
    }
  ]
}
```

#### GET `/api/agents/<agent_name>/tasks`
Returns agent's tasks.

**Response**:
```json
{
  "current": [
    {
      "description": "Test IAM root account control",
      "assigned_by": "Maurice",
      "assigned_on": "2025-12-04",
      "priority": "high",
      "due": "2025-12-06"
    }
  ],
  "completed": [...],
  "delegated": [...]
}
```

## Usage

### Starting the Enhanced Dashboard

```python
from src.agents.agent_factory import AgentFactory
from src.web.agent_dashboard import run_dashboard

# Create agents with knowledge
factory = AgentFactory("config/agent_models.yaml")
team = {
    "maurice": factory.create_agent("maurice", load_knowledge=True),
    "esther": factory.create_agent("esther", load_knowledge=True),
    "hillel": factory.create_agent("hillel", load_knowledge=True)
}

# Run dashboard
run_dashboard(
    agent_team=team,
    config_path="config/agent_models.yaml",
    host='127.0.0.1',
    port=5000
)
```

### Quick Test

```bash
# Run the test script
python3 examples/test_enhanced_dashboard.py

# Open browser to http://127.0.0.1:5000
```

## Dashboard Navigation

### Main View
- **Agent Cards**: Click any agent card to open detailed view
- **Stats**: Top row shows team-wide statistics
- **Auto-Refresh**: Dashboard refreshes every 5 seconds
- **Manual Refresh**: Click the refresh button (bottom right)

### Agent Detail Modal

**6 Tabs Available**:

1. **Info** - Basic agent information and statistics
2. **Capabilities** - Tools, AWS access, and abilities
3. **Knowledge** - Loaded procedures and guidelines
4. **Tasks** - Current, completed, and delegated tasks
5. **Actions** - Detailed action history
6. **Memory** - Conversation history with LLM

**Navigation**:
- Click tabs to switch views
- Data loads automatically when tab is selected
- Close modal by clicking X or clicking outside

## What You Can See

### For Maurice (Audit Manager)
- **Tools**: create_workpaper, store_evidence, manage_tasks
- **Knowledge**: 3 procedures (risk assessment, audit planning, workpaper review)
- **Tasks**: Can create and assign tasks to team
- **AWS**: No direct AWS access (delegates to senior auditors)

### For Esther (Senior Auditor)
- **Tools**: query_iam, create_workpaper, store_evidence, manage_tasks
- **Knowledge**: 1 procedure (control testing)
- **Tasks**: Receives tasks from Maurice, delegates to Hillel
- **AWS**: Full IAM access (9 operations)

### For Hillel (Staff Auditor)
- **Tools**: create_workpaper, store_evidence, manage_tasks
- **Knowledge**: 1 procedure (evidence gathering)
- **Tasks**: Receives tasks from Esther
- **AWS**: No direct AWS access (collects evidence through tools)

## Benefits

### Complete Oversight
- See exactly what each agent can do
- Understand their knowledge and procedures
- Track task delegation flow
- Monitor all activities in real-time

### Debugging & Development
- Verify agents have correct tools
- Confirm knowledge loaded properly
- Check task assignments
- Review action history for issues

### Audit Trail
- Complete record of all agent actions
- Task assignment history
- Tool usage tracking
- LLM conversation history

### Performance Monitoring
- Track LLM usage and costs
- Monitor action counts
- See memory usage
- Identify bottlenecks

## Tips

### Best Practices
1. **Check Capabilities First** - Verify agent has required tools before assigning work
2. **Review Knowledge** - Ensure agents have loaded correct procedures
3. **Monitor Tasks** - Track task delegation and completion
4. **Watch Actions** - Review action history to understand agent behavior
5. **Check Memory** - Review LLM conversations to see reasoning

### Troubleshooting
- **No Knowledge Showing**: Check that knowledge files exist in `knowledge/{agent_name}/`
- **No Tasks Showing**: Check that task files exist in `tasks/{agent_name}-tasks.md`
- **No AWS Capabilities**: Only Esther has IAM access currently
- **Dashboard Not Loading**: Ensure agents are created with `load_knowledge=True`

## Future Enhancements

Planned improvements:
- [ ] Real-time task updates (WebSocket)
- [ ] Task creation UI in dashboard
- [ ] Knowledge file editing
- [ ] Tool execution from dashboard
- [ ] Agent goal setting UI
- [ ] Cost alerts and budgets
- [ ] Export capabilities
- [ ] Task delegation visualization

## Files Modified

### Backend
- `src/web/agent_dashboard.py` - Added 3 new API endpoints

### Frontend
- `src/web/templates/dashboard.html` - Added 3 new tabs and JavaScript functions

### Examples
- `examples/test_enhanced_dashboard.py` - Test script for enhanced dashboard

## Summary

The enhanced dashboard provides complete visibility into:
- ✅ What agents can do (tools and AWS access)
- ✅ What agents know (loaded procedures)
- ✅ What agents are working on (tasks)
- ✅ What agents have done (actions)
- ✅ How agents think (memory)

This gives you comprehensive oversight to monitor, debug, and optimize your agent team.

---
**Created**: December 4, 2025  
**Status**: ✅ Complete  
**Test**: `python3 examples/test_enhanced_dashboard.py`
