# What is an Audit Plan?

## Overview

An **Audit Plan** is a detailed roadmap that specifies exactly how the audit will be conducted. It's created by the Senior Auditors (Esther, Chuck, Victor) after they complete the risk assessment, and it must be approved by Maurice (Audit Manager) before any testing work can begin.

Think of it as the "battle plan" for the audit engagement.

---

## Components of an Audit Plan

An Audit Plan contains 5 key components:

### 1. **Timeline (ExecutionSchedule)**
A 6-week schedule broken into phases:

```
Week 1-2: Planning & Evidence Collection
Week 3-4: Testing & Analysis  
Week 5-6: Reporting & Review
```

Each phase includes:
- Start and end dates
- Activities to be performed
- Milestones to track progress

**Example**:
```python
Phase 1: "Planning & Evidence Collection"
  Start: 2024-01-01
  End: 2024-01-14
  Activities:
    - Review company documentation
    - Collect IAM policies
    - Gather S3 bucket configurations
    - Document network architecture
```

### 2. **Budget (BudgetAllocation)**
Total audit hours allocated across control domains based on risk levels:

**Example**:
```
Total Hours: 120 hours

By Domain:
  - Access Control: 30 hours (high risk)
  - Data Protection: 25 hours (high risk)
  - Network Security: 20 hours (high risk)
  - Logging & Monitoring: 15 hours (medium risk)
  - Change Management: 15 hours (medium risk)
  - Backup & Recovery: 15 hours (medium risk)
```

**Risk-Based Allocation**: High-risk areas get more audit hours!

### 3. **Test Procedures**
Specific tests that will be performed for each control:

**Example Test Procedure**:
```python
TestProcedure(
    procedure_id="TEST-IAM-001",
    control_domain="Access Control",
    control_objective="Ensure MFA is enabled for privileged accounts",
    procedure_description="Review all IAM users with admin privileges and verify MFA is enabled",
    evidence_required=[
        "IAM user list",
        "MFA status report",
        "Admin policy assignments"
    ],
    assigned_to="Hillel",  # Staff auditor
    estimated_hours=4.0
)
```

Each procedure specifies:
- **What** control is being tested
- **Why** it's being tested (control objective)
- **How** it will be tested (procedure description)
- **What evidence** is needed
- **Who** will do the work
- **How long** it will take

### 4. **Resource Allocation**
Which auditors work on which domains:

```
Esther (Senior) + Hillel (Staff):
  - Access Control: 30 hours
  - Network Security: 20 hours

Chuck (Senior) + Neil (Staff):
  - Data Protection: 25 hours
  - Logging & Monitoring: 15 hours

Victor (Senior) + Juman (Staff):
  - Change Management: 15 hours
  - Backup & Recovery: 15 hours
```

### 5. **Approval Tracking**
Tracks whether Maurice has approved the plan:

```python
approved: bool = False
approved_by: Optional[str] = None  # "Maurice"
approved_at: Optional[datetime] = None  # Timestamp
review_comments: Optional[str] = None  # Maurice's feedback
```

---

## Real Example: What Maurice Sees

When Maurice reviews an audit plan (with `interactive=True`), he sees:

```
================================================================================
AUDIT PLAN REVIEW - CloudRetail Inc
================================================================================

Reviewer: Maurice (Audit Manager)
Date: 2024-01-15 10:30:00

TIMELINE:
  Start Date: 2024-01-15
  End Date: 2024-02-26
  Duration: 42 days
  Phases: 3
    - Planning & Evidence Collection: 2024-01-15 to 2024-01-28
    - Testing & Analysis: 2024-01-29 to 2024-02-11
    - Reporting & Review: 2024-02-12 to 2024-02-26

BUDGET:
  Total Hours: 120
  Allocation by Domain:
    - Access Control: 30 hours
    - Data Protection: 25 hours
    - Network Security: 20 hours
    - Logging & Monitoring: 15 hours
    - Change Management: 15 hours
    - Backup & Recovery: 15 hours

TEST PROCEDURES (18 total):

  Access Control (6 procedures):
    • Ensure MFA is enabled for privileged accounts
      Procedure: Review all IAM users with admin privileges and verify MFA
      Assigned to: Hillel
      Estimated: 4 hours
      Evidence: IAM user list, MFA status report, Admin policy assignments

    • Verify least privilege access controls
      Procedure: Review IAM policies for excessive permissions
      Assigned to: Hillel
      Estimated: 5 hours
      Evidence: IAM policies, Role assignments, Permission boundaries

    [... more procedures ...]

  Data Protection (5 procedures):
    • Verify encryption at rest for sensitive data
      Procedure: Check S3 bucket encryption settings for customer data
      Assigned to: Neil
      Estimated: 5 hours
      Evidence: S3 bucket configurations, Encryption settings, KMS keys

    [... more procedures ...]

================================================================================
APPROVAL REQUIRED
================================================================================

The audit plan must be approved before test execution can begin.
Review the test procedures above to ensure they are appropriate.

Do you approve this audit plan? (yes/no/comments): 
```

---

## Why Must Risk Assessment Be Approved Before Creating Test Procedures?

The risk assessment is the **INPUT** for creating test procedures:

```
Risk Assessment → Identifies WHAT to test (the risks)
        ↓
Test Procedures → Defines HOW to test those risks
        ↓
Assignments → Authorizes WHO executes the tests
```

**Example Flow**:

1. **Risk Assessment** (by Esther) - Identifies WHAT to test:
   ```
   Finding: "Admin account without MFA" = HIGH RISK
   Impact: High (affects Customer Database - PII)
   Likelihood: High
   
   → This tells us: "MFA controls need testing"
   ```

2. **Test Procedures Created** (by Esther, based on risk assessment) - Defines HOW to test:
   ```
   Because MFA is HIGH RISK, create test procedure:
   
   TEST-IAM-001:
   - Control: "Ensure MFA enabled for privileged accounts"
   - Procedure: "Review all IAM users with admin privileges and verify MFA"
   - Evidence: IAM user list, MFA status report
   - Assigned to: Hillel
   - Hours: 4
   ```

3. **Audit Plan Approved** (by Maurice) - Authorizes execution:
   ```
   Maurice reviews all test procedures and approves them
   → Now Hillel can receive the assignment and start work
   ```

**Why this sequence matters**:

- If Maurice rejects the risk assessment (e.g., "You missed a critical risk!"), then the test procedures would be incomplete because they're based on incomplete risk information
- You can't define test procedures until you know what's risky
- You can't assign work to staff until the test procedures are authorized

**That's why the workflow enforces**: 
1. Risk Assessment Approval → THEN → Test Procedures Created
2. Test Procedures Approval → THEN → Assignments Made

---

## Workflow Gates in Action

### ✅ Correct Sequence:
```
1. Esther assesses risks → Creates RiskAssessment
2. Maurice reviews & approves RiskAssessment (interactive=True)
3. Esther creates audit plan based on approved risks → Creates AuditPlan
4. Maurice reviews & approves AuditPlan (interactive=True)
5. Esther assigns tasks to Hillel → Hillel can now work
6. Hillel collects evidence and executes tests
```

### ❌ Blocked Sequence:
```
1. Esther assesses risks → Creates RiskAssessment
2. Maurice REJECTS RiskAssessment (needs revision)
3. Esther tries to create audit plan → ⚠️ BLOCKED
   Error: "Cannot create audit plan - risk assessment not approved"
```

### ❌ Another Blocked Sequence:
```
1. Esther creates audit plan → Creates AuditPlan
2. Maurice hasn't approved it yet
3. Esther tries to assign task to Hillel → ⚠️ BLOCKED
4. Hillel tries to collect evidence → ⚠️ BLOCKED
   Error: "Cannot accept assignment - audit plan not approved"
```

---

## Summary

**Audit Plan** = The detailed execution roadmap containing:
- **When**: 6-week timeline with phases
- **How much**: Budget allocation by risk level
- **What**: Specific test procedures for each control
- **Who**: Resource assignments (which auditor does what)
- **Status**: Approval tracking by Maurice

**Why the gate exists**: The audit plan is based on the risk assessment, so you can't approve a plan that's based on unapproved (or wrong) risk information.

**Real-world parallel**: You wouldn't approve a construction plan before approving the architectural design it's based on!

---

## See It In Action

Run this example to see the full workflow with approvals:

```bash
python examples/full_approval_workflow.py
```

This will show you:
1. Risk assessment → Your approval
2. Audit plan creation → Your approval  
3. Test execution → Only after both approvals

You'll see exactly what Maurice sees when reviewing the audit plan!
