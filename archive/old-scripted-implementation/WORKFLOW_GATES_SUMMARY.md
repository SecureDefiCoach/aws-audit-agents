# Workflow Gates - Quick Reference

## The Core Principle

**Each step produces the INPUT for the next step.**

You can't do step N+1 until step N is complete and approved.

---

## The 4 Gates

### Gate 1: Risk Assessment → Test Procedures
**Rule**: Risk assessment must be approved before test procedures can be created

**Why**: Risk assessment identifies WHAT to test (the risks). Test procedures define HOW to test those risks. You can't define HOW until you know WHAT.

**Example**:
```
Risk Assessment: "Admin without MFA = HIGH RISK"
        ↓ (INPUT)
Test Procedure: "Review all admin IAM users and verify MFA enabled"
```

---

### Gate 2: Test Procedures → Assignments
**Rule**: Test procedures must be approved before staff can receive assignments

**Why**: Test procedures define the authorized scope of work. Staff can't be assigned unauthorized work.

**Example**:
```
Test Procedure: "TEST-IAM-001: Verify MFA for admin accounts"
        ↓ (APPROVED)
Assignment to Hillel: "Execute TEST-IAM-001"
```

---

### Gate 3: Assignment → Evidence Collection
**Rule**: Staff cannot collect evidence without an approved assignment

**Why**: Staff need authorized work orders before performing audit activities.

**Example**:
```
Assignment: "Hillel: Collect IAM evidence for TEST-IAM-001"
        ↓ (AUTHORIZED)
Evidence Collection: Hillel collects IAM user data
```

---

### Gate 4: Evidence → Test Execution
**Rule**: Staff cannot execute tests without collected evidence

**Why**: Tests evaluate evidence against control criteria. You can't evaluate what you don't have.

**Example**:
```
Evidence: "IAM user admin-john, MFA=False"
        ↓ (FACTS)
Test Execution: Compare against requirement "MFA must be enabled"
Result: FAIL
```

---

## Visual Flow

```
┌──────────────────┐
│ Risk Assessment  │ ← Identifies WHAT to test
└────────┬─────────┘
         │ INPUT
         ↓
┌──────────────────┐
│ Test Procedures  │ ← Defines HOW to test
└────────┬─────────┘
         │ APPROVAL
         ↓
┌──────────────────┐
│ Assignments      │ ← Authorizes WHO executes
└────────┬─────────┘
         │ WORK ORDER
         ↓
┌──────────────────┐
│ Evidence         │ ← Gathers FACTS
└────────┬─────────┘
         │ DATA
         ↓
┌──────────────────┐
│ Test Execution   │ ← Evaluates facts
└──────────────────┘
```

---

## What Gets Blocked

### ❌ Blocked: Creating test procedures before risk assessment approved
```python
# Risk assessment not approved yet
esther.create_audit_plan(company, risk_assessment, hours)
# Result: Can't create test procedures - don't know what's risky yet!
```

### ❌ Blocked: Assigning work before test procedures approved
```python
# Audit plan (test procedures) not approved yet
esther.supervise_staff(hillel, task)
# Result: Can't assign unauthorized work!
```

### ❌ Blocked: Collecting evidence without assignment
```python
# Hillel has no assignment
hillel.collect_evidence("IAM")
# Result: Can't work without authorization!
```

### ❌ Blocked: Executing tests without evidence
```python
# No evidence collected yet
hillel.execute_test(procedure)
# Result: Can't test without facts!
```

---

## Real-World Analogy

Building a house:

1. **Survey** (Risk Assessment) → "Soil is unstable" (WHAT's risky)
2. **Foundation Design** (Test Procedures) → "Use deep pilings" (HOW to address risk)
3. **Work Order** (Assignment) → "Crew: Build foundation" (WHO does it)
4. **Materials** (Evidence) → Concrete, rebar delivered (FACTS)
5. **Construction** (Test Execution) → Build using materials (EVALUATE)

You can't design the foundation before knowing the soil is unstable!

---

## Key Takeaway

**Risk Assessment is the INPUT for test procedures, not just a prerequisite.**

The workflow enforces: WHAT → HOW → WHO → FACTS → EVALUATE
