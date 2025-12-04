# AuditAgent - LLM-Based Autonomous Agent

## Overview

The `AuditAgent` class is the foundation for LLM-powered autonomous audit agents. Unlike traditional scripted automation, these agents **reason independently** using Large Language Models to achieve goals.

**Core Principle**: Agents are given **GOALS and TOOLS**, not step-by-step instructions.

## Key Features

### 1. LLM Integration
- Supports multiple LLM providers (OpenAI, Anthropic, Ollama)
- Built-in rate limiting to stay within API limits
- Cost tracking for all LLM calls
- Conversation memory management

### 2. Goal-Based Reasoning
- Agents receive high-level goals (e.g., "Assess IAM risks")
- LLM reasons about how to achieve the goal
- Adapts approach based on findings
- Documents reasoning process

### 3. Tool System
- Flexible tool registration
- Tools can be AWS clients, workpaper generators, etc.
- Agents decide which tools to use and when
- Error handling and recovery

### 4. Memory & Context
- Maintains conversation history with LLM
- Tracks all actions taken
- Preserves context across reasoning cycles
- Can be reset for testing

### 5. Autonomous Execution
- Run agent until goal is complete
- Configurable iteration limits
- Graceful error handling
- Status tracking (idle, working, complete, blocked)

## Architecture

```
┌─────────────────────────────────────────┐
│         AuditAgent                      │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │  LLM Brain                      │   │
│  │  - Reasons about goals          │   │
│  │  - Makes decisions              │   │
│  │  - Adapts to findings           │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │  Tools                          │   │
│  │  - AWS clients                  │   │
│  │  - Workpaper generator          │   │
│  │  - Evidence collector           │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │  Memory                         │   │
│  │  - Conversation history         │   │
│  │  - Action history               │   │
│  │  - Context/state                │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

## Usage

### Basic Example

```python
from src.agents.audit_agent import AuditAgent, Tool
from src.agents.llm_client import LLMClient

# Create LLM client
llm = LLMClient(
    provider='openai',
    model='gpt-4o',
    rate_limit=10
)

# Create agent (must subclass and implement create_workpaper)
class MyAuditorAgent(AuditAgent):
    def create_workpaper(self):
        return {"workpaper": "content"}

agent = MyAuditorAgent(
    name="Esther",
    role="Senior Auditor - IAM",
    llm_client=llm
)

# Register tools
def list_users(**kwargs):
    return {"users": [...]}

tool = Tool(
    name="list_iam_users",
    description="Lists IAM users",
    parameters={...},
    execute=list_users
)
agent.register_tool(tool)

# Set goal
agent.set_goal("Assess IAM security risks")

# Run autonomously
result = agent.run_autonomously(max_iterations=10)

print(f"Status: {result['status']}")
print(f"Actions: {result['actions_taken']}")
```

### Reasoning Loop

The agent follows a **reason → act → document** loop:

1. **Reason**: LLM decides what to do next
2. **Act**: Execute the decision (use tool, document, etc.)
3. **Document**: Record action and result
4. **Repeat** until goal is complete

### LLM Decision Format

The LLM responds with JSON decisions:

**Use a tool:**
```json
{
    "action": "use_tool",
    "tool": "list_iam_users",
    "parameters": {"include_mfa": true},
    "reasoning": "I need to see which users lack MFA"
}
```

**Complete goal:**
```json
{
    "action": "goal_complete",
    "summary": "Found 3 users without MFA",
    "next_steps": "Recommend enabling MFA"
}
```

**Document findings:**
```json
{
    "action": "document",
    "content": "IAM findings...",
    "reasoning": "Documenting for workpaper"
}
```

## Tool System

### Creating Tools

Tools are simple functions wrapped in a `Tool` object:

```python
def my_tool_function(param1, param2):
    """Tool implementation"""
    # Do something
    return {"result": "data"}

tool = Tool(
    name="my_tool",
    description="What this tool does",
    parameters={
        "type": "object",
        "properties": {
            "param1": {"type": "string"},
            "param2": {"type": "number"}
        }
    },
    execute=my_tool_function
)

agent.register_tool(tool)
```

### Tool Execution

When the agent decides to use a tool:

1. Agent reasons: "I should use tool X with parameters Y"
2. `act()` method executes the tool
3. Result is added to agent's memory
4. LLM sees the result and decides next action

### Error Handling

Tools can fail gracefully:

```python
def risky_tool(**kwargs):
    if something_wrong:
        raise ValueError("Tool failed")
    return {"result": "success"}
```

The agent will:
- Catch the error
- Add error to memory
- Let LLM adapt (try different approach)

## Memory Management

### Conversation History

The agent maintains a conversation with the LLM:

```python
agent.memory = [
    {"role": "system", "content": "You are Esther..."},
    {"role": "user", "content": "Your goal: Assess IAM..."},
    {"role": "assistant", "content": '{"action": "use_tool"...}'},
    {"role": "user", "content": "Tool result: {...}"},
    ...
]
```

### Action History

All actions are logged:

```python
for action in agent.get_action_history():
    print(f"{action.timestamp}: {action.action_type}")
    print(f"  {action.description}")
```

### Reset

For testing, you can reset the agent:

```python
agent.reset()  # Clears memory, actions, goal
```

## Autonomous Execution

### Run Until Complete

```python
result = agent.run_autonomously(max_iterations=10)

# result = {
#     "status": "complete",  # or "blocked"
#     "iterations": 7,
#     "actions_taken": 15
# }
```

### Manual Control

For more control, run the loop manually:

```python
agent.set_goal("My goal")

while agent.goal_status == "working":
    decision = agent.reason()
    result = agent.act(decision)
    
    if decision["action"] == "goal_complete":
        break
```

## Subclassing

The `AuditAgent` is abstract. Subclasses must implement:

```python
class SeniorAuditorAgent(AuditAgent):
    def create_workpaper(self):
        """Create a professional audit workpaper"""
        return Workpaper(
            reference_number=self._generate_ref(),
            control_domain=self.context['domain'],
            findings=self.context['findings'],
            ...
        )
```

## Cost Management

### Rate Limiting

```python
llm = LLMClient(
    provider='openai',
    model='gpt-4o',
    rate_limit=10  # Max 10 calls/minute
)
```

The agent will automatically pause when rate limit is reached.

### Cost Tracking

```python
# After execution
llm.print_cost_summary()

# Output:
# ============================================================
# LLM Cost Summary
# ============================================================
# Total API calls: 15
# Total tokens: 12,450
# Total cost: $0.0623
# Avg cost per call: $0.0042
# ============================================================
```

### Provider Options

**Development (Free):**
```python
llm = LLMClient(provider='ollama', model='llama3')
```

**Production (Low Cost):**
```python
llm = LLMClient(provider='anthropic', model='claude-3-haiku')
```

**Premium (Best Reasoning):**
```python
llm = LLMClient(provider='openai', model='gpt-4o')
```

## Testing

### Unit Tests

See `tests/unit/test_audit_agent.py` for examples:

```python
def test_agent_reasoning():
    llm = Mock(spec=LLMClient)
    llm.chat = Mock(return_value=mock_response)
    
    agent = TestAuditAgent(name="Test", role="Tester", llm_client=llm)
    agent.set_goal("Test goal")
    
    decision = agent.reason()
    
    assert decision["action"] == "use_tool"
```

### Integration Tests

Test with real LLM (use Ollama for free testing):

```python
llm = LLMClient(provider='ollama', model='llama3')
agent = MyAgent(name="Test", role="Tester", llm_client=llm)

agent.set_goal("Real goal")
result = agent.run_autonomously(max_iterations=5)

assert result["status"] == "complete"
```

## Best Practices

### 1. Clear Goals

❌ Bad: "Do IAM stuff"
✅ Good: "Assess IAM security. Identify users without MFA. Document findings with risk ratings."

### 2. Descriptive Tools

❌ Bad: `Tool(name="get_data", description="Gets data")`
✅ Good: `Tool(name="list_iam_users", description="Lists all IAM users with MFA status and policies")`

### 3. Error Recovery

Let the agent adapt to errors:

```python
# Tool fails → Error added to memory → LLM tries different approach
```

### 4. Iteration Limits

Set reasonable limits to prevent infinite loops:

```python
agent.run_autonomously(max_iterations=20)  # Reasonable
agent.run_autonomously(max_iterations=1000)  # Too high
```

### 5. Monitor Costs

Always track LLM costs:

```python
result = agent.run_autonomously()
llm.print_cost_summary()  # Check costs after execution
```

## Requirements Validated

This implementation satisfies:

- **Requirement 9.1**: Agents use LLMs for reasoning and decision-making
- **Requirement 9.2**: Agents document reasoning process
- **Requirement 9.3**: Agents adapt to unexpected situations

## Next Steps

1. Implement specific agent types (SeniorAuditorAgent, AuditManagerAgent)
2. Create AWS tool wrappers (IAMTool, S3Tool, etc.)
3. Implement workpaper generation tools
4. Build orchestrator to coordinate multiple agents
5. Test with real AWS account

## Example Output

```
🎯 Esther: New goal set
   Assess IAM security for CloudRetail Inc

🤔 Esther: Reasoning about next action...
💭 Esther: I should start by listing all IAM users to understand the account

🔧 Esther: Using tool 'list_iam_users'
   Reasoning: Need to see all users and their MFA status
✅ Esther: Tool executed successfully

🤔 Esther: Reasoning about next action...
💭 Esther: I found 3 users without MFA. This is a HIGH risk. I should document this.

📝 Esther: Documented work

🤔 Esther: Reasoning about next action...
💭 Esther: I've completed my assessment. Time to finalize.

✅ Esther: Goal completed!
   Summary: Identified 3 users without MFA (HIGH RISK)
   Next steps: Recommend immediate MFA enablement
```

## Verifying Agentic Quality

### Interactive Interview System

You can interview agents to verify they're truly autonomous and not just following scripts:

```bash
# Interactive interview - ask your own questions
python examples/interview_agent.py

# Demo interview - pre-scripted questions
python examples/demo_agent_interview.py
```

### What to Look For

When interviewing agents, verify:

1. **Independent Reasoning**: Responses aren't scripted, they reason through scenarios
2. **Adaptation**: Can handle unexpected situations and new information
3. **Professional Judgment**: Makes risk-based decisions with clear rationale
4. **Contextual Understanding**: Understands audit concepts and their role
5. **Communication**: Explains thinking clearly and professionally

### Sample Interview Questions

**Role Understanding:**
- "Can you describe your role and responsibilities?"
- "What do you focus on during an audit?"

**Reasoning:**
- "If you found X issue, how would you assess the risk?"
- "Walk me through your thinking on Y scenario"

**Adaptation:**
- "What if you encountered a technology you haven't seen before?"
- "How would you handle conflicting evidence?"

**Decision Making:**
- "You have limited time. How do you prioritize between A and B?"
- "What factors influence your risk ratings?"

**Communication:**
- "How would you explain this finding to management?"
- "How do you collaborate with other auditors?"

### Example Interview Output

```
Interviewer: If you discovered that 3 out of 5 IAM users don't have MFA 
enabled, including an admin account, how would you assess the risk?

Esther: This is a significant finding that I would rate as HIGH risk. 
Let me walk you through my reasoning:

First, I'd consider the inherent risk. MFA is a critical compensating 
control for password-based authentication. Without it, accounts are 
vulnerable to credential compromise through phishing, password reuse, 
or brute force attacks.

The fact that an admin account lacks MFA is particularly concerning 
because:
1. Admin accounts have elevated privileges across the entire AWS environment
2. Compromise of an admin account could lead to complete infrastructure takeover
3. This violates AWS security best practices and most compliance frameworks

For the risk rating, I'd assess:
- Impact: HIGH (potential for complete environment compromise)
- Likelihood: HIGH (password-only auth is easily compromised)
- Overall Risk: HIGH

I would document this as a critical finding and recommend immediate 
remediation. I'd also investigate whether there's a password policy 
in place and check for any recent suspicious login activity.

Would you like me to elaborate on any part of this assessment?
```

This demonstrates:
- ✅ Independent reasoning (not a script)
- ✅ Risk-based thinking
- ✅ Professional communication
- ✅ Contextual understanding
- ✅ Proactive follow-up

## See Also

- `llm_client.py` - LLM integration and cost tracking
- `examples/audit_agent_example.py` - Working example
- `examples/interview_agent.py` - Interactive agent interview
- `examples/demo_agent_interview.py` - Demo interview
- `tests/unit/test_audit_agent.py` - Unit tests
- Design document: `.kiro/specs/aws-audit-agents/design-llm-agents.md`
