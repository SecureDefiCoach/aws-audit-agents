# AWS Audit Agent Definitions

This document provides an overview of all audit agents implemented in the system.

## Agent Hierarchy

```
AuditAgent (Base Class)
├── AuditManagerAgent (Maurice)
├── SeniorAuditorAgent (Esther, Chuck, Victor)
└── StaffAuditorAgent (Hillel, Neil, Juman)
```

---

## 1. AuditAgent (Base Class)

**Purpose**: Abstract base class for all audit agents providing common functionality.

**Key Attributes**:
- `name`: Agent's name
- `time_simulator`: Optional time simulator for testing
- `audit_trail`: List of all actions taken by the agent

**Key Methods**:
- `log_action()`: Logs all agent actions to audit trail with transparency
- `get_audit_trail()`: Returns all audit trail entries
- `_get_simulated_time()`: Gets current time (simulated or real)

**Transparency**: All agent actions are logged with the agent's name visible for demonstration and audit purposes.

---

## 2. AuditManagerAgent (Maurice)

**Role**: Audit Manager - Oversees the entire audit engagement

**Initialization**:
```python
maurice = AuditManagerAgent(time_simulator=None)
```

**Responsibilities**:
- Review and approve risk assessments (with human-in-the-loop)
- Review and approve audit plans (with human-in-the-loop)
- Approve budget allocations
- Review workpapers created by the team
- Sign off on final audit reports

**Key Methods**:

### `review_risk_assessment(assessment, company_name, interactive=False)`
Reviews risk assessment with optional human approval gate.
- **Args**: 
  - `assessment`: RiskAssessment object
  - `company_name`: Name of company being audited
  - `interactive`: If True, prompts for human approval
- **Returns**: Review decision with approval status
- **Human-in-the-Loop**: When interactive=True, presents assessment summary and prompts for approval

### `review_audit_plan(plan, company_name, interactive=False)`
Reviews audit plan with optional human approval gate.
- **Args**:
  - `plan`: AuditPlan object
  - `company_name`: Name of company
  - `interactive`: If True, prompts for human approval
- **Returns**: Review decision with approval status
- **Human-in-the-Loop**: When interactive=True, presents plan details and prompts for approval

### `approve_budget(budget, company_name)`
Approves budget allocation for the audit.
- **Args**: 
  - `budget`: BudgetAllocation object
  - `company_name`: Name of company
- **Returns**: Approval decision

### `review_workpaper(workpaper)`
Reviews workpaper created by audit team.
- **Args**: `workpaper`: Workpaper object
- **Returns**: Review decision

### `sign_report(report)`
Signs off on final audit report.
- **Args**: `report`: AuditReport object
- **Returns**: Signed report

**Workflow Gates Enforced**:
- Risk assessment must be approved before test procedures can be created (risk assessment is the INPUT for test procedures)
- Test procedures must be approved before staff can receive assignments (staff need authorized work orders)

---

## 3. SeniorAuditorAgent (Esther, Chuck, Victor)

**Role**: Senior Auditors - Lead specific control domains and supervise staff

**Initialization**:
```python
esther = SeniorAuditorAgent(
    name="Esther",
    control_domains=["Access Control", "Network Security"],
    staff_auditor="Hillel",
    time_simulator=None
)
```

**Specializations**:
- **Esther**: Access Control, Network Security (supervises Hillel)
- **Chuck**: Data Protection, Logging & Monitoring (supervises Neil)
- **Victor**: Change Management, Backup & Recovery (supervises Juman)

**Responsibilities**:
- Assess risks in assigned control domains
- Create audit plans for their areas
- Supervise staff auditors
- Collect evidence (direct and via requests)
- Execute testing procedures
- Evaluate controls and create findings
- Create workpapers

**Key Methods**:

### `assess_risk(company)`
Performs asset-based risk assessment using CIA triad analysis.
- **Process**:
  1. Identifies information assets in assigned domains
  2. Assesses impact (Confidentiality, Integrity, Availability)
  3. Identifies threats and vulnerabilities
  4. Calculates risk = impact × likelihood
- **Args**: `company`: CompanyProfile object
- **Returns**: RiskAssessment with inherent and residual risks
- **Asset-Based**: Links vulnerabilities to information assets for accurate impact assessment

### `create_audit_plan(company, risk_assessment, total_hours)`
Creates detailed audit plan based on risk assessment.
- **Process**:
  1. Creates 6-week timeline with phases
  2. Allocates budget based on risk levels
  3. Defines test procedures for each control
- **Args**:
  - `company`: CompanyProfile object
  - `risk_assessment`: RiskAssessment from assess_risk()
  - `total_hours`: Total audit hours available
- **Returns**: AuditPlan with timeline, budget, and procedures
- **Risk-Based**: Higher-risk areas receive more audit hours

### `supervise_staff(staff_name, task)`
Assigns tasks to staff auditor.
- **Args**:
  - `staff_name`: Name of staff auditor
  - `task`: Task details dictionary
- **Returns**: Assignment result

### `collect_evidence_direct(company, service, resource_id)`
Directly collects evidence from AWS services.
- **AWS Services Supported**:
  - IAM (users, roles, policies, MFA status)
  - S3 (buckets, encryption, versioning, public access)
  - EC2 (instances, security groups, key pairs)
  - VPC (VPCs, subnets, route tables, NACLs)
  - CloudTrail (trails, logging status, events)
- **Args**:
  - `company`: CompanyProfile object
  - `service`: AWS service name
  - `resource_id`: Specific resource identifier
- **Returns**: Evidence object with collected data

### `request_evidence(staff_name, request)`
Requests evidence collection from staff auditor.
- **Args**:
  - `staff_name`: Name of staff auditor
  - `request`: EvidenceRequest object
- **Returns**: Request confirmation

### `execute_test(company, procedure, evidence_list)`
Executes a test procedure against collected evidence.
- **Control-Specific Logic**: Different testing logic for each control domain
- **Args**:
  - `company`: CompanyProfile object
  - `procedure`: TestProcedure to execute
  - `evidence_list`: List of Evidence objects
- **Returns**: Test result with pass/fail status and findings

### `evaluate_control(test_result, procedure)`
Evaluates control effectiveness based on test results.
- **Args**:
  - `test_result`: Result from execute_test()
  - `procedure`: TestProcedure that was executed
- **Returns**: Control evaluation with effectiveness rating

### `create_workpaper(company, procedure, evidence_list, test_result)`
Creates professional audit workpaper documenting the work performed.
- **Contents**:
  - Unique workpaper reference
  - Control objective and test procedure
  - Evidence collected and analyzed
  - Test results and findings
  - Conclusion and recommendations
- **Args**:
  - `company`: CompanyProfile object
  - `procedure`: TestProcedure executed
  - `evidence_list`: Evidence collected
  - `test_result`: Test execution results
- **Returns**: Workpaper object

---

## 4. StaffAuditorAgent (Hillel, Neil, Juman)

**Role**: Staff Auditors - Execute assigned tasks under senior supervision

**Initialization**:
```python
hillel = StaffAuditorAgent(
    name="Hillel",
    senior_auditor="Esther",
    time_simulator=None
)
```

**Assignments**:
- **Hillel**: Reports to Esther (Access Control, Network Security)
- **Neil**: Reports to Chuck (Data Protection, Logging & Monitoring)
- **Juman**: Reports to Victor (Change Management, Backup & Recovery)

**Responsibilities**:
- Receive assignments from senior auditor
- Collect evidence from AWS services
- Execute testing procedures
- Document findings

**Key Methods**:

### `receive_assignment(task, audit_plan_approved=True)`
Receives task assignment from senior auditor.
- **Workflow Gate**: Cannot accept assignments if audit plan not approved
- **Args**:
  - `task`: Task details dictionary
  - `audit_plan_approved`: Whether audit plan is approved
- **Returns**: Assignment result (accepted or blocked)

### `collect_evidence(service, has_assignment=True)`
Collects evidence from AWS service.
- **Workflow Gate**: Cannot collect evidence without approved assignment
- **Args**:
  - `service`: AWS service name
  - `has_assignment`: Whether staff has approved assignment
- **Returns**: Evidence object or None if blocked

### `execute_test(procedure, has_evidence=True, audit_plan_approved=True)`
Executes a testing procedure.
- **Workflow Gates**: 
  - Cannot execute tests without evidence
  - Cannot execute tests if audit plan not approved
- **Args**:
  - `procedure`: TestProcedure to execute
  - `has_evidence`: Whether evidence has been collected
  - `audit_plan_approved`: Whether audit plan is approved
- **Returns**: Test result or blocked status

### `document_finding(finding)`
Documents an audit finding.
- **Args**: `finding`: Finding object
- **Returns**: Documentation confirmation

---

## Workflow Gates

The system enforces proper audit methodology through workflow gates:

1. **Risk Assessment → Test Procedures**: 
   - Risk assessment identifies WHAT needs to be tested (high-risk areas)
   - Test procedures are created based on those risks (HOW to test them)
   - Maurice must approve risk assessment before test procedures can be created
   - **Rationale**: You can't define test procedures until you know what's risky

2. **Test Procedures Approval → Assignments**: 
   - Maurice must approve the audit plan (containing test procedures) before staff can receive assignments
   - **Rationale**: Staff can't be assigned work until the test procedures are authorized

3. **Assignment Required → Evidence Collection**: 
   - Staff cannot collect evidence without an approved assignment
   - **Rationale**: Staff need authorized work orders before performing audit activities

4. **Evidence Required → Test Execution**: 
   - Staff cannot execute tests without collected evidence
   - **Rationale**: Tests require evidence to evaluate

All blocked operations are logged to the audit trail for transparency.

---

## Human-in-the-Loop Approval

Maurice (Audit Manager) can present assessments for human approval:

### Risk Assessment Approval
```python
result = maurice.review_risk_assessment(
    assessment=risk_assessment,
    company_name="CloudRetail Inc",
    interactive=True  # Prompts for human approval
)
```

### Audit Plan Approval
```python
result = maurice.review_audit_plan(
    plan=audit_plan,
    company_name="CloudRetail Inc",
    interactive=True  # Prompts for human approval
)
```

When `interactive=True`, Maurice presents a detailed summary and prompts:
```
Do you approve this [assessment/plan]? (yes/no/comments): 
```

---

## Audit Trail Transparency

All agent actions are logged with:
- Agent name visible
- Action type and description
- Decision rationale
- Evidence references
- Metadata

Example log entry:
```
[Esther] assess_risk: Assessing risks for CloudRetail Inc in domains: Access Control, Network Security
```

This ensures complete transparency and traceability of all audit activities.

---

## Testing

All agents have comprehensive test coverage:
- Unit tests: 70+ tests passing
- Property-based tests: Planned for future implementation
- Integration tests: Full workflow testing
- Workflow gate tests: Enforcement validation

See `tests/unit/test_audit_team.py` and `tests/unit/test_workflow_gates.py` for details.
