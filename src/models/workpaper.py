"""Workpaper and reporting data models."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional, Any
from .evidence import Evidence
from .finding import Finding


@dataclass
class Workpaper:
    """Audit workpaper documenting testing and findings."""
    reference_number: str  # e.g., "WP-IAM-001"
    control_domain: str
    control_objective: str
    testing_procedures: List[str]
    evidence_collected: List[Evidence]
    analysis: str
    conclusion: str
    created_by: str  # Agent ID
    created_at: datetime  # Simulated
    cross_references: List[str] = field(default_factory=list)


@dataclass
class Index:
    """Index of workpapers."""
    entries: List[Dict[str, Any]] = field(default_factory=list)
    # Each entry: {"reference": str, "domain": str, "page": int}


@dataclass
class VarianceReport:
    """Budget variance report."""
    total_budgeted: float
    total_actual: float
    variance: float
    variance_percentage: float
    by_domain: Dict[str, Dict[str, float]] = field(default_factory=dict)
    # by_domain: {domain: {"budgeted": float, "actual": float, "variance": float}}


@dataclass
class AuditReport:
    """Final audit report."""
    executive_summary: str
    scope: str
    methodology: str
    findings_by_domain: Dict[str, List[Finding]]
    overall_opinion: str
    workpaper_index: Index
    budget_variance: VarianceReport
    generated_at: datetime
    generated_by: str = "Maurice"  # Audit Manager
