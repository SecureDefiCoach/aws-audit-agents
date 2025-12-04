# Knowledge Structure Update - Shared Control Procedures

## Summary

Updated the agent knowledge system to use **shared control procedures** that any auditor can use, rather than siloing procedures by individual agent.

## Problem Solved

Previously, audit procedures were stored in individual agent folders (e.g., `knowledge/victor/logging-monitoring-procedures.md`). This meant:
- Only Victor could test logging controls
- Only Neil could test encryption controls
- Procedures weren't reusable across the team
- Knowledge was artificially siloed

## New Structure

### Shared Procedures (Available to All Auditors)

Located in `knowledge/shared/`:

1. **iam-control-procedures.md** - IAM control testing procedures
   - Root account protection
   - MFA enforcement
   - Least privilege access
   - Password policy
   - Access key rotation
   - IAM role usage
   - Inactive user accounts
   - Privileged access monitoring

2. **logging-control-procedures.md** - Logging and monitoring procedures
   - CloudTrail configuration
   - Log retention and storage
   - Log monitoring and alerting
   - VPC Flow Logs
   - CloudWatch Logs
   - Log integrity and protection
   - Incident response logging
   - SIEM integration

3. **encryption-control-procedures.md** - Encryption control procedures
   - S3 bucket encryption
   - EBS volume encryption
   - RDS database encryption
   - Encryption key management
   - Encryption in transit
   - Certificate management
   - Secrets management
   - Data classification and encryption standards

4. **network-control-procedures.md** - Network security procedures
   - Security group configuration
   - Network ACL configuration
   - VPC configuration and isolation
   - Internet gateway and NAT configuration
   - VPN and Direct Connect security
   - Public IP address management
   - Network segmentation
   - Network monitoring and logging

### Role-Specific Knowledge

Located in `knowledge/{agent_name}/`:

These files contain **role-specific guidance only**, not control procedures:

- **Maurice**: Audit manager duties, workpaper review, risk assessment oversight
- **Esther**: Senior auditor responsibilities, team supervision
- **Chuck**: Evidence provider role, company representative duties
- **Hillel**: Staff auditor basics, evidence gathering
- **Victor**: Senior auditor responsibilities (when active)
- **Neil**: Staff auditor basics (when active)
- **Juman**: Staff auditor basics (when active)

## How It Works

### Automatic Loading

When an agent is created with `load_knowledge=True`:

1. **First**: Loads ALL shared procedures from `knowledge/shared/`
2. **Then**: Loads agent-specific knowledge from `knowledge/{agent_name}/`

Example for Hillel:
```python
hillel = factory.create_agent("hillel", load_knowledge=True)
```

Hillel gets:
- ✅ All 4 shared control procedures (IAM, Logging, Encryption, Network)
- ✅ His role-specific knowledge (evidence-gathering-basics.md)

### Benefits

1. **Flexibility**: Any auditor can be assigned any control
   - Esther can test IAM controls
   - Hillel can test IAM controls if assigned
   - Victor can test IAM controls if needed

2. **Consistency**: All auditors use the same procedures
   - Same testing steps
   - Same evidence requirements
   - Same risk assessment criteria

3. **Efficiency**: No duplicate procedure documentation
   - One source of truth for each control domain
   - Updates apply to all auditors

4. **Realistic**: Matches real audit practice
   - Procedures are standardized across team
   - Any qualified auditor can perform any test
   - Assignment based on workload and expertise, not artificial restrictions

## Implementation Details

### Code Changes

**File**: `src/agents/audit_agent.py`

Updated `load_knowledge()` method to:
1. Load shared procedures first
2. Then load agent-specific knowledge
3. Print what was loaded for visibility

```python
def load_knowledge(self, path: str):
    # Load shared procedures first (available to all auditors)
    shared_dir = Path("knowledge/shared")
    if shared_dir.exists():
        for file in shared_dir.glob("*.md"):
            procedure_name = f"shared/{file.stem}"
            procedure_content = file.read_text()
            self.knowledge[procedure_name] = procedure_content
            print(f"📚 {self.name}: Loaded shared procedure '{file.stem}'")
    
    # Load agent-specific knowledge
    knowledge_dir = Path(path)
    if knowledge_dir.exists():
        for file in knowledge_dir.glob("*.md"):
            procedure_name = file.stem
            procedure_content = file.read_text()
            self.knowledge[procedure_name] = procedure_content
            print(f"📚 {self.name}: Loaded knowledge '{procedure_name}'")
```

### Files Created

1. `knowledge/shared/iam-control-procedures.md` (comprehensive IAM testing)
2. `knowledge/shared/logging-control-procedures.md` (comprehensive logging testing)
3. `knowledge/shared/encryption-control-procedures.md` (comprehensive encryption testing)
4. `knowledge/shared/network-control-procedures.md` (comprehensive network testing)

### Files to Update (Next Steps)

Role-specific knowledge files should be updated to remove control procedures and focus on role duties:

- `knowledge/maurice/*.md` - Keep manager-specific guidance
- `knowledge/esther/*.md` - Keep senior auditor guidance, remove control procedures
- `knowledge/hillel/*.md` - Keep staff auditor basics
- `knowledge/chuck/*.md` - Keep evidence provider guidance
- `knowledge/victor/*.md` - Update to senior auditor guidance only
- `knowledge/neil/*.md` - Update to staff auditor basics only
- `knowledge/juman/*.md` - Update to staff auditor basics only

## Example Usage

### Risk Assessment Scenario

During risk assessment, Esther identifies these high-risk controls:
1. IAM - Root account protection (High risk)
2. IAM - MFA enforcement (High risk)
3. Logging - CloudTrail configuration (High risk)

### Task Assignment

Esther can assign:
- **Hillel**: Test IAM root account control
  - Hillel has `iam-control-procedures.md` loaded
  - He follows the standardized procedure
  - He can complete the test independently

- **Hillel**: Test IAM MFA enforcement
  - Same procedures available
  - Consistent testing approach

- **Victor** (if active): Test CloudTrail configuration
  - Victor has `logging-control-procedures.md` loaded
  - He follows the standardized procedure

### Flexibility Example

If Victor is unavailable and logging controls need testing:
- Esther can assign logging controls to Hillel
- Hillel has the logging procedures loaded
- He can perform the tests following the procedures
- Esther reviews his work as senior auditor

## Dashboard Impact

When viewing agents in the dashboard:

**Knowledge Tab** will show:
- Shared procedures (4 control domains)
- Agent-specific knowledge (role guidance)

Example for Hillel:
```
Knowledge Files:
✓ shared/iam-control-procedures
✓ shared/logging-control-procedures
✓ shared/encryption-control-procedures
✓ shared/network-control-procedures
✓ evidence-gathering-basics
```

## Benefits for System Prompt Tuning

This structure makes system prompt tuning easier:

1. **Control procedures** are in shared files (standardized)
2. **Role behavior** is in system prompts (customizable)
3. **Role guidance** is in agent-specific knowledge (supplementary)

You can tune how agents behave without changing control procedures.

## Next Steps

1. ✅ Shared procedures created
2. ✅ Agent base class updated to load shared procedures
3. ⏳ Test dashboard with all 7 agents
4. ⏳ Update role-specific knowledge files (remove duplicate procedures)
5. ⏳ Review system prompts for each agent
6. ⏳ Begin controlled testing with risk assessment

---

**Created**: December 4, 2025  
**Purpose**: Document shared control procedure implementation  
**Status**: Core implementation complete, ready for testing
