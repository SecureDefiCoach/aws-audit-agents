"""
Chuck Agent - CloudRetail IT Manager (Evidence Provider)

Chuck represents the company being audited (CloudRetail Inc). He provides
evidence and answers questions from auditors. Unlike auditors, Chuck has
full access to the AWS environment to retrieve any requested information.
"""

from typing import Optional, Dict, Any
from pathlib import Path

from .audit_agent import AuditAgent
from .llm_client import LLMClient
from .tools import WorkpaperTool, EvidenceTool
from ..aws.iam_client import IAMClient
from ..aws.s3_client import S3Client
from ..aws.ec2_client import EC2Client
from ..aws.vpc_client import VPCClient
from ..aws.cloudtrail_client import CloudTrailClient


class ChuckAgent(AuditAgent):
    """
    Chuck - CloudRetail IT Manager
    
    Role: Company representative who provides evidence to auditors
    
    Responsibilities:
    - Answer questions from auditors about AWS configurations
    - Provide requested evidence and documentation
    - Explain company's AWS setup and security controls
    - Coordinate evidence collection with audit team
    
    AWS Access: Full read access to all AWS services (company employee)
    """
    
    def __init__(
        self,
        llm_client: LLMClient,
        iam_client: Optional[IAMClient] = None,
        s3_client: Optional[S3Client] = None,
        ec2_client: Optional[EC2Client] = None,
        vpc_client: Optional[VPCClient] = None,
        cloudtrail_client: Optional[CloudTrailClient] = None,
        output_dir: str = "output",
        knowledge_path: Optional[str] = None
    ):
        """
        Initialize Chuck agent.
        
        Args:
            llm_client: LLM client for reasoning
            iam_client: IAM client for identity and access queries
            s3_client: S3 client for storage queries
            ec2_client: EC2 client for compute queries
            vpc_client: VPC client for network queries
            cloudtrail_client: CloudTrail client for audit log queries
            output_dir: Directory for output files
            knowledge_path: Path to Chuck's knowledge folder
        """
        # Initialize base agent
        # Chuck only provides evidence, he doesn't create workpapers (he's not an auditor)
        super().__init__(
            name="Chuck",
            role="CloudRetail IT Manager - Evidence Provider",
            llm_client=llm_client,
            tools=[EvidenceTool()],  # Only evidence tool, no workpaper creation
            knowledge_path=knowledge_path
        )
        
        # AWS clients (full access as company employee)
        self.iam_client = iam_client or IAMClient(read_only=True)
        self.s3_client = s3_client or S3Client(read_only=True)
        self.ec2_client = ec2_client or EC2Client(read_only=True)
        self.vpc_client = vpc_client or VPCClient(read_only=True)
        self.cloudtrail_client = cloudtrail_client or CloudTrailClient(read_only=True)
        
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Register AWS query tools
        self._register_aws_tools()
        
        # Re-initialize system message with Chuck's custom prompt
        self.memory = []
        self._init_system_message()
        
        print(f"✓ {self.name} initialized with full AWS access")
        print(f"  Role: {self.role}")
        print(f"  AWS Services: IAM, S3, EC2, VPC, CloudTrail")
    
    def _init_system_message(self):
        """Initialize Chuck's custom system message with audit manager defined capabilities."""
        system_msg = """You are Chuck, the IT Manager for CloudRetail Inc. This agent acts as the organization's virtual IT Manager, representing the company during audits, maintaining awareness of the full computing environment, and ensuring clear, accurate communication with auditors and internal stakeholders.

## Core Capabilities

### 1. Deep Understanding of IT Operations
- Maintains a comprehensive view of the company's systems, infrastructure, applications, network topology, and security tools.
- Understands how services are deployed and configured across AWS.
- Tracks ongoing IT initiatives, system changes, and operational risks.

### 2. Evidence Collection & Technical Analysis
- Uses approved tools to collect logs, screenshots, AWS configuration data, and other required audit evidence.
- Performs preliminary analysis of AWS infrastructure (IAM, S3, EC2, VPC, CloudTrail, Config, etc.) to assess control design and compliance readiness.
- Flags anomalies, potential weaknesses, or deviations from security baselines.

### 3. Clear & Effective Communication
- Communicates technical details in a structured, easy-to-understand manner for auditors and management.
- Serves as a consistent advocate for secure operations and control integrity.
- Documents questions, requirements, and next steps with precision.

### 4. Support for Management & Compliance Activities
- Helps leadership understand audit requirements, timelines, and expectations.
- Ensures IT operations remain aligned with security frameworks and organizational policies.
- Coordinates evidence preparation and remediation activities.

### 5. Auditor Engagement & Responsiveness
- Answers auditor questions directly when the information is available.
- When unable to provide an answer immediately, records the question, identifies dependencies, and commits to delivering a complete response promptly.
- Maintains a professional, cooperative, and solutions-oriented presence throughout the audit.

### 6. Internal Coordination & SME Routing
- Knows the internal personnel across engineering, DevOps, security, and operations.
- Connects auditors to the correct subject matter experts when deeper technical detail or walkthroughs are required.
- Tracks all auditor–SME interactions to ensure follow-through and consistency.

### 7. Primary Communication Channels
- Communicates primarily with Maurice and Esther on audit and compliance matters.
- Ensures they remain informed of risks, evidence status, auditor requests, and any emerging challenges.

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

When you need to provide information or answer a question, respond with:
{
    "action": "document",
    "content": "Your response or information",
    "reasoning": "Your thought process"
}

When you need to send a message to another agent (Maurice or Esther), respond with:
{
    "action": "send_message",
    "to": "agent_name",
    "message": "Your message content"
}

Always explain your reasoning. Be thorough, accurate, and professional in all communications.
"""
        self.memory.append({"role": "system", "content": system_msg})
    
    def load_knowledge(self, path: str):
        """
        Load knowledge for Chuck (company representative).
        Chuck does NOT load shared audit procedures - he's not an auditor.
        He only loads company-specific knowledge.
        """
        knowledge_dir = Path(path)
        if not knowledge_dir.exists():
            return
        
        for file in knowledge_dir.glob("*.md"):
            procedure_name = file.stem
            procedure_content = file.read_text()
            self.knowledge[procedure_name] = procedure_content
            print(f"📚 {self.name}: Loaded knowledge '{procedure_name}'")
    
    def _register_aws_tools(self):
        """Register AWS query tools for evidence collection."""
        from .tools import ToolParameter
        
        # Create a concrete tool class for AWS queries
        class AWSQueryTool(object):
            def __init__(self, name, description, execute_fn):
                self.name = name
                self.description = description
                self._execute_fn = execute_fn
                self._parameters = []
            
            def add_parameter(self, name, param_type, description, required=True):
                param = ToolParameter(name, param_type, description, required)
                self._parameters.append(param)
            
            def execute(self, **kwargs):
                return self._execute_fn(**kwargs)
            
            def get_parameters(self):
                properties = {}
                required = []
                for param in self._parameters:
                    properties[param.name] = {
                        "type": param.type,
                        "description": param.description
                    }
                    if param.required:
                        required.append(param.name)
                return {
                    "type": "object",
                    "properties": properties,
                    "required": required
                }
        
        # IAM Tools
        iam_tool = AWSQueryTool("query_iam", "Query IAM for users, roles, policies, and access configurations", self._execute_iam_query)
        iam_tool.add_parameter("query_type", "string", "Type of IAM query: list_users, list_roles, get_user, get_role, list_policies, get_credential_report, get_account_summary", True)
        iam_tool.add_parameter("resource_name", "string", "Name of specific resource (for get_user, get_role queries)", False)
        self.register_tool(iam_tool)
        
        # S3 Tools
        s3_tool = AWSQueryTool("query_s3", "Query S3 for buckets, encryption settings, and access configurations", self._execute_s3_query)
        s3_tool.add_parameter("query_type", "string", "Type of S3 query: list_buckets, get_bucket_encryption, get_bucket_policy, get_bucket_acl", True)
        s3_tool.add_parameter("bucket_name", "string", "Name of specific bucket (for bucket-specific queries)", False)
        self.register_tool(s3_tool)
        
        # EC2 Tools
        ec2_tool = AWSQueryTool("query_ec2", "Query EC2 for instances, security groups, and compute configurations", self._execute_ec2_query)
        ec2_tool.add_parameter("query_type", "string", "Type of EC2 query: list_instances, list_security_groups, get_instance, get_security_group", True)
        ec2_tool.add_parameter("resource_id", "string", "ID of specific resource (for get queries)", False)
        self.register_tool(ec2_tool)
        
        # VPC Tools
        vpc_tool = AWSQueryTool("query_vpc", "Query VPC for network configurations, subnets, and routing", self._execute_vpc_query)
        vpc_tool.add_parameter("query_type", "string", "Type of VPC query: list_vpcs, list_subnets, list_route_tables, get_flow_logs", True)
        vpc_tool.add_parameter("vpc_id", "string", "ID of specific VPC (for VPC-specific queries)", False)
        self.register_tool(vpc_tool)
        
        # CloudTrail Tools
        cloudtrail_tool = AWSQueryTool("query_cloudtrail", "Query CloudTrail for audit logs and trail configurations", self._execute_cloudtrail_query)
        cloudtrail_tool.add_parameter("query_type", "string", "Type of CloudTrail query: list_trails, get_trail_status, lookup_events", True)
        cloudtrail_tool.add_parameter("trail_name", "string", "Name of specific trail (for trail-specific queries)", False)
        cloudtrail_tool.add_parameter("event_name", "string", "Event name to lookup (for lookup_events)", False)
        self.register_tool(cloudtrail_tool)
    
    def _execute_iam_query(self, query_type: str, resource_name: Optional[str] = None) -> Dict[str, Any]:
        """Execute IAM query."""
        try:
            if query_type == "list_users":
                return {"users": self.iam_client.list_users()}
            elif query_type == "list_roles":
                return {"roles": self.iam_client.list_roles()}
            elif query_type == "get_user" and resource_name:
                return {"user": self.iam_client.get_user(resource_name)}
            elif query_type == "get_role" and resource_name:
                return {"role": self.iam_client.get_role(resource_name)}
            elif query_type == "get_credential_report":
                return {"report": self.iam_client.get_credential_report()}
            elif query_type == "get_account_summary":
                return {"summary": self.iam_client.get_account_summary()}
            else:
                return {"error": f"Unknown IAM query type: {query_type}"}
        except Exception as e:
            return {"error": str(e)}
    
    def _execute_s3_query(self, query_type: str, bucket_name: Optional[str] = None) -> Dict[str, Any]:
        """Execute S3 query."""
        try:
            if query_type == "list_buckets":
                return {"buckets": self.s3_client.list_buckets()}
            elif query_type == "get_bucket_encryption" and bucket_name:
                return {"encryption": self.s3_client.get_bucket_encryption(bucket_name)}
            elif query_type == "get_bucket_policy" and bucket_name:
                return {"policy": self.s3_client.get_bucket_policy(bucket_name)}
            elif query_type == "get_bucket_acl" and bucket_name:
                return {"acl": self.s3_client.get_bucket_acl(bucket_name)}
            else:
                return {"error": f"Unknown S3 query type: {query_type}"}
        except Exception as e:
            return {"error": str(e)}
    
    def _execute_ec2_query(self, query_type: str, resource_id: Optional[str] = None) -> Dict[str, Any]:
        """Execute EC2 query."""
        try:
            if query_type == "list_instances":
                return {"instances": self.ec2_client.list_instances()}
            elif query_type == "list_security_groups":
                return {"security_groups": self.ec2_client.list_security_groups()}
            elif query_type == "get_instance" and resource_id:
                return {"instance": self.ec2_client.get_instance(resource_id)}
            elif query_type == "get_security_group" and resource_id:
                return {"security_group": self.ec2_client.get_security_group(resource_id)}
            else:
                return {"error": f"Unknown EC2 query type: {query_type}"}
        except Exception as e:
            return {"error": str(e)}
    
    def _execute_vpc_query(self, query_type: str, vpc_id: Optional[str] = None) -> Dict[str, Any]:
        """Execute VPC query."""
        try:
            if query_type == "list_vpcs":
                return {"vpcs": self.vpc_client.list_vpcs()}
            elif query_type == "list_subnets":
                return {"subnets": self.vpc_client.list_subnets(vpc_id)}
            elif query_type == "list_route_tables":
                return {"route_tables": self.vpc_client.list_route_tables(vpc_id)}
            elif query_type == "get_flow_logs":
                return {"flow_logs": self.vpc_client.get_flow_logs(vpc_id)}
            else:
                return {"error": f"Unknown VPC query type: {query_type}"}
        except Exception as e:
            return {"error": str(e)}
    
    def _execute_cloudtrail_query(
        self,
        query_type: str,
        trail_name: Optional[str] = None,
        event_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Execute CloudTrail query."""
        try:
            if query_type == "list_trails":
                return {"trails": self.cloudtrail_client.list_trails()}
            elif query_type == "get_trail_status" and trail_name:
                return {"status": self.cloudtrail_client.get_trail_status(trail_name)}
            elif query_type == "lookup_events":
                return {"events": self.cloudtrail_client.lookup_events(event_name)}
            else:
                return {"error": f"Unknown CloudTrail query type: {query_type}"}
        except Exception as e:
            return {"error": str(e)}
    
    def create_workpaper(self) -> Dict[str, Any]:
        """
        Chuck doesn't create workpapers (he's not an auditor).
        He provides evidence to auditors.
        """
        return {
            "error": "Chuck is a company representative, not an auditor. He provides evidence but doesn't create workpapers."
        }
