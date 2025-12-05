"""
Esther - Senior Auditor.

Esther is an autonomous LLM-powered Senior Auditor agent. She assesses risks,
collects evidence, and documents findings in professional workpapers.
Control domain assignments are made dynamically during audit planning.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime

from .audit_agent import AuditAgent
from .llm_client import LLMClient
from .tools import Tool, WorkpaperTool, EvidenceTool, ToolExecutionError
from ..aws.iam_client import IAMClient


class IAMTool(Tool):
    """
    Tool for querying AWS IAM service.
    
    This tool wraps the IAMClient and provides it as a tool that
    Esther can use to collect IAM evidence.
    """
    
    def __init__(self, iam_client: IAMClient):
        """
        Initialize IAM tool.
        
        Args:
            iam_client: IAM client instance
        """
        super().__init__(
            name="query_iam",
            description="Query AWS IAM service to collect evidence about users, roles, policies, and access controls"
        )
        
        self.iam_client = iam_client
        
        # Define parameters
        self.add_parameter(
            "operation",
            "string",
            "IAM operation to perform: 'list_users', 'list_roles', 'get_user', 'get_role', "
            "'list_user_policies', 'list_attached_user_policies', 'list_access_keys', "
            "'list_mfa_devices', 'get_account_summary', 'get_credential_report'",
            required=True
        )
        self.add_parameter(
            "user_name",
            "string",
            "User name (required for user-specific operations)",
            required=False,
            default=None
        )
        self.add_parameter(
            "role_name",
            "string",
            "Role name (required for role-specific operations)",
            required=False,
            default=None
        )
        self.add_parameter(
            "policy_name",
            "string",
            "Policy name (required for policy-specific operations)",
            required=False,
            default=None
        )
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute an IAM query operation.
        
        Args:
            operation: IAM operation to perform
            user_name: Optional user name
            role_name: Optional role name
            policy_name: Optional policy name
        
        Returns:
            Dict with operation results
        
        Raises:
            ToolExecutionError: If operation fails
        """
        try:
            self.validate_parameters(**kwargs)
            
            operation = kwargs["operation"]
            user_name = kwargs.get("user_name")
            role_name = kwargs.get("role_name")
            policy_name = kwargs.get("policy_name")
            
            # Execute the requested operation
            if operation == "list_users":
                result = self.iam_client.list_users()
            
            elif operation == "list_roles":
                result = self.iam_client.list_roles()
            
            elif operation == "get_user":
                if not user_name:
                    raise ToolExecutionError("user_name required for get_user operation")
                result = self.iam_client.get_user(user_name)
            
            elif operation == "get_role":
                if not role_name:
                    raise ToolExecutionError("role_name required for get_role operation")
                result = self.iam_client.get_role(role_name)
            
            elif operation == "list_user_policies":
                if not user_name:
                    raise ToolExecutionError("user_name required for list_user_policies operation")
                result = self.iam_client.list_user_policies(user_name)
            
            elif operation == "list_attached_user_policies":
                if not user_name:
                    raise ToolExecutionError("user_name required for list_attached_user_policies operation")
                result = self.iam_client.list_attached_user_policies(user_name)
            
            elif operation == "list_access_keys":
                if not user_name:
                    raise ToolExecutionError("user_name required for list_access_keys operation")
                result = self.iam_client.list_access_keys(user_name)
            
            elif operation == "list_mfa_devices":
                if not user_name:
                    raise ToolExecutionError("user_name required for list_mfa_devices operation")
                result = self.iam_client.list_mfa_devices(user_name)
            
            elif operation == "get_account_summary":
                result = self.iam_client.get_account_summary()
            
            elif operation == "get_credential_report":
                result = self.iam_client.get_credential_report()
                # Convert bytes to string if present
                if result:
                    result = result.decode('utf-8') if isinstance(result, bytes) else result
            
            else:
                raise ToolExecutionError(f"Unknown IAM operation: {operation}")
            
            return {
                "status": "success",
                "operation": operation,
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
        
        except ToolExecutionError:
            raise
        except Exception as e:
            raise ToolExecutionError(f"IAM operation failed: {str(e)}")


class EstherAgent(AuditAgent):
    """
    Esther - Senior Auditor.
    
    Esther is an autonomous agent who:
    - Assesses risks for AWS accounts
    - Collects evidence based on assigned controls
    - Analyzes controls and identifies weaknesses
    - Documents findings in professional workpapers
    - Adapts her approach based on what she discovers
    
    Control domain assignments are made dynamically during audit planning.
    """
    
    def __init__(
        self,
        llm_client: LLMClient,
        iam_client: Optional[IAMClient] = None,
        output_dir: str = "output",
        knowledge_path: Optional[str] = None
    ):
        """
        Initialize Esther.
        
        Args:
            llm_client: LLM client for reasoning
            iam_client: Optional IAM client (creates default if not provided)
            output_dir: Directory for workpapers and evidence
            knowledge_path: Path to Esther's knowledge folder
        """
        # Initialize base agent
        super().__init__(
            name="Esther",
            role="Senior Auditor",
            llm_client=llm_client,
            tools=[],
            knowledge_path=knowledge_path
        )
        
        # Set up IAM client
        if iam_client is None:
            iam_client = IAMClient(read_only=True)
        self.iam_client = iam_client
        
        # Register tools
        self.register_tool(IAMTool(iam_client))
        self.register_tool(WorkpaperTool(f"{output_dir}/workpapers"))
        self.register_tool(EvidenceTool(f"{output_dir}/evidence"))
        
        # Control domains and staff assignments are made dynamically
        self.control_domains = []  # Assigned during audit planning
        self.staff_auditor = None  # Assigned during audit planning
        
        # Workpaper tracking
        self.workpapers_created: List[str] = []
        self.evidence_collected: List[str] = []
        
        # Re-initialize system message with Esther's custom prompt
        self.memory = []
        self._init_system_message()
    
    def _init_system_message(self):
        """Initialize Esther's custom system message with audit manager defined capabilities."""
        import json
        
        system_msg = """You are Esther, an autonomous audit agent specializing in IAM and Logical Access. You independently reason about audit objectives, evaluate identity and access management controls, and produce professional audit documentation. You collaborate with other agents when necessary to complete audit procedures efficiently and accurately.

## Core Capabilities

### 1. Independent Audit Reasoning
- Understand audit objectives for IAM, provisioning, deprovisioning, role-based access, MFA, privileged access, and periodic access reviews.
- Determine the correct next step based on evidence, risk, and findings.
- Adjust your approach when new information changes the control evaluation.

### 2. Evidence Collection & AWS Access Analysis
Use inspection tools to analyze AWS IAM, including:
- Users, roles, policies, permissions, access keys
- MFA enforcement
- Password and key rotation settings
- Privileged access patterns
- CloudTrail logs relevant to authentication and authorization

Collect screenshots, configuration outputs, and logs as required evidence.
Identify gaps, misconfigurations, or control breakdowns.

### 3. Professional Documentation
Produce clear audit workpapers documenting:
- Procedures performed
- Evidence collected
- Reasoning and conclusions
- Exceptions or control weaknesses

Maintain a structured audit trail for every decision.
Write in a professional, concise format suitable for external review.

### 4. Collaboration With Other Agents
- Coordinate with the IT Manager Agent, AWS Evidence Collector Agent, and the Lead Auditor Agent when additional context or assistance is needed.
- Request clarification or follow-up information from other agents when evidence is incomplete.
- Communicate findings or risks that impact other audit domains.

## Available Tools
"""
        # Add tools dynamically
        system_msg += self._format_tools_for_prompt()
        
        # Add knowledge context
        system_msg += "\n\n" + self.get_knowledge_context()
        
        # Add required JSON response format instructions
        system_msg += """

## Response Format

When you decide to use a tool, respond with a JSON object:
{
    "action": "use_tool",
    "tool": "tool_name",
    "parameters": {"param1": "value1", "param2": "value2"},
    "reasoning": "Why you're using this tool"
}

When you've completed your goal, respond with:
{
    "action": "goal_complete",
    "summary": "What you accomplished",
    "next_steps": "Any recommendations or follow-up needed"
}

When you need to document findings, respond with:
{
    "action": "document",
    "content": "Your findings and analysis",
    "reasoning": "Your thought process"
}

Always explain your reasoning. Your thought process is as important as your actions.

When following procedures from your knowledge base, reference which procedure you're using in your reasoning.
"""
        self.memory.append({"role": "system", "content": system_msg})
    
    def create_workpaper(
        self,
        reference_number: str,
        control_objective: str,
        testing_procedures: List[str],
        evidence_ids: List[str],
        analysis: str,
        conclusion: str,
        cross_references: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create a workpaper documenting IAM audit findings.
        
        Args:
            reference_number: Workpaper reference (e.g., 'WP-IAM-001')
            control_objective: Control objective being evaluated
            testing_procedures: List of procedures performed
            evidence_ids: List of evidence IDs referenced
            analysis: Detailed analysis
            conclusion: Conclusion about control effectiveness
            cross_references: Optional related workpapers
        
        Returns:
            Dict with workpaper creation result
        """
        workpaper_tool = self.tools.get("create_workpaper")
        
        if not workpaper_tool:
            raise ValueError("WorkpaperTool not registered")
        
        result = workpaper_tool.execute(
            reference_number=reference_number,
            control_domain="IAM",
            control_objective=control_objective,
            testing_procedures=testing_procedures,
            evidence_ids=evidence_ids,
            analysis=analysis,
            conclusion=conclusion,
            created_by=self.name,
            cross_references=cross_references or []
        )
        
        # Track workpaper
        if result.get("status") == "success":
            self.workpapers_created.append(reference_number)
        
        return result
    
    def assess_iam_risks(self, company_name: str = "CloudRetail Inc") -> Dict[str, Any]:
        """
        Autonomous goal: Assess IAM risks for a company.
        
        This is a convenience method that sets the goal and runs autonomously.
        
        Args:
            company_name: Name of the company being audited
        
        Returns:
            Dict with assessment results
        """
        goal = f"Assess IAM risks and document findings for {company_name}"
        self.set_goal(goal)
        
        # Run autonomously
        result = self.run_autonomously(max_iterations=15)
        
        return {
            "goal": goal,
            "status": result["status"],
            "iterations": result["iterations"],
            "workpapers_created": self.workpapers_created,
            "evidence_collected": self.evidence_collected
        }
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of Esther's work.
        
        Returns:
            Dict with work summary
        """
        return {
            "name": self.name,
            "role": self.role,
            "current_goal": self.current_goal,
            "goal_status": self.goal_status,
            "control_domains": self.control_domains,
            "staff_auditor": self.staff_auditor,
            "workpapers_created": len(self.workpapers_created),
            "evidence_collected": len(self.evidence_collected),
            "actions_taken": len(self.action_history),
            "llm_model": self.llm.model
        }
