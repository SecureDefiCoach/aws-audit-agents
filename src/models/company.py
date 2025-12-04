"""Company-related data models."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any


@dataclass
class InformationAsset:
    """Represents a critical information asset that needs protection."""
    asset_id: str
    asset_name: str
    asset_type: str  # "S3 Bucket", "Database", "Application", "IAM User"
    location: str  # Resource identifier (bucket name, instance ID, etc.)
    data_classification: str  # "PII", "Financial", "Confidential", "Public"
    confidentiality_impact: str  # "high", "medium", "low" - impact if exposed
    integrity_impact: str  # "high", "medium", "low" - impact if modified
    availability_impact: str  # "high", "medium", "low" - impact if unavailable
    business_process: str  # "Payment Processing", "Customer Data", etc.
    description: str


@dataclass
class SecurityIssue:
    """Represents an intentional security issue in the simulated company."""
    issue_type: str  # e.g., "missing_mfa", "unencrypted_bucket"
    resource_id: str
    control_domain: str  # Maps to ISACA domain
    severity: str  # "high", "medium", "low"
    description: str


@dataclass
class InfrastructureConfig:
    """Configuration of the company's AWS infrastructure."""
    iam_users: List[Dict[str, Any]] = field(default_factory=list)
    s3_buckets: List[Dict[str, Any]] = field(default_factory=list)
    ec2_instances: List[Dict[str, Any]] = field(default_factory=list)
    vpc_config: Dict[str, Any] = field(default_factory=dict)
    cloudtrail_config: Dict[str, Any] = field(default_factory=dict)
    region: str = "us-east-1"


@dataclass
class CompanyProfile:
    """Profile of the simulated company being audited."""
    name: str
    business_type: str
    services: List[str]
    infrastructure: InfrastructureConfig
    intentional_issues: List[SecurityIssue]
    created_at: datetime
    information_assets: List[InformationAsset] = field(default_factory=list)
