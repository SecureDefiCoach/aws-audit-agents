"""
Time simulation utility for AWS Audit Agent System.

This module provides time compression functionality where 1 real day = 1 simulated week,
allowing the audit workflow to demonstrate realistic timing over a compressed timeframe.
"""

from datetime import datetime, timedelta
from typing import Optional
from enum import Enum


class AuditPhase(Enum):
    """
    Audit workflow phases with start week and duration.
    Format: (start_week, duration_weeks)
    """
    INITIALIZATION = (0, 1)      # Week 1
    COMPANY_SETUP = (0, 1)       # Week 1 (overlaps with initialization)
    RISK_ASSESSMENT = (0, 2)     # Week 1-2
    AUDIT_PLANNING = (1, 1)      # Week 2
    EVIDENCE_COLLECTION = (1, 3) # Week 2-4
    TESTING_EVALUATION = (2, 3)  # Week 3-5
    REPORTING = (4, 2)           # Week 5-6
    CLEANUP = (6, 0)             # After audit (not part of timeline)


class TimeSimulator:
    """
    Simulates audit timeline with time compression.
    
    Time compression ratio: 1 real day = 1 simulated week (7 days)
    This allows a 6-week audit to be demonstrated in approximately 6 real days.
    """
    
    # Time compression ratio: 1 real day = 7 simulated days (1 week)
    COMPRESSION_RATIO = 7
    
    def __init__(self, start_time: Optional[datetime] = None):
        """
        Initialize the time simulator.
        
        Args:
            start_time: The real-world start time. Defaults to current time.
        """
        self.real_start_time = start_time or datetime.now()
        self.simulated_start_time = self.real_start_time
        
    def get_simulated_time(self, real_time: Optional[datetime] = None) -> datetime:
        """
        Convert real time to simulated time using compression ratio.
        
        Args:
            real_time: The real-world time to convert. Defaults to current time.
            
        Returns:
            The simulated time with compression applied.
        """
        if real_time is None:
            real_time = datetime.now()
            
        # Calculate elapsed real time since start
        real_elapsed = real_time - self.real_start_time
        
        # Apply compression ratio to get simulated elapsed time
        simulated_elapsed = real_elapsed * self.COMPRESSION_RATIO
        
        # Return simulated time
        return self.simulated_start_time + simulated_elapsed
    
    def get_phase_start_time(self, phase: AuditPhase) -> datetime:
        """
        Get the simulated start time for a specific audit phase.
        
        Args:
            phase: The audit phase to get the start time for.
            
        Returns:
            The simulated start time for the phase.
        """
        # Get start week from phase value tuple
        start_week, _ = phase.value
        
        # Convert weeks to simulated time
        simulated_offset = timedelta(weeks=start_week)
        return self.simulated_start_time + simulated_offset
    
    def get_phase_end_time(self, phase: AuditPhase) -> datetime:
        """
        Get the simulated end time for a specific audit phase.
        
        Args:
            phase: The audit phase to get the end time for.
            
        Returns:
            The simulated end time for the phase.
        """
        start_time = self.get_phase_start_time(phase)
        # Get duration from phase value tuple
        _, duration_weeks = phase.value
        phase_duration = timedelta(weeks=duration_weeks)
        return start_time + phase_duration
    
    def space_activities_in_phase(
        self, 
        phase: AuditPhase, 
        num_activities: int
    ) -> list[datetime]:
        """
        Generate realistic activity timestamps spaced throughout a phase.
        
        This creates evenly distributed timestamps within a phase to simulate
        realistic work patterns (e.g., daily activities, weekly milestones).
        
        Args:
            phase: The audit phase to space activities within.
            num_activities: Number of activities to space out.
            
        Returns:
            List of simulated timestamps for activities.
        """
        if num_activities <= 0:
            return []
            
        start_time = self.get_phase_start_time(phase)
        end_time = self.get_phase_end_time(phase)
        
        # If only one activity, place it at the start
        if num_activities == 1:
            return [start_time]
        
        # Calculate spacing between activities
        total_duration = end_time - start_time
        spacing = total_duration / (num_activities - 1)
        
        # Generate timestamps
        timestamps = []
        for i in range(num_activities):
            timestamp = start_time + (spacing * i)
            timestamps.append(timestamp)
            
        return timestamps
    
    def get_realistic_activity_time(
        self, 
        phase: AuditPhase, 
        activity_index: int, 
        total_activities: int
    ) -> datetime:
        """
        Get a realistic timestamp for a specific activity within a phase.
        
        Args:
            phase: The audit phase the activity belongs to.
            activity_index: The index of this activity (0-based).
            total_activities: Total number of activities in the phase.
            
        Returns:
            A simulated timestamp for the activity.
        """
        timestamps = self.space_activities_in_phase(phase, total_activities)
        
        if activity_index < len(timestamps):
            return timestamps[activity_index]
        else:
            # If index is out of range, return end of phase
            return self.get_phase_end_time(phase)
    
    def get_total_audit_duration(self) -> timedelta:
        """
        Get the total duration of the audit in simulated time.
        
        Returns:
            Total simulated duration from start to end of all phases.
        """
        # Find the latest end time among all phases (except cleanup)
        max_end_week = 0
        for phase in AuditPhase:
            if phase != AuditPhase.CLEANUP:
                start_week, duration = phase.value
                end_week = start_week + duration
                max_end_week = max(max_end_week, end_week)
        
        return timedelta(weeks=max_end_week)
    
    def format_simulated_time(self, simulated_time: datetime) -> str:
        """
        Format a simulated timestamp for display.
        
        Args:
            simulated_time: The simulated timestamp to format.
            
        Returns:
            Formatted string representation.
        """
        return simulated_time.strftime("%Y-%m-%d %H:%M:%S")
