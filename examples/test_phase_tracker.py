"""
Test the Audit Phase Tracker in the Dashboard.

This script demonstrates how to update audit phase status programmatically.
"""

import time
import requests
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.agent_factory import AgentFactory
from src.web.agent_dashboard import run_dashboard, init_dashboard
import threading


def update_phase(phase_num, status):
    """Update a phase status via API."""
    try:
        response = requests.post(
            'http://127.0.0.1:5000/api/audit/phases',
            json={'phase': phase_num, 'status': status}
        )
        if response.status_code == 200:
            print(f"✓ Phase {phase_num} set to '{status}'")
        else:
            print(f"✗ Failed to update phase {phase_num}: {response.text}")
    except Exception as e:
        print(f"✗ Error updating phase {phase_num}: {e}")


def demo_phase_progression():
    """Demonstrate phase progression through the audit lifecycle."""
    print("\n" + "=" * 80)
    print("AUDIT PHASE TRACKER DEMO")
    print("=" * 80)
    print()
    print("This demo will simulate an audit progressing through all 6 phases.")
    print("Watch the dashboard at http://127.0.0.1:5000 to see the phases update!")
    print()
    print("=" * 80)
    print()
    
    # Wait for dashboard to start
    time.sleep(3)
    
    # Phase 1: Risk Assessment & Planning
    print("\n📋 Phase 1: Risk Assessment & Planning")
    print("   Starting risk assessment...")
    update_phase(1, 'in-progress')
    time.sleep(5)
    print("   Risk assessment complete!")
    update_phase(1, 'complete')
    time.sleep(2)
    
    # Phase 2: Control Testing
    print("\n🔍 Phase 2: Control Testing (Fieldwork)")
    print("   Beginning control testing...")
    update_phase(2, 'in-progress')
    time.sleep(5)
    print("   Control testing complete!")
    update_phase(2, 'complete')
    time.sleep(2)
    
    # Phase 3: Workpaper Review
    print("\n📝 Phase 3: Workpaper Review & QA")
    print("   Reviewing workpapers...")
    update_phase(3, 'in-progress')
    time.sleep(5)
    print("   Workpaper review complete!")
    update_phase(3, 'complete')
    time.sleep(2)
    
    # Phase 4: Remediation Planning
    print("\n🔧 Phase 4: Remediation Planning")
    print("   Planning remediation...")
    update_phase(4, 'in-progress')
    time.sleep(5)
    print("   Remediation plans finalized!")
    update_phase(4, 'complete')
    time.sleep(2)
    
    # Phase 5: Audit Reporting
    print("\n📊 Phase 5: Audit Reporting")
    print("   Drafting audit report...")
    update_phase(5, 'in-progress')
    time.sleep(5)
    print("   Audit report complete!")
    update_phase(5, 'complete')
    time.sleep(2)
    
    # Phase 6: Follow-Up
    print("\n✅ Phase 6: Follow-Up")
    print("   Beginning follow-up activities...")
    update_phase(6, 'in-progress')
    time.sleep(5)
    print("   Follow-up complete!")
    update_phase(6, 'complete')
    
    print("\n" + "=" * 80)
    print("AUDIT COMPLETE!")
    print("=" * 80)
    print()
    print("All phases have been completed. Check the dashboard to see the final status.")
    print()


def main():
    """Run the phase tracker demo."""
    print("\n" + "=" * 80)
    print("AUDIT PHASE TRACKER - DASHBOARD DEMO")
    print("=" * 80)
    print()
    print("This demo will:")
    print("  1. Start the dashboard web server")
    print("  2. Create a sample audit team")
    print("  3. Simulate audit phase progression")
    print()
    print("Open your browser to http://127.0.0.1:5000 to watch the phases update!")
    print()
    print("=" * 80)
    
    # Create agent team
    factory = AgentFactory()
    team = factory.create_audit_team()
    
    # Initialize dashboard
    init_dashboard(team)
    
    # Start dashboard in a separate thread
    dashboard_thread = threading.Thread(
        target=lambda: run_dashboard(team, debug=False),
        daemon=True
    )
    dashboard_thread.start()
    
    # Wait for dashboard to start
    print("\nWaiting for dashboard to start...")
    time.sleep(3)
    
    print("\n✓ Dashboard started at http://127.0.0.1:5000")
    print("\nStarting phase progression demo in 3 seconds...")
    time.sleep(3)
    
    # Run the demo
    demo_phase_progression()
    
    print("\nDemo complete! Press Ctrl+C to exit.")
    
    # Keep running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nShutting down...")


if __name__ == '__main__':
    main()
