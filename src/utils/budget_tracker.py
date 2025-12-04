"""Budget tracking utility for audit execution."""
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime


@dataclass
class BudgetEntry:
    """Represents a single budget tracking entry."""
    control_domain: str
    agent_id: str
    hours: float
    timestamp: datetime  # Simulated
    activity_description: str


@dataclass
class DomainBudgetStatus:
    """Budget status for a single control domain."""
    control_domain: str
    budgeted_hours: float
    actual_hours: float
    variance_hours: float
    variance_percentage: float
    entries: List[BudgetEntry] = field(default_factory=list)


@dataclass
class BudgetVarianceReport:
    """Complete budget variance report."""
    total_budgeted: float
    total_actual: float
    total_variance_hours: float
    total_variance_percentage: float
    by_domain: Dict[str, DomainBudgetStatus]
    generated_at: datetime


class BudgetTracker:
    """Tracks actual hours spent against budgeted hours by control domain."""
    
    def __init__(self, budgeted_hours_by_domain: Dict[str, float]):
        """
        Initialize the budget tracker.
        
        Args:
            budgeted_hours_by_domain: Dictionary mapping control domain to budgeted hours
        """
        self.budgeted_hours = budgeted_hours_by_domain.copy()
        self.actual_hours: Dict[str, float] = {domain: 0.0 for domain in budgeted_hours_by_domain}
        self.entries: List[BudgetEntry] = []
    
    def track_hours(
        self,
        control_domain: str,
        agent_id: str,
        hours: float,
        timestamp: datetime,
        activity_description: str = ""
    ) -> None:
        """
        Track hours spent on a control domain.
        
        Args:
            control_domain: The control domain being worked on
            agent_id: Identifier of the agent performing the work
            hours: Number of hours spent
            timestamp: Simulated timestamp of the activity
            activity_description: Description of the activity performed
        
        Raises:
            ValueError: If control_domain is not in the budget or hours is negative
        """
        if control_domain not in self.budgeted_hours:
            raise ValueError(f"Control domain '{control_domain}' not found in budget")
        
        if hours < 0:
            raise ValueError(f"Hours must be non-negative, got {hours}")
        
        # Create entry
        entry = BudgetEntry(
            control_domain=control_domain,
            agent_id=agent_id,
            hours=hours,
            timestamp=timestamp,
            activity_description=activity_description
        )
        
        # Add to entries list
        self.entries.append(entry)
        
        # Update actual hours
        self.actual_hours[control_domain] += hours
    
    def get_variance(self, control_domain: Optional[str] = None) -> BudgetVarianceReport:
        """
        Calculate budget variance for all domains or a specific domain.
        
        Args:
            control_domain: Optional specific domain to get variance for.
                          If None, returns variance for all domains.
        
        Returns:
            BudgetVarianceReport containing variance information
        
        Raises:
            ValueError: If specified control_domain is not in the budget
        """
        if control_domain is not None and control_domain not in self.budgeted_hours:
            raise ValueError(f"Control domain '{control_domain}' not found in budget")
        
        # Determine which domains to include
        domains_to_report = [control_domain] if control_domain else list(self.budgeted_hours.keys())
        
        # Calculate variance by domain
        by_domain: Dict[str, DomainBudgetStatus] = {}
        
        for domain in domains_to_report:
            budgeted = self.budgeted_hours[domain]
            actual = self.actual_hours[domain]
            variance_hours = actual - budgeted
            
            # Calculate percentage variance (avoid division by zero)
            if budgeted > 0:
                variance_percentage = (variance_hours / budgeted) * 100
            else:
                # If budgeted is 0 but actual > 0, that's infinite variance
                variance_percentage = float('inf') if actual > 0 else 0.0
            
            # Get entries for this domain
            domain_entries = [e for e in self.entries if e.control_domain == domain]
            
            by_domain[domain] = DomainBudgetStatus(
                control_domain=domain,
                budgeted_hours=budgeted,
                actual_hours=actual,
                variance_hours=variance_hours,
                variance_percentage=variance_percentage,
                entries=domain_entries
            )
        
        # Calculate totals
        total_budgeted = sum(self.budgeted_hours[d] for d in domains_to_report)
        total_actual = sum(self.actual_hours[d] for d in domains_to_report)
        total_variance_hours = total_actual - total_budgeted
        
        if total_budgeted > 0:
            total_variance_percentage = (total_variance_hours / total_budgeted) * 100
        else:
            total_variance_percentage = float('inf') if total_actual > 0 else 0.0
        
        return BudgetVarianceReport(
            total_budgeted=total_budgeted,
            total_actual=total_actual,
            total_variance_hours=total_variance_hours,
            total_variance_percentage=total_variance_percentage,
            by_domain=by_domain,
            generated_at=datetime.now()
        )
    
    def get_domain_status(self, control_domain: str) -> DomainBudgetStatus:
        """
        Get budget status for a specific control domain.
        
        Args:
            control_domain: The control domain to get status for
        
        Returns:
            DomainBudgetStatus for the specified domain
        
        Raises:
            ValueError: If control_domain is not in the budget
        """
        if control_domain not in self.budgeted_hours:
            raise ValueError(f"Control domain '{control_domain}' not found in budget")
        
        variance_report = self.get_variance(control_domain)
        return variance_report.by_domain[control_domain]
    
    def get_all_entries(self, control_domain: Optional[str] = None) -> List[BudgetEntry]:
        """
        Get all budget entries, optionally filtered by control domain.
        
        Args:
            control_domain: Optional domain to filter by
        
        Returns:
            List of BudgetEntry objects
        """
        if control_domain is None:
            return self.entries.copy()
        
        return [e for e in self.entries if e.control_domain == control_domain]
