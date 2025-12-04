"""Unit tests for BudgetTracker."""
import pytest
from datetime import datetime
from src.utils.budget_tracker import BudgetTracker, BudgetEntry


class TestBudgetTracker:
    """Test suite for BudgetTracker class."""
    
    def test_initialization(self):
        """Test BudgetTracker initialization."""
        budgeted = {
            "IAM": 40.0,
            "Encryption": 30.0,
            "Network": 25.0
        }
        
        tracker = BudgetTracker(budgeted)
        
        assert tracker.budgeted_hours == budgeted
        assert tracker.actual_hours == {"IAM": 0.0, "Encryption": 0.0, "Network": 0.0}
        assert tracker.entries == []
    
    def test_track_hours_basic(self):
        """Test basic hour tracking."""
        budgeted = {"IAM": 40.0}
        tracker = BudgetTracker(budgeted)
        
        timestamp = datetime(2025, 1, 15, 10, 0, 0)
        tracker.track_hours("IAM", "Esther", 5.0, timestamp, "User review")
        
        assert tracker.actual_hours["IAM"] == 5.0
        assert len(tracker.entries) == 1
        assert tracker.entries[0].control_domain == "IAM"
        assert tracker.entries[0].agent_id == "Esther"
        assert tracker.entries[0].hours == 5.0
    
    def test_track_hours_multiple_entries(self):
        """Test tracking multiple entries for same domain."""
        budgeted = {"IAM": 40.0}
        tracker = BudgetTracker(budgeted)
        
        timestamp1 = datetime(2025, 1, 15, 10, 0, 0)
        timestamp2 = datetime(2025, 1, 15, 14, 0, 0)
        
        tracker.track_hours("IAM", "Esther", 5.0, timestamp1, "User review")
        tracker.track_hours("IAM", "Hillel", 3.0, timestamp2, "Policy analysis")
        
        assert tracker.actual_hours["IAM"] == 8.0
        assert len(tracker.entries) == 2
    
    def test_track_hours_invalid_domain(self):
        """Test tracking hours for non-existent domain raises error."""
        budgeted = {"IAM": 40.0}
        tracker = BudgetTracker(budgeted)
        
        timestamp = datetime(2025, 1, 15, 10, 0, 0)
        
        with pytest.raises(ValueError, match="Control domain 'InvalidDomain' not found"):
            tracker.track_hours("InvalidDomain", "Esther", 5.0, timestamp)
    
    def test_track_hours_negative_hours(self):
        """Test tracking negative hours raises error."""
        budgeted = {"IAM": 40.0}
        tracker = BudgetTracker(budgeted)
        
        timestamp = datetime(2025, 1, 15, 10, 0, 0)
        
        with pytest.raises(ValueError, match="Hours must be non-negative"):
            tracker.track_hours("IAM", "Esther", -5.0, timestamp)
    
    def test_get_variance_single_domain_under_budget(self):
        """Test variance calculation when under budget."""
        budgeted = {"IAM": 40.0}
        tracker = BudgetTracker(budgeted)
        
        timestamp = datetime(2025, 1, 15, 10, 0, 0)
        tracker.track_hours("IAM", "Esther", 30.0, timestamp)
        
        report = tracker.get_variance("IAM")
        
        assert report.total_budgeted == 40.0
        assert report.total_actual == 30.0
        assert report.total_variance_hours == -10.0
        assert report.total_variance_percentage == -25.0
        assert "IAM" in report.by_domain
        assert report.by_domain["IAM"].variance_hours == -10.0
    
    def test_get_variance_single_domain_over_budget(self):
        """Test variance calculation when over budget."""
        budgeted = {"IAM": 40.0}
        tracker = BudgetTracker(budgeted)
        
        timestamp = datetime(2025, 1, 15, 10, 0, 0)
        tracker.track_hours("IAM", "Esther", 50.0, timestamp)
        
        report = tracker.get_variance("IAM")
        
        assert report.total_budgeted == 40.0
        assert report.total_actual == 50.0
        assert report.total_variance_hours == 10.0
        assert report.total_variance_percentage == 25.0
    
    def test_get_variance_all_domains(self):
        """Test variance calculation for all domains."""
        budgeted = {
            "IAM": 40.0,
            "Encryption": 30.0,
            "Network": 25.0
        }
        tracker = BudgetTracker(budgeted)
        
        timestamp = datetime(2025, 1, 15, 10, 0, 0)
        tracker.track_hours("IAM", "Esther", 45.0, timestamp)
        tracker.track_hours("Encryption", "Chuck", 25.0, timestamp)
        tracker.track_hours("Network", "Chuck", 30.0, timestamp)
        
        report = tracker.get_variance()
        
        assert report.total_budgeted == 95.0
        assert report.total_actual == 100.0
        assert report.total_variance_hours == 5.0
        assert abs(report.total_variance_percentage - 5.263) < 0.01
        
        assert len(report.by_domain) == 3
        assert report.by_domain["IAM"].variance_hours == 5.0
        assert report.by_domain["Encryption"].variance_hours == -5.0
        assert report.by_domain["Network"].variance_hours == 5.0
    
    def test_get_variance_zero_budget(self):
        """Test variance calculation when budget is zero."""
        budgeted = {"IAM": 0.0}
        tracker = BudgetTracker(budgeted)
        
        timestamp = datetime(2025, 1, 15, 10, 0, 0)
        tracker.track_hours("IAM", "Esther", 10.0, timestamp)
        
        report = tracker.get_variance("IAM")
        
        assert report.total_budgeted == 0.0
        assert report.total_actual == 10.0
        assert report.total_variance_percentage == float('inf')
    
    def test_get_variance_zero_budget_zero_actual(self):
        """Test variance when both budget and actual are zero."""
        budgeted = {"IAM": 0.0}
        tracker = BudgetTracker(budgeted)
        
        report = tracker.get_variance("IAM")
        
        assert report.total_budgeted == 0.0
        assert report.total_actual == 0.0
        assert report.total_variance_percentage == 0.0
    
    def test_get_variance_invalid_domain(self):
        """Test getting variance for non-existent domain raises error."""
        budgeted = {"IAM": 40.0}
        tracker = BudgetTracker(budgeted)
        
        with pytest.raises(ValueError, match="Control domain 'InvalidDomain' not found"):
            tracker.get_variance("InvalidDomain")
    
    def test_get_domain_status(self):
        """Test getting status for a specific domain."""
        budgeted = {"IAM": 40.0, "Encryption": 30.0}
        tracker = BudgetTracker(budgeted)
        
        timestamp = datetime(2025, 1, 15, 10, 0, 0)
        tracker.track_hours("IAM", "Esther", 35.0, timestamp)
        
        status = tracker.get_domain_status("IAM")
        
        assert status.control_domain == "IAM"
        assert status.budgeted_hours == 40.0
        assert status.actual_hours == 35.0
        assert status.variance_hours == -5.0
        assert len(status.entries) == 1
    
    def test_get_all_entries_no_filter(self):
        """Test getting all entries without filter."""
        budgeted = {"IAM": 40.0, "Encryption": 30.0}
        tracker = BudgetTracker(budgeted)
        
        timestamp = datetime(2025, 1, 15, 10, 0, 0)
        tracker.track_hours("IAM", "Esther", 5.0, timestamp)
        tracker.track_hours("Encryption", "Chuck", 3.0, timestamp)
        
        entries = tracker.get_all_entries()
        
        assert len(entries) == 2
        assert entries[0].control_domain == "IAM"
        assert entries[1].control_domain == "Encryption"
    
    def test_get_all_entries_with_filter(self):
        """Test getting entries filtered by domain."""
        budgeted = {"IAM": 40.0, "Encryption": 30.0}
        tracker = BudgetTracker(budgeted)
        
        timestamp = datetime(2025, 1, 15, 10, 0, 0)
        tracker.track_hours("IAM", "Esther", 5.0, timestamp)
        tracker.track_hours("Encryption", "Chuck", 3.0, timestamp)
        tracker.track_hours("IAM", "Hillel", 2.0, timestamp)
        
        entries = tracker.get_all_entries("IAM")
        
        assert len(entries) == 2
        assert all(e.control_domain == "IAM" for e in entries)
