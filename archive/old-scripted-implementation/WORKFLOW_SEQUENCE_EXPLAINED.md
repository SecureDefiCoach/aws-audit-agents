# Audit Workflow Sequence - The "Why" Behind Each Gate

## The Core Principle

Each step in the audit workflow **produces the input** needed for the next step. You can't do step N+1 until step N is complete and approved.

---

## The Complete Sequence

```
┌─────────────────────────────────────────────────────────────────┐
│ Step 1: RISK ASSESSMENT                                         │
│ Agent: Esther (Senior Auditor)                                  │
│ Output: List of risks with severity levels                      │
│                                                                  │
│ Example Output:                                                 │
│   • "Admin without MFA" = HIGH RISK                            │
│   • "Unencrypted S3 bucket" = HIGH RISK                        │
│   • "SSH open to internet" = HIGH RISK                         │
│                                                                  │
│ This tells us WHAT needs to be tested                          │
└─────────────────────────────────────────────────────────────────┘
                            ↓
                    ⚠️ GATE 1: APPROVAL
                    Maurice reviews & approves
                    
                    WHY? If risks are wrong/incomplete,
                    everything built on them will be wrong
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 2: CREATE TEST PROCEDURES                                  │
│ Agent: Esther (Senior Auditor)                                  │
│ Input: Approved risk assessment                                 │
│ Output: Specific test procedures                                │
│                                                                  │
│ Example Output:                                                 │
│   TEST-IAM-001:                                                 │
│   • Control: "Ensure MFA for privileged accounts"              │
│   • Procedure: "Review IAM users, verify MFA enabled"          │
│   • Evidence: IAM user list, MFA status                        │
│   • Assigned to: Hillel                                        │
│   • Hours: 4                                                    │
│                                                                  │
│ This defines HOW to test the risks                             │
└─────────────────────────────────────────────────────────────────┘
                            ↓
                    ⚠️ GATE 2: APPROVAL
                    Maurice reviews & approves test procedures
                    
                    WHY? Staff can't be assigned unauthorized work.
                    Test procedures must be reviewed for appropriateness.
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 3: MAKE ASSIGNMENTS                                        │
│ Agent: Esther (Senior Auditor)                                  │
│ Input: Approved test procedures                                 │
│ Output: Work assignments to staff                               │
│                                                                  │
│ Example Output:                                                 │
│   Assignment to Hillel:                                         │
│   • Task: Execute TEST-IAM-001                                 │
│   • Collect IAM evidence                                       │
│   • Report findings                                            │
│                                                                  │
│ This authorizes WHO does the work                              │
└─────────────────────────────────────────────────────────────────┘
                            ↓
                    ⚠️ GATE 3: ASSIGNMENT CHECK
                    Hillel can only work if he has an assignment
                    
                    WHY? Staff need authorized work orders
                    before performing audit activities
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 4: COLLECT EVIDENCE                                        │
│ Agent: Hillel (Staff Auditor)                                   │
│ Input: Approved assignment                                      │
│ Output: Evidence collected from AWS                             │
│                                                                  │
│ Example Output:                                                 │
│   Evidence-IAM-001:                                             │
│   • IAM user: admin-john                                       │
│   • MFA enabled: False                                         │
│   • Admin policy: AdministratorAccess                          │
│   • Last login: 2024-01-10                                     │
│                                                                  │
│ This gathers the facts needed for testing                      │
└─────────────────────────────────────────────────────────────────┘
                            ↓
                    ⚠️ GATE 4: EVIDENCE CHECK
                    Hillel can only execute tests if he has evidence
                    
                    WHY? You can't test without facts to evaluate
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 5: EXECUTE TEST                                            │
│ Agent: Hillel (Staff Auditor)                                   │
│ Input: Evidence + Test procedure                                │
│ Output: Test result (Pass/Fail)                                 │
│                                                                  │
│ Example Output:                                                 │
│   Test Result:                                                  │
│   • Test: TEST-IAM-001                                         │
│   • Result: FAIL                                               │
│   • Finding: "Admin account admin-john has no MFA"            │
│   • Severity: HIGH                                             │
│                                                                  │
│ This evaluates the evidence against the control                │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 6: CREATE WORKPAPER                                        │
│ Agent: Esther (Senior Auditor)                                  │
│ Input: Test results + Evidence                                  │
│ Output: Documented audit workpaper                              │
│                                                                  │
│ This creates the audit documentation                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## Why Each Gate Exists

### Gate 1: Risk Assessment Approval

**Question**: Why can't we create test procedures before risk assessment is approved?

**Answer**: Because the risk assessment tells us WHAT to test. 

**Example**:
- If risk assessment says "MFA is HIGH RISK" → Create 6 IAM test procedures
- If risk assessment says "MFA is LOW RISK" → Create 1 IAM test procedure
- If Maurice rejects risk assessment saying "You missed encryption risks!" → We need to add encryption test procedures

**Without approval**: We might create test procedures for the wrong things, wasting audit hours on low-risk areas while missing high-risk areas.

---

### Gate 2: Test Procedures Approval

**Question**: Why can't we assign work to staff before test procedures are approved?

**Answer**: Because test procedures define the authorized scope of work.

**Example**:
- Test procedure says: "Review IAM users with admin privileges"
- Maurice might say: "No, that's too narrow. Review ALL IAM users, not just admins"
- If Hillel already started work on the narrow scope, he'd have to redo it

**Without approval**: Staff might perform inappropriate or insufficient testing, leading to audit deficiencies.

---

### Gate 3: Assignment Required

**Question**: Why can't staff collect evidence without an assignment?

**Answer**: Because staff need authorized work orders before performing audit activities.

**Example**:
- Hillel can't just randomly decide to collect S3 bucket data
- He needs Esther to assign him: "Collect S3 evidence for TEST-S3-001"
- This ensures work is coordinated and tracked

**Without assignment**: Chaos - staff doing random work, duplicating effort, missing required tests.

---

### Gate 4: Evidence Required

**Question**: Why can't staff execute tests without evidence?

**Answer**: Because tests evaluate evidence against control criteria.

**Example**:
- Test: "Verify MFA is enabled for admin accounts"
- Without evidence: How do you verify? You need the IAM user data!
- With evidence: Compare IAM user data against MFA requirement

**Without evidence**: Tests would be meaningless - you can't evaluate what you don't have.

---

## Real-World Analogy

Think of building a house:

```
1. Architectural Survey (Risk Assessment)
   → Identifies: "Soil is unstable" (HIGH RISK)
   ⚠️ APPROVAL: Architect reviews survey
   
2. Foundation Design (Test Procedures)
   → Creates: "Deep foundation with pilings" (based on soil risk)
   ⚠️ APPROVAL: Architect approves foundation design
   
3. Work Orders (Assignments)
   → Assigns: "Construction crew: Build foundation per design"
   ⚠️ CHECK: Crew has authorized work order
   
4. Materials Delivered (Evidence)
   → Delivers: Concrete, rebar, pilings
   ⚠️ CHECK: Materials match specifications
   
5. Build Foundation (Execute Test)
   → Constructs: Foundation using materials per design
```

You can't design the foundation before knowing the soil is unstable.
You can't assign construction before the foundation design is approved.
You can't build without materials.

**Same logic applies to auditing!**

---

## Summary

Each gate enforces a dependency:

| Gate | Enforces | Reason |
|------|----------|--------|
| Gate 1 | Risk Assessment → Test Procedures | Risk assessment is INPUT for test procedures |
| Gate 2 | Test Procedures → Assignments | Test procedures define authorized work scope |
| Gate 3 | Assignments → Evidence Collection | Staff need work orders before acting |
| Gate 4 | Evidence → Test Execution | Tests evaluate evidence against criteria |

**Bottom line**: Each step produces the input needed for the next step. You can't skip ahead!
