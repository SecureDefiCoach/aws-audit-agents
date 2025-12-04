# Audit Team Agents

This module implements the audit team agent classes for the AWS Audit Agent System.

## Overview

The audit team consists of 7 named agents organized in a realistic audit hierarchy:

### Audit Manager
- **Maurice** - Reviews and approves audit plans, budgets, workpapers, and final reports

### Senior Auditors
- **Esther** - Lead Auditor for IAM & Logical Access Controls (supervises Hillel)
- **Chuck** - Lead Auditor for Data Encryption & Network Security (supervises Neil)
- **Victor** - Lead Auditor for Logging, Monitoring & Incident Response (supervises Juman)

### Staff Auditors
- **Hillel** - Staff Auditor supporting Esther on IAM controls
- **Neil** - Staff Auditor supporting Chuck on encryption and network
- **Juman** - Staff Auditor supporting Victor on logging and monitoring

## Agent Classes

### AuditAgent (Base Class)

The base class for all audit agents. Provides:
- Agent name identification
- Audit trail logging with `log_action()`
- Simulated timestamp support
- Transparent action tracking

All agent actions are logged with the agent's name visible for demonstration purposes.

```python
from src.agents.audit_team import AuditAgent

class MyAgent(AuditAgent):
    def __init__(self):
        super().__init__(name="MyAgent")
    
    def do_something(self):
        self.log_action(
            action_type="custom_action",
            description="Performing custom action",
            decision_rationale="Because it's needed"
        )
```

### AuditManagerAgent

Maurice's responsibilities:
- `review_audit_plan(plan)` - Review and approve audit plans
- `approve_budget(budget)` - Approve budget allocations
- `review_workpaper(workpaper)` - Review workpapers created by team
- `sign_off_report(report)` - Sign off on final audit report

```python
from src.agents.audit_team import AuditManagerAgent

maurice = AuditManagerAgent()
approval = maurice.approve_budget(budget)
print(f"Budget approved: {approval['approved']}")
```

### SeniorAuditorAgent

Senior auditor responsibilities:
- `assess_risk(company)` - Assess risks in assigned control domains
- `create_audit_plan(risks)` - Create audit plan based on risks
- `supervise_staff(task)` - Assign tasks to staff auditors
- `collect_evidence_direct(service)` - Collect evidence directly from AWS
- `request_evidence(request)` - Request evidence from auditee agents
- `execute_test(procedure, evidence)` - Execute testing procedures
- `evaluate_control(test_result)` - Evaluate control effectiveness
- `create_workpaper(finding)` - Create workpaper documenting findings

```python
from src.agents.audit_team import SeniorAuditorAgent

esther = SeniorAuditorAgent(
    name="Esther",
    control_domains=["IAM", "Logical Access"],
    staff_auditor="Hillel"
)

# Assign task to staff
task = {"description": "Collect IAM evidence", "service": "IAM"}
assignment = esther.supervise_staff(task)
```

### StaffAuditorAgent

Staff auditor responsibilities:
- `receive_assignment(task)` - Receive task from senior auditor
- `collect_evidence(service)` - Collect evidence from AWS services
- `execute_test(procedure)` - Execute testing procedures
- `document_finding(result)` - Document findings from tests

```python
from src.agents.audit_team import StaffAuditorAgent

hillel = StaffAuditorAgent(
    name="Hillel",
    senior_auditor="Esther"
)

# Receive and execute assignment
hillel.receive_assignment(task)
hillel.collect_evidence("IAM")
```

## Audit Trail

All agents maintain a comprehensive audit trail of their actions:

```python
# Get audit trail for an agent
trail = maurice.get_audit_trail()

for entry in trail:
    print(f"[{entry.timestamp}] {entry.agent_id}: {entry.action_description}")
    if entry.decision_rationale:
        print(f"  Rationale: {entry.decision_rationale}")
```

Each audit trail entry includes:
- `timestamp` - Simulated timestamp of the action
- `agent_id` - Name of the agent (e.g., "Maurice", "Esther")
- `action_type` - Type of action (e.g., "review_audit_plan", "collect_evidence")
- `action_description` - Human-readable description
- `decision_rationale` - Optional explanation of why the action was taken
- `evidence_refs` - Optional list of evidence IDs referenced
- `metadata` - Optional additional metadata

## Time Simulation

Agents support time simulation for realistic audit timelines:

```python
from src.utils.time_simulator import TimeSimulator

time_sim = TimeSimulator(compression_ratio=7)  # 1 day = 1 week

maurice = AuditManagerAgent(time_simulator=time_sim)
# All logged actions will use simulated timestamps
```

## Requirements Coverage

This implementation satisfies the following requirements:

- **Requirement 4.8**: All testing procedures are documented in the audit trail
- **Requirement 5.1**: All agent actions are logged with timestamp, agent ID, and description
- **Requirement 5.4**: All decisions are logged with rationale and supporting evidence

## Example Usage

See `examples/audit_team_example.py` for a complete demonstration of the audit team workflow.

## Testing

Unit tests are available in `tests/unit/test_audit_team.py`:

```bash
pytest tests/unit/test_audit_team.py -v
```

All tests verify:
- Agent initialization with correct names
- Audit trail logging functionality
- Agent-specific methods (review, approve, assign, etc.)
- Agent name visibility in all logs

## Future Implementation

The following methods are placeholders for future tasks:
- Risk assessment logic
- Audit plan creation
- Evidence collection from AWS services
- Testing procedure execution
- Control evaluation
- Workpaper generation

These will be implemented in subsequent tasks as the system is built out.
