"""
Unit tests for AuditAgent base class.
"""

import pytest
import json
from datetime import datetime
from unittest.mock import Mock, MagicMock

from src.agents.audit_agent import AuditAgent, Tool, AgentAction
from src.agents.llm_client import LLMClient, LLMResponse


class TestAuditAgent(AuditAgent):
    """Concrete implementation for testing"""
    
    def create_workpaper(self):
        return {"workpaper": "test"}


def test_agent_initialization():
    """Test agent can be initialized with name, role, and LLM client"""
    llm = Mock(spec=LLMClient)
    agent = TestAuditAgent(
        name="TestAgent",
        role="Test Auditor",
        llm_client=llm
    )
    
    assert agent.name == "TestAgent"
    assert agent.role == "Test Auditor"
    assert agent.llm == llm
    assert agent.goal_status == "idle"
    assert agent.current_goal is None
    assert len(agent.memory) == 1  # System message
    assert agent.memory[0]["role"] == "system"


def test_tool_registration():
    """Test tools can be registered with the agent"""
    llm = Mock(spec=LLMClient)
    agent = TestAuditAgent(
        name="TestAgent",
        role="Test Auditor",
        llm_client=llm
    )
    
    # Create a test tool
    def test_execute(**kwargs):
        return {"result": "success"}
    
    tool = Tool(
        name="test_tool",
        description="A test tool",
        parameters={"param1": {"type": "string"}},
        execute=test_execute
    )
    
    agent.register_tool(tool)
    
    assert "test_tool" in agent.tools
    assert agent.tools["test_tool"].name == "test_tool"


def test_set_goal():
    """Test setting a goal for the agent"""
    llm = Mock(spec=LLMClient)
    agent = TestAuditAgent(
        name="TestAgent",
        role="Test Auditor",
        llm_client=llm
    )
    
    goal = "Test goal for the agent"
    agent.set_goal(goal)
    
    assert agent.current_goal == goal
    assert agent.goal_status == "working"
    assert len(agent.memory) == 2  # System message + goal message
    assert len(agent.action_history) == 1
    assert agent.action_history[0].action_type == "goal_set"


def test_reason_with_tool_decision():
    """Test agent reasoning returns a tool use decision"""
    llm = Mock(spec=LLMClient)
    
    # Mock LLM response
    llm_response = LLMResponse(
        content=json.dumps({
            "action": "use_tool",
            "tool": "test_tool",
            "parameters": {"param1": "value1"},
            "reasoning": "I need to use this tool to collect data"
        }),
        model="test-model",
        tokens_used=100,
        cost=0.01,
        timestamp=datetime.now()
    )
    llm.chat = Mock(return_value=llm_response)
    
    agent = TestAuditAgent(
        name="TestAgent",
        role="Test Auditor",
        llm_client=llm
    )
    
    agent.set_goal("Test goal")
    decision = agent.reason()
    
    assert decision["action"] == "use_tool"
    assert decision["tool"] == "test_tool"
    assert decision["parameters"]["param1"] == "value1"
    assert "reasoning" in decision
    assert len(agent.action_history) == 2  # goal_set + reason


def test_execute_tool():
    """Test agent can execute a tool"""
    llm = Mock(spec=LLMClient)
    agent = TestAuditAgent(
        name="TestAgent",
        role="Test Auditor",
        llm_client=llm
    )
    
    # Register a test tool
    def test_execute(param1):
        return {"result": f"executed with {param1}"}
    
    tool = Tool(
        name="test_tool",
        description="A test tool",
        parameters={"param1": {"type": "string"}},
        execute=test_execute
    )
    agent.register_tool(tool)
    
    # Execute tool through act()
    decision = {
        "action": "use_tool",
        "tool": "test_tool",
        "parameters": {"param1": "test_value"},
        "reasoning": "Testing tool execution"
    }
    
    result = agent.act(decision)
    
    assert result["result"] == "executed with test_value"
    assert any(a.action_type == "tool_call" for a in agent.action_history)


def test_complete_goal():
    """Test agent can complete a goal"""
    llm = Mock(spec=LLMClient)
    agent = TestAuditAgent(
        name="TestAgent",
        role="Test Auditor",
        llm_client=llm
    )
    
    agent.set_goal("Test goal")
    
    decision = {
        "action": "goal_complete",
        "summary": "Goal completed successfully",
        "next_steps": "Review findings"
    }
    
    result = agent.act(decision)
    
    assert result["status"] == "complete"
    assert agent.goal_status == "complete"
    assert any(a.action_type == "goal_complete" for a in agent.action_history)


def test_document_work():
    """Test agent can document work"""
    llm = Mock(spec=LLMClient)
    agent = TestAuditAgent(
        name="TestAgent",
        role="Test Auditor",
        llm_client=llm
    )
    
    decision = {
        "action": "document",
        "content": "Test findings",
        "reasoning": "Documenting test results"
    }
    
    result = agent.act(decision)
    
    assert result["status"] == "documented"
    assert result["content"] == "Test findings"
    assert any(a.action_type == "document" for a in agent.action_history)


def test_action_history_tracking():
    """Test agent tracks all actions in history"""
    llm = Mock(spec=LLMClient)
    agent = TestAuditAgent(
        name="TestAgent",
        role="Test Auditor",
        llm_client=llm
    )
    
    # Perform several actions
    agent.set_goal("Test goal")
    
    agent._log_action(
        action_type="test_action",
        description="Test action",
        details={"key": "value"}
    )
    
    history = agent.get_action_history()
    
    assert len(history) >= 2
    assert all(isinstance(action, AgentAction) for action in history)
    assert all(hasattr(action, "timestamp") for action in history)


def test_reset_agent():
    """Test agent can be reset to initial state"""
    llm = Mock(spec=LLMClient)
    agent = TestAuditAgent(
        name="TestAgent",
        role="Test Auditor",
        llm_client=llm
    )
    
    # Set up some state
    agent.set_goal("Test goal")
    agent._log_action("test", "test action")
    
    # Reset
    agent.reset()
    
    assert agent.current_goal is None
    assert agent.goal_status == "idle"
    assert len(agent.memory) == 1  # Only system message
    assert len(agent.action_history) == 0
    assert len(agent.context) == 0


def test_parse_llm_response_with_json_block():
    """Test parsing LLM response with JSON code block"""
    llm = Mock(spec=LLMClient)
    agent = TestAuditAgent(
        name="TestAgent",
        role="Test Auditor",
        llm_client=llm
    )
    
    response = """Here's my decision:
    
```json
{
    "action": "use_tool",
    "tool": "test_tool",
    "reasoning": "Need to collect data"
}
```

That's what I'll do next."""
    
    decision = agent._parse_llm_response(response)
    
    assert decision["action"] == "use_tool"
    assert decision["tool"] == "test_tool"


def test_parse_llm_response_plain_json():
    """Test parsing LLM response with plain JSON"""
    llm = Mock(spec=LLMClient)
    agent = TestAuditAgent(
        name="TestAgent",
        role="Test Auditor",
        llm_client=llm
    )
    
    response = '{"action": "goal_complete", "summary": "Done"}'
    
    decision = agent._parse_llm_response(response)
    
    assert decision["action"] == "goal_complete"
    assert decision["summary"] == "Done"


def test_tool_execution_error_handling():
    """Test agent handles tool execution errors gracefully"""
    llm = Mock(spec=LLMClient)
    agent = TestAuditAgent(
        name="TestAgent",
        role="Test Auditor",
        llm_client=llm
    )
    
    # Register a tool that raises an error
    def failing_tool(**kwargs):
        raise ValueError("Tool failed")
    
    tool = Tool(
        name="failing_tool",
        description="A tool that fails",
        parameters={},
        execute=failing_tool
    )
    agent.register_tool(tool)
    
    decision = {
        "action": "use_tool",
        "tool": "failing_tool",
        "parameters": {},
        "reasoning": "Testing error handling"
    }
    
    result = agent.act(decision)
    
    assert "error" in result
    assert "Tool execution failed" in result["error"]


def test_unknown_tool_error():
    """Test agent handles unknown tool gracefully"""
    llm = Mock(spec=LLMClient)
    agent = TestAuditAgent(
        name="TestAgent",
        role="Test Auditor",
        llm_client=llm
    )
    
    decision = {
        "action": "use_tool",
        "tool": "nonexistent_tool",
        "parameters": {},
        "reasoning": "Testing unknown tool"
    }
    
    result = agent.act(decision)
    
    assert "error" in result
    assert "not found" in result["error"]


def test_memory_management():
    """Test agent maintains conversation memory"""
    llm = Mock(spec=LLMClient)
    agent = TestAuditAgent(
        name="TestAgent",
        role="Test Auditor",
        llm_client=llm
    )
    
    initial_memory_size = len(agent.memory)
    
    # Set goal adds to memory
    agent.set_goal("Test goal")
    assert len(agent.memory) > initial_memory_size
    
    # Mock LLM response
    llm_response = LLMResponse(
        content='{"action": "goal_complete", "summary": "Done"}',
        model="test",
        tokens_used=10,
        cost=0.0,
        timestamp=datetime.now()
    )
    llm.chat = Mock(return_value=llm_response)
    
    # Reasoning adds to memory
    agent.reason()
    assert len(agent.memory) > initial_memory_size + 1
