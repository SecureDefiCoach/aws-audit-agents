"""Audit trail data models."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional


@dataclass
class AuditTrailEntry:
    """Single entry in the audit trail."""
    timestamp: datetime  # Simulated
    agent_id: str
    action_type: str
    action_description: str
    decision_rationale: Optional[str] = None
    evidence_refs: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
