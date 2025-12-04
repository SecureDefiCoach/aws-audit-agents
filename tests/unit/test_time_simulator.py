"""
Unit tests for TimeSimulator class.
"""

import pytest
from datetime import datetime, timedelta
from src.utils.time_simulator import TimeSimulator, AuditPhase


class TestTimeSimulator:
    """Test suite for TimeSimulator class."""
    
    def test_initialization_with_default_time(self):
        """Test TimeSimulator initializes with current time by default."""
        before = datetime.now()
        simulator = TimeSimulator()
        after = datetime.now()
        
        assert before <= simulator.real_start_time <= after
        assert simulator.real_start_time == simulator.simulated_start_time
    
    def test_initialization_with_custom_time(self):
        """Test TimeSimulator initializes with provided start time."""
        custom_time = datetime(2025, 1, 1, 0, 0, 0)
        simulator = TimeSimulator(start_time=custom_time)
        
        assert simulator.real_start_time == custom_time
        assert simulator.simulated_start_time == custom_time
    
    def test_compression_ratio(self):
        """Test that compression ratio is set correctly."""
        assert TimeSimulator.COMPRESSION_RATIO == 7
    
    def test_get_simulated_time_at_start(self):
        """Test simulated time equals start time at initialization."""
        start_time = datetime(2025, 1, 1, 0, 0, 0)
        simulator = TimeSimulator(start_time=start_time)
        
        simulated = simulator.get_simulated_time(start_time)
        assert simulated == start_time
    
    def test_get_simulated_time_one_day_later(self):
        """Test simulated time after 1 real day equals 1 week simulated."""
        start_time = datetime(2025, 1, 1, 0, 0, 0)
        simulator = TimeSimulator(start_time=start_time)
        
        one_day_later = start_time + timedelta(days=1)
        simulated = simulator.get_simulated_time(one_day_later)
        
        expected = start_time + timedelta(weeks=1)
        assert simulated == expected
    
    def test_get_simulated_time_with_hours(self):
        """Test simulated time compression with fractional days."""
        start_time = datetime(2025, 1, 1, 0, 0, 0)
        simulator = TimeSimulator(start_time=start_time)
        
        # 12 hours real time = 3.5 days simulated (12 hours * 7)
        twelve_hours_later = start_time + timedelta(hours=12)
        simulated = simulator.get_simulated_time(twelve_hours_later)
        
        expected = start_time + timedelta(hours=12 * 7)
        assert simulated == expected
    
    def test_get_simulated_time_default_current_time(self):
        """Test get_simulated_time uses current time when not specified."""
        start_time = datetime.now()
        simulator = TimeSimulator(start_time=start_time)
        
        # Small delay to ensure time has passed
        simulated = simulator.get_simulated_time()
        
        # Simulated time should be >= start time
        assert simulated >= start_time
    
    def test_get_phase_start_time_initialization(self):
        """Test phase start time for initialization phase."""
        start_time = datetime(2025, 1, 1, 0, 0, 0)
        simulator = TimeSimulator(start_time=start_time)
        
        phase_start = simulator.get_phase_start_time(AuditPhase.INITIALIZATION)
        assert phase_start == start_time
    
    def test_get_phase_start_time_company_setup(self):
        """Test phase start time for company setup phase."""
        start_time = datetime(2025, 1, 1, 0, 0, 0)
        simulator = TimeSimulator(start_time=start_time)
        
        # Company setup starts at week 0 (same as initialization)
        phase_start = simulator.get_phase_start_time(AuditPhase.COMPANY_SETUP)
        expected = start_time
        assert phase_start == expected
    
    def test_get_phase_start_time_evidence_collection(self):
        """Test phase start time for evidence collection phase."""
        start_time = datetime(2025, 1, 1, 0, 0, 0)
        simulator = TimeSimulator(start_time=start_time)
        
        # Evidence collection starts at week 1 (week 2-4 in documentation)
        phase_start = simulator.get_phase_start_time(AuditPhase.EVIDENCE_COLLECTION)
        expected = start_time + timedelta(weeks=1)
        assert phase_start == expected
    
    def test_get_phase_end_time(self):
        """Test phase end time calculation."""
        start_time = datetime(2025, 1, 1, 0, 0, 0)
        simulator = TimeSimulator(start_time=start_time)
        
        # Risk assessment is 2 weeks long, starts at week 0
        phase_end = simulator.get_phase_end_time(AuditPhase.RISK_ASSESSMENT)
        expected = start_time + timedelta(weeks=2)  # Starts at week 0, ends at week 2
        assert phase_end == expected
    
    def test_space_activities_empty(self):
        """Test spacing activities with zero activities."""
        start_time = datetime(2025, 1, 1, 0, 0, 0)
        simulator = TimeSimulator(start_time=start_time)
        
        timestamps = simulator.space_activities_in_phase(AuditPhase.INITIALIZATION, 0)
        assert timestamps == []
    
    def test_space_activities_single(self):
        """Test spacing a single activity."""
        start_time = datetime(2025, 1, 1, 0, 0, 0)
        simulator = TimeSimulator(start_time=start_time)
        
        timestamps = simulator.space_activities_in_phase(AuditPhase.INITIALIZATION, 1)
        assert len(timestamps) == 1
        assert timestamps[0] == simulator.get_phase_start_time(AuditPhase.INITIALIZATION)
    
    def test_space_activities_multiple(self):
        """Test spacing multiple activities evenly."""
        start_time = datetime(2025, 1, 1, 0, 0, 0)
        simulator = TimeSimulator(start_time=start_time)
        
        # Space 3 activities in a 1-week phase
        timestamps = simulator.space_activities_in_phase(AuditPhase.INITIALIZATION, 3)
        assert len(timestamps) == 3
        
        # First should be at start
        assert timestamps[0] == simulator.get_phase_start_time(AuditPhase.INITIALIZATION)
        
        # Last should be at end
        assert timestamps[2] == simulator.get_phase_end_time(AuditPhase.INITIALIZATION)
        
        # Middle should be halfway
        expected_middle = start_time + timedelta(days=3.5)
        assert timestamps[1] == expected_middle
    
    def test_get_realistic_activity_time(self):
        """Test getting realistic activity time."""
        start_time = datetime(2025, 1, 1, 0, 0, 0)
        simulator = TimeSimulator(start_time=start_time)
        
        # Get timestamp for 2nd activity out of 5
        timestamp = simulator.get_realistic_activity_time(
            AuditPhase.EVIDENCE_COLLECTION, 
            1,  # Second activity (0-indexed)
            5   # Total of 5 activities
        )
        
        # Should be between phase start and end
        phase_start = simulator.get_phase_start_time(AuditPhase.EVIDENCE_COLLECTION)
        phase_end = simulator.get_phase_end_time(AuditPhase.EVIDENCE_COLLECTION)
        
        assert phase_start <= timestamp <= phase_end
    
    def test_get_realistic_activity_time_out_of_range(self):
        """Test getting activity time with index out of range."""
        start_time = datetime(2025, 1, 1, 0, 0, 0)
        simulator = TimeSimulator(start_time=start_time)
        
        # Request activity beyond total
        timestamp = simulator.get_realistic_activity_time(
            AuditPhase.INITIALIZATION, 
            10,  # Way beyond total
            3    # Only 3 activities
        )
        
        # Should return phase end time
        assert timestamp == simulator.get_phase_end_time(AuditPhase.INITIALIZATION)
    
    def test_get_total_audit_duration(self):
        """Test total audit duration calculation."""
        simulator = TimeSimulator()
        
        total_duration = simulator.get_total_audit_duration()
        
        # Latest phase end: Reporting starts at week 4, lasts 2 weeks = week 6
        expected = timedelta(weeks=6)
        assert total_duration == expected
    
    def test_format_simulated_time(self):
        """Test formatting simulated time."""
        simulator = TimeSimulator()
        
        test_time = datetime(2025, 3, 15, 14, 30, 45)
        formatted = simulator.format_simulated_time(test_time)
        
        assert formatted == "2025-03-15 14:30:45"
    
    def test_audit_phase_enum_values(self):
        """Test that audit phase enum has correct start and duration values."""
        assert AuditPhase.INITIALIZATION.value == (0, 1)
        assert AuditPhase.COMPANY_SETUP.value == (0, 1)
        assert AuditPhase.RISK_ASSESSMENT.value == (0, 2)
        assert AuditPhase.AUDIT_PLANNING.value == (1, 1)
        assert AuditPhase.EVIDENCE_COLLECTION.value == (1, 3)
        assert AuditPhase.TESTING_EVALUATION.value == (2, 3)
        assert AuditPhase.REPORTING.value == (4, 2)
        assert AuditPhase.CLEANUP.value == (6, 0)
