# Agent Workflow Setup - Risk Assessment Driven

## Overview

The agent workflow has been restructured to follow a proper audit methodology where the risk assessment drives all subsequent task assignments. Agents autonomously assign tasks based on risk assessment findings.

## Current State

### Task Assignments

**Maurice (Audit Manager)**:
- Review and approve risk assessment workpaper
- After approval, will autonomously create audit plan and assign controls to auditors

**Esther (Senior Auditor - IAM)**:
- Perform risk assessment for CloudRetail AWS environment
- After completion, submit to Maurice for review
- After approval, will receive control testing assignments from Maurice

**Hillel (Staff Auditor)**:
- No tasks assigned yet
- Will receive evidence collection tasks from senior auditors based on risk assessment

### Knowledge Distribution

**Risk Assessment Knowledge** (Restricted):
- Maurice: Has risk-assessment-procedure.md (manager perspective - approval focus)
- Esther: Has risk-assessment-procedure.md (senior auditor perspective - execution focus)
- Hillel: Does NOT have risk assessment knowledge (not his role)

**Other Knowledge**:
- Maurice: audit-planning-guide.md, workpaper-review-checklist.md
- Esther: control-testing-procedures.md
- Hillel: evidence-gathering-basics.md

## Workflow Sequence

### Phase 1: Risk Assessment (Current Phase)
1. **Esther performs risk assessment**
   - Uses IAM query tools to assess current state
   - Evaluates risks across all control domains
   - Calculates risk scores (Likelihood × Impact)
   - Creates WP-RISK-001 workpaper
   - Submits to Maurice for review

2. **Maurice reviews and approves**
   - Reviews risk assessment for completeness
   - Validates risk scores and rationale
   - Approves or requests revisions
   - Once approved, moves to Phase 2

### Phase 2: Audit Planning (Agent-Driven)
1. **Maurice creates audit plan**
   - Uses approved risk assessment
   - Selects high-risk controls from ISACA program
   - Creates audit plan workpaper (WP-PLAN-001)
   - Assigns controls to senior auditors

2. **Senior auditors receive assignments**
   - Esther gets IAM controls
   - Chuck gets encryption controls (when added)
   - Victor gets network controls (when added)

### Phase 3: Control Testing (Agent-Driven)
1. **Senior auditors test controls**
   - Follow ISACA testing procedures
   - Collect evidence (may delegate to staff)
   - Analyze findings
   - Create control testing workpapers

2. **Staff auditors support**
   - Hillel receives evidence collection tasks from Esther
   - Neil receives tasks from Chuck (when added)
   - Juman receives tasks from Victor (when added)

### Phase 4: Reporting (Agent-Driven)
1. **Maurice compiles findings**
   - Reviews all workpapers
   - Identifies control deficiencies
   - Creates audit report
   - Presents to management

## Key Principles

### 1. One Task, One Owner
- Each task is assigned to exactly ONE agent
- No duplicate assignments
- Clear accountability

### 2. Knowledge-Based Assignments
- Only agents with relevant knowledge can perform tasks
- Risk assessment: Maurice and Esther only
- Control testing: Senior auditors only
- Evidence collection: All auditors

### 3. Agent Autonomy
- Agents decide HOW to accomplish their goals
- Agents assign tasks based on their findings
- No pre-scripted task lists beyond initial risk assessment

### 4. Hierarchical Delegation
- Audit Manager → Senior Auditors → Staff Auditors
- Each level delegates appropriate work down
- Each level reviews work from below

## Testing the Workflow

### Start the Dashboard
```bash
python3 examples/test_enhanced_dashboard.py
```

### Monitor Progress
1. Open http://127.0.0.1:5000
2. Click on Esther's card
3. Go to Tasks tab - see risk assessment task
4. Go to Knowledge tab - verify she has risk assessment procedure
5. Click on Maurice's card
6. Go to Tasks tab - see review task and delegated risk assessment
7. Click on Hillel's card
8. Go to Tasks tab - should be empty (waiting for assignments)

### Execute Risk Assessment
```python
# In a Python script or interactive session
from src.agents.agent_factory import AgentFactory

factory = AgentFactory("config/agent_models.yaml")
esther = factory.create_agent("esther", load_knowledge=True)

# Give Esther her goal
esther.set_goal("Perform risk assessment for CloudRetail AWS environment")

# Let her work autonomously
result = esther.run_autonomously(max_iterations=20)

# Check her workpaper
# She should create WP-RISK-001 with risk scores
```

## What Happens Next

After Esther completes the risk assessment:

1. **Maurice reviews** the workpaper
2. **Maurice approves** (or requests revisions)
3. **Maurice creates audit plan** based on risk scores
4. **Maurice assigns controls** to senior auditors:
   - High-risk IAM controls → Esther
   - High-risk encryption controls → Chuck (when added)
   - High-risk network controls → Victor (when added)
5. **Senior auditors test controls** and delegate evidence collection
6. **Staff auditors collect evidence** as assigned
7. **Maurice compiles findings** into audit report

## Files Modified

### Task Files (Cleared and Reset)
- `tasks/maurice-tasks.md` - Review and approve risk assessment
- `tasks/esther-tasks.md` - Perform risk assessment
- `tasks/hillel-tasks.md` - Empty (waiting for assignments)

### Knowledge Files (Added)
- `knowledge/esther/risk-assessment-procedure.md` - Added risk assessment knowledge

### Knowledge Files (Unchanged)
- `knowledge/maurice/risk-assessment-procedure.md` - Already had it
- `knowledge/maurice/audit-planning-guide.md` - Already had it
- `knowledge/maurice/workpaper-review-checklist.md` - Already had it
- `knowledge/esther/control-testing-procedures.md` - Already had it
- `knowledge/hillel/evidence-gathering-basics.md` - Already had it

## Benefits of This Approach

✅ **Realistic Audit Workflow**: Mirrors real-world audit methodology
✅ **Risk-Driven**: All work is prioritized based on risk assessment
✅ **Agent Autonomy**: Agents make decisions based on their findings
✅ **Clear Roles**: Each agent has specific responsibilities
✅ **Knowledge Segregation**: Agents only have knowledge relevant to their role
✅ **Scalable**: Easy to add more agents and controls
✅ **Traceable**: Complete audit trail through task assignments

## Next Steps

1. **Fine-tune system prompts** using the dashboard editor
2. **Run Esther's risk assessment** and monitor her progress
3. **Review Maurice's approval process** when Esther completes
4. **Observe autonomous task assignment** as the audit progresses
5. **Add more agents** (Chuck, Victor, Neil, Juman) as needed

---
**Created**: December 4, 2025  
**Status**: ✅ Complete  
**Workflow**: Risk Assessment → Audit Planning → Control Testing → Reporting
