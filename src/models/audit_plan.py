"""Audit planning data models."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional


@dataclass
class AuditPhase:
    """Represents a phase in the audit timeline."""
    phase_name: str
    start_date: datetime  # Simulated
    end_date: datetime  # Simulated
    activities: List[str] = field(default_factory=list)


@dataclass
class Milestone:
    """Represents a milestone in the audit."""
    milestone_name: str
    target_date: datetime  # Simulated
    description: str
    completed: bool = False


@dataclass
class ExecutionSchedule:
    """Timeline for audit execution."""
    start_date: datetime  # Simulated
    end_date: datetime  # Simulated
    phases: List[AuditPhase]
    milestones: List[Milestone]


@dataclass
class BudgetAllocation:
    """Budget allocation for the audit."""
    total_hours: float
    by_domain: Dict[str, float]  # control_domain -> hours
    by_phase: Dict[str, float]  # phase_name -> hours


@dataclass
class TestProcedure:
    """Represents a testing procedure to be executed."""
    procedure_id: str
    control_domain: str
    control_objective: str
    procedure_description: str
    evidence_required: List[str]
    assigned_to: str  # Agent name
    estimated_hours: float


@dataclass
class AuditPlan:
    """Complete audit plan."""
    timeline: ExecutionSchedule
    budget: BudgetAllocation
    procedures: List[TestProcedure]
    resource_allocation: Dict[str, float]  # domain -> hours
    approved: bool = False
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    review_comments: Optional[str] = None
