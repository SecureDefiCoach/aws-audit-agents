## Agent Monitoring Guide

## Overview

The `AgentMonitor` provides visibility and control over agent attributes during execution. You can inspect agent state, track progress, view reasoning, and monitor costs.

## Quick Start

```python
from src.agents.agent_factory import AgentFactory
from src.agents.agent_monitor import AgentMonitor

# Create agents
factory = AgentFactory("config/agent_models.yaml")
team = factory.create_audit_team()

# Create monitor
monitor = AgentMonitor(team)

# View team summary
monitor.print_team_summary()

# Inspect specific agent
monitor.print_agent_info("esther")
```

## What You Can Monitor

### 1. Agent Configuration
- Name and role
- LLM model and provider
- Available tools
- Current goal and status

```python
info = monitor.get_agent_info("esther")
print(f"Model: {info['model']}")
print(f"Status: {info['goal_status']}")
print(f"Tools: {info['tools']}")
```

### 2. Agent Memory
View the conversation history between the agent and LLM:

```python
# Print last 5 messages
monitor.print_agent_memory("esther", last_n=5)

# Get memory programmatically
memory = monitor.get_agent_memory("esther")
```

### 3. Agent Actions
See what actions the agent has taken:

```python
# Print last 10 actions
monitor.print_agent_actions("esther", last_n=10)

# Get actions programmatically
actions = monitor.get_agent_actions("esther")
for action in actions:
    print(f"{action.timestamp}: {action.action_type}")
    print(f"  {action.description}")
```

### 4. LLM Costs
Track costs by agent and model:

```python
# Print detailed cost breakdown
monitor.print_cost_breakdown()

# Get cost data programmatically
breakdown = monitor.get_cost_breakdown()
print(f"Total: ${breakdown['total_cost']:.4f}")
print(f"GPT-5: ${breakdown['by_model']['gpt-5']['total_cost']:.4f}")
```

### 5. Team Summary
View all agents at once:

```python
monitor.print_team_summary()
```

Output:
```
╔═══════════╦═══════════════════════════╦═══════════════╦═════════╦═════════╦═══════════╦═════════╗
║ Agent     ║ Role                      ║ Model         ║ Status  ║ Actions ║ LLM Calls ║ Cost    ║
╠═══════════╬═══════════════════════════╬═══════════════╬═════════╬═════════╬═══════════╬═════════╣
║ Maurice   ║ Audit Manager             ║ gpt-4-turbo   ║ idle    ║ 0       ║ 0         ║ $0.0000 ║
║ Esther    ║ Senior Auditor - IAM      ║ gpt-5         ║ working ║ 5       ║ 3         ║ $0.1234 ║
║ Chuck     ║ Senior Auditor - Encrypt  ║ gpt-5         ║ idle    ║ 0       ║ 0         ║ $0.0000 ║
...
╚═══════════╩═══════════════════════════╩═══════════════╩═════════╩═════════╩═══════════╩═════════╝
```

## Interactive Mode

For real-time monitoring during agent execution:

```python
monitor.interactive_monitor()
```

Commands:
- `list` - List all agents
- `summary` - Show team summary
- `info <agent>` - Show agent details
- `memory <agent>` - Show agent memory
- `actions <agent>` - Show agent actions
- `costs` - Show cost breakdown
- `export <agent>` - Export agent state to JSON
- `quit` - Exit monitor

## Export Agent State

Save complete agent state for analysis:

```python
monitor.export_agent_state("esther", "esther_state.json")
```

Exports:
- Configuration (name, role, model)
- Current state (goal, status)
- Complete memory
- All actions with timestamps
- LLM usage statistics

## Use Cases

### 1. Debugging Agent Behavior

```python
# Agent not working as expected?
monitor.print_agent_info("esther")  # Check status
monitor.print_agent_memory("esther")  # See what LLM is thinking
monitor.print_agent_actions("esther")  # See what it tried
```

### 2. Cost Optimization

```python
# Which agents are expensive?
monitor.print_cost_breakdown()

# Check specific agent
info = monitor.get_agent_info("esther")
print(f"Esther cost: ${info['llm_cost']:.4f}")
```

### 3. Progress Tracking

```python
# Check if agents are making progress
summary = monitor.get_team_summary()
for agent in summary:
    print(f"{agent['name']}: {agent['status']} ({agent['actions']} actions)")
```

### 4. Audit Trail

```python
# Export complete audit trail
for agent_name in monitor.list_agents():
    monitor.export_agent_state(agent_name, f"audit_trail/{agent_name}.json")
```

## Integration with Workflows

### During Execution

```python
# Create team and monitor
team = factory.create_audit_team()
monitor = AgentMonitor(team)

# Set goals
for agent in team.values():
    agent.set_goal("...")

# Monitor progress
while any(a.goal_status == "working" for a in team.values()):
    monitor.print_team_summary()
    time.sleep(10)  # Check every 10 seconds
```

### After Execution

```python
# Analyze results
monitor.print_cost_breakdown()
monitor.print_team_summary()

# Export for reporting
for name in monitor.list_agents():
    monitor.export_agent_state(name, f"results/{name}.json")
```

## Accessing Agent Attributes Directly

You can also access agent attributes directly:

```python
agent = team['esther']

# Configuration
print(agent.name)
print(agent.role)
print(agent.llm.model)

# State
print(agent.current_goal)
print(agent.goal_status)
print(agent.tools)

# Memory
print(len(agent.memory))
print(agent.memory[-1])  # Last message

# Actions
print(len(agent.action_history))
for action in agent.action_history:
    print(action.action_type, action.description)

# LLM usage
print(agent.llm.cost_tracker.total_cost)
print(agent.llm.cost_tracker.total_tokens)
print(agent.llm.cost_tracker.call_count)
```

## Best Practices

1. **Create monitor early**: Set up monitoring before agents start working
2. **Check status regularly**: Use `print_team_summary()` to track progress
3. **Export state**: Save agent state at key milestones
4. **Monitor costs**: Check costs frequently to avoid surprises
5. **Use interactive mode**: For debugging, interactive mode is very helpful

## Example: Complete Monitoring Workflow

```python
# 1. Setup
factory = AgentFactory("config/agent_models.yaml")
team = factory.create_audit_team()
monitor = AgentMonitor(team)

# 2. Initial state
print("Initial team state:")
monitor.print_team_summary()

# 3. Set goals
team['esther'].set_goal("Assess IAM risks")
team['chuck'].set_goal("Assess encryption controls")

# 4. Monitor during execution
print("\nAfter setting goals:")
monitor.print_team_summary()

# 5. Check specific agent
print("\nEsther's details:")
monitor.print_agent_info("esther")

# 6. View reasoning
print("\nEsther's recent memory:")
monitor.print_agent_memory("esther", last_n=3)

# 7. Track costs
print("\nCost breakdown:")
monitor.print_cost_breakdown()

# 8. Export results
monitor.export_agent_state("esther", "output/esther_final.json")
```

## Troubleshooting

**Agent not responding?**
```python
monitor.print_agent_info("esther")
# Check goal_status - should be "working"
# Check llm_calls - should be increasing
```

**High costs?**
```python
monitor.print_cost_breakdown()
# Identify which agents/models are expensive
# Consider switching some agents to cheaper models
```

**Want to see what agent is thinking?**
```python
monitor.print_agent_memory("esther")
# View the conversation with the LLM
```

**Need complete audit trail?**
```python
monitor.export_agent_state("esther", "audit_trail.json")
# Exports everything for detailed analysis
```
