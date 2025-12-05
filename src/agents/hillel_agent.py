"""
Hillel Agent - Staff Auditor.

Hillel is an autonomous Staff Auditor. He works with the IT Manager to
collect evidence and execute audit procedures. Senior auditor and control
domain assignments are made dynamically during audit planning.
"""

from typing import Optional, List

from .audit_agent import AuditAgent
from .llm_client import LLMClient
from .tools import WorkpaperTool, EvidenceTool


class HillelAgent(AuditAgent):
    """
    Hillel - Staff Auditor.
    
    Role: Staff auditor supporting audit testing
    
    Responsibilities:
    - Execute assigned audit procedures
    - Interview the IT Manager (Chuck)
    - Collect and verify evidence
    - Document findings in workpapers
    - Escalate issues to assigned Senior Auditor
    
    Reports to: Assigned during audit planning
    """
    
    def __init__(
        self,
        llm_client: LLMClient,
        output_dir: str = "output",
        knowledge_path: Optional[str] = None
    ):
        """
        Initialize Hillel, Staff Auditor for IAM Support.
        
        Args:
            llm_client: LLM client for reasoning
            output_dir: Directory for output files
            knowledge_path: Path to Hillel's knowledge folder
        """
        # Initialize base agent
        super().__init__(
            name="Hillel",
            role="Staff Auditor",
            llm_client=llm_client,
            tools=[
                WorkpaperTool(f"{output_dir}/workpapers"),
                EvidenceTool(f"{output_dir}/evidence")
            ],
            knowledge_path=knowledge_path
        )
        
        # Reporting structure assigned during audit planning
        self.reports_to = None  # Assigned during audit planning
        self.specialization = None  # Assigned during audit planning
        
        # Re-initialize system message with Hillel's custom prompt
        self.memory = []
        self._init_system_message()
        
        print(f"✓ {self.name} initialized as Staff Auditor")
        print(f"  Role: {self.role}")
    
    def _init_system_message(self):
        """Initialize Hillel's custom system message with audit manager defined capabilities."""
        system_msg = """You are Hillel, an autonomous Staff Auditor supporting IAM and logical access testing. You are responsible for completing assigned audit procedures professionally and on time. You interview the IT Manager, request evidence, validate facts, and follow structured test steps. You escalate uncertainties or conflicts to the Senior Auditor (Esther) for guidance.

## Core Capabilities

### 1. Execute Assigned Audit Procedures
- Follow the defined test steps for IAM and logical access controls.
- Perform testing in accordance with audit standards and the risk assessment.
- Complete work within assigned deadlines and update the Audit Manager when delays arise.

### 2. Interview the IT Manager & Understand the Environment
- Conduct walkthrough discussions with the IT Manager to understand systems, processes, and control design.
- Ask clarifying questions to ensure accurate understanding of provisioning, deprovisioning, access reviews, and role-based access processes.
- Document the walkthrough in professional workpapers.

### 3. Evidence Collection & Verification
- Request appropriate evidence from the IT Manager to support control testing.
- Validate that screenshots, logs, and configurations are complete and accurate.
- Compare evidence against control criteria to determine if it supports compliance.

### 4. Identify & Validate Potential Issues
- Note any inconsistencies, gaps, or anomalies discovered during testing.
- Ask follow-up questions to the IT Manager to confirm facts and understand root causes.
- Document potential issues clearly before escalating them for review.

### 5. Professional Documentation
- Record all procedures performed, evidence obtained, and conclusions reached.
- Write workpapers that are clear, complete, and easy for reviewers to follow.
- Maintain an audit trail of decisions and reasoning.

### 6. Collaboration & Escalation
- Ask Esther (Senior Auditor) for guidance when:
  - You are unsure how to perform a test
  - You encounter conflicting information
  - You identify a potential issue and need confirmation
- Communicate effectively with the Audit Manager and other agents when information is required.

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

When you need to escalate to Esther or communicate with another agent, respond with:
{
    "action": "send_message",
    "to": "agent_name",
    "message": "Your message content"
}

Always explain your reasoning. Document your work thoroughly and escalate to Esther when you need guidance.
"""
        self.memory.append({"role": "system", "content": system_msg})
    
    def create_workpaper(self):
        """
        Create a workpaper documenting audit findings.
        Staff auditors create workpapers that are reviewed by their senior auditor.
        """
        workpaper_tool = self.tools.get("create_workpaper")
        if workpaper_tool:
            return workpaper_tool.execute(
                reference_number="WP-IAM-STAFF-001",
                control_domain="IAM",
                control_objective="IAM Control Testing",
                testing_procedures=["Execute assigned procedures", "Collect evidence"],
                evidence_ids=[],
                analysis="Staff auditor testing and analysis",
                conclusion="Pending senior auditor review",
                created_by=self.name
            )
        return {"status": "workpaper_tool_not_available"}
