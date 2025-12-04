# Human-in-the-Loop Risk Assessment Approval

## Overview

Added human-in-the-loop approval for risk assessments, ensuring proper audit governance and oversight before proceeding to audit planning and execution.

## What Was Added

### 1. Risk Assessment Approval Tracking

Enhanced `RiskAssessment` model in `src/models/risk.py`:

```python
@dataclass
class RiskAssessment:
    inherent_risks: List[Risk]
    residual_risks: List[Risk]
    prioritized_domains: List[ControlDomain]
    risk_matrix: Dict[str, str]
    
    # Approval tracking
    approved: bool = False
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    review_comments: Optional[str] = None
```

### 2. Maurice's Review Method

Added `review_risk_assessment()` to `AuditManagerAgent`:

**Features:**
- Presents comprehensive risk assessment summary
- Shows prioritized control domains
- Highlights high-risk issues
- Prompts for human approval (yes/no/comments)
- Updates risk assessment with approval status
- Logs all decisions to audit trail

**Interactive Prompts:**
```
Do you approve this risk assessment? (yes/no/comments):
```

**Options:**
- `yes` / `y` / `approve` → Approves and allows proceeding
- `no` / `n` / `reject` → Rejects and requests revision with feedback
- `comments` / `c` → Add comments and continue review

### 3. Interactive Example

Created `examples/risk_assessment_approval.py` demonstrating:
1. Senior auditors perform risk assessment
2. Maurice presents for human review
3. Human approves or rejects
4. System responds based on decision

## Proper Audit Workflow

### Phase 1: Risk Assessment
```
1. Senior Auditors → Perform risk assessment
2. Maurice → Review and present to human
3. Human → Approve or reject
   ├─ If approved → Proceed to Phase 2
   └─ If rejected → Revise and re-submit
```

### Phase 2: Audit Planning (After Approval)
```
4. Senior Auditors → Create audit plan
5. Maurice → Review and present to human
6. Human → Approve or reject
   ├─ If approved → Proceed to Phase 3
   └─ If rejected → Revise and re-submit
```

### Phase 3: Execution (After Approval)
```
7. Audit Team → Execute approved test procedures
8. Collect evidence and document findings
```

## Example Output

```
================================================================================
RISK ASSESSMENT REVIEW - CloudRetail Inc
================================================================================

Reviewer: Maurice (Audit Manager)
Date: 2025-12-03 17:30:00

SUMMARY:
  Total Inherent Risks: 4
  Total Residual Risks: 4
  High-Risk Areas: 3
  Medium-Risk Areas: 1
  Low-Risk Areas: 0

PRIORITIZED CONTROL DOMAINS:
  1. IAM - Risk Level: HIGH
  2. Data Encryption - Risk Level: HIGH
  3. Network Security - Risk Level: HIGH
  4. Logging - Risk Level: MEDIUM

HIGH-RISK ISSUES REQUIRING ATTENTION:

  • Administrator account without MFA enabled - Affects: Administrator Account
    Domain: IAM
    Impact: HIGH | Likelihood: HIGH

  • Customer data bucket without encryption at rest - Affects: Customer Database
    Domain: Data Encryption
    Impact: HIGH | Likelihood: HIGH

  • SSH port 22 open to internet (0.0.0.0/0) - Affects: Payment Processing System
    Domain: Network Security
    Impact: HIGH | Likelihood: HIGH

================================================================================
APPROVAL REQUIRED
================================================================================

The risk assessment must be approved before proceeding to audit planning.

Do you approve this risk assessment? (yes/no/comments): 
```

## Benefits

1. **Proper Governance**: Human oversight at critical decision points
2. **Audit Trail**: All approvals/rejections logged with rationale
3. **Quality Control**: Ensures risk assessment is reviewed before planning
4. **Flexibility**: Can reject and request revisions
5. **Transparency**: Clear presentation of risks and priorities
6. **Compliance**: Follows standard audit methodology

## Usage

### Running the Interactive Example

```bash
PYTHONPATH=. python examples/risk_assessment_approval.py
```

This will:
1. Load CloudRetail Inc company profile
2. Have senior auditors perform risk assessment
3. Present to you (as Maurice) for approval
4. Wait for your decision
5. Proceed based on your approval/rejection

### In Code

```python
# Senior auditors perform assessment
risk_assessment = esther.assess_risk(company)

# Maurice reviews and gets human approval
maurice = AuditManagerAgent()
review = maurice.review_risk_assessment(risk_assessment, company.name)

# Check if approved
if review["approved"]:
    # Proceed to audit planning
    audit_plan = esther.create_audit_plan(risk_assessment)
else:
    # Revise based on feedback
    print(f"Revision needed: {review['comments']}")
```

## Next Steps

Similar approval gates should be added for:
1. **Audit Plan Approval** - Before test execution
2. **Test Procedure Approval** - Before evidence collection
3. **Workpaper Review** - Before finalizing findings
4. **Report Sign-off** - Before distribution

This ensures human oversight at every critical phase of the audit.

## Files Modified

- `src/models/risk.py` - Added approval tracking fields
- `src/agents/audit_team.py` - Added `review_risk_assessment()` method

## Files Created

- `examples/risk_assessment_approval.py` - Interactive demonstration
- `HUMAN_IN_THE_LOOP_APPROVAL.md` - This document

## Testing

✅ All existing tests pass  
✅ Maurice can review risk assessments  
✅ Approval status tracked correctly  
✅ Audit trail logs all decisions  
✅ Interactive example ready to run  

You can now run the interactive example to approve or reject risk assessments before the audit team proceeds to planning!
