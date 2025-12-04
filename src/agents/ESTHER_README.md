# Esther - Senior Auditor for IAM & Logical Access

Esther is an autonomous LLM-powered agent specializing in Identity and Access Management (IAM) audits. She assesses IAM risks, collects evidence, and documents findings in professional workpapers.

## Overview

Esther is the first fully implemented LLM-based audit agent. She demonstrates the core capabilities of autonomous agents:

- **Autonomous Reasoning**: Uses LLM to reason about goals and determine next steps
- **Tool Usage**: Queries AWS IAM service to collect evidence
- **Adaptive Behavior**: Adjusts approach based on what she discovers
- **Professional Documentation**: Creates workpapers with findings and analysis

## Capabilities

### IAM Assessment
- List and analyze IAM users and roles
- Check access key status and rotation
- Verify MFA device configuration
- Review user policies and permissions
- Analyze account-level IAM settings

### Evidence Collection
- Collects evidence directly from AWS IAM
- Stores evidence with proper audit trail metadata
- References evidence in workpapers

### Workpaper Creation
- Documents testing procedures performed
- Provides detailed analysis of findings
- Draws conclusions about control effectiveness
- Maintains cross-references to related workpapers

## Usage

### Basic Example

```python
from src.agents.esther_agent import EstherAgent
from src.agents.llm_client import LLMClient
from src.aws.iam_client import IAMClient

# Create LLM client
llm = LLMClient(
    provider="openai",
    model="gpt-5",  # Esther uses GPT-5 for sophisticated reasoning
    temperature=0.7
)

# Create IAM client
iam_client = IAMClient(read_only=True)

# Create Esther
esther = EstherAgent(
    llm_client=llm,
    iam_client=iam_client,
    output_dir="output"
)

# Set a goal
esther.set_goal("Assess IAM risks for CloudRetail Inc and document findings")

# Run autonomously
result = esther.run_autonomously(max_iterations=15)

# Check results
print(f"Status: {result['status']}")
print(f"Workpapers created: {esther.workpapers_created}")
print(f"Evidence collected: {esther.evidence_collected}")
```

### Using the Convenience Method

```python
# Esther has a convenience method for IAM risk assessment
result = esther.assess_iam_risks("CloudRetail Inc")

print(f"Goal: {result['goal']}")
print(f"Status: {result['status']}")
print(f"Iterations: {result['iterations']}")
```

### Creating Workpapers Manually

```python
# You can also create workpapers directly
result = esther.create_workpaper(
    reference_number="WP-IAM-001",
    control_objective="Ensure proper IAM access controls are in place",
    testing_procedures=[
        "Listed all IAM users",
        "Checked MFA status for each user",
        "Reviewed access key rotation"
    ],
    evidence_ids=["EVD-IAM-001", "EVD-IAM-002"],
    analysis="Analysis of IAM controls shows...",
    conclusion="Pass with minor recommendations"
)
```

## Tools Available to Esther

### 1. query_iam
Queries AWS IAM service to collect evidence.

**Operations:**
- `list_users` - List all IAM users
- `list_roles` - List all IAM roles
- `get_user` - Get details for a specific user
- `get_role` - Get details for a specific role
- `list_user_policies` - List inline policies for a user
- `list_attached_user_policies` - List managed policies for a user
- `list_access_keys` - List access keys for a user
- `list_mfa_devices` - List MFA devices for a user
- `get_account_summary` - Get account-level IAM statistics
- `get_credential_report` - Get IAM credential report

### 2. create_workpaper
Creates professional audit workpapers.

**Parameters:**
- `reference_number` - Unique workpaper ID (e.g., "WP-IAM-001")
- `control_objective` - What control is being tested
- `testing_procedures` - List of procedures performed
- `evidence_ids` - List of evidence references
- `analysis` - Detailed analysis
- `conclusion` - Control effectiveness conclusion

### 3. store_evidence
Stores audit evidence with metadata.

**Parameters:**
- `evidence_id` - Unique evidence ID (e.g., "EVD-IAM-001")
- `source` - Evidence source (e.g., "IAM")
- `collection_method` - "direct" or "agent_request"
- `collected_by` - Agent name
- `data` - The actual evidence data

## Configuration

Esther is configured in `config/agent_models.yaml`:

```yaml
esther:
  name: Esther
  role: Senior Auditor - IAM & Logical Access
  model: gpt-5
  control_domains:
    - IAM
    - Logical Access
  staff_auditor: Hillel
  rationale: Complex risk assessment and judgment calls require advanced reasoning
```

## Output

Esther creates two types of output:

### Workpapers
Location: `output/workpapers/`

Format: JSON and Markdown

Example: `WP-IAM-001.md`

### Evidence
Location: `output/evidence/`

Format: JSON

Example: `EVD-IAM-001.json`

## Autonomous Behavior

Esther operates autonomously using a reasoning loop:

1. **Reason**: Uses LLM to think about what to do next
2. **Act**: Executes the decided action (use tool, document, etc.)
3. **Adapt**: Adjusts approach based on results
4. **Repeat**: Continues until goal is complete

Example reasoning:
```
"I need to understand the IAM structure first. Let me list all users."
→ Uses query_iam tool with operation="list_users"

"I found 5 users. Now I should check if they have MFA enabled."
→ Uses query_iam tool with operation="list_mfa_devices" for each user

"I've collected enough evidence. Time to document my findings."
→ Uses create_workpaper tool to document results
```

## Integration with Team

Esther works with:
- **Hillel** (Staff Auditor) - Esther's staff auditor who assists with evidence collection
- **Maurice** (Audit Manager) - Reviews Esther's workpapers and provides feedback

## Testing

Run Esther's tests:
```bash
python3 -m pytest tests/unit/test_esther_agent.py -v
```

Run the example:
```bash
python3 examples/esther_agent_example.py
```

## Cost Optimization

Esther uses GPT-5 for sophisticated reasoning about IAM risks. This is appropriate because:
- IAM risk assessment requires complex judgment
- Security implications are significant
- Cost is justified by quality of analysis

For development/testing, you can use GPT-4 Turbo or Ollama:
```python
llm = LLMClient(provider="openai", model="gpt-4-turbo")  # Cost-effective
llm = LLMClient(provider="ollama", model="llama3")       # Free, local
```

## Next Steps

After implementing Esther, the next agents to implement are:

1. **Chuck** - Senior Auditor for Data Encryption & Network Security
2. **Victor** - Senior Auditor for Logging & Monitoring
3. **Hillel, Neil, Juman** - Staff Auditors who assist the seniors

See `tasks-llm-agents.md` for the full implementation plan.
