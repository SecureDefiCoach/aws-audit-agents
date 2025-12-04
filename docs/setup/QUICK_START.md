# Quick Start Guide

## Directory Structure

Your project root should look like this:

```
aws-audit-agents/           ← YOU SHOULD BE HERE
├── src/
│   ├── agents/
│   ├── aws/
│   ├── models/
│   ├── utils/
│   └── web/
├── examples/
│   ├── launch_dashboard.py
│   ├── agent_monitoring.py
│   └── ...
├── config/
│   └── agent_models.yaml
├── tests/
├── requirements.txt
└── README.md
```

## Running Python Scripts

### ✅ Correct Way

```bash
# 1. Navigate to project root
cd /path/to/aws-audit-agents

# 2. Verify you're in the right place
ls
# You should see: src/ examples/ config/ tests/ requirements.txt

# 3. Run scripts from here
python examples/launch_dashboard.py
python examples/agent_monitoring.py
python examples/multi_model_agents.py
```

### ❌ Wrong Way

```bash
# DON'T do this
cd examples
python launch_dashboard.py  # Will fail with import errors
```

## Why?

Python needs to find the `src/` module. When you run from the project root:
- Python can import `from src.agents.agent_factory import ...`
- Relative paths work correctly (`config/agent_models.yaml`)
- Output directories are created in the right place

## Quick Commands

### Launch Web Dashboard
```bash
# From project root
python examples/launch_dashboard.py
```

### Run Agent Monitoring Example
```bash
# From project root
python examples/agent_monitoring.py
```

### Run Multi-Model Example
```bash
# From project root
python examples/multi_model_agents.py
```

### Run Tests
```bash
# From project root
python -m pytest tests/unit/test_tools.py -v
```

## Checking Your Location

```bash
# Print current directory
pwd

# Should show something like:
# /Users/yourname/aws-audit-agents
# or
# /home/yourname/aws-audit-agents
```

## If You Get Import Errors

```
ModuleNotFoundError: No module named 'src'
```

**Solution**: You're in the wrong directory!

```bash
# Go up one level
cd ..

# Or navigate to project root
cd /path/to/aws-audit-agents
```

## Setting Up Your Environment

### First Time Setup

```bash
# 1. Navigate to project root
cd /path/to/aws-audit-agents

# 2. Create virtual environment (optional but recommended)
python -m venv venv

# 3. Activate virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set API key (if using OpenAI)
export OPENAI_API_KEY='your-key-here'
```

### Every Time You Work

```bash
# 1. Navigate to project root
cd /path/to/aws-audit-agents

# 2. Activate virtual environment (if using one)
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# 3. Run your scripts
python examples/launch_dashboard.py
```

## Common Scenarios

### Scenario 1: Launch Dashboard

```bash
cd /path/to/aws-audit-agents
python examples/launch_dashboard.py
# Opens http://127.0.0.1:5000
```

### Scenario 2: Run Tests

```bash
cd /path/to/aws-audit-agents
python -m pytest tests/unit/ -v
```

### Scenario 3: Create Agents Programmatically

```bash
cd /path/to/aws-audit-agents
python
>>> from src.agents.agent_factory import AgentFactory
>>> factory = AgentFactory("config/agent_models.yaml")
>>> team = factory.create_audit_team()
```

### Scenario 4: Run Custom Script

```bash
cd /path/to/aws-audit-agents
python your_script.py
```

## Pro Tips

### 1. Add Project Root to PYTHONPATH

```bash
# Add to ~/.bashrc or ~/.zshrc
export PYTHONPATH="/path/to/aws-audit-agents:$PYTHONPATH"

# Then you can run from anywhere
cd ~/Documents
python /path/to/aws-audit-agents/examples/launch_dashboard.py
```

### 2. Create Aliases

```bash
# Add to ~/.bashrc or ~/.zshrc
alias audit-dashboard='cd /path/to/aws-audit-agents && python examples/launch_dashboard.py'
alias audit-monitor='cd /path/to/aws-audit-agents && python examples/agent_monitoring.py'

# Then just run:
audit-dashboard
```

### 3. Use VS Code

Open the project root folder in VS Code:
```bash
cd /path/to/aws-audit-agents
code .
```

Then use the integrated terminal (already in the right directory).

## Troubleshooting

### "No such file or directory: config/agent_models.yaml"

**Problem**: You're not in the project root

**Solution**:
```bash
pwd  # Check where you are
cd /path/to/aws-audit-agents  # Go to project root
ls config/  # Verify config directory exists
```

### "ModuleNotFoundError: No module named 'src'"

**Problem**: Python can't find the src module

**Solution**:
```bash
cd /path/to/aws-audit-agents  # Go to project root
python examples/launch_dashboard.py  # Run from here
```

### "Permission denied"

**Problem**: Script isn't executable or wrong Python

**Solution**:
```bash
# Use python explicitly
python examples/launch_dashboard.py

# Or make executable
chmod +x examples/launch_dashboard.py
./examples/launch_dashboard.py
```

## Summary

**Always run from project root:**
```bash
cd /path/to/aws-audit-agents  # ← Be here
python examples/script_name.py
```

**Never run from subdirectories:**
```bash
cd examples  # ← Don't be here
python script_name.py  # ← Will fail
```

That's it! When in doubt, `cd` to the project root and run from there. 🚀
