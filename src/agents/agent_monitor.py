"""
Agent Monitor - Tool for inspecting and managing agent attributes.

This module provides utilities to monitor agent state, view their attributes,
track their progress, and inspect their reasoning process.
"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from tabulate import tabulate


class AgentMonitor:
    """
    Monitor and inspect agent attributes and state.
    
    Provides visibility into:
    - Agent configuration (name, role, model)
    - Current state (goal, status, memory)
    - Action history
    - Tool usage
    - LLM costs
    """
    
    def __init__(self, agents: Optional[Dict[str, Any]] = None):
        """
        Initialize the agent monitor.
        
        Args:
            agents: Optional dict of agents to monitor
        """
        self.agents = agents or {}
    
    def add_agent(self, name: str, agent: Any):
        """Add an agent to monitor."""
        self.agents[name] = agent
    
    def add_agents(self, agents: Dict[str, Any]):
        """Add multiple agents to monitor."""
        self.agents.update(agents)
    
    def get_agent_info(self, agent_name: str) -> Dict[str, Any]:
        """
        Get comprehensive information about an agent.
        
        Args:
            agent_name: Name of the agent
        
        Returns:
            Dict with agent information
        """
        if agent_name not in self.agents:
            return {"error": f"Agent '{agent_name}' not found"}
        
        agent = self.agents[agent_name]
        
        # Get all agent attributes
        info = {
            # Basic Identity
            "name": agent.name,
            "role": agent.role,
            
            # LLM Configuration
            "model": agent.llm.model,
            "provider": agent.llm.provider,
            "temperature": agent.llm.temperature,
            "rate_limit": agent.llm.rate_limiter.max_calls,
            
            # Current State
            "current_goal": agent.current_goal,
            "goal_status": agent.goal_status,
            
            # Tools
            "tools": list(agent.tools.keys()),
            "tool_details": {
                name: {
                    "description": tool.description,
                    "parameters": tool.get_parameters()
                }
                for name, tool in agent.tools.items()
            },
            
            # Memory & Context
            "memory_size": len(agent.memory),
            "context_keys": list(agent.context.keys()) if hasattr(agent, 'context') else [],
            
            # Activity
            "action_count": len(agent.action_history),
            
            # LLM Usage
            "llm_calls": agent.llm.cost_tracker.call_count,
            "llm_cost": agent.llm.cost_tracker.total_cost,
            "llm_tokens": agent.llm.cost_tracker.total_tokens,
            "avg_tokens_per_call": agent.llm.cost_tracker.total_tokens / agent.llm.cost_tracker.call_count if agent.llm.cost_tracker.call_count > 0 else 0,
            
            # All Attributes (for debugging)
            "all_attributes": {
                attr: str(getattr(agent, attr))[:100]  # Truncate long values
                for attr in dir(agent)
                if not attr.startswith('_') and not callable(getattr(agent, attr))
            }
        }
        
        return info
    
    def print_agent_info(self, agent_name: str):
        """Print formatted agent information."""
        info = self.get_agent_info(agent_name)
        
        if "error" in info:
            print(f"❌ {info['error']}")
            return
        
        print("\n" + "=" * 80)
        print(f"AGENT: {info['name']}")
        print("=" * 80)
        print()
        print(f"Role:          {info['role']}")
        print(f"LLM Model:     {info['model']} ({info['provider']})")
        print()
        print("CURRENT STATE:")
        print(f"  Goal:        {info['current_goal'] or 'None'}")
        print(f"  Status:      {info['goal_status']}")
        print()
        print("TOOLS:")
        for tool in info['tools']:
            print(f"  • {tool}")
        print()
        print("ACTIVITY:")
        print(f"  Memory size: {info['memory_size']} messages")
        print(f"  Actions:     {info['action_count']}")
        print()
        print("LLM USAGE:")
        print(f"  API calls:   {info['llm_calls']}")
        print(f"  Tokens:      {info['llm_tokens']:,}")
        print(f"  Cost:        ${info['llm_cost']:.4f}")
        print()
    
    def get_team_summary(self) -> List[Dict[str, Any]]:
        """
        Get summary of all agents.
        
        Returns:
            List of agent summaries
        """
        summaries = []
        
        for name, agent in self.agents.items():
            summaries.append({
                "key": name,  # Dictionary key (e.g., "maurice", "esther")
                "name": agent.name,  # Display name (e.g., "Maurice", "Esther")
                "role": agent.role,
                "model": agent.llm.model,
                "status": agent.goal_status,
                "actions": len(agent.action_history),
                "llm_calls": agent.llm.cost_tracker.call_count,
                "cost": agent.llm.cost_tracker.total_cost
            })
        
        return summaries
    
    def print_team_summary(self):
        """Print formatted team summary."""
        summaries = self.get_team_summary()
        
        if not summaries:
            print("No agents to monitor")
            return
        
        print("\n" + "=" * 80)
        print("TEAM SUMMARY")
        print("=" * 80)
        print()
        
        # Prepare table data
        headers = ["Agent", "Role", "Model", "Status", "Actions", "LLM Calls", "Cost"]
        rows = []
        
        for s in summaries:
            rows.append([
                s["name"],
                s["role"][:30] + "..." if len(s["role"]) > 30 else s["role"],
                s["model"],
                s["status"],
                s["actions"],
                s["llm_calls"],
                f"${s['cost']:.4f}"
            ])
        
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        print()
        
        # Totals
        total_actions = sum(s["actions"] for s in summaries)
        total_calls = sum(s["llm_calls"] for s in summaries)
        total_cost = sum(s["cost"] for s in summaries)
        
        print(f"TOTALS:")
        print(f"  Total Actions:    {total_actions}")
        print(f"  Total LLM Calls:  {total_calls}")
        print(f"  Total Cost:       ${total_cost:.4f}")
        print()
    
    def get_agent_memory(self, agent_name: str, last_n: Optional[int] = None) -> List[Dict]:
        """
        Get agent's conversation memory.
        
        Args:
            agent_name: Name of the agent
            last_n: Optional number of recent messages to return
        
        Returns:
            List of memory messages
        """
        if agent_name not in self.agents:
            return []
        
        agent = self.agents[agent_name]
        memory = agent.memory
        
        if last_n:
            return memory[-last_n:]
        
        return memory
    
    def print_agent_memory(self, agent_name: str, last_n: Optional[int] = 5):
        """Print agent's recent memory."""
        memory = self.get_agent_memory(agent_name, last_n)
        
        if not memory:
            print(f"No memory for agent '{agent_name}'")
            return
        
        print("\n" + "=" * 80)
        print(f"AGENT MEMORY: {agent_name}")
        if last_n:
            print(f"(Last {last_n} messages)")
        print("=" * 80)
        print()
        
        for i, msg in enumerate(memory, 1):
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            
            print(f"[{i}] {role.upper()}:")
            print(f"{content[:500]}...")
            print()
    
    def get_agent_actions(self, agent_name: str, last_n: Optional[int] = None) -> List[Any]:
        """
        Get agent's action history.
        
        Args:
            agent_name: Name of the agent
            last_n: Optional number of recent actions to return
        
        Returns:
            List of actions
        """
        if agent_name not in self.agents:
            return []
        
        agent = self.agents[agent_name]
        actions = agent.action_history
        
        if last_n:
            return actions[-last_n:]
        
        return actions
    
    def print_agent_actions(self, agent_name: str, last_n: Optional[int] = 10):
        """Print agent's recent actions."""
        actions = self.get_agent_actions(agent_name, last_n)
        
        if not actions:
            print(f"No actions for agent '{agent_name}'")
            return
        
        print("\n" + "=" * 80)
        print(f"AGENT ACTIONS: {agent_name}")
        if last_n:
            print(f"(Last {last_n} actions)")
        print("=" * 80)
        print()
        
        for i, action in enumerate(actions, 1):
            timestamp = action.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{i}] {timestamp} - {action.action_type}")
            print(f"    {action.description}")
            if action.result:
                result_str = str(action.result)[:100]
                print(f"    Result: {result_str}...")
            print()
    
    def get_cost_breakdown(self) -> Dict[str, Any]:
        """
        Get cost breakdown by agent and model.
        
        Returns:
            Dict with cost analysis
        """
        by_agent = {}
        by_model = {}
        
        for name, agent in self.agents.items():
            model = agent.llm.model
            cost = agent.llm.cost_tracker.total_cost
            tokens = agent.llm.cost_tracker.total_tokens
            calls = agent.llm.cost_tracker.call_count
            
            by_agent[name] = {
                "model": model,
                "cost": cost,
                "tokens": tokens,
                "calls": calls
            }
            
            if model not in by_model:
                by_model[model] = {
                    "agents": [],
                    "total_cost": 0,
                    "total_tokens": 0,
                    "total_calls": 0
                }
            
            by_model[model]["agents"].append(name)
            by_model[model]["total_cost"] += cost
            by_model[model]["total_tokens"] += tokens
            by_model[model]["total_calls"] += calls
        
        return {
            "by_agent": by_agent,
            "by_model": by_model,
            "total_cost": sum(a["cost"] for a in by_agent.values()),
            "total_tokens": sum(a["tokens"] for a in by_agent.values()),
            "total_calls": sum(a["calls"] for a in by_agent.values())
        }
    
    def print_cost_breakdown(self):
        """Print detailed cost breakdown."""
        breakdown = self.get_cost_breakdown()
        
        print("\n" + "=" * 80)
        print("COST BREAKDOWN")
        print("=" * 80)
        print()
        
        # By model
        print("BY MODEL:")
        for model, data in sorted(breakdown["by_model"].items()):
            print(f"\n  {model}:")
            print(f"    Agents:      {', '.join(data['agents'])}")
            print(f"    Total Cost:  ${data['total_cost']:.4f}")
            print(f"    Total Tokens: {data['total_tokens']:,}")
            print(f"    Total Calls:  {data['total_calls']}")
        
        print()
        print("BY AGENT:")
        for name, data in sorted(breakdown["by_agent"].items()):
            print(f"  {name:15} ({data['model']:15}): ${data['cost']:.4f} ({data['tokens']:,} tokens, {data['calls']} calls)")
        
        print()
        print("TOTALS:")
        print(f"  Total Cost:   ${breakdown['total_cost']:.4f}")
        print(f"  Total Tokens: {breakdown['total_tokens']:,}")
        print(f"  Total Calls:  {breakdown['total_calls']}")
        print()
    
    def export_agent_state(self, agent_name: str, filepath: str):
        """
        Export agent state to JSON file.
        
        Args:
            agent_name: Name of the agent
            filepath: Path to save JSON file
        """
        if agent_name not in self.agents:
            print(f"Agent '{agent_name}' not found")
            return
        
        agent = self.agents[agent_name]
        
        state = {
            "name": agent.name,
            "role": agent.role,
            "model": agent.llm.model,
            "provider": agent.llm.provider,
            "current_goal": agent.current_goal,
            "goal_status": agent.goal_status,
            "tools": list(agent.tools.keys()),
            "memory": agent.memory,
            "actions": [
                {
                    "timestamp": a.timestamp.isoformat(),
                    "action_type": a.action_type,
                    "description": a.description,
                    "details": a.details,
                    "result": str(a.result) if a.result else None
                }
                for a in agent.action_history
            ],
            "llm_usage": {
                "calls": agent.llm.cost_tracker.call_count,
                "tokens": agent.llm.cost_tracker.total_tokens,
                "cost": agent.llm.cost_tracker.total_cost
            },
            "exported_at": datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2, default=str)
        
        print(f"✓ Exported {agent_name} state to {filepath}")
    
    def list_agents(self) -> List[str]:
        """Get list of monitored agent names."""
        return list(self.agents.keys())
    
    def interactive_monitor(self):
        """
        Interactive monitoring interface.
        
        Provides a simple CLI for inspecting agents.
        """
        print("\n" + "=" * 80)
        print("AGENT MONITOR - Interactive Mode")
        print("=" * 80)
        print()
        print("Commands:")
        print("  list              - List all agents")
        print("  summary           - Show team summary")
        print("  info <agent>      - Show agent details")
        print("  memory <agent>    - Show agent memory")
        print("  actions <agent>   - Show agent actions")
        print("  costs             - Show cost breakdown")
        print("  export <agent>    - Export agent state to JSON")
        print("  quit              - Exit monitor")
        print()
        
        while True:
            try:
                cmd = input("monitor> ").strip().lower()
                
                if not cmd:
                    continue
                
                parts = cmd.split()
                command = parts[0]
                
                if command == "quit" or command == "exit":
                    print("Exiting monitor...")
                    break
                
                elif command == "list":
                    agents = self.list_agents()
                    print(f"\nMonitored agents ({len(agents)}):")
                    for name in agents:
                        print(f"  • {name}")
                    print()
                
                elif command == "summary":
                    self.print_team_summary()
                
                elif command == "info":
                    if len(parts) < 2:
                        print("Usage: info <agent_name>")
                    else:
                        self.print_agent_info(parts[1])
                
                elif command == "memory":
                    if len(parts) < 2:
                        print("Usage: memory <agent_name> [count]")
                    else:
                        count = int(parts[2]) if len(parts) > 2 else 5
                        self.print_agent_memory(parts[1], count)
                
                elif command == "actions":
                    if len(parts) < 2:
                        print("Usage: actions <agent_name> [count]")
                    else:
                        count = int(parts[2]) if len(parts) > 2 else 10
                        self.print_agent_actions(parts[1], count)
                
                elif command == "costs":
                    self.print_cost_breakdown()
                
                elif command == "export":
                    if len(parts) < 2:
                        print("Usage: export <agent_name> [filepath]")
                    else:
                        filepath = parts[2] if len(parts) > 2 else f"{parts[1]}_state.json"
                        self.export_agent_state(parts[1], filepath)
                
                else:
                    print(f"Unknown command: {command}")
                    print("Type 'quit' to exit or see commands above")
            
            except KeyboardInterrupt:
                print("\nExiting monitor...")
                break
            except Exception as e:
                print(f"Error: {e}")
