"""
Base AuditAgent class with LLM reasoning.

This module implements autonomous agents that use LLMs to reason about goals,
make decisions, and document their work. Agents are given goals and tools,
not step-by-step instructions.
"""

import json
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from abc import ABC, abstractmethod
from pathlib import Path

from .llm_client import LLMClient, LLMResponse
from .tools import Tool


@dataclass
class AgentAction:
    """Record of an agent action"""
    timestamp: datetime
    action_type: str  # "reason", "tool_call", "document", "message"
    description: str
    details: Dict[str, Any] = field(default_factory=dict)
    result: Optional[Any] = None


class AuditAgent(ABC):
    """
    Base class for LLM-powered audit agents.
    
    Agents reason independently using LLMs, execute actions using tools,
    and document their work in professional workpapers.
    
    Core principle: Agents are given GOALS and TOOLS, not step-by-step instructions.
    """
    
    def __init__(
        self,
        name: str,
        role: str,
        llm_client: LLMClient,
        tools: Optional[List[Tool]] = None,
        knowledge_path: Optional[str] = None
    ):
        """
        Initialize an audit agent.
        
        Args:
            name: Agent's name (e.g., "Esther", "Maurice")
            role: Agent's role (e.g., "Senior Auditor - IAM")
            llm_client: LLM client for reasoning
            tools: List of tools available to the agent
            knowledge_path: Path to agent's knowledge folder (e.g., "knowledge/maurice")
        """
        self.name = name
        self.role = role
        self.llm = llm_client
        self.tools: Dict[str, Tool] = {}
        self.knowledge: Dict[str, str] = {}  # Loaded knowledge/procedures
        
        # Register tools
        if tools:
            for tool in tools:
                self.register_tool(tool)
        
        # Load agent-specific knowledge (this also loads shared procedures)
        if knowledge_path:
            self.load_knowledge(knowledge_path)
        
        # Agent state
        self.current_goal: Optional[str] = None
        self.goal_status: str = "idle"  # "idle", "working", "complete", "blocked"
        self.memory: List[Dict[str, str]] = []  # Conversation history with LLM
        self.action_history: List[AgentAction] = []  # Record of all actions
        self.context: Dict[str, Any] = {}  # Additional context/state
        
        # Initialize system message
        self._init_system_message()
    
    def load_knowledge(self, path: str):
        """
        Load knowledge/procedures from a folder.
        Loads both shared procedures and agent-specific knowledge.
        
        Args:
            path: Path to knowledge folder (e.g., "knowledge/maurice")
        """
        # Load shared procedures first (available to all auditors)
        shared_dir = Path("knowledge/shared")
        if shared_dir.exists():
            for file in shared_dir.glob("*.md"):
                procedure_name = f"shared/{file.stem}"
                procedure_content = file.read_text()
                self.knowledge[procedure_name] = procedure_content
                print(f"📚 {self.name}: Loaded shared procedure '{file.stem}'")
        
        # Load agent-specific knowledge
        knowledge_dir = Path(path)
        if not knowledge_dir.exists():
            return
        
        for file in knowledge_dir.glob("*.md"):
            procedure_name = file.stem
            procedure_content = file.read_text()
            self.knowledge[procedure_name] = procedure_content
            print(f"📚 {self.name}: Loaded knowledge '{procedure_name}'")
    
    def get_knowledge_context(self) -> str:
        """
        Get all loaded knowledge as a formatted string for LLM context.
        
        Returns:
            Formatted string with all knowledge/procedures
        """
        if not self.knowledge:
            return "No specialized knowledge loaded."
        
        context = "## Your Knowledge and Procedures\n\n"
        context += "You have access to the following procedures and guidelines:\n\n"
        
        for name, content in self.knowledge.items():
            context += f"### {name.replace('-', ' ').title()}\n\n"
            context += f"{content}\n\n"
            context += "---\n\n"
        
        return context
    
    def _init_system_message(self):
        """Initialize the system message that defines the agent's identity"""
        system_msg = f"""You are {self.name}, a {self.role}.

You are an autonomous audit agent. You reason independently, make decisions, 
and document your work professionally.

Your capabilities:
- Reason about audit goals and determine next steps
- Use tools to collect evidence and analyze AWS infrastructure
- Adapt your approach based on what you discover
- Document your findings and reasoning in professional workpapers
- Communicate with other agents when needed

Available tools:
{self._format_tools_for_prompt()}

{self.get_knowledge_context()}

When you decide to use a tool, respond with a JSON object:
{{
    "action": "use_tool",
    "tool": "tool_name",
    "parameters": {{"param1": "value1", "param2": "value2"}},
    "reasoning": "Why you're using this tool"
}}

When you've completed your goal, respond with:
{{
    "action": "goal_complete",
    "summary": "What you accomplished",
    "next_steps": "Any recommendations or follow-up needed"
}}

When you need to document findings, respond with:
{{
    "action": "document",
    "content": "Your findings and analysis",
    "reasoning": "Your thought process"
}}

Always explain your reasoning. Your thought process is as important as your actions.

When following procedures from your knowledge base, reference which procedure you're using in your reasoning.
"""
        self.memory.append({"role": "system", "content": system_msg})
    
    def _format_tools_for_prompt(self) -> str:
        """Format tools list for LLM prompt"""
        if not self.tools:
            return "No tools available"
        
        tool_descriptions = []
        for tool_name, tool in self.tools.items():
            params = json.dumps(tool.get_parameters(), indent=2)
            tool_descriptions.append(
                f"- {tool_name}: {tool.description}\n  Parameters: {params}"
            )
        
        return "\n".join(tool_descriptions)
    
    def register_tool(self, tool: Tool):
        """Register a tool for the agent to use"""
        self.tools[tool.name] = tool
        print(f"🔧 {self.name}: Registered tool '{tool.name}'")
    
    def set_goal(self, goal: str):
        """
        Set a goal for the agent to achieve.
        
        Args:
            goal: High-level objective (e.g., "Assess IAM risks for CloudRetail Inc")
        """
        self.current_goal = goal
        self.goal_status = "working"
        
        # Add goal to memory
        goal_msg = f"""Your goal: {goal}

Think step by step about how to achieve this goal. What should you do first?"""
        
        self.memory.append({"role": "user", "content": goal_msg})
        
        # Log action
        self._log_action(
            action_type="goal_set",
            description=f"Goal set: {goal}",
            details={"goal": goal}
        )
        
        print(f"\n🎯 {self.name}: New goal set")
        print(f"   {goal}")
    
    def reason(self) -> Dict[str, Any]:
        """
        Agent reasons about what to do next using LLM.
        
        Returns:
            Dict with action decision and reasoning
        """
        if not self.current_goal:
            raise ValueError("No goal set. Call set_goal() first.")
        
        if self.goal_status != "working":
            raise ValueError(f"Agent is not working (status: {self.goal_status})")
        
        print(f"\n🤔 {self.name}: Reasoning about next action...")
        
        # Get LLM response
        response = self.llm.chat(self.memory)
        
        # Add to memory
        self.memory.append({"role": "assistant", "content": response.content})
        
        # Parse response
        try:
            decision = self._parse_llm_response(response.content)
        except Exception as e:
            print(f"⚠️  {self.name}: Failed to parse LLM response: {e}")
            print(f"   Raw response: {response.content[:200]}...")
            
            # Ask LLM to clarify
            clarification_msg = """Your response wasn't in the expected JSON format. 
Please respond with a valid JSON object specifying your action."""
            self.memory.append({"role": "user", "content": clarification_msg})
            
            # Try again
            response = self.llm.chat(self.memory)
            self.memory.append({"role": "assistant", "content": response.content})
            decision = self._parse_llm_response(response.content)
        
        # Log reasoning
        self._log_action(
            action_type="reason",
            description="Agent reasoned about next action",
            details=decision,
            result=decision.get("reasoning", "")
        )
        
        print(f"💭 {self.name}: {decision.get('reasoning', 'No reasoning provided')}")
        
        return decision
    
    def _parse_llm_response(self, content: str) -> Dict[str, Any]:
        """Parse LLM response into structured decision"""
        # Try to extract JSON from response
        content = content.strip()
        
        # Look for JSON block
        if "```json" in content:
            start = content.find("```json") + 7
            end = content.find("```", start)
            json_str = content[start:end].strip()
        elif "```" in content:
            start = content.find("```") + 3
            end = content.find("```", start)
            json_str = content[start:end].strip()
        elif content.startswith("{"):
            json_str = content
        else:
            # Try to find JSON object in text
            start = content.find("{")
            end = content.rfind("}") + 1
            if start >= 0 and end > start:
                json_str = content[start:end]
            else:
                raise ValueError("No JSON object found in response")
        
        return json.loads(json_str)
    
    def act(self, decision: Dict[str, Any]) -> Any:
        """
        Execute an action based on the agent's decision.
        
        Args:
            decision: Decision dict from reason()
        
        Returns:
            Result of the action
        """
        action_type = decision.get("action")
        
        if action_type == "use_tool":
            return self._execute_tool(decision)
        
        elif action_type == "goal_complete":
            return self._complete_goal(decision)
        
        elif action_type == "document":
            return self._document_work(decision)
        
        elif action_type == "send_message":
            return self._send_message(decision)
        
        else:
            raise ValueError(f"Unknown action type: {action_type}")
    
    def _execute_tool(self, decision: Dict[str, Any]) -> Any:
        """Execute a tool based on agent's decision"""
        tool_name = decision.get("tool")
        parameters = decision.get("parameters", {})
        reasoning = decision.get("reasoning", "")
        
        if tool_name not in self.tools:
            error_msg = f"Tool '{tool_name}' not found. Available tools: {list(self.tools.keys())}"
            print(f"❌ {self.name}: {error_msg}")
            
            # Add error to memory so agent can adapt
            self.memory.append({"role": "user", "content": error_msg})
            return {"error": error_msg}
        
        tool = self.tools[tool_name]
        
        print(f"🔧 {self.name}: Using tool '{tool_name}'")
        print(f"   Reasoning: {reasoning}")
        
        try:
            # Execute tool
            result = tool.execute(**parameters)
            
            # Log action
            self._log_action(
                action_type="tool_call",
                description=f"Used tool: {tool_name}",
                details={"tool": tool_name, "parameters": parameters, "reasoning": reasoning},
                result=result
            )
            
            # Add result to memory
            result_msg = f"""Tool '{tool_name}' executed successfully.

Result:
{json.dumps(result, indent=2, default=str)}

What should you do next?"""
            
            self.memory.append({"role": "user", "content": result_msg})
            
            print(f"✅ {self.name}: Tool executed successfully")
            
            return result
        
        except Exception as e:
            error_msg = f"Tool execution failed: {str(e)}"
            print(f"❌ {self.name}: {error_msg}")
            
            # Log error
            self._log_action(
                action_type="tool_call",
                description=f"Tool call failed: {tool_name}",
                details={"tool": tool_name, "parameters": parameters, "error": str(e)},
                result=None
            )
            
            # Add error to memory
            self.memory.append({"role": "user", "content": error_msg})
            
            return {"error": error_msg}
    
    def _complete_goal(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Mark goal as complete"""
        summary = decision.get("summary", "")
        next_steps = decision.get("next_steps", "")
        
        self.goal_status = "complete"
        
        # Log completion
        self._log_action(
            action_type="goal_complete",
            description="Goal completed",
            details={"summary": summary, "next_steps": next_steps}
        )
        
        print(f"\n✅ {self.name}: Goal completed!")
        print(f"   Summary: {summary}")
        if next_steps:
            print(f"   Next steps: {next_steps}")
        
        return {
            "status": "complete",
            "summary": summary,
            "next_steps": next_steps
        }
    
    def _document_work(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Document work (to be implemented by subclasses)"""
        content = decision.get("content", "")
        reasoning = decision.get("reasoning", "")
        
        # Log documentation
        self._log_action(
            action_type="document",
            description="Documented work",
            details={"content": content, "reasoning": reasoning}
        )
        
        print(f"📝 {self.name}: Documented work")
        
        return {
            "status": "documented",
            "content": content,
            "reasoning": reasoning
        }
    
    def _send_message(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Send message to another agent (to be implemented by orchestrator)"""
        to = decision.get("to", "")
        message = decision.get("message", "")
        
        # Log message
        self._log_action(
            action_type="message",
            description=f"Sent message to {to}",
            details={"to": to, "message": message}
        )
        
        print(f"💬 {self.name} → {to}: {message[:100]}...")
        
        return {
            "status": "sent",
            "to": to,
            "message": message
        }
    
    def _log_action(
        self,
        action_type: str,
        description: str,
        details: Optional[Dict[str, Any]] = None,
        result: Optional[Any] = None
    ):
        """Log an action to the agent's history"""
        action = AgentAction(
            timestamp=datetime.now(),
            action_type=action_type,
            description=description,
            details=details or {},
            result=result
        )
        self.action_history.append(action)
    
    def run_autonomously(self, max_iterations: int = 10) -> Dict[str, Any]:
        """
        Run the agent autonomously until goal is complete or max iterations reached.
        
        Args:
            max_iterations: Maximum reasoning-action cycles
        
        Returns:
            Final status dict
        """
        if not self.current_goal:
            raise ValueError("No goal set. Call set_goal() first.")
        
        print(f"\n🚀 {self.name}: Starting autonomous execution")
        print(f"   Goal: {self.current_goal}")
        print(f"   Max iterations: {max_iterations}")
        
        iteration = 0
        
        while self.goal_status == "working" and iteration < max_iterations:
            iteration += 1
            print(f"\n--- Iteration {iteration}/{max_iterations} ---")
            
            try:
                # Reason about next action
                decision = self.reason()
                
                # Execute action
                result = self.act(decision)
                
                # Check if goal is complete
                if decision.get("action") == "goal_complete":
                    break
                
                # Small delay to avoid tight loop
                time.sleep(0.5)
            
            except Exception as e:
                print(f"❌ {self.name}: Error during execution: {e}")
                self.goal_status = "blocked"
                break
        
        if iteration >= max_iterations:
            print(f"\n⚠️  {self.name}: Reached max iterations without completing goal")
            self.goal_status = "blocked"
        
        return {
            "status": self.goal_status,
            "iterations": iteration,
            "actions_taken": len(self.action_history)
        }
    
    def get_action_history(self) -> List[AgentAction]:
        """Get the agent's action history"""
        return self.action_history
    
    def get_memory_summary(self) -> str:
        """Get a summary of the agent's memory/context"""
        return f"Memory: {len(self.memory)} messages, {len(self.action_history)} actions"
    
    def reset(self):
        """Reset agent state (useful for testing)"""
        self.current_goal = None
        self.goal_status = "idle"
        self.memory = []
        self.action_history = []
        self.context = {}
        self._init_system_message()
        
        print(f"🔄 {self.name}: Agent reset")
    
    @abstractmethod
    def create_workpaper(self) -> Any:
        """
        Create a workpaper documenting the agent's work.
        
        To be implemented by subclasses (e.g., SeniorAuditorAgent).
        """
        pass
