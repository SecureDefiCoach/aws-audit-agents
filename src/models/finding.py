"""Audit findings and workpaper data models."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Finding:
    """Represents an audit finding."""
    finding_id: str
    control_domain: str
    control_objective: str
    test_procedure: str
    result: str  # "pass" or "fail"
    evidence_refs: List[str]
    affected_resources: List[str]
    risk_rating: str  # "high", "medium", "low"
    recommendations: List[str]
    workpaper_ref: Optional[str] = None
    created_by: str = ""  # Agent name
    created_at: Optional[datetime] = None  # Simulated
