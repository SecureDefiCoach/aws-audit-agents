"""Evidence collection data models."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List, Optional


@dataclass
class Evidence:
    """Evidence collected during the audit."""
    evidence_id: str
    source: str  # AWS service
    collection_method: str  # "direct" or "agent_request"
    collected_at: datetime  # Simulated
    collected_by: str  # Agent ID
    data: Dict[str, Any]
    storage_path: str
    control_domain: Optional[str] = None


@dataclass
class EvidenceRequest:
    """Request for evidence from auditee agent."""
    request_id: str
    control_domain: str
    requested_items: List[str]
    requested_by: str  # Auditor agent ID
    requested_at: datetime  # Simulated
    status: str  # "pending", "fulfilled", "failed"
    fulfilled_at: Optional[datetime] = None  # Simulated
    evidence_refs: List[str] = field(default_factory=list)
