"""
Tool interface and base tools for audit agents.

This module provides the Tool base class and concrete tool implementations
for creating audit documentation and storing evidence.
"""

import json
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional, List, Callable
from pathlib import Path

from ..models.workpaper import Workpaper
from ..models.evidence import Evidence


class ToolExecutionError(Exception):
    """Exception raised when tool execution fails."""
    pass


@dataclass
class ToolParameter:
    """Definition of a tool parameter."""
    name: str
    type: str  # "string", "number", "boolean", "object", "array"
    description: str
    required: bool = True
    default: Optional[Any] = None


class Tool(ABC):
    """
    Base class for agent tools.
    
    Tools provide capabilities to agents, such as creating workpapers,
    storing evidence, or querying AWS services.
    """
    
    def __init__(self, name: str, description: str):
        """
        Initialize a tool.
        
        Args:
            name: Tool name (used by agents to invoke the tool)
            description: Human-readable description of what the tool does
        """
        self.name = name
        self.description = description
        self._parameters: List[ToolParameter] = []
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the tool with given parameters.
        
        Args:
            **kwargs: Tool-specific parameters
        
        Returns:
            Dict containing execution results
        
        Raises:
            ToolExecutionError: If execution fails
        """
        pass
    
    def add_parameter(
        self,
        name: str,
        param_type: str,
        description: str,
        required: bool = True,
        default: Optional[Any] = None
    ):
        """Add a parameter definition to the tool."""
        param = ToolParameter(
            name=name,
            type=param_type,
            description=description,
            required=required,
            default=default
        )
        self._parameters.append(param)
    
    def get_parameters(self) -> Dict[str, Any]:
        """
        Get parameter schema for this tool.
        
        Returns:
            Dict describing parameters in JSON Schema format
        """
        properties = {}
        required = []
        
        for param in self._parameters:
            properties[param.name] = {
                "type": param.type,
                "description": param.description
            }
            if param.default is not None:
                properties[param.name]["default"] = param.default
            
            if param.required:
                required.append(param.name)
        
        return {
            "type": "object",
            "properties": properties,
            "required": required
        }
    
    def validate_parameters(self, **kwargs) -> None:
        """
        Validate that required parameters are provided.
        
        Args:
            **kwargs: Parameters to validate
        
        Raises:
            ToolExecutionError: If required parameters are missing
        """
        for param in self._parameters:
            if param.required and param.name not in kwargs:
                raise ToolExecutionError(
                    f"Missing required parameter '{param.name}' for tool '{self.name}'"
                )
    
    def __repr__(self) -> str:
        return f"Tool(name='{self.name}', description='{self.description}')"


class WorkpaperTool(Tool):
    """
    Tool for creating and managing audit workpapers.
    
    This tool allows agents to document their findings, analysis, and
    conclusions in professional audit workpapers.
    """
    
    def __init__(self, output_dir: str = "output/workpapers"):
        """
        Initialize the workpaper tool.
        
        Args:
            output_dir: Directory where workpapers will be saved
        """
        super().__init__(
            name="create_workpaper",
            description="Create an audit workpaper documenting testing procedures, evidence, analysis, and conclusions"
        )
        
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Define parameters
        self.add_parameter(
            "reference_number",
            "string",
            "Unique workpaper reference (e.g., 'WP-IAM-001')",
            required=True
        )
        self.add_parameter(
            "control_domain",
            "string",
            "Control domain being tested (e.g., 'IAM', 'Encryption', 'Logging')",
            required=True
        )
        self.add_parameter(
            "control_objective",
            "string",
            "The control objective being evaluated",
            required=True
        )
        self.add_parameter(
            "testing_procedures",
            "array",
            "List of testing procedures performed",
            required=True
        )
        self.add_parameter(
            "evidence_ids",
            "array",
            "List of evidence IDs referenced in this workpaper",
            required=True
        )
        self.add_parameter(
            "analysis",
            "string",
            "Detailed analysis of the evidence and findings",
            required=True
        )
        self.add_parameter(
            "conclusion",
            "string",
            "Conclusion about control effectiveness (e.g., 'Pass', 'Fail', 'Deficiency Noted')",
            required=True
        )
        self.add_parameter(
            "created_by",
            "string",
            "Agent name who created this workpaper",
            required=True
        )
        self.add_parameter(
            "cross_references",
            "array",
            "List of related workpaper references",
            required=False,
            default=[]
        )
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Create a workpaper with the provided information.
        
        Args:
            reference_number: Workpaper reference number
            control_domain: Control domain
            control_objective: Control objective
            testing_procedures: List of procedures
            evidence_ids: List of evidence IDs
            analysis: Analysis text
            conclusion: Conclusion text
            created_by: Agent name
            cross_references: Optional list of related workpapers
        
        Returns:
            Dict with workpaper details and file path
        
        Raises:
            ToolExecutionError: If workpaper creation fails
        """
        try:
            # Validate parameters
            self.validate_parameters(**kwargs)
            
            # Extract parameters
            reference_number = kwargs["reference_number"]
            control_domain = kwargs["control_domain"]
            control_objective = kwargs["control_objective"]
            testing_procedures = kwargs["testing_procedures"]
            evidence_ids = kwargs["evidence_ids"]
            analysis = kwargs["analysis"]
            conclusion = kwargs["conclusion"]
            created_by = kwargs["created_by"]
            cross_references = kwargs.get("cross_references", [])
            
            # Create workpaper object (with placeholder evidence objects)
            # In a real implementation, we'd load actual Evidence objects
            evidence_list = [
                Evidence(
                    evidence_id=eid,
                    source="placeholder",
                    collection_method="direct",
                    collected_at=datetime.now(),
                    collected_by=created_by,
                    data={},
                    storage_path=f"output/evidence/{eid}.json"
                )
                for eid in evidence_ids
            ]
            
            workpaper = Workpaper(
                reference_number=reference_number,
                control_domain=control_domain,
                control_objective=control_objective,
                testing_procedures=testing_procedures,
                evidence_collected=evidence_list,
                analysis=analysis,
                conclusion=conclusion,
                created_by=created_by,
                created_at=datetime.now(),
                cross_references=cross_references
            )
            
            # Save workpaper to file
            file_path = self._save_workpaper(workpaper)
            
            return {
                "status": "success",
                "reference_number": reference_number,
                "file_path": str(file_path),
                "created_at": workpaper.created_at.isoformat(),
                "message": f"Workpaper {reference_number} created successfully"
            }
        
        except ToolExecutionError:
            raise
        except Exception as e:
            raise ToolExecutionError(f"Failed to create workpaper: {str(e)}")
    
    def _save_workpaper(self, workpaper: Workpaper) -> Path:
        """
        Save workpaper to JSON and Markdown files.
        
        Args:
            workpaper: Workpaper object to save
        
        Returns:
            Path to the saved JSON file
        """
        # Create filename from reference number
        filename = workpaper.reference_number.replace(" ", "_")
        
        # Save as JSON
        json_path = self.output_dir / f"{filename}.json"
        with open(json_path, 'w') as f:
            json.dump(self._workpaper_to_dict(workpaper), f, indent=2, default=str)
        
        # Save as Markdown
        md_path = self.output_dir / f"{filename}.md"
        with open(md_path, 'w') as f:
            f.write(self._workpaper_to_markdown(workpaper))
        
        return json_path
    
    def _workpaper_to_dict(self, workpaper: Workpaper) -> Dict[str, Any]:
        """Convert workpaper to dictionary."""
        return {
            "reference_number": workpaper.reference_number,
            "control_domain": workpaper.control_domain,
            "control_objective": workpaper.control_objective,
            "testing_procedures": workpaper.testing_procedures,
            "evidence_collected": [
                {
                    "evidence_id": e.evidence_id,
                    "source": e.source,
                    "collection_method": e.collection_method,
                    "collected_at": e.collected_at.isoformat(),
                    "collected_by": e.collected_by,
                    "storage_path": e.storage_path
                }
                for e in workpaper.evidence_collected
            ],
            "analysis": workpaper.analysis,
            "conclusion": workpaper.conclusion,
            "created_by": workpaper.created_by,
            "created_at": workpaper.created_at.isoformat(),
            "cross_references": workpaper.cross_references
        }
    
    def _workpaper_to_markdown(self, workpaper: Workpaper) -> str:
        """Convert workpaper to Markdown format."""
        md = f"""# Workpaper {workpaper.reference_number}

## Control Domain
{workpaper.control_domain}

## Control Objective
{workpaper.control_objective}

## Testing Procedures
"""
        for i, procedure in enumerate(workpaper.testing_procedures, 1):
            md += f"{i}. {procedure}\n"
        
        md += f"""
## Evidence Collected
"""
        for evidence in workpaper.evidence_collected:
            md += f"- **{evidence.evidence_id}**: {evidence.source} (collected by {evidence.collected_by})\n"
        
        md += f"""
## Analysis
{workpaper.analysis}

## Conclusion
{workpaper.conclusion}

---
**Created by:** {workpaper.created_by}  
**Created at:** {workpaper.created_at.strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        if workpaper.cross_references:
            md += f"\n**Cross-references:** {', '.join(workpaper.cross_references)}\n"
        
        return md


class EvidenceTool(Tool):
    """
    Tool for storing and referencing audit evidence.
    
    This tool allows agents to store evidence collected from AWS services
    and other sources, maintaining proper audit trail metadata.
    """
    
    def __init__(self, output_dir: str = "output/evidence"):
        """
        Initialize the evidence tool.
        
        Args:
            output_dir: Directory where evidence will be saved
        """
        super().__init__(
            name="store_evidence",
            description="Store audit evidence with proper metadata and audit trail information"
        )
        
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Define parameters
        self.add_parameter(
            "evidence_id",
            "string",
            "Unique identifier for this evidence (e.g., 'EVD-IAM-001')",
            required=True
        )
        self.add_parameter(
            "source",
            "string",
            "Source of the evidence (e.g., 'IAM', 'S3', 'CloudTrail')",
            required=True
        )
        self.add_parameter(
            "collection_method",
            "string",
            "How evidence was collected: 'direct' or 'agent_request'",
            required=True
        )
        self.add_parameter(
            "collected_by",
            "string",
            "Agent name who collected this evidence",
            required=True
        )
        self.add_parameter(
            "data",
            "object",
            "The actual evidence data (configurations, logs, etc.)",
            required=True
        )
        self.add_parameter(
            "control_domain",
            "string",
            "Control domain this evidence relates to",
            required=False,
            default=None
        )
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Store evidence with proper metadata.
        
        Args:
            evidence_id: Unique evidence identifier
            source: Evidence source
            collection_method: Collection method
            collected_by: Agent name
            data: Evidence data
            control_domain: Optional control domain
        
        Returns:
            Dict with evidence details and storage path
        
        Raises:
            ToolExecutionError: If evidence storage fails
        """
        try:
            # Validate parameters
            self.validate_parameters(**kwargs)
            
            # Extract parameters
            evidence_id = kwargs["evidence_id"]
            source = kwargs["source"]
            collection_method = kwargs["collection_method"]
            collected_by = kwargs["collected_by"]
            data = kwargs["data"]
            control_domain = kwargs.get("control_domain")
            
            # Validate collection method
            if collection_method not in ["direct", "agent_request"]:
                raise ToolExecutionError(
                    f"Invalid collection_method: {collection_method}. "
                    "Must be 'direct' or 'agent_request'"
                )
            
            # Create evidence object
            collected_at = datetime.now()
            storage_path = self._get_storage_path(evidence_id)
            
            evidence = Evidence(
                evidence_id=evidence_id,
                source=source,
                collection_method=collection_method,
                collected_at=collected_at,
                collected_by=collected_by,
                data=data,
                storage_path=str(storage_path),
                control_domain=control_domain
            )
            
            # Save evidence to file
            self._save_evidence(evidence)
            
            return {
                "status": "success",
                "evidence_id": evidence_id,
                "storage_path": str(storage_path),
                "collected_at": collected_at.isoformat(),
                "message": f"Evidence {evidence_id} stored successfully"
            }
        
        except ToolExecutionError:
            raise
        except Exception as e:
            raise ToolExecutionError(f"Failed to store evidence: {str(e)}")
    
    def _get_storage_path(self, evidence_id: str) -> Path:
        """Get the storage path for an evidence file."""
        filename = evidence_id.replace(" ", "_")
        return self.output_dir / f"{filename}.json"
    
    def _save_evidence(self, evidence: Evidence) -> None:
        """
        Save evidence to JSON file.
        
        Args:
            evidence: Evidence object to save
        """
        file_path = Path(evidence.storage_path)
        
        evidence_dict = {
            "evidence_id": evidence.evidence_id,
            "source": evidence.source,
            "collection_method": evidence.collection_method,
            "collected_at": evidence.collected_at.isoformat(),
            "collected_by": evidence.collected_by,
            "control_domain": evidence.control_domain,
            "data": evidence.data
        }
        
        with open(file_path, 'w') as f:
            json.dump(evidence_dict, f, indent=2, default=str)
    
    def load_evidence(self, evidence_id: str) -> Optional[Evidence]:
        """
        Load evidence from storage.
        
        Args:
            evidence_id: Evidence identifier
        
        Returns:
            Evidence object if found, None otherwise
        """
        storage_path = self._get_storage_path(evidence_id)
        
        if not storage_path.exists():
            return None
        
        try:
            with open(storage_path, 'r') as f:
                data = json.load(f)
            
            return Evidence(
                evidence_id=data["evidence_id"],
                source=data["source"],
                collection_method=data["collection_method"],
                collected_at=datetime.fromisoformat(data["collected_at"]),
                collected_by=data["collected_by"],
                data=data["data"],
                storage_path=str(storage_path),
                control_domain=data.get("control_domain")
            )
        
        except Exception as e:
            raise ToolExecutionError(f"Failed to load evidence {evidence_id}: {str(e)}")


class TaskManagementTool(Tool):
    """
    Tool for agents to manage tasks and assignments.
    
    This tool allows agents to:
    - Read their own task list
    - Create tasks for themselves
    - Assign tasks to other agents
    - Mark tasks as complete
    """
    
    def __init__(self, tasks_dir: str = "tasks"):
        """
        Initialize the task management tool.
        
        Args:
            tasks_dir: Directory where task files are stored
        """
        super().__init__(
            name="manage_tasks",
            description="Create, read, assign, and complete tasks. Enables autonomous task delegation and tracking."
        )
        
        self.tasks_dir = Path(tasks_dir)
        self.tasks_dir.mkdir(parents=True, exist_ok=True)
        
        # Define parameters
        self.add_parameter(
            "action",
            "string",
            "Action to perform: 'read_my_tasks', 'create_task', 'assign_task', 'complete_task', 'list_all_tasks'",
            required=True
        )
        self.add_parameter(
            "agent_name",
            "string",
            "Name of the agent performing the action",
            required=True
        )
        self.add_parameter(
            "task_description",
            "string",
            "Description of the task",
            required=False
        )
        self.add_parameter(
            "assignee",
            "string",
            "Agent to assign task to (for assign_task action)",
            required=False
        )
        self.add_parameter(
            "priority",
            "string",
            "Task priority: 'high', 'medium', or 'low'",
            required=False,
            default="medium"
        )
        self.add_parameter(
            "task_index",
            "number",
            "Index of task to complete (for complete_task action)",
            required=False
        )
        self.add_parameter(
            "due_date",
            "string",
            "Due date for task (YYYY-MM-DD format)",
            required=False
        )
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute task management action.
        
        Args:
            action: Action to perform
            agent_name: Agent performing the action
            task_description: Task description (for create/assign)
            assignee: Agent to assign to (for assign)
            priority: Task priority
            task_index: Task index (for complete)
            due_date: Due date for task
        
        Returns:
            Dict with action result
        
        Raises:
            ToolExecutionError: If action fails
        """
        try:
            self.validate_parameters(**kwargs)
            
            action = kwargs["action"]
            agent_name = kwargs["agent_name"]
            
            if action == "read_my_tasks":
                return self.read_tasks(agent_name)
            
            elif action == "create_task":
                return self.create_task(
                    agent_name=agent_name,
                    task=kwargs.get("task_description", ""),
                    priority=kwargs.get("priority", "medium"),
                    due_date=kwargs.get("due_date")
                )
            
            elif action == "assign_task":
                return self.assign_task(
                    from_agent=agent_name,
                    to_agent=kwargs.get("assignee", ""),
                    task=kwargs.get("task_description", ""),
                    priority=kwargs.get("priority", "medium"),
                    due_date=kwargs.get("due_date")
                )
            
            elif action == "complete_task":
                return self.complete_task(
                    agent_name=agent_name,
                    task_index=int(kwargs.get("task_index", 0))
                )
            
            elif action == "list_all_tasks":
                return self.list_all_tasks()
            
            else:
                raise ToolExecutionError(f"Unknown action: {action}")
        
        except ToolExecutionError:
            raise
        except Exception as e:
            raise ToolExecutionError(f"Task management failed: {str(e)}")
    
    def read_tasks(self, agent_name: str) -> Dict[str, Any]:
        """Read an agent's task list."""
        task_file = self._get_task_file(agent_name)
        
        if not task_file.exists():
            # Create empty task file
            self._init_task_file(agent_name)
            return {
                "status": "success",
                "agent": agent_name,
                "tasks": "No tasks yet. Your task list has been created.",
                "current_tasks": [],
                "completed_tasks": [],
                "delegated_tasks": []
            }
        
        content = task_file.read_text()
        tasks = self._parse_task_file(content)
        
        return {
            "status": "success",
            "agent": agent_name,
            "tasks": content,
            "current_tasks": tasks["current"],
            "completed_tasks": tasks["completed"],
            "delegated_tasks": tasks["delegated"]
        }
    
    def create_task(
        self,
        agent_name: str,
        task: str,
        priority: str = "medium",
        due_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a task for the agent themselves."""
        task_file = self._get_task_file(agent_name)
        
        if not task_file.exists():
            self._init_task_file(agent_name)
        
        # Create task entry
        task_entry = self._format_task_entry(
            task=task,
            assigned_by="Self",
            priority=priority,
            due_date=due_date
        )
        
        # Append to current tasks section
        content = task_file.read_text()
        
        # Find the "## Current Tasks" section and add task
        if "## Current Tasks" in content:
            parts = content.split("## Completed Tasks")
            current_section = parts[0]
            completed_section = "## Completed Tasks" + parts[1] if len(parts) > 1 else "\n## Completed Tasks\n"
            
            updated_content = current_section + task_entry + "\n" + completed_section
        else:
            updated_content = content + "\n## Current Tasks\n" + task_entry
        
        task_file.write_text(updated_content)
        
        return {
            "status": "success",
            "message": f"Task created for {agent_name}",
            "task": task,
            "priority": priority
        }
    
    def assign_task(
        self,
        from_agent: str,
        to_agent: str,
        task: str,
        priority: str = "medium",
        due_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """Assign a task to another agent."""
        # Add to assignee's task list
        assignee_file = self._get_task_file(to_agent)
        
        if not assignee_file.exists():
            self._init_task_file(to_agent)
        
        task_entry = self._format_task_entry(
            task=task,
            assigned_by=from_agent,
            priority=priority,
            due_date=due_date
        )
        
        # Append to assignee's current tasks
        content = assignee_file.read_text()
        parts = content.split("## Completed Tasks")
        current_section = parts[0]
        completed_section = "## Completed Tasks" + parts[1] if len(parts) > 1 else "\n## Completed Tasks\n"
        
        updated_content = current_section + task_entry + "\n" + completed_section
        assignee_file.write_text(updated_content)
        
        # Add to assigner's delegated tasks
        assigner_file = self._get_task_file(from_agent)
        if not assigner_file.exists():
            self._init_task_file(from_agent)
        
        delegated_entry = f"""- [ ] {task}
  - Assigned to: {to_agent}
  - Assigned on: {datetime.now().strftime('%Y-%m-%d')}
  - Priority: {priority}
  - Status: Not Started
"""
        
        content = assigner_file.read_text()
        if "## Delegated Tasks" in content:
            parts = content.split("## Delegated Tasks")
            before = parts[0]
            after = parts[1] if len(parts) > 1 else "\n"
            updated_content = before + "## Delegated Tasks\n" + delegated_entry + after
        else:
            updated_content = content + "\n## Delegated Tasks (Waiting on Others)\n" + delegated_entry
        
        assigner_file.write_text(updated_content)
        
        return {
            "status": "success",
            "message": f"Task assigned from {from_agent} to {to_agent}",
            "task": task,
            "assignee": to_agent,
            "priority": priority
        }
    
    def complete_task(self, agent_name: str, task_index: int) -> Dict[str, Any]:
        """Mark a task as complete."""
        task_file = self._get_task_file(agent_name)
        
        if not task_file.exists():
            raise ToolExecutionError(f"No task file found for {agent_name}")
        
        content = task_file.read_text()
        lines = content.split("\n")
        
        # Find the task to complete
        task_count = 0
        task_line_idx = -1
        task_description = ""
        
        for i, line in enumerate(lines):
            if line.strip().startswith("- [ ]"):
                if task_count == task_index:
                    task_line_idx = i
                    task_description = line.strip()[6:].split("\n")[0]
                    break
                task_count += 1
        
        if task_line_idx == -1:
            raise ToolExecutionError(f"Task index {task_index} not found")
        
        # Mark as complete and move to completed section
        lines[task_line_idx] = lines[task_line_idx].replace("- [ ]", "- [x]")
        
        # Add completion date
        completion_line = f"  - Completed on: {datetime.now().strftime('%Y-%m-%d')}"
        lines.insert(task_line_idx + 1, completion_line)
        
        # Move to completed section
        task_block = []
        i = task_line_idx
        while i < len(lines) and (lines[i].startswith("- [x]") or lines[i].startswith("  ")):
            task_block.append(lines[i])
            i += 1
        
        # Remove from current location
        for _ in range(len(task_block)):
            lines.pop(task_line_idx)
        
        # Add to completed section
        completed_idx = -1
        for i, line in enumerate(lines):
            if line.strip() == "## Completed Tasks":
                completed_idx = i + 1
                break
        
        if completed_idx == -1:
            lines.append("\n## Completed Tasks")
            completed_idx = len(lines)
        
        for line in task_block:
            lines.insert(completed_idx, line)
            completed_idx += 1
        
        task_file.write_text("\n".join(lines))
        
        return {
            "status": "success",
            "message": f"Task completed by {agent_name}",
            "task": task_description
        }
    
    def list_all_tasks(self) -> Dict[str, Any]:
        """List all tasks across all agents."""
        all_tasks = {}
        
        for task_file in self.tasks_dir.glob("*-tasks.md"):
            agent_name = task_file.stem.replace("-tasks", "").title()
            content = task_file.read_text()
            tasks = self._parse_task_file(content)
            
            all_tasks[agent_name] = {
                "current": len(tasks["current"]),
                "completed": len(tasks["completed"]),
                "delegated": len(tasks["delegated"])
            }
        
        return {
            "status": "success",
            "all_tasks": all_tasks
        }
    
    def _get_task_file(self, agent_name: str) -> Path:
        """Get the task file path for an agent."""
        filename = f"{agent_name.lower()}-tasks.md"
        return self.tasks_dir / filename
    
    def _init_task_file(self, agent_name: str):
        """Initialize an empty task file for an agent."""
        task_file = self._get_task_file(agent_name)
        
        content = f"""# {agent_name.title()}'s Tasks

## Current Tasks

## Completed Tasks

## Delegated Tasks (Waiting on Others)
"""
        task_file.write_text(content)
    
    def _format_task_entry(
        self,
        task: str,
        assigned_by: str,
        priority: str,
        due_date: Optional[str] = None
    ) -> str:
        """Format a task entry."""
        entry = f"""- [ ] {task}
  - Assigned by: {assigned_by}
  - Assigned on: {datetime.now().strftime('%Y-%m-%d')}
  - Priority: {priority}
  - Status: Not Started
"""
        if due_date:
            entry += f"  - Due: {due_date}\n"
        
        return entry
    
    def _parse_task_file(self, content: str) -> Dict[str, List[str]]:
        """Parse task file content into structured data."""
        tasks = {
            "current": [],
            "completed": [],
            "delegated": []
        }
        
        current_section = None
        current_task = None
        
        for line in content.split("\n"):
            if line.strip() == "## Current Tasks":
                current_section = "current"
            elif line.strip() == "## Completed Tasks":
                current_section = "completed"
            elif line.strip().startswith("## Delegated"):
                current_section = "delegated"
            elif line.strip().startswith("- [ ]") or line.strip().startswith("- [x]"):
                if current_section:
                    current_task = line.strip()[6:]
                    tasks[current_section].append(current_task)
        
        return tasks


def create_tool_from_function(
    name: str,
    description: str,
    func: Callable,
    parameters: List[ToolParameter]
) -> Tool:
    """
    Create a Tool from a function.
    
    This is a helper function for creating simple tools from existing functions.
    
    Args:
        name: Tool name
        description: Tool description
        func: Function to execute
        parameters: List of parameter definitions
    
    Returns:
        Tool instance
    """
    class FunctionTool(Tool):
        def __init__(self):
            super().__init__(name, description)
            self._func = func
            for param in parameters:
                self._parameters.append(param)
        
        def execute(self, **kwargs) -> Dict[str, Any]:
            try:
                self.validate_parameters(**kwargs)
                result = self._func(**kwargs)
                return {
                    "status": "success",
                    "result": result
                }
            except Exception as e:
                raise ToolExecutionError(f"Function execution failed: {str(e)}")
    
    return FunctionTool()
