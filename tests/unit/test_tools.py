"""Unit tests for agent tools."""
import pytest
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

from src.agents.tools import (
    Tool,
    ToolParameter,
    ToolExecutionError,
    WorkpaperTool,
    EvidenceTool,
    create_tool_from_function
)


class TestToolParameter:
    """Tests for ToolParameter dataclass."""
    
    def test_create_required_parameter(self):
        """Test creating a required parameter."""
        param = ToolParameter(
            name="test_param",
            type="string",
            description="A test parameter",
            required=True
        )
        
        assert param.name == "test_param"
        assert param.type == "string"
        assert param.description == "A test parameter"
        assert param.required is True
        assert param.default is None
    
    def test_create_optional_parameter_with_default(self):
        """Test creating an optional parameter with default value."""
        param = ToolParameter(
            name="optional_param",
            type="number",
            description="An optional parameter",
            required=False,
            default=42
        )
        
        assert param.name == "optional_param"
        assert param.required is False
        assert param.default == 42


class TestToolBase:
    """Tests for Tool base class."""
    
    def test_tool_initialization(self):
        """Test tool initialization."""
        class SimpleTool(Tool):
            def execute(self, **kwargs):
                return {"result": "success"}
        
        tool = SimpleTool("test_tool", "A test tool")
        
        assert tool.name == "test_tool"
        assert tool.description == "A test tool"
        assert len(tool._parameters) == 0
    
    def test_add_parameter(self):
        """Test adding parameters to a tool."""
        class SimpleTool(Tool):
            def execute(self, **kwargs):
                return {"result": "success"}
        
        tool = SimpleTool("test_tool", "A test tool")
        tool.add_parameter("param1", "string", "First parameter", required=True)
        tool.add_parameter("param2", "number", "Second parameter", required=False, default=10)
        
        assert len(tool._parameters) == 2
        assert tool._parameters[0].name == "param1"
        assert tool._parameters[1].name == "param2"
    
    def test_get_parameters_schema(self):
        """Test getting parameter schema."""
        class SimpleTool(Tool):
            def execute(self, **kwargs):
                return {"result": "success"}
        
        tool = SimpleTool("test_tool", "A test tool")
        tool.add_parameter("required_param", "string", "Required parameter", required=True)
        tool.add_parameter("optional_param", "number", "Optional parameter", required=False, default=5)
        
        schema = tool.get_parameters()
        
        assert schema["type"] == "object"
        assert "required_param" in schema["properties"]
        assert "optional_param" in schema["properties"]
        assert "required_param" in schema["required"]
        assert "optional_param" not in schema["required"]
        assert schema["properties"]["optional_param"]["default"] == 5
    
    def test_validate_parameters_success(self):
        """Test parameter validation with valid parameters."""
        class SimpleTool(Tool):
            def execute(self, **kwargs):
                return {"result": "success"}
        
        tool = SimpleTool("test_tool", "A test tool")
        tool.add_parameter("param1", "string", "First parameter", required=True)
        
        # Should not raise
        tool.validate_parameters(param1="value")
    
    def test_validate_parameters_missing_required(self):
        """Test parameter validation with missing required parameter."""
        class SimpleTool(Tool):
            def execute(self, **kwargs):
                return {"result": "success"}
        
        tool = SimpleTool("test_tool", "A test tool")
        tool.add_parameter("param1", "string", "First parameter", required=True)
        
        with pytest.raises(ToolExecutionError) as exc_info:
            tool.validate_parameters()
        
        assert "Missing required parameter 'param1'" in str(exc_info.value)


class TestWorkpaperTool:
    """Tests for WorkpaperTool."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test outputs."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    def test_workpaper_tool_initialization(self, temp_dir):
        """Test WorkpaperTool initialization."""
        tool = WorkpaperTool(output_dir=temp_dir)
        
        assert tool.name == "create_workpaper"
        assert "workpaper" in tool.description.lower()
        assert Path(temp_dir).exists()
        assert len(tool._parameters) > 0
    
    def test_create_workpaper_success(self, temp_dir):
        """Test creating a workpaper successfully."""
        tool = WorkpaperTool(output_dir=temp_dir)
        
        result = tool.execute(
            reference_number="WP-IAM-001",
            control_domain="IAM",
            control_objective="Ensure MFA is enabled for all users",
            testing_procedures=["Review IAM users", "Check MFA status"],
            evidence_ids=["EVD-IAM-001", "EVD-IAM-002"],
            analysis="Analysis of IAM controls shows 2 users without MFA",
            conclusion="Deficiency Noted",
            created_by="Esther",
            cross_references=["WP-IAM-002"]
        )
        
        assert result["status"] == "success"
        assert result["reference_number"] == "WP-IAM-001"
        assert "file_path" in result
        
        # Verify files were created
        json_file = Path(temp_dir) / "WP-IAM-001.json"
        md_file = Path(temp_dir) / "WP-IAM-001.md"
        
        assert json_file.exists()
        assert md_file.exists()
        
        # Verify JSON content
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        assert data["reference_number"] == "WP-IAM-001"
        assert data["control_domain"] == "IAM"
        assert data["created_by"] == "Esther"
        assert len(data["evidence_collected"]) == 2
    
    def test_create_workpaper_missing_required_parameter(self, temp_dir):
        """Test creating workpaper with missing required parameter."""
        tool = WorkpaperTool(output_dir=temp_dir)
        
        with pytest.raises(ToolExecutionError) as exc_info:
            tool.execute(
                reference_number="WP-IAM-001",
                control_domain="IAM"
                # Missing other required parameters
            )
        
        assert "Missing required parameter" in str(exc_info.value)
    
    def test_workpaper_markdown_format(self, temp_dir):
        """Test that workpaper markdown is properly formatted."""
        tool = WorkpaperTool(output_dir=temp_dir)
        
        tool.execute(
            reference_number="WP-TEST-001",
            control_domain="Testing",
            control_objective="Test objective",
            testing_procedures=["Procedure 1", "Procedure 2"],
            evidence_ids=["EVD-001"],
            analysis="Test analysis",
            conclusion="Pass",
            created_by="TestAgent"
        )
        
        md_file = Path(temp_dir) / "WP-TEST-001.md"
        with open(md_file, 'r') as f:
            content = f.read()
        
        assert "# Workpaper WP-TEST-001" in content
        assert "## Control Domain" in content
        assert "Testing" in content
        assert "## Testing Procedures" in content
        assert "Procedure 1" in content
        assert "## Analysis" in content
        assert "Test analysis" in content


class TestEvidenceTool:
    """Tests for EvidenceTool."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test outputs."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    def test_evidence_tool_initialization(self, temp_dir):
        """Test EvidenceTool initialization."""
        tool = EvidenceTool(output_dir=temp_dir)
        
        assert tool.name == "store_evidence"
        assert "evidence" in tool.description.lower()
        assert Path(temp_dir).exists()
        assert len(tool._parameters) > 0
    
    def test_store_evidence_success(self, temp_dir):
        """Test storing evidence successfully."""
        tool = EvidenceTool(output_dir=temp_dir)
        
        evidence_data = {
            "users": [
                {"username": "admin", "mfa_enabled": False},
                {"username": "developer", "mfa_enabled": True}
            ]
        }
        
        result = tool.execute(
            evidence_id="EVD-IAM-001",
            source="IAM",
            collection_method="direct",
            collected_by="Esther",
            data=evidence_data,
            control_domain="IAM"
        )
        
        assert result["status"] == "success"
        assert result["evidence_id"] == "EVD-IAM-001"
        assert "storage_path" in result
        
        # Verify file was created
        evidence_file = Path(temp_dir) / "EVD-IAM-001.json"
        assert evidence_file.exists()
        
        # Verify content
        with open(evidence_file, 'r') as f:
            data = json.load(f)
        
        assert data["evidence_id"] == "EVD-IAM-001"
        assert data["source"] == "IAM"
        assert data["collected_by"] == "Esther"
        assert data["data"] == evidence_data
    
    def test_store_evidence_invalid_collection_method(self, temp_dir):
        """Test storing evidence with invalid collection method."""
        tool = EvidenceTool(output_dir=temp_dir)
        
        with pytest.raises(ToolExecutionError) as exc_info:
            tool.execute(
                evidence_id="EVD-001",
                source="IAM",
                collection_method="invalid_method",
                collected_by="Agent",
                data={}
            )
        
        assert "Invalid collection_method" in str(exc_info.value)
    
    def test_load_evidence_success(self, temp_dir):
        """Test loading evidence from storage."""
        tool = EvidenceTool(output_dir=temp_dir)
        
        # Store evidence first
        evidence_data = {"test": "data"}
        tool.execute(
            evidence_id="EVD-LOAD-001",
            source="S3",
            collection_method="agent_request",
            collected_by="Chuck",
            data=evidence_data
        )
        
        # Load evidence
        evidence = tool.load_evidence("EVD-LOAD-001")
        
        assert evidence is not None
        assert evidence.evidence_id == "EVD-LOAD-001"
        assert evidence.source == "S3"
        assert evidence.collected_by == "Chuck"
        assert evidence.data == evidence_data
    
    def test_load_evidence_not_found(self, temp_dir):
        """Test loading non-existent evidence."""
        tool = EvidenceTool(output_dir=temp_dir)
        
        evidence = tool.load_evidence("EVD-NONEXISTENT")
        
        assert evidence is None


class TestCreateToolFromFunction:
    """Tests for create_tool_from_function helper."""
    
    def test_create_simple_function_tool(self):
        """Test creating a tool from a simple function."""
        def add_numbers(a: int, b: int) -> int:
            return a + b
        
        parameters = [
            ToolParameter("a", "number", "First number", required=True),
            ToolParameter("b", "number", "Second number", required=True)
        ]
        
        tool = create_tool_from_function(
            name="add",
            description="Add two numbers",
            func=add_numbers,
            parameters=parameters
        )
        
        assert tool.name == "add"
        assert tool.description == "Add two numbers"
        
        result = tool.execute(a=5, b=3)
        
        assert result["status"] == "success"
        assert result["result"] == 8
    
    def test_function_tool_error_handling(self):
        """Test error handling in function tool."""
        def failing_function():
            raise ValueError("Something went wrong")
        
        tool = create_tool_from_function(
            name="fail",
            description="A failing function",
            func=failing_function,
            parameters=[]
        )
        
        with pytest.raises(ToolExecutionError) as exc_info:
            tool.execute()
        
        assert "Function execution failed" in str(exc_info.value)


class TestToolErrorHandling:
    """Tests for tool error handling."""
    
    def test_tool_execution_error_message(self):
        """Test ToolExecutionError message."""
        error = ToolExecutionError("Test error message")
        assert str(error) == "Test error message"
    
    def test_workpaper_tool_handles_file_system_errors(self, tmp_path):
        """Test WorkpaperTool handles file system errors gracefully."""
        # Create a tool with a valid directory
        tool = WorkpaperTool(output_dir=str(tmp_path))
        
        # Make the directory read-only to cause write errors
        import os
        os.chmod(tmp_path, 0o444)
        
        try:
            # The tool should handle the error and raise ToolExecutionError
            with pytest.raises(ToolExecutionError):
                tool.execute(
                    reference_number="WP-001",
                    control_domain="Test",
                    control_objective="Test",
                    testing_procedures=["Test"],
                    evidence_ids=["EVD-001"],
                    analysis="Test",
                    conclusion="Test",
                    created_by="Test"
                )
        finally:
            # Restore permissions for cleanup
            os.chmod(tmp_path, 0o755)
