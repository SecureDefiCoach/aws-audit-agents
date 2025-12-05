"""
Victor Agent - Senior Auditor.

Victor is an autonomous LLM-powered Senior Auditor agent. He has access to
CloudTrail, CloudWatch, and VPC Flow Logs for evidence gathering.
Control domain assignments are made dynamically during audit planning.
"""

from typing import Optional, Callable, Any
from .audit_agent import AuditAgent
from .llm_client import LLMClient
from ..aws.cloudtrail_client import CloudTrailClient
from ..aws.vpc_client import VPCClient


class AWSQueryTool:
    """Helper class to wrap AWS query functions as tools."""
    
    def __init__(self, name: str, func: Callable, description: str):
        self.name = name
        self.func = func
        self.description = description
    
    def get_parameters(self) -> dict:
        """Get tool parameters schema."""
        return {
            "type": "object",
            "properties": {},
            "required": []
        }
    
    def execute(self, *args, **kwargs) -> Any:
        """Execute the tool."""
        return self.func(*args, **kwargs)
    
    def __call__(self, *args, **kwargs) -> Any:
        return self.func(*args, **kwargs)


class VictorAgent(AuditAgent):
    """
    Victor - Senior Auditor.
    
    Responsibilities:
    - Test assigned control domains
    - Review configurations and evidence
    - Analyze logs and data
    - Assess procedures
    - Supervise assigned staff auditors
    
    Control domain assignments are made dynamically during audit planning.
    """
    
    def __init__(
        self,
        llm_client: LLMClient,
        cloudtrail_client: Optional[CloudTrailClient] = None,
        vpc_client: Optional[VPCClient] = None,
        output_dir: str = "output",
        knowledge_path: Optional[str] = None
    ):
        """
        Initialize Victor with logging and monitoring capabilities.
        
        Args:
            llm_client: LLM client for agent reasoning
            cloudtrail_client: CloudTrail client for log analysis
            vpc_client: VPC client for flow log analysis
            output_dir: Directory for workpaper output
            knowledge_path: Path to Victor's knowledge base
        """
        # Initialize AWS clients
        self.cloudtrail_client = cloudtrail_client
        self.vpc_client = vpc_client
        
        # Create AWS query tools
        tools = self._create_aws_tools()
        
        # Initialize base agent
        super().__init__(
            name="Victor",
            role="Senior Auditor",
            llm_client=llm_client,
            tools=tools,
            knowledge_path=knowledge_path
        )
        
        self.output_dir = output_dir
    
    def _create_aws_tools(self) -> list:
        """Create AWS query tools for Victor."""
        tools = []
        
        # CloudTrail tools
        if self.cloudtrail_client:
            tools.append(
                AWSQueryTool(
                    name="query_cloudtrail",
                    func=self.cloudtrail_client.lookup_events,
                    description="Query CloudTrail events. Input should be a dict with optional keys: event_name, username, resource_name, start_time, end_time, max_results"
                )
            )
            
            tools.append(
                AWSQueryTool(
                    name="describe_trails",
                    func=self.cloudtrail_client.describe_trails,
                    description="Describe all CloudTrail trails in the account. No input required."
                )
            )
            
            tools.append(
                AWSQueryTool(
                    name="get_trail_status",
                    func=self.cloudtrail_client.get_trail_status,
                    description="Get status of a CloudTrail trail. Input should be the trail name or ARN."
                )
            )
        
        # VPC Flow Logs tools
        if self.vpc_client:
            tools.append(
                AWSQueryTool(
                    name="describe_flow_logs",
                    func=self.vpc_client.describe_flow_logs,
                    description="Describe all VPC Flow Logs. No input required."
                )
            )
            
            tools.append(
                AWSQueryTool(
                    name="describe_vpcs",
                    func=self.vpc_client.describe_vpcs,
                    description="Describe all VPCs in the account. No input required."
                )
            )
        
        return tools
    
    def create_workpaper(self, control_id: str, findings: dict) -> dict:
        """
        Create a workpaper for logging control testing.
        
        Args:
            control_id: ISACA control identifier
            findings: Test results and findings
        
        Returns:
            Workpaper metadata
        """
        workpaper = {
            "auditor": "Victor",
            "role": "Senior Auditor - Logging & Monitoring",
            "control_id": control_id,
            "findings": findings,
            "status": "draft"
        }
        
        return workpaper
    
    def analyze_cloudtrail_coverage(self) -> dict:
        """
        Analyze CloudTrail coverage across the AWS account.
        
        Returns:
            Analysis results
        """
        if not self.cloudtrail_client:
            return {"error": "CloudTrail client not available"}
        
        trails = self.cloudtrail_client.describe_trails()
        
        analysis = {
            "total_trails": len(trails),
            "trails": [],
            "issues": []
        }
        
        for trail in trails:
            trail_status = self.cloudtrail_client.get_trail_status(trail['TrailARN'])
            
            trail_info = {
                "name": trail.get('Name'),
                "arn": trail.get('TrailARN'),
                "is_logging": trail_status.get('IsLogging', False),
                "multi_region": trail.get('IsMultiRegionTrail', False),
                "log_file_validation": trail.get('LogFileValidationEnabled', False)
            }
            
            analysis['trails'].append(trail_info)
            
            # Identify issues
            if not trail_info['is_logging']:
                analysis['issues'].append(f"Trail {trail_info['name']} is not actively logging")
            
            if not trail_info['multi_region']:
                analysis['issues'].append(f"Trail {trail_info['name']} is not multi-region")
            
            if not trail_info['log_file_validation']:
                analysis['issues'].append(f"Trail {trail_info['name']} does not have log file validation enabled")
        
        return analysis
    
    def analyze_vpc_flow_logs(self) -> dict:
        """
        Analyze VPC Flow Log coverage.
        
        Returns:
            Analysis results
        """
        if not self.vpc_client:
            return {"error": "VPC client not available"}
        
        vpcs = self.vpc_client.describe_vpcs()
        flow_logs = self.vpc_client.describe_flow_logs()
        
        # Map flow logs to VPCs
        vpc_flow_log_map = {}
        for flow_log in flow_logs:
            resource_id = flow_log.get('ResourceId')
            if resource_id:
                vpc_flow_log_map[resource_id] = flow_log
        
        analysis = {
            "total_vpcs": len(vpcs),
            "vpcs_with_flow_logs": 0,
            "vpcs_without_flow_logs": [],
            "flow_logs": flow_logs
        }
        
        for vpc in vpcs:
            vpc_id = vpc.get('VpcId')
            if vpc_id in vpc_flow_log_map:
                analysis['vpcs_with_flow_logs'] += 1
            else:
                analysis['vpcs_without_flow_logs'].append(vpc_id)
        
        return analysis
