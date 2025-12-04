"""
Unit tests for Esther Agent.
"""

import pytest
import os
import json
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, MagicMock, patch

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.agents.esther_agent import EstherAgent, IAMTool
from src.agents.llm_client import LLMClient, LLMResponse
from src.aws.iam_client import IAMClient


@pytest.fixture
def mock_llm():
    """Create a mock LLM client."""
    llm = Mock(spec=LLMClient)
    llm.model = "gpt-4-turbo"
    llm.provider = "openai"
    return llm


@pytest.fixture
def mock_iam_client():
    """Create a mock IAM client."""
    iam = Mock(spec=IAMClient)
    iam.read_only = True
    return iam


@pytest.fixture
def esther(mock_llm, mock_iam_client, tmp_path):
    """Create an Esther agent instance."""
    return EstherAgent(
        llm_client=mock_llm,
        iam_client=mock_iam_client,
        output_dir=str(tmp_path)
    )


class TestEstherAgent:
    """Tests for EstherAgent class."""
    
    def test_initialization(self, esther):
        """Test that Esther initializes correctly."""
        assert esther.name == "Esther"
        assert esther.role == "Senior Auditor - IAM & Logical Access"
        assert "IAM" in esther.control_domains
        assert esther.staff_auditor == "Hillel"
        
        # Check tools are registered
        assert "query_iam" in esther.tools
        assert "create_workpaper" in esther.tools
        assert "store_evidence" in esther.tools
    
    def test_set_goal(self, esther):
        """Test setting a goal for Esther."""
        goal = "Assess IAM risks for CloudRetail Inc"
        esther.set_goal(goal)
        
        assert esther.current_goal == goal
        assert esther.goal_status == "working"
        assert len(esther.action_history) == 1
        assert esther.action_history[0].action_type == "goal_set"
    
    def test_get_summary(self, esther):
        """Test getting Esther's work summary."""
        esther.set_goal("Test goal")
        esther.workpapers_created = ["WP-IAM-001", "WP-IAM-002"]
        esther.evidence_collected = ["EVD-IAM-001"]
        
        summary = esther.get_summary()
        
        assert summary["name"] == "Esther"
        assert summary["role"] == "Senior Auditor - IAM & Logical Access"
        assert summary["current_goal"] == "Test goal"
        assert summary["workpapers_created"] == 2
        assert summary["evidence_collected"] == 1
        assert summary["staff_auditor"] == "Hillel"
    
    def test_create_workpaper(self, esther, tmp_path):
        """Test creating a workpaper."""
        result = esther.create_workpaper(
            reference_number="WP-IAM-001",
            control_objective="Ensure proper IAM access controls",
            testing_procedures=["Review user list", "Check MFA status"],
            evidence_ids=["EVD-IAM-001", "EVD-IAM-002"],
            analysis="Analysis of IAM controls",
            conclusion="Pass"
        )
        
        assert result["status"] == "success"
        assert result["reference_number"] == "WP-IAM-001"
        assert "WP-IAM-001" in esther.workpapers_created
        
        # Check files were created
        json_file = tmp_path / "workpapers" / "WP-IAM-001.json"
        md_file = tmp_path / "workpapers" / "WP-IAM-001.md"
        assert json_file.exists()
        assert md_file.exists()


class TestIAMTool:
    """Tests for IAMTool class."""
    
    @pytest.fixture
    def iam_tool(self, mock_iam_client):
        """Create an IAM tool instance."""
        return IAMTool(mock_iam_client)
    
    def test_initialization(self, iam_tool):
        """Test IAM tool initialization."""
        assert iam_tool.name == "query_iam"
        assert "IAM" in iam_tool.description
        
        # Check parameters
        params = iam_tool.get_parameters()
        assert "operation" in params["properties"]
        assert "user_name" in params["properties"]
        assert "role_name" in params["properties"]
    
    def test_list_users(self, iam_tool, mock_iam_client):
        """Test listing IAM users."""
        mock_iam_client.list_users.return_value = [
            {"UserName": "alice", "UserId": "AIDAI123"},
            {"UserName": "bob", "UserId": "AIDAI456"}
        ]
        
        result = iam_tool.execute(operation="list_users")
        
        assert result["status"] == "success"
        assert result["operation"] == "list_users"
        assert len(result["result"]) == 2
        assert result["result"][0]["UserName"] == "alice"
        mock_iam_client.list_users.assert_called_once()
    
    def test_list_roles(self, iam_tool, mock_iam_client):
        """Test listing IAM roles."""
        mock_iam_client.list_roles.return_value = [
            {"RoleName": "AdminRole", "RoleId": "AROAI123"}
        ]
        
        result = iam_tool.execute(operation="list_roles")
        
        assert result["status"] == "success"
        assert result["operation"] == "list_roles"
        assert len(result["result"]) == 1
        mock_iam_client.list_roles.assert_called_once()
    
    def test_get_user(self, iam_tool, mock_iam_client):
        """Test getting specific user details."""
        mock_iam_client.get_user.return_value = {
            "UserName": "alice",
            "UserId": "AIDAI123"
        }
        
        result = iam_tool.execute(operation="get_user", user_name="alice")
        
        assert result["status"] == "success"
        assert result["result"]["UserName"] == "alice"
        mock_iam_client.get_user.assert_called_once_with("alice")
    
    def test_get_user_missing_parameter(self, iam_tool):
        """Test that get_user fails without user_name."""
        with pytest.raises(Exception) as exc_info:
            iam_tool.execute(operation="get_user")
        
        assert "user_name required" in str(exc_info.value)
    
    def test_list_access_keys(self, iam_tool, mock_iam_client):
        """Test listing access keys for a user."""
        mock_iam_client.list_access_keys.return_value = [
            {"AccessKeyId": "AKIAI123", "Status": "Active"}
        ]
        
        result = iam_tool.execute(operation="list_access_keys", user_name="alice")
        
        assert result["status"] == "success"
        assert len(result["result"]) == 1
        mock_iam_client.list_access_keys.assert_called_once_with("alice")
    
    def test_list_mfa_devices(self, iam_tool, mock_iam_client):
        """Test listing MFA devices for a user."""
        mock_iam_client.list_mfa_devices.return_value = [
            {"SerialNumber": "arn:aws:iam::123456789012:mfa/alice"}
        ]
        
        result = iam_tool.execute(operation="list_mfa_devices", user_name="alice")
        
        assert result["status"] == "success"
        assert len(result["result"]) == 1
        mock_iam_client.list_mfa_devices.assert_called_once_with("alice")
    
    def test_get_account_summary(self, iam_tool, mock_iam_client):
        """Test getting account summary."""
        mock_iam_client.get_account_summary.return_value = {
            "Users": 10,
            "Roles": 5,
            "Groups": 3
        }
        
        result = iam_tool.execute(operation="get_account_summary")
        
        assert result["status"] == "success"
        assert result["result"]["Users"] == 10
        mock_iam_client.get_account_summary.assert_called_once()
    
    def test_unknown_operation(self, iam_tool):
        """Test that unknown operations raise an error."""
        with pytest.raises(Exception) as exc_info:
            iam_tool.execute(operation="invalid_operation")
        
        assert "Unknown IAM operation" in str(exc_info.value)


class TestEstherIntegration:
    """Integration tests for Esther with mocked LLM responses."""
    
    def test_reason_and_act_query_iam(self, esther, mock_llm, mock_iam_client):
        """Test Esther reasoning and querying IAM."""
        # Set up goal
        esther.set_goal("List all IAM users")
        
        # Mock LLM response to query IAM
        mock_llm.chat.return_value = LLMResponse(
            content='{"action": "use_tool", "tool": "query_iam", '
                    '"parameters": {"operation": "list_users"}, '
                    '"reasoning": "I need to see all IAM users first"}',
            model="gpt-4-turbo",
            tokens_used=150,
            cost=0.001,
            timestamp=datetime.now()
        )
        
        # Mock IAM response
        mock_iam_client.list_users.return_value = [
            {"UserName": "alice", "UserId": "AIDAI123"}
        ]
        
        # Reason and act
        decision = esther.reason()
        result = esther.act(decision)
        
        assert decision["action"] == "use_tool"
        assert decision["tool"] == "query_iam"
        assert result["status"] == "success"
        assert len(result["result"]) == 1
    
    def test_reason_and_act_complete_goal(self, esther, mock_llm):
        """Test Esther completing a goal."""
        esther.set_goal("Test goal")
        
        # Mock LLM response to complete goal
        mock_llm.chat.return_value = LLMResponse(
            content='{"action": "goal_complete", '
                    '"summary": "Successfully completed the assessment", '
                    '"next_steps": "Review findings with manager"}',
            model="gpt-4-turbo",
            tokens_used=150,
            cost=0.001,
            timestamp=datetime.now()
        )
        
        # Reason and act
        decision = esther.reason()
        result = esther.act(decision)
        
        assert decision["action"] == "goal_complete"
        assert esther.goal_status == "complete"
        assert result["status"] == "complete"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
