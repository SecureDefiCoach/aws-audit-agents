"""Risk assessment data models."""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime


@dataclass
class Risk:
    """Represents a risk identified during assessment."""
    risk_id: str
    control_domain: str
    description: str
    impact: str  # "high", "medium", "low"
    likelihood: str  # "high", "medium", "low"
    risk_level: str  # "high", "medium", "low" (combined impact + likelihood)
    mitigation_controls: List[str] = field(default_factory=list)


@dataclass
class ControlDomain:
    """Represents an ISACA control domain."""
    domain_name: str
    description: str
    priority: int  # Lower number = higher priority
    risk_level: str  # "high", "medium", "low"
    control_objectives: List[str] = field(default_factory=list)


@dataclass
class RiskAssessment:
    """Complete risk assessment for the company."""
    inherent_risks: List[Risk]
    residual_risks: List[Risk]
    prioritized_domains: List[ControlDomain]
    risk_matrix: Dict[str, str]  # domain -> risk_level
    approved: bool = False
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    review_comments: Optional[str] = None
