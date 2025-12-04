"""
Agent Dashboard - Web-based UI for monitoring and configuring agents.

This provides a Flask web application for:
- Viewing agent configuration and status
- Monitoring agent progress in real-time
- Editing agent configuration
- Tracking costs
- Viewing agent memory and actions
"""

from flask import Flask, render_template, jsonify, request, send_from_directory
import os
import json
import yaml
from pathlib import Path
from datetime import datetime

from ..agents.agent_monitor import AgentMonitor
from ..agents.agent_factory import AgentFactory


app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')

# Global state
monitor = None
factory = None
team = None
phase_status = {
    1: "not-started",
    2: "not-started",
    3: "not-started",
    4: "not-started",
    5: "not-started",
    6: "not-started"
}


def init_dashboard(agent_team=None, config_path="config/agent_models.yaml"):
    """
    Initialize the dashboard with agents.
    
    Args:
        agent_team: Optional dict of agents
        config_path: Path to agent configuration
    """
    global monitor, factory, team, phase_status
    
    factory = AgentFactory(config_path)
    
    if agent_team:
        team = agent_team
    else:
        team = {}
    
    monitor = AgentMonitor(team)
    
    # Load phase status from file if it exists
    phase_file = Path("output/audit_phase_status.json")
    if phase_file.exists():
        try:
            with open(phase_file, 'r') as f:
                loaded_status = json.load(f)
                # Convert string keys to integers
                phase_status = {int(k): v for k, v in loaded_status.items()}
        except Exception as e:
            print(f"Warning: Could not load phase status: {e}")


@app.route('/')
def index():
    """Main dashboard page."""
    return render_template('dashboard.html')


@app.route('/api/agents')
def get_agents():
    """Get list of all agents with their status."""
    if not monitor:
        return jsonify({"error": "Dashboard not initialized"}), 500
    
    summaries = monitor.get_team_summary()
    return jsonify(summaries)


@app.route('/api/agents/<agent_name>')
def get_agent_info(agent_name):
    """Get detailed information about a specific agent."""
    if not monitor:
        return jsonify({"error": "Dashboard not initialized"}), 500
    
    info = monitor.get_agent_info(agent_name)
    return jsonify(info)


@app.route('/api/agents/<agent_name>/memory')
def get_agent_memory(agent_name):
    """Get agent's conversation memory."""
    if not monitor:
        return jsonify({"error": "Dashboard not initialized"}), 500
    
    last_n = request.args.get('last_n', default=10, type=int)
    memory = monitor.get_agent_memory(agent_name, last_n=last_n)
    return jsonify(memory)


@app.route('/api/agents/<agent_name>/actions')
def get_agent_actions(agent_name):
    """Get agent's action history."""
    if not monitor:
        return jsonify({"error": "Dashboard not initialized"}), 500
    
    last_n = request.args.get('last_n', default=20, type=int)
    actions = monitor.get_agent_actions(agent_name, last_n=last_n)
    
    # Convert to JSON-serializable format
    actions_data = [
        {
            "timestamp": a.timestamp.isoformat(),
            "action_type": a.action_type,
            "description": a.description,
            "details": a.details,
            "result": str(a.result) if a.result else None
        }
        for a in actions
    ]
    
    return jsonify(actions_data)


@app.route('/api/costs')
def get_costs():
    """Get cost breakdown."""
    if not monitor:
        return jsonify({"error": "Dashboard not initialized"}), 500
    
    breakdown = monitor.get_cost_breakdown()
    return jsonify(breakdown)


@app.route('/api/config')
def get_config():
    """Get current agent configuration."""
    if not factory:
        return jsonify({"error": "Dashboard not initialized"}), 500
    
    return jsonify(factory.config)


@app.route('/api/config', methods=['POST'])
def update_config():
    """Update agent configuration."""
    if not factory:
        return jsonify({"error": "Dashboard not initialized"}), 500
    
    try:
        new_config = request.json
        
        # Save to file
        config_path = factory.config_path
        with open(config_path, 'w') as f:
            yaml.dump(new_config, f, default_flow_style=False)
        
        # Reload factory
        factory.config = factory._load_config()
        
        return jsonify({"success": True, "message": "Configuration updated"})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/agents/<agent_name>/goal', methods=['POST'])
def set_agent_goal(agent_name):
    """Set a goal for an agent."""
    if not team or agent_name not in team:
        return jsonify({"error": f"Agent '{agent_name}' not found"}), 404
    
    try:
        data = request.json
        goal = data.get('goal')
        
        if not goal:
            return jsonify({"error": "Goal is required"}), 400
        
        agent = team[agent_name]
        agent.set_goal(goal)
        
        return jsonify({
            "success": True,
            "message": f"Goal set for {agent_name}",
            "goal": goal
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/agents/<agent_name>/export')
def export_agent_state(agent_name):
    """Export agent state to JSON."""
    if not monitor:
        return jsonify({"error": "Dashboard not initialized"}), 500
    
    try:
        # Create output directory
        output_dir = Path("output/exports")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Export
        filepath = output_dir / f"{agent_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        monitor.export_agent_state(agent_name, str(filepath))
        
        return jsonify({
            "success": True,
            "filepath": str(filepath)
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/agents/<agent_name>/knowledge')
def get_agent_knowledge(agent_name):
    """Get agent's knowledge base."""
    if not team or agent_name not in team:
        return jsonify({"error": f"Agent '{agent_name}' not found"}), 404
    
    agent = team[agent_name]
    
    knowledge_data = []
    for name, content in agent.knowledge.items():
        # Get first few lines as preview
        lines = content.split('\n')
        preview = '\n'.join(lines[:5]) + ('...' if len(lines) > 5 else '')
        
        knowledge_data.append({
            "name": name,
            "title": name.replace('-', ' ').title(),
            "preview": preview,
            "size": len(content),
            "lines": len(lines)
        })
    
    return jsonify({
        "count": len(knowledge_data),
        "procedures": knowledge_data
    })


@app.route('/api/agents/<agent_name>/tasks')
def get_agent_tasks(agent_name):
    """Get agent's tasks."""
    tasks_dir = Path("tasks")
    task_file = tasks_dir / f"{agent_name.lower()}-tasks.md"
    
    if not task_file.exists():
        return jsonify({
            "current": [],
            "completed": [],
            "delegated": []
        })
    
    content = task_file.read_text()
    
    # Parse tasks
    tasks = {
        "current": [],
        "completed": [],
        "delegated": []
    }
    
    current_section = None
    current_task = None
    task_details = {}
    
    for line in content.split('\n'):
        if line.strip() == "## Current Tasks":
            current_section = "current"
        elif line.strip() == "## Completed Tasks":
            current_section = "completed"
        elif line.strip().startswith("## Delegated"):
            current_section = "delegated"
        elif line.strip().startswith("- [ ]") or line.strip().startswith("- [x]"):
            if current_section and current_task:
                # Save previous task
                tasks[current_section].append({
                    "description": current_task,
                    **task_details
                })
            
            # Start new task
            current_task = line.strip()[6:]
            task_details = {}
        elif line.strip().startswith("- ") and current_task:
            # Parse task details
            detail = line.strip()[2:]
            if ": " in detail:
                key, value = detail.split(": ", 1)
                task_details[key.lower().replace(" ", "_")] = value
    
    # Add last task
    if current_section and current_task:
        tasks[current_section].append({
            "description": current_task,
            **task_details
        })
    
    return jsonify(tasks)


@app.route('/api/agents/<agent_name>/capabilities')
def get_agent_capabilities(agent_name):
    """Get agent's capabilities and tools."""
    if not team or agent_name not in team:
        return jsonify({"error": f"Agent '{agent_name}' not found"}), 404
    
    agent = team[agent_name]
    
    # Get tool details
    tools_data = []
    for tool_name, tool in agent.tools.items():
        tool_info = {
            "name": tool_name,
            "description": tool.description,
            "parameters": []
        }
        
        # Get parameters
        for param in tool._parameters:
            tool_info["parameters"].append({
                "name": param.name,
                "type": param.type,
                "description": param.description,
                "required": param.required
            })
        
        tools_data.append(tool_info)
    
    # Check for AWS capabilities
    aws_capabilities = []
    if hasattr(agent, 'iam_client'):
        aws_capabilities.append({
            "service": "IAM",
            "description": "Identity and Access Management",
            "operations": [
                "list_users", "list_roles", "get_user", "get_role",
                "list_user_policies", "list_attached_user_policies",
                "list_access_keys", "list_mfa_devices",
                "get_account_summary", "get_credential_report"
            ]
        })
    
    return jsonify({
        "tools": tools_data,
        "aws_capabilities": aws_capabilities,
        "knowledge_count": len(agent.knowledge),
        "can_delegate_tasks": "manage_tasks" in agent.tools
    })


@app.route('/api/agents/<agent_name>/system_prompt', methods=['GET'])
def get_system_prompt(agent_name):
    """Get agent's system prompt."""
    if not team or agent_name not in team:
        return jsonify({"error": f"Agent '{agent_name}' not found"}), 404
    
    agent = team[agent_name]
    
    # Get system message (first message in memory)
    system_prompt = ""
    if agent.memory and agent.memory[0].get("role") == "system":
        system_prompt = agent.memory[0].get("content", "")
    
    return jsonify({
        "prompt": system_prompt
    })


@app.route('/api/agents/<agent_name>/system_prompt', methods=['POST'])
def update_system_prompt(agent_name):
    """Update agent's system prompt."""
    if not team or agent_name not in team:
        return jsonify({"error": f"Agent '{agent_name}' not found"}), 404
    
    try:
        data = request.json
        new_prompt = data.get('prompt')
        
        if not new_prompt:
            return jsonify({"error": "Prompt is required"}), 400
        
        agent = team[agent_name]
        
        # Update system message (first message in memory)
        if agent.memory and agent.memory[0].get("role") == "system":
            agent.memory[0]["content"] = new_prompt
        else:
            # If no system message, add one at the beginning
            agent.memory.insert(0, {"role": "system", "content": new_prompt})
        
        return jsonify({
            "success": True,
            "message": f"System prompt updated for {agent_name}"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/agents/<agent_name>/tools', methods=['GET'])
def get_agent_tools(agent_name):
    """Get list of tools for an agent."""
    if not team or agent_name not in team:
        return jsonify({"error": f"Agent '{agent_name}' not found"}), 404
    
    agent = team[agent_name]
    tools_list = []
    
    for tool_name, tool in agent.tools.items():
        tools_list.append({
            "name": tool_name,
            "description": tool.description
        })
    
    return jsonify({"tools": tools_list})


@app.route('/api/agents/<agent_name>/tools/remove', methods=['POST'])
def remove_agent_tool(agent_name):
    """Remove a tool from an agent."""
    if not team or agent_name not in team:
        return jsonify({"error": f"Agent '{agent_name}' not found"}), 404
    
    try:
        data = request.json
        tool_name = data.get('tool_name')
        
        if not tool_name:
            return jsonify({"error": "tool_name is required"}), 400
        
        agent = team[agent_name]
        
        if tool_name not in agent.tools:
            return jsonify({"error": f"Tool '{tool_name}' not found on agent"}), 404
        
        # Remove the tool
        del agent.tools[tool_name]
        
        # Reinitialize system message to update tool list
        agent._init_system_message()
        
        return jsonify({
            "success": True,
            "message": f"Tool '{tool_name}' removed from {agent_name}"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/tools/available', methods=['GET'])
def get_available_tools():
    """Get list of all available tools that can be added to agents."""
    from .tools import WorkpaperTool, EvidenceTool
    
    available = [
        {
            "name": "create_workpaper",
            "class": "WorkpaperTool",
            "description": "Create and manage audit workpapers"
        },
        {
            "name": "store_evidence",
            "class": "EvidenceTool", 
            "description": "Store and retrieve audit evidence"
        }
    ]
    
    return jsonify({"tools": available})


@app.route('/api/agents/<agent_name>/tools/add', methods=['POST'])
def add_agent_tool(agent_name):
    """Add a tool to an agent."""
    if not team or agent_name not in team:
        return jsonify({"error": f"Agent '{agent_name}' not found"}), 404
    
    try:
        data = request.json
        tool_class = data.get('tool_class')
        
        if not tool_class:
            return jsonify({"error": "tool_class is required"}), 400
        
        agent = team[agent_name]
        
        # Import and instantiate the tool
        from ..agents.tools import WorkpaperTool, EvidenceTool
        
        tool_map = {
            "WorkpaperTool": WorkpaperTool,
            "EvidenceTool": EvidenceTool
        }
        
        if tool_class not in tool_map:
            return jsonify({"error": f"Unknown tool class: {tool_class}"}), 400
        
        # Create tool instance
        tool = tool_map[tool_class]()
        
        # Check if tool already exists
        if tool.name in agent.tools:
            return jsonify({"error": f"Tool '{tool.name}' already exists on agent"}), 400
        
        # Add the tool
        agent.register_tool(tool)
        
        # Reinitialize system message to update tool list
        agent._init_system_message()
        
        return jsonify({
            "success": True,
            "message": f"Tool '{tool.name}' added to {agent_name}"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/audit/phases', methods=['GET'])
def get_audit_phases():
    """Get current status of all audit phases."""
    global phase_status
    
    phases = []
    phase_names = {
        1: "Risk Assessment & Planning",
        2: "Control Testing (Fieldwork)",
        3: "Workpaper Review & QA",
        4: "Remediation Planning",
        5: "Audit Reporting",
        6: "Follow-Up"
    }
    
    for phase_num in range(1, 7):
        phases.append({
            "number": phase_num,
            "name": phase_names[phase_num],
            "status": phase_status.get(phase_num, "not-started")
        })
    
    return jsonify(phases)


@app.route('/api/audit/phases', methods=['POST'])
def update_audit_phase():
    """Update the status of an audit phase."""
    global phase_status
    
    try:
        data = request.json
        phase_num = data.get('phase')
        status = data.get('status')
        
        if not phase_num or phase_num not in range(1, 7):
            return jsonify({"error": "Invalid phase number (must be 1-6)"}), 400
        
        if status not in ['not-started', 'in-progress', 'complete']:
            return jsonify({"error": "Invalid status (must be 'not-started', 'in-progress', or 'complete')"}), 400
        
        phase_status[phase_num] = status
        
        # Optionally save to file for persistence
        phase_file = Path("output/audit_phase_status.json")
        phase_file.parent.mkdir(parents=True, exist_ok=True)
        with open(phase_file, 'w') as f:
            json.dump(phase_status, f, indent=2)
        
        return jsonify({
            "success": True,
            "message": f"Phase {phase_num} status updated to '{status}'"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/audit/phases/<int:phase_num>', methods=['PUT'])
def set_phase_status(phase_num):
    """Set the status of a specific audit phase."""
    global phase_status
    
    try:
        if phase_num not in range(1, 7):
            return jsonify({"error": "Invalid phase number (must be 1-6)"}), 400
        
        data = request.json
        status = data.get('status')
        
        if status not in ['not-started', 'in-progress', 'complete']:
            return jsonify({"error": "Invalid status (must be 'not-started', 'in-progress', or 'complete')"}), 400
        
        phase_status[phase_num] = status
        
        # Save to file for persistence
        phase_file = Path("output/audit_phase_status.json")
        phase_file.parent.mkdir(parents=True, exist_ok=True)
        with open(phase_file, 'w') as f:
            json.dump(phase_status, f, indent=2)
        
        return jsonify({
            "success": True,
            "phase": phase_num,
            "status": status
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def run_dashboard(agent_team=None, config_path="config/agent_models.yaml", 
                  host='127.0.0.1', port=5000, debug=True):
    """
    Run the agent dashboard web server.
    
    Args:
        agent_team: Optional dict of agents to monitor
        config_path: Path to agent configuration
        host: Host to bind to
        port: Port to bind to
        debug: Enable debug mode
    """
    init_dashboard(agent_team, config_path)
    
    print("\n" + "=" * 80)
    print("AGENT DASHBOARD")
    print("=" * 80)
    print()
    print(f"Starting web server at http://{host}:{port}")
    print()
    print("Features:")
    print("  • View agent status and configuration")
    print("  • Monitor agent progress in real-time")
    print("  • Edit agent configuration")
    print("  • Track LLM costs")
    print("  • View agent memory and actions")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 80)
    print()
    
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    run_dashboard()
