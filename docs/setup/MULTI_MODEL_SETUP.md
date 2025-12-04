# Multi-Model Agent Configuration

## Overview

The audit agent system supports using different LLM models for different agent levels, mirroring real-world audit teams where senior staff have more expertise.

## Configuration Strategy

### Recommended Setup

- **Senior Auditors** (Esther, Chuck, Victor): **GPT-5**
  - Complex risk assessment and judgment calls
  - Sophisticated pattern recognition
  - Advanced reasoning for security analysis
  
- **Staff Auditors** (Hillel, Neil, Juman): **GPT-4 Turbo**
  - Routine evidence collection
  - Configuration checks
  - Data gathering tasks
  
- **Audit Manager** (Maurice): **GPT-4 Turbo**
  - Reviews and approvals
  - Doesn't require most advanced model

### Cost Optimization

**Pricing (per 1M tokens):**
- GPT-5: $15 input / $45 output
- GPT-4 Turbo: $10 input / $30 output

**Estimated Savings:**
- vs All GPT-5: ~33% cost reduction
- vs All GPT-4 Turbo: +20% cost for better senior reasoning

**Team Composition:**
- 3 Senior Auditors (GPT-5)
- 3 Staff Auditors (GPT-4 Turbo)
- 1 Audit Manager (GPT-4 Turbo)

## Usage

### Option 1: Using AgentFactory (Recommended)

```python
from src.agents.agent_factory import AgentFactory

# Create factory
factory = AgentFactory("config/agent_models.yaml")

# Print configuration summary
factory.print_team_summary()

# Create entire team
team = factory.create_audit_team()

# Access individual agents
esther = team['esther']  # GPT-5
hillel = team['hillel']  # GPT-4 Turbo
```

### Option 2: Manual Creation

```python
from src.agents.agent_factory import create_agent_with_model

# Create senior auditor with GPT-5
esther = create_agent_with_model(
    name="Esther",
    role="Senior Auditor - IAM",
    model="gpt-5"
)

# Create staff auditor with GPT-4 Turbo
hillel = create_agent_with_model(
    name="Hillel",
    role="Staff Auditor - IAM Support",
    model="gpt-4-turbo"
)
```

## Configuration File

Edit `config/agent_models.yaml` to customize:

```yaml
# LLM Provider Settings
provider: openai
rate_limit: 10
temperature: 0.7

# Agent Model Assignments
agents:
  esther:
    name: Esther
    role: Senior Auditor - IAM & Logical Access
    model: gpt-5
    control_domains:
      - IAM
      - Logical Access
    staff_auditor: Hillel
```

## Alternative Configurations

### All GPT-5 (Highest Quality)
Best for: Production audits where quality is paramount

```yaml
# Set all agents to gpt-5
```

### All GPT-4 Turbo (Balanced)
Best for: Development and testing

```yaml
# Set all agents to gpt-4-turbo
```

### Ollama (Free, Local)
Best for: Development without API costs

```yaml
provider: ollama
# Set all agents to llama3
```

### Hybrid with Claude
Best for: Comparing different LLM providers

```yaml
provider: anthropic
# Seniors: claude-3-opus
# Staff: claude-3-haiku
```

## Cost Tracking

Each agent tracks its own LLM costs:

```python
# Get cost summary for an agent
esther.llm.print_cost_summary()

# Get total team cost
total_cost = sum(agent.llm.cost_tracker.total_cost for agent in team.values())
print(f"Total: ${total_cost:.4f}")
```

## Benefits

1. **Cost Optimization**: 30-40% savings vs all GPT-5
2. **Realistic Structure**: Mirrors real audit teams
3. **Quality Where It Matters**: GPT-5 for complex reasoning
4. **Flexibility**: Easy to adjust per agent or globally

## Examples

See `examples/multi_model_agents.py` for a complete demonstration.

## Next Steps

1. Run the example: `python examples/multi_model_agents.py`
2. Customize `config/agent_models.yaml` for your needs
3. Use `AgentFactory` in your audit workflows
