# Agent Dashboard - Web Interface Guide

## Overview

The Agent Dashboard provides a beautiful, user-friendly web interface for monitoring and managing your audit agents. No command line required!

## Quick Start

### 1. Install Dependencies

```bash
pip install Flask>=3.0.0
```

### 2. Launch the Dashboard

```bash
python examples/launch_dashboard.py
```

### 3. Open in Browser

Navigate to: **http://127.0.0.1:5000**

## Features

### 📊 Real-Time Monitoring

- **Team Overview**: See all agents at a glance
- **Live Stats**: Total agents, active agents, actions, and costs
- **Auto-Refresh**: Updates every 5 seconds automatically
- **Status Indicators**: Color-coded agent status (idle, working, complete, blocked)

### 🔍 Agent Details

Click any agent card to see:

- **Info Tab**: Complete agent configuration
  - Name, role, model, provider
  - Current goal and status
  - Available tools
  - Memory size and action count
  - LLM usage and costs

- **Actions Tab**: What the agent has done
  - Chronological action history
  - Action types and descriptions
  - Timestamps for each action

- **Memory Tab**: Agent's conversation with LLM
  - Recent messages
  - System prompts
  - Agent responses
  - LLM outputs

### 💰 Cost Tracking

- Real-time cost monitoring
- Per-agent cost breakdown
- Total team costs
- Token usage statistics

### 🎨 Beautiful UI

- Modern, responsive design
- Color-coded status indicators
- Smooth animations
- Mobile-friendly layout

## Screenshots

### Main Dashboard
```
┌─────────────────────────────────────────────────────────┐
│  🤖 Agent Dashboard                                      │
│  Monitor and manage your audit agents in real-time      │
└─────────────────────────────────────────────────────────┘

┌──────────┬──────────┬──────────┬──────────┐
│ Total    │ Active   │ Total    │ Total    │
│ Agents   │ Agents   │ Actions  │ Cost     │
│   7      │   2      │   45     │ $0.1234  │
└──────────┴──────────┴──────────┴──────────┘

┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ Esther          │  │ Chuck           │  │ Victor          │
│ Senior Auditor  │  │ Senior Auditor  │  │ Senior Auditor  │
│ gpt-5           │  │ gpt-5           │  │ gpt-5           │
│ [working]       │  │ [idle]          │  │ [idle]          │
│ 15 actions      │  │ 0 actions       │  │ 0 actions       │
│ $0.0456         │  │ $0.0000         │  │ $0.0000         │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

### Agent Detail Modal
```
┌─────────────────────────────────────────────────────────┐
│  Esther                                            [×]   │
├─────────────────────────────────────────────────────────┤
│  [Info] [Actions] [Memory]                              │
├─────────────────────────────────────────────────────────┤
│  Name: Esther                    Model: gpt-5           │
│  Role: Senior Auditor - IAM      Provider: openai       │
│  Status: working                 Tools: 3               │
│  Goal: Assess IAM risks for CloudRetail Inc             │
│  Memory: 12 messages             Actions: 15            │
│  LLM Calls: 8                    Tokens: 4,523          │
│  Cost: $0.0456                                          │
└─────────────────────────────────────────────────────────┘
```

## Usage Examples

### Monitor Agent Progress

1. Launch dashboard
2. Agents appear as cards
3. Watch status change from "idle" → "working" → "complete"
4. See action count increase in real-time
5. Monitor costs as they accumulate

### Inspect Agent Behavior

1. Click on an agent card
2. View "Actions" tab to see what it's doing
3. View "Memory" tab to see its reasoning
4. Check "Info" tab for configuration

### Track Costs

1. View total cost in top stats bar
2. Click agents to see individual costs
3. Compare costs across different models
4. Monitor token usage

## API Endpoints

The dashboard exposes a REST API:

### GET /api/agents
Get list of all agents with status

### GET /api/agents/<name>
Get detailed info about specific agent

### GET /api/agents/<name>/memory
Get agent's conversation memory

### GET /api/agents/<name>/actions
Get agent's action history

### GET /api/costs
Get cost breakdown by agent and model

### GET /api/config
Get current agent configuration

### POST /api/config
Update agent configuration

### POST /api/agents/<name>/goal
Set a goal for an agent

### GET /api/agents/<name>/export
Export agent state to JSON

## Configuration

### Change Port

```python
run_dashboard(
    agent_team=team,
    host='127.0.0.1',
    port=8080,  # Change port
    debug=True
)
```

### Enable External Access

```python
run_dashboard(
    agent_team=team,
    host='0.0.0.0',  # Allow external connections
    port=5000,
    debug=False  # Disable debug in production
)
```

### Custom Configuration Path

```python
run_dashboard(
    agent_team=team,
    config_path="path/to/custom/config.yaml",
    host='127.0.0.1',
    port=5000
)
```

## Integration with Your Code

### Option 1: Launch with Existing Agents

```python
from src.agents.agent_factory import AgentFactory
from src.web.agent_dashboard import run_dashboard

# Create agents
factory = AgentFactory("config/agent_models.yaml")
team = factory.create_audit_team()

# Set goals
team['esther'].set_goal("Assess IAM risks")

# Launch dashboard
run_dashboard(agent_team=team)
```

### Option 2: Launch Empty, Add Agents Later

```python
from src.web.agent_dashboard import init_dashboard, app

# Initialize empty
init_dashboard(agent_team={})

# Add agents dynamically
from src.agents.agent_monitor import monitor
monitor.add_agent("esther", esther_agent)

# Run
app.run(host='127.0.0.1', port=5000)
```

### Option 3: Use as Monitoring Tool

```python
# In your main script
from src.web.agent_dashboard import run_dashboard
import threading

# Launch dashboard in background thread
dashboard_thread = threading.Thread(
    target=run_dashboard,
    kwargs={'agent_team': team, 'debug': False}
)
dashboard_thread.daemon = True
dashboard_thread.start()

# Continue with your audit workflow
# Dashboard runs in background
```

## Troubleshooting

### Port Already in Use

```bash
# Change port in launch script
python examples/launch_dashboard.py --port 8080
```

Or kill the process using port 5000:
```bash
# macOS/Linux
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Dashboard Shows No Agents

1. Check that agents were created successfully
2. Verify config file exists: `config/agent_models.yaml`
3. Check console for error messages
4. Try refreshing the page

### Agents Not Updating

1. Check that auto-refresh is working (every 5 seconds)
2. Click the "🔄 Refresh" button manually
3. Check browser console for errors
4. Verify agents are actually running

### High Memory Usage

The dashboard stores agent state in memory. For long-running audits:

1. Restart dashboard periodically
2. Export agent state before restarting
3. Use the API to query specific data instead of loading everything

## Best Practices

1. **Launch Early**: Start dashboard before running agents
2. **Monitor Costs**: Check costs frequently to avoid surprises
3. **Export State**: Save agent state at key milestones
4. **Use Tabs**: Switch between Info/Actions/Memory for different views
5. **Auto-Refresh**: Let it update automatically, don't refresh manually

## Advanced Features

### Custom Styling

Edit `src/web/templates/dashboard.html` to customize:
- Colors
- Layout
- Fonts
- Animations

### Add New Endpoints

Edit `src/web/agent_dashboard.py` to add:
- New API endpoints
- Custom data views
- Additional functionality

### Embed in Larger App

```python
from src.web.agent_dashboard import app as dashboard_app
from flask import Flask

# Your main app
main_app = Flask(__name__)

# Mount dashboard as blueprint
main_app.register_blueprint(dashboard_app, url_prefix='/agents')
```

## Security Notes

⚠️ **For Development Only**

The dashboard is designed for local development and demos. For production:

1. Add authentication
2. Use HTTPS
3. Restrict access by IP
4. Disable debug mode
5. Add rate limiting
6. Validate all inputs

## Comparison: CLI vs Web

| Feature | CLI Monitor | Web Dashboard |
|---------|-------------|---------------|
| Ease of Use | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Visual Appeal | ⭐ | ⭐⭐⭐⭐⭐ |
| Real-Time Updates | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Detailed Info | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Scriptable | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Remote Access | ⭐ | ⭐⭐⭐⭐⭐ |

**Use CLI when**: Scripting, automation, detailed analysis

**Use Web when**: Monitoring, demos, presentations, ease of use

## Next Steps

1. Launch the dashboard: `python examples/launch_dashboard.py`
2. Open http://127.0.0.1:5000 in your browser
3. Create some agents and watch them work
4. Explore the different tabs and features
5. Customize the UI to your liking

Enjoy your beautiful agent dashboard! 🎉
