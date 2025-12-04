# LLM-Based Audit Agents - Quick Start Guide

## What Changed?

We've pivoted from **scripted automation** to **true LLM-based autonomous agents**. 

### Before (Scripted):
- Agents followed hardcoded algorithms
- Deterministic, predictable behavior
- Fast execution
- Not truly "agentic"

### After (LLM-Based):
- Agents reason independently using LLMs
- Adaptive, autonomous behavior  
- Realistic pace (rate-limited)
- True agentic behavior

---

## Architecture Overview

```
Your Computer (Local)          AWS Account (Audit Target)
┌─────────────────────┐       ┌──────────────────────────┐
│                     │       │                          │
│  LLM-Based Agents   │──────▶│  CloudRetail Inc         │
│  - Esther (IAM)     │ boto3 │  - IAM users             │
│  - Chuck (Data)     │       │  - S3 buckets            │
│  - Victor (Logs)    │       │  - EC2 instances         │
│  - Maurice (Mgr)    │       │  - VPC, CloudTrail       │
│                     │       │                          │
│  LLM: Ollama/Claude │       │  (Real AWS resources)    │
└─────────────────────┘       └──────────────────────────┘
```

**Key Point**: Agents run locally, query AWS remotely. All your AWS infrastructure work is still valuable!

---

## Setup Instructions

### 1. Install Ollama (Free Local LLM)

```bash
# macOS
brew install ollama

# Or download from https://ollama.ai

# Pull a model
ollama pull llama3

# Test it
ollama run llama3 "You are an auditor. What should you check first?"
```

### 2. Install Python Dependencies

```bash
# Already have most dependencies
pip install ollama anthropic openai  # LLM clients
```

### 3. Set Up AWS Credentials

```bash
# Already configured if you ran create_cloudretail.py
aws configure list
```

---

## What We're Building

### Phase 1: Esther (First Agent)

**Goal**: Build one LLM-based agent that actually reasons

**What Esther Does**:
1. Receives goal: "Assess IAM risks for CloudRetail Inc"
2. Reasons: "I should list IAM users first..."
3. Acts: Calls IAMClient.list_users() 
4. Analyzes: "I found 3 users without MFA - this is high risk because..."
5. Documents: Creates workpaper with findings and reasoning

**Success Criteria**:
- Esther uses LLM to decide what to do (not hardcoded)
- Esther adapts based on what she finds
- Esther documents her reasoning in workpaper
- Workpaper reads like a human auditor wrote it

### Phase 2: Full Team

Once Esther works, add:
- Chuck (data protection & network)
- Victor (logging & monitoring)
- Maurice (reviews workpapers)

### Phase 3: Complete Audit

Run full audit with agent communication and human approvals.

---

## File Structure

### Keep (Still Valuable):
```
src/aws/              # AWS clients - become agent tools
src/models/           # Data models - still used
src/utils/            # Time simulator, budget tracker
templates/            # Company template
create_cloudretail.py # Creates audit target
```

### New (LLM Agent Code):
```
src/agents/
  llm_agent.py        # Base LLM agent class
  esther.py           # Esther agent
  chuck.py            # Chuck agent
  victor.py           # Victor agent
  maurice.py          # Maurice agent
  tools/              # Agent tools
    iam_tool.py
    s3_tool.py
    workpaper_tool.py
  
src/orchestrator/
  orchestrator.py     # Coordinates agents
  message_bus.py      # Agent communication
  rate_limiter.py     # LLM rate limiting
```

### Archive (Old Scripted Code):
```
archive/old-scripted-implementation/
  # Old docs and implementation
```

---

## Development Workflow

### Step 1: Build Base Agent Class

```python
# src/agents/llm_agent.py
class AuditAgent:
    def __init__(self, name, role, llm, tools):
        self.name = name
        self.llm = llm
        self.tools = tools
    
    def set_goal(self, goal):
        self.current_goal = goal
    
    def reason(self):
        # Agent uses LLM to decide what to do
        prompt = f"You are {self.name}. Your goal: {self.current_goal}. What should you do next?"
        return self.llm.chat(prompt)
    
    def act(self, action):
        # Agent executes action using tools
        return self.execute_tool(action)
```

### Step 2: Build Esther

```python
# src/agents/esther.py
class EstherAgent(AuditAgent):
    def __init__(self, llm, aws_session):
        tools = {
            'iam': IAMTool(aws_session),
            'workpaper': WorkpaperTool()
        }
        super().__init__(
            name="Esther",
            role="Senior Auditor - IAM & Access Control",
            llm=llm,
            tools=tools
        )
```

### Step 3: Test Esther

```python
# test_esther.py
import ollama
from src.agents.esther import EstherAgent

# Create Esther with local LLM
llm = ollama.Client()
esther = EstherAgent(llm, aws_session)

# Give Esther a goal
esther.set_goal("Assess IAM risks for CloudRetail Inc")

# Let Esther work
while not esther.goal_achieved():
    action = esther.reason()  # Esther decides what to do
    result = esther.act(action)  # Esther does it
    
# Review Esther's workpaper
print(esther.workpaper)
```

---

## Cost Estimates

### Development (FREE):
- Ollama running locally: $0
- AWS API calls (read-only): $0
- AWS resources (Free Tier): $0
- **Total: $0**

### Demo Run ($1-5):
- Claude Haiku API: $0.50-2
- AWS resources: $0-1
- **Total: $1-5**

### Rate Limiting:
- 10 LLM calls/minute = slow but free
- Reflects realistic audit pace
- Can increase if needed

---

## Success Metrics

### Agent Quality Checklist:

✅ **Independent Reasoning**
- Agent decides what to do (not hardcoded)
- Agent explains why it made that decision

✅ **Adaptive Behavior**
- Agent changes approach based on findings
- Agent investigates deeper when needed

✅ **Professional Documentation**
- Workpaper reads like human wrote it
- Clear reasoning and evidence trail
- Appropriate risk ratings

✅ **Natural Communication**
- Agents use natural language
- Agents ask clarifying questions
- Agents respond to feedback

---

## Next Steps

1. **Review updated spec files**:
   - `.kiro/specs/aws-audit-agents/requirements.md` (updated)
   - `.kiro/specs/aws-audit-agents/design-llm-agents.md` (new)
   - `.kiro/specs/aws-audit-agents/tasks-llm-agents.md` (new)

2. **Start with Task 1**: Set up LLM integration
   - Install Ollama
   - Create LLM client wrapper
   - Test basic LLM calls

3. **Build Esther** (Tasks 2-5):
   - Implement base AuditAgent class
   - Create Esther agent
   - Test against CloudRetail AWS account
   - Review workpaper quality

4. **Iterate**:
   - If Esther's reasoning is good → add Chuck and Victor
   - If Esther's reasoning is weak → refine prompts and try again

---

## Questions?

**Q: Can we still use the AWS account we created?**
A: Yes! All your AWS infrastructure is still the audit target.

**Q: What about the AWS client code we wrote?**
A: Keep it! Those become "tools" that agents use.

**Q: Will this be slower?**
A: Yes, but that's OK. Real audits take weeks. Rate-limited LLM calls reflect realistic pace.

**Q: What if we hit rate limits?**
A: Agent pauses and resumes. Reflects real audit workflow.

**Q: How do we test this?**
A: Start with Esther. If her workpaper looks good, we're on the right track.

---

## The Vision

**End Goal**: Run this command and watch autonomous agents perform a real audit:

```bash
python run_audit.py --company cloudretail --llm ollama

# Output:
# [Esther] Starting IAM risk assessment...
# [Esther] Found 5 IAM users, checking MFA status...
# [Esther] Concerning: 3 users without MFA, investigating further...
# [Esther] Created workpaper WP-IAM-001 with findings
# [Maurice] Reviewing WP-IAM-001...
# [Maurice] Question for Esther: Did you check actual S3 usage?
# [Esther] Good point, investigating usage patterns...
# [Esther] Updated WP-IAM-001 with usage analysis
# [Maurice] Approved WP-IAM-001
# ...
# Audit complete! See workpapers/ for findings.
```

**That's true agentic behavior.**

Let's build it! 🚀
