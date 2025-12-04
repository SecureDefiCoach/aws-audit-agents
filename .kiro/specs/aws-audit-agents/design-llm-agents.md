# LLM-Based Audit Agents - Design Document

## Overview

This system implements **true autonomous agents** using Large Language Models (LLMs) to perform AWS audits. Each agent reasons independently, makes decisions, and documents their work - demonstrating genuine agentic behavior.

**Core Principle**: Agents are given **goals and tools**, not step-by-step instructions. They reason about how to achieve their goals, adapt to what they discover, and document their thinking in professional workpapers.

---

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Local Computer (Your Machine)                              │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Orchestrator                                       │    │
│  │  - Assigns goals to agents                         │    │
│  │  - Monitors agent progress                         │    │
│  │  - Handles rate limiting                           │    │
│  │  - Coordinates human approvals                     │    │
│  └────────────────────────────────────────────────────┘    │
│                          │                                   │
│         ┌────────────────┼────────────────┐                │
│         │                │                │                │
│         ▼                ▼                ▼                │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐            │
│  │  Esther  │    │  Chuck   │    │  Victor  │            │
│  │  (LLM)   │    │  (LLM)   │    │  (LLM)   │            │
│  │          │    │          │    │          │            │
│  │ Tools:   │    │ Tools:   │    │ Tools:   │            │
│  │ - IAM    │    │ - S3     │    │ - CT     │            │
│  │ - WP     │    │ - EC2    │    │ - CW     │            │
│  └──────────┘    └──────────┘    └──────────┘            │
│         │                │                │                │
└─────────┼────────────────┼────────────────┼────────────────┘
          │                │                │
          │    boto3 SDK (AWS API calls)   │
          │                │                │
          ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────┐
│  AWS Account (CloudRetail Inc - Audit Target)               │
│                                                              │
│  • IAM users (with security issues)                         │
│  • S3 buckets (unencrypted, public)                        │
│  • EC2 instances (weak security groups)                    │
│  • VPC (network misconfigurations)                         │
│  • CloudTrail (logging gaps)                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Agent Architecture

### Core Agent Structure

Each agent has:

1. **LLM Brain**: Reasons about goals and makes decisions
2. **Tools**: AWS clients, workpaper writer, evidence collector
3. **Memory**: Context about the audit and previous actions
4. **Goal**: High-level objective to achieve

```python
class AuditAgent:
    def __init__(self, name, role, llm, tools):
        self.name = name
        self.role = role
        self.llm = llm  # Ollama, Claude, or GPT-4
        self.tools = tools  # AWS clients, workpaper tool, etc.
        self.memory = []  # Conversation history
        self.current_goal = None
    
    def set_goal(self, goal: str):
        """Give agent a goal to achieve"""
        self.current_goal = goal
    
    def reason(self) -> str:
        """Agent reasons about how to achieve goal"""
        prompt = f"""
        You are {self.name}, a {self.role}.
        
        Your goal: {self.current_goal}
        
        Available tools: {self.tools}
        
        What should you do next? Think step by step.
        """
        return self.llm.chat(prompt, self.memory)
    
    def act(self, action: str):
        """Agent executes an action using tools"""
        # Parse action and call appropriate tool
        result = self.execute_tool(action)
        self.memory.append({"action": action, "result": result})
        return result
    
    def document(self, findings: str):
        """Agent documents work in workpaper"""
        workpaper = self.tools['workpaper'].create(
            agent=self.name,
            findings=findings,
            reasoning=self.memory
        )
        return workpaper
```

---

## The Audit Team

### Esther - Senior Auditor (IAM & Access Control)

**Role**: Lead auditor for identity and access management

**Goal Example**: 
> "Assess IAM risks for CloudRetail Inc. Identify security issues related to user access, MFA, permissions, and credential management. Document your findings in a professional workpaper."

**Tools**:
- `IAMClient`: List users, get credential reports, check MFA status
- `WorkpaperTool`: Create and update workpapers
- `EvidenceTool`: Store and reference evidence

**Reasoning Example**:
```
Esther's thought process (visible in workpaper):

"I need to assess IAM risks. Let me start by understanding what IAM 
resources exist in this account.

First, I'll list all IAM users to see who has access...
[calls IAMClient.list_users()]

I found 5 users. Now I should check if they have MFA enabled, as 
missing MFA is a critical risk...
[calls IAMClient.get_credential_report()]

Concerning: I found 3 users without MFA, including 'admin-john' who 
has AdministratorAccess policy. This is HIGH RISK because...

Let me also check for overly permissive policies...
[calls IAMClient.list_policies()]

Finding: The 'developer-access' policy grants s3:* permissions, which 
violates least privilege principle...

I'll document these findings in my workpaper with evidence references."
```

### Chuck - Senior Auditor (Data Protection & Network)

**Role**: Lead auditor for encryption and network security

**Goal Example**:
> "Assess data protection and network security risks for CloudRetail Inc. Examine S3 encryption, EC2 security groups, and VPC configurations. Document findings with clear risk ratings."

**Tools**:
- `S3Client`: List buckets, check encryption, review policies
- `EC2Client`: List instances, review security groups
- `VPCClient`: Review VPC configuration, subnets, NACLs
- `WorkpaperTool`: Document findings

### Victor - Senior Auditor (Logging & Monitoring)

**Role**: Lead auditor for logging, monitoring, and incident response

**Goal Example**:
> "Assess logging and monitoring controls for CloudRetail Inc. Verify CloudTrail configuration, CloudWatch alarms, and log retention. Identify gaps in detective controls."

**Tools**:
- `CloudTrailClient`: Check trail status, review events
- `CloudWatchClient`: List alarms, check SNS topics
- `WorkpaperTool`: Document findings

### Maurice - Audit Manager

**Role**: Review agent work and approve findings

**Goal Example**:
> "Review the workpapers created by Esther, Chuck, and Victor. Assess whether their findings are well-supported by evidence and their risk ratings are appropriate. Approve or request revisions."

**Tools**:
- `WorkpaperReviewer`: Read and comment on workpapers
- `ApprovalTool`: Approve or reject findings

---

## Agent Communication Protocol

Agents communicate through **natural language messages**, not function calls:

```python
# Esther sends message to Maurice
esther.send_message(
    to="Maurice",
    message="""
    I've completed my IAM risk assessment for CloudRetail Inc.
    
    Key findings:
    - 3 users without MFA (HIGH RISK)
    - Overly permissive developer policy (MEDIUM RISK)
    - No password policy configured (MEDIUM RISK)
    
    My workpaper is ready for your review: WP-IAM-001
    
    I recommend we prioritize the MFA issue as it affects privileged accounts.
    """
)

# Maurice responds
maurice.send_message(
    to="Esther",
    message="""
    I've reviewed WP-IAM-001. Your findings are well-documented.
    
    Question: For the developer policy issue, did you verify what 
    resources they actually access? The policy may be overly broad 
    but if they only use specific buckets, the residual risk is lower.
    
    Please investigate actual usage patterns and update your risk rating.
    """
)

# Esther adapts based on feedback
esther.set_goal(
    "Investigate actual S3 usage by developers to refine risk rating"
)
```

---

## LLM Integration

### LLM Options

**Development** (Free):
```python
import ollama

llm = ollama.Client()
response = llm.chat(
    model='llama3',
    messages=[{'role': 'user', 'content': prompt}]
)
```

**Production** (Low Cost):
```python
import anthropic

llm = anthropic.Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])
response = llm.messages.create(
    model='claude-3-haiku-20240307',  # $0.25 per 1M input tokens
    messages=[{'role': 'user', 'content': prompt}]
)
```

**Premium** (Best Reasoning):
```python
import openai

llm = openai.OpenAI(api_key=os.environ['OPENAI_API_KEY'])
response = llm.chat.completions.create(
    model='gpt-4-turbo',
    messages=[{'role': 'user', 'content': prompt}]
)
```

### Rate Limiting Strategy

```python
class RateLimiter:
    def __init__(self, max_calls_per_minute=10):
        self.max_calls = max_calls_per_minute
        self.calls = []
    
    def wait_if_needed(self):
        """Pause if rate limit reached"""
        now = time.time()
        # Remove calls older than 1 minute
        self.calls = [c for c in self.calls if now - c < 60]
        
        if len(self.calls) >= self.max_calls:
            wait_time = 60 - (now - self.calls[0])
            print(f"Rate limit reached. Pausing for {wait_time:.0f}s...")
            time.sleep(wait_time)
        
        self.calls.append(now)
```

---

## Tools Architecture

### Tool Interface

```python
class Tool:
    """Base class for agent tools"""
    
    @property
    def name(self) -> str:
        """Tool name for LLM"""
        pass
    
    @property
    def description(self) -> str:
        """What this tool does"""
        pass
    
    @property
    def parameters(self) -> dict:
        """Tool parameters schema"""
        pass
    
    def execute(self, **kwargs) -> dict:
        """Execute the tool"""
        pass
```

### Example: IAM Tool

```python
class IAMTool(Tool):
    def __init__(self, aws_session):
        self.client = IAMClient(aws_session)
    
    @property
    def name(self):
        return "list_iam_users"
    
    @property
    def description(self):
        return "Lists all IAM users in the AWS account with their MFA status and access keys"
    
    @property
    def parameters(self):
        return {
            "type": "object",
            "properties": {
                "include_mfa": {"type": "boolean", "description": "Include MFA status"},
                "include_keys": {"type": "boolean", "description": "Include access key info"}
            }
        }
    
    def execute(self, include_mfa=True, include_keys=True):
        users = self.client.list_users()
        
        if include_mfa:
            for user in users:
                user['mfa_enabled'] = self.client.check_mfa(user['UserName'])
        
        if include_keys:
            for user in users:
                user['access_keys'] = self.client.list_access_keys(user['UserName'])
        
        return {"users": users, "count": len(users)}
```

### Example: Workpaper Tool

```python
class WorkpaperTool(Tool):
    @property
    def name(self):
        return "create_workpaper"
    
    @property
    def description(self):
        return "Creates a professional audit workpaper documenting findings and reasoning"
    
    def execute(self, title, findings, evidence_refs, risk_rating, reasoning):
        workpaper = Workpaper(
            reference_number=self._generate_ref(),
            title=title,
            prepared_by=self.agent_name,
            findings=findings,
            evidence_references=evidence_refs,
            risk_rating=risk_rating,
            auditor_reasoning=reasoning,
            date=datetime.now()
        )
        
        # Save to disk
        self._save_workpaper(workpaper)
        
        return {"workpaper_ref": workpaper.reference_number}
```

---

## Workpaper-Centric Documentation

All meaningful agent work is documented in **workpapers**, not logs.

### Workpaper Structure

```markdown
# Workpaper WP-IAM-001

**Prepared by**: Esther (Senior Auditor - IAM)
**Date**: 2024-01-15
**Control Domain**: Identity & Access Management
**Company**: CloudRetail Inc

## Objective

Assess IAM security controls and identify risks related to user access, 
authentication, and authorization.

## Procedures Performed

1. Listed all IAM users in the account
2. Reviewed MFA status for each user
3. Analyzed IAM policies for excessive permissions
4. Checked password policy configuration
5. Reviewed access key age and usage

## Evidence Collected

- Evidence-IAM-001: IAM user list (5 users)
- Evidence-IAM-002: Credential report showing MFA status
- Evidence-IAM-003: IAM policy documents
- Evidence-IAM-004: Access key metadata

## Findings

### Finding 1: Missing MFA on Privileged Accounts (HIGH RISK)

**Observation**: 3 out of 5 IAM users do not have MFA enabled, including:
- admin-john (AdministratorAccess policy)
- admin-sarah (PowerUserAccess policy)  
- developer-mike (Custom developer policy)

**Risk**: Without MFA, these accounts are vulnerable to credential compromise. 
If an attacker obtains the password, they gain full access with no second 
factor to prevent unauthorized access.

**Impact**: HIGH - Affects privileged accounts with broad permissions
**Likelihood**: HIGH - Password-only authentication is easily compromised

**Evidence**: Evidence-IAM-002 (Credential Report)

**Recommendation**: Enable MFA for all users, especially those with 
administrative or elevated privileges. Consider enforcing MFA through 
IAM policy conditions.

### Finding 2: Overly Permissive Developer Policy (MEDIUM RISK)

**Observation**: The "developer-access" policy grants s3:* permissions 
on all resources, violating the principle of least privilege.

**Analysis**: I investigated actual S3 usage by developers (per Maurice's 
request). CloudTrail logs show developers only access 2 specific buckets:
- cloudretail-app-code
- cloudretail-test-data

However, the policy grants access to ALL S3 buckets including the 
customer data bucket.

**Risk**: Developers have unnecessary access to sensitive customer data. 
While not currently exploited, this increases the blast radius if a 
developer account is compromised.

**Impact**: MEDIUM - Potential access to sensitive data
**Likelihood**: MEDIUM - Requires account compromise to exploit

**Evidence**: Evidence-IAM-003 (Policy Document), Evidence-IAM-005 
(CloudTrail usage analysis)

**Recommendation**: Restrict the developer policy to only the specific 
buckets they need. Use resource-level permissions: 
`"Resource": ["arn:aws:s3:::cloudretail-app-code/*", ...]`

## Auditor Reasoning

My approach was to start broad (list all users) then drill into specific 
risks (MFA, permissions). When Maurice questioned my initial risk rating 
for the developer policy, I adapted my investigation to analyze actual 
usage patterns, which provided better context for the risk assessment.

The MFA finding is straightforward and high-priority. The developer policy 
finding required more nuanced analysis - the policy is overly broad, but 
actual risk depends on what developers do with that access.

## Conclusion

CloudRetail Inc has significant IAM security gaps, particularly around 
MFA and least privilege. The missing MFA on privileged accounts is the 
highest priority issue requiring immediate remediation.

**Overall IAM Risk Rating**: HIGH

---
**Reviewed by**: Maurice (Audit Manager)
**Review Date**: 2024-01-16
**Status**: Approved
**Reviewer Comments**: "Well-documented findings with clear evidence trail. 
The additional usage analysis strengthened the developer policy finding. 
Approved for inclusion in final audit report."
```

---

## Orchestrator Design

The orchestrator coordinates agents but doesn't control them:

```python
class AuditOrchestrator:
    def __init__(self, agents, rate_limiter):
        self.agents = agents
        self.rate_limiter = rate_limiter
        self.message_queue = []
    
    def start_audit(self, company_name):
        """Kick off the audit by assigning goals"""
        
        # Assign goals to senior auditors
        self.agents['esther'].set_goal(
            f"Assess IAM risks for {company_name}. Document findings in workpaper."
        )
        
        self.agents['chuck'].set_goal(
            f"Assess data protection and network risks for {company_name}. Document findings."
        )
        
        self.agents['victor'].set_goal(
            f"Assess logging and monitoring controls for {company_name}. Document findings."
        )
        
        # Let agents work autonomously
        self.run_agent_loop()
    
    def run_agent_loop(self):
        """Let agents work until goals are achieved"""
        
        while not self.all_goals_complete():
            for agent in self.active_agents():
                # Rate limiting
                self.rate_limiter.wait_if_needed()
                
                # Agent reasons about next action
                action = agent.reason()
                
                # Agent executes action
                result = agent.act(action)
                
                # Check if agent completed goal
                if agent.goal_achieved():
                    print(f"{agent.name} completed their goal!")
                    agent.status = "complete"
            
            # Process inter-agent messages
            self.process_messages()
            
            # Small delay to avoid tight loop
            time.sleep(1)
        
        # All agents done - have Maurice review
        self.agents['maurice'].set_goal(
            "Review all workpapers and approve findings"
        )
```

---

## Testing Strategy

### Unit Tests
- Test individual tools (IAM client, S3 client, etc.)
- Test workpaper generation
- Test rate limiting logic

### Integration Tests
- Test agent with mock LLM responses
- Test agent tool usage
- Test workpaper creation flow

### End-to-End Tests
- Run one agent (Esther) against real AWS account
- Verify workpaper is created with findings
- Verify evidence is collected and referenced

### Manual Testing
- Run full audit with all agents
- Review workpapers for quality
- Verify agent reasoning is documented

---

## Cost Management

### Development Phase (FREE)
```python
# Use Ollama locally
llm = ollama.Client()
model = 'llama3'  # Free, runs on your machine
```

### Demo Phase ($1-5)
```python
# Use Claude Haiku (cheap and fast)
llm = anthropic.Anthropic()
model = 'claude-3-haiku-20240307'  # $0.25 per 1M tokens
```

### Rate Limiting
```python
# Limit to 10 LLM calls per minute
rate_limiter = RateLimiter(max_calls_per_minute=10)

# This makes audit run slower but:
# - Stays within free tier limits
# - Reflects realistic audit pace
# - Reduces costs
```

---

## Success Criteria

An agent is "truly autonomous" if:

1. ✅ **Reasons independently**: Uses LLM to decide what to do next
2. ✅ **Adapts to findings**: Changes approach based on what it discovers
3. ✅ **Documents reasoning**: Explains WHY it made decisions
4. ✅ **Communicates naturally**: Uses natural language, not function calls
5. ✅ **Achieves goals**: Completes objectives without step-by-step instructions

---

## Next Steps

1. Implement base `AuditAgent` class with LLM integration
2. Create tool interfaces and implement IAM tool
3. Build Esther (first agent) with goal-based reasoning
4. Test Esther against CloudRetail AWS account
5. Review Esther's workpaper for quality
6. Implement Chuck and Victor
7. Implement Maurice for review
8. Run full audit end-to-end

---

## Key Differences from Old Design

| Old (Scripted) | New (LLM-Based) |
|----------------|-----------------|
| Hardcoded algorithms | LLM reasoning |
| Method calls | Goals and tools |
| Logs for transparency | Workpapers for documentation |
| Deterministic | Adaptive |
| Fast execution | Realistic pace (rate limited) |
| Predictable | Autonomous |

This is a **true agentic sys