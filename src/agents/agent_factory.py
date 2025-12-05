"""
Agent Factory - Create agents with configured LLM models.

This module provides utilities to create audit agents with different
LLM models based on configuration files.
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional

from .llm_client import LLMClient
from .audit_agent import AuditAgent
from .tools import WorkpaperTool, EvidenceTool
from .esther_agent import EstherAgent
from .chuck_agent import ChuckAgent
from .victor_agent import VictorAgent
from .maurice_agent import MauriceAgent
from .hillel_agent import HillelAgent
from .neil_agent import NeilAgent
from .juman_agent import JumanAgent
from ..aws.iam_client import IAMClient
from ..aws.s3_client import S3Client
from ..aws.ec2_client import EC2Client
from ..aws.vpc_client import VPCClient
from ..aws.cloudtrail_client import CloudTrailClient


class AgentFactory:
    """Factory for creating agents with configured LLM models."""
    
    def __init__(self, config_path: str = "config/agent_models.yaml"):
        """
        Initialize the agent factory.
        
        Args:
            config_path: Path to agent configuration YAML file
        """
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        return config
    
    def create_llm_client(self, model: str, provider: Optional[str] = None) -> LLMClient:
        """
        Create an LLM client with specified model.
        
        Args:
            model: Model name (e.g., "gpt-5", "gpt-4-turbo")
            provider: Optional provider override (uses config default if not specified)
        
        Returns:
            Configured LLMClient
        """
        provider = provider or self.config.get('provider', 'openai')
        rate_limit = self.config.get('rate_limit', 10)
        temperature = self.config.get('temperature', 0.7)
        
        return LLMClient(
            provider=provider,
            model=model,
            rate_limit=rate_limit,
            temperature=temperature
        )
    
    def create_agent(
        self,
        agent_name: str,
        tools: Optional[list] = None,
        load_knowledge: bool = True
    ) -> AuditAgent:
        """
        Create an agent from configuration.
        
        Args:
            agent_name: Agent name (e.g., "esther", "hillel")
            tools: Optional list of tools (uses default if not specified)
            load_knowledge: Whether to load agent-specific knowledge (default: True)
        
        Returns:
            Configured AuditAgent
        """
        # Get agent config
        agent_config = self.config['agents'].get(agent_name.lower())
        if not agent_config:
            raise ValueError(f"Agent '{agent_name}' not found in configuration")
        
        # Create LLM client
        model = agent_config['model']
        llm = self.create_llm_client(model)
        
        # Determine knowledge path
        knowledge_path = None
        if load_knowledge:
            knowledge_path = f"knowledge/{agent_name.lower()}"
        
        # Create specialized agents based on name
        agent_name_lower = agent_name.lower()
        
        if agent_name_lower == 'esther':
            # Create Esther with IAM capabilities
            iam_client = IAMClient(read_only=True)
            agent = EstherAgent(
                llm_client=llm,
                iam_client=iam_client,
                output_dir="output",
                knowledge_path=knowledge_path
            )
        elif agent_name_lower == 'chuck':
            # Create Chuck with full AWS access (company representative)
            iam_client = IAMClient(read_only=True)
            s3_client = S3Client(read_only=True)
            ec2_client = EC2Client(read_only=True)
            vpc_client = VPCClient(read_only=True)
            cloudtrail_client = CloudTrailClient(read_only=True)
            agent = ChuckAgent(
                llm_client=llm,
                iam_client=iam_client,
                s3_client=s3_client,
                ec2_client=ec2_client,
                vpc_client=vpc_client,
                cloudtrail_client=cloudtrail_client,
                output_dir="output",
                knowledge_path=knowledge_path
            )
        elif agent_name_lower == 'victor':
            # Create Victor with logging and monitoring capabilities
            cloudtrail_client = CloudTrailClient(read_only=True)
            vpc_client = VPCClient(read_only=True)
            agent = VictorAgent(
                llm_client=llm,
                cloudtrail_client=cloudtrail_client,
                vpc_client=vpc_client,
                output_dir="output",
                knowledge_path=knowledge_path
            )
        elif agent_name_lower == 'maurice':
            # Create Maurice as Audit Manager
            agent = MauriceAgent(
                llm_client=llm,
                output_dir="output",
                knowledge_path=knowledge_path
            )
        elif agent_name_lower == 'hillel':
            # Create Hillel as Staff Auditor for IAM Support
            agent = HillelAgent(
                llm_client=llm,
                output_dir="output",
                knowledge_path=knowledge_path
            )
        elif agent_name_lower == 'neil':
            # Create Neil as Staff Auditor for Encryption & Network Support
            agent = NeilAgent(
                llm_client=llm,
                output_dir="output",
                knowledge_path=knowledge_path
            )
        elif agent_name_lower == 'juman':
            # Create Juman as Staff Auditor for Logging Support
            agent = JumanAgent(
                llm_client=llm,
                output_dir="output",
                knowledge_path=knowledge_path
            )
        else:
            # For other agents, use generic implementation
            # Default tools if not specified
            if tools is None:
                tools = [
                    WorkpaperTool(),
                    EvidenceTool()
                ]
            
            # Create generic agent (use a concrete implementation, not abstract base)
            class ConcreteAuditAgent(AuditAgent):
                """Concrete implementation of AuditAgent for factory use."""
                def create_workpaper(self):
                    """Placeholder workpaper creation."""
                    return {"status": "workpaper_placeholder"}
            
            agent = ConcreteAuditAgent(
                name=agent_config['name'],
                role=agent_config['role'],
                llm_client=llm,
                tools=tools,
                knowledge_path=knowledge_path
            )
        
        print(f"✓ Created {agent_config['name']} ({agent_config['role']}) using {model}")
        
        return agent
    
    def create_audit_team(self) -> Dict[str, AuditAgent]:
        """
        Create the entire audit team from configuration.
        
        Returns:
            Dict mapping agent names to AuditAgent instances
        """
        team = {}
        
        print("\n" + "=" * 80)
        print("CREATING AUDIT TEAM")
        print("=" * 80)
        print()
        
        # Create agents in order: manager, seniors, staff
        agent_order = ['maurice', 'esther', 'chuck', 'victor', 'hillel', 'neil', 'juman']
        
        for agent_name in agent_order:
            if agent_name in self.config['agents']:
                agent = self.create_agent(agent_name)
                team[agent_name] = agent
        
        print()
        print("=" * 80)
        print("TEAM CREATED")
        print("=" * 80)
        print()
        
        # Show model distribution
        model_counts = {}
        for agent in team.values():
            model = agent.llm.model
            model_counts[model] = model_counts.get(model, 0) + 1
        
        print("Model Distribution:")
        for model, count in sorted(model_counts.items()):
            print(f"  {model}: {count} agents")
        print()
        
        return team
    
    def get_agent_config(self, agent_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific agent.
        
        Args:
            agent_name: Agent name
        
        Returns:
            Agent configuration dict
        """
        return self.config['agents'].get(agent_name.lower(), {})
    
    def list_agents(self) -> list:
        """
        List all configured agents.
        
        Returns:
            List of agent names
        """
        return list(self.config['agents'].keys())
    
    def print_team_summary(self):
        """Print a summary of the team configuration."""
        print("\n" + "=" * 80)
        print("AUDIT TEAM CONFIGURATION")
        print("=" * 80)
        print()
        print(f"Provider: {self.config.get('provider', 'openai')}")
        print(f"Rate Limit: {self.config.get('rate_limit', 10)} calls/minute")
        print(f"Temperature: {self.config.get('temperature', 0.7)}")
        print()
        
        # Group by role
        managers = []
        seniors = []
        staff = []
        
        for agent_name, agent_config in self.config['agents'].items():
            role = agent_config['role']
            if 'Manager' in role:
                managers.append((agent_name, agent_config))
            elif 'Senior' in role:
                seniors.append((agent_name, agent_config))
            elif 'Staff' in role:
                staff.append((agent_name, agent_config))
        
        # Print managers
        if managers:
            print("AUDIT MANAGER:")
            for name, config in managers:
                print(f"  • {config['name']} - {config['model']}")
                if 'rationale' in config:
                    print(f"    Rationale: {config['rationale']}")
            print()
        
        # Print senior auditors
        if seniors:
            print("SENIOR AUDITORS:")
            for name, config in seniors:
                print(f"  • {config['name']} - {config['model']}")
                if 'control_domains' in config:
                    print(f"    Domains: {', '.join(config['control_domains'])}")
                if 'staff_auditor' in config:
                    print(f"    Supervises: {config['staff_auditor']}")
                if 'rationale' in config:
                    print(f"    Rationale: {config['rationale']}")
                print()
        
        # Print staff auditors
        if staff:
            print("STAFF AUDITORS:")
            for name, config in staff:
                print(f"  • {config['name']} - {config['model']}")
                if 'reports_to' in config:
                    print(f"    Reports to: {config['reports_to']}")
                if 'rationale' in config:
                    print(f"    Rationale: {config['rationale']}")
                print()
        
        print("=" * 80)
        print()


def create_agent_with_model(
    name: str,
    role: str,
    model: str,
    provider: str = "openai",
    tools: Optional[list] = None
) -> AuditAgent:
    """
    Convenience function to create an agent with a specific model.
    
    Args:
        name: Agent name
        role: Agent role
        model: LLM model
        provider: LLM provider
        tools: Optional list of tools
    
    Returns:
        Configured AuditAgent
    """
    llm = LLMClient(
        provider=provider,
        model=model,
        rate_limit=10,
        temperature=0.7
    )
    
    if tools is None:
        tools = [WorkpaperTool(), EvidenceTool()]
    
    agent = AuditAgent(
        name=name,
        role=role,
        llm_client=llm,
        tools=tools
    )
    
    return agent
