"""Example demonstrating the audit team agents.

This example shows how to create and use the audit team agents:
- Maurice (Audit Manager)
- Esther, Chuck, Victor (Senior Auditors)
- Hillel, Neil, Juman (Staff Auditors)
"""
from datetime import datetime
from src.agents.audit_team import (
    AuditManagerAgent,
    SeniorAuditorAgent,
    StaffAuditorAgent
)
from src.models.audit_plan import (
    AuditPlan,
    BudgetAllocation,
    ExecutionSchedule,
    TestProcedure
)
from src.models.workpaper import Workpaper, AuditReport, Index, VarianceReport


def main():
    """Demonstrate the audit team agents."""
    
    print("=" * 80)
    print("AWS Audit Agent System - Audit Team Demonstration")
    print("=" * 80)
    print()
    
    # Create the audit team
    print("Creating the audit team...")
    print()
    
    # Audit Manager
    maurice = AuditManagerAgent()
    print(f"✓ {maurice.name} - Audit Manager")
    
    # Senior Auditors
    esther = SeniorAuditorAgent(
        name="Esther",
        control_domains=["IAM", "Logical Access"],
        staff_auditor="Hillel"
    )
    print(f"✓ {esther.name} - Senior Auditor (IAM & Logical Access)")
    
    chuck = SeniorAuditorAgent(
        name="Chuck",
        control_domains=["Data Encryption", "Network Security"],
        staff_auditor="Neil"
    )
    print(f"✓ {chuck.name} - Senior Auditor (Encryption & Network)")
    
    victor = SeniorAuditorAgent(
        name="Victor",
        control_domains=["Logging", "Monitoring", "Incident Response"],
        staff_auditor="Juman"
    )
    print(f"✓ {victor.name} - Senior Auditor (Logging & Monitoring)")
    
    # Staff Auditors
    hillel = StaffAuditorAgent(name="Hillel", senior_auditor="Esther")
    print(f"✓ {hillel.name} - Staff Auditor (reports to Esther)")
    
    neil = StaffAuditorAgent(name="Neil", senior_auditor="Chuck")
    print(f"✓ {neil.name} - Staff Auditor (reports to Chuck)")
    
    juman = StaffAuditorAgent(name="Juman", senior_auditor="Victor")
    print(f"✓ {juman.name} - Staff Auditor (reports to Victor)")
    
    print()
    print("=" * 80)
    print("Simulating Audit Workflow")
    print("=" * 80)
    print()
    
    # Phase 1: Maurice approves the audit plan
    print("Phase 1: Audit Planning")
    print("-" * 80)
    
    schedule = ExecutionSchedule(
        start_date=datetime.now(),
        end_date=datetime.now(),
        phases=[],
        milestones=[]
    )
    
    budget = BudgetAllocation(
        total_hours=200,
        by_domain={
            "IAM": 50,
            "Data Encryption": 40,
            "Network Security": 35,
            "Logging": 40,
            "Monitoring": 35
        },
        by_phase={
            "Planning": 20,
            "Execution": 150,
            "Reporting": 30
        }
    )
    
    plan = AuditPlan(
        timeline=schedule,
        budget=budget,
        procedures=[],
        resource_allocation=budget.by_domain
    )
    
    maurice_approval = maurice.approve_budget(budget)
    print(f"✓ Maurice approved budget: {maurice_approval['total_hours']} hours")
    
    plan_approval = maurice.review_audit_plan(plan)
    print(f"✓ Maurice approved audit plan: {plan_approval['comments']}")
    print()
    
    # Phase 2: Senior auditors assign tasks to staff
    print("Phase 2: Task Assignment")
    print("-" * 80)
    
    task1 = {
        "description": "Collect IAM user list and credential report",
        "service": "IAM",
        "deadline": "Week 3"
    }
    assignment1 = esther.supervise_staff(task1)
    print(f"✓ Esther assigned task to Hillel: {task1['description']}")
    
    task2 = {
        "description": "Collect S3 bucket encryption configurations",
        "service": "S3",
        "deadline": "Week 3"
    }
    assignment2 = chuck.supervise_staff(task2)
    print(f"✓ Chuck assigned task to Neil: {task2['description']}")
    
    task3 = {
        "description": "Collect CloudTrail logs and CloudWatch alarms",
        "service": "CloudTrail",
        "deadline": "Week 3"
    }
    assignment3 = victor.supervise_staff(task3)
    print(f"✓ Victor assigned task to Juman: {task3['description']}")
    print()
    
    # Phase 3: Staff auditors receive and execute assignments
    print("Phase 3: Evidence Collection")
    print("-" * 80)
    
    hillel.receive_assignment(task1)
    print(f"✓ Hillel received assignment from Esther")
    hillel.collect_evidence("IAM")
    print(f"✓ Hillel collected IAM evidence")
    
    neil.receive_assignment(task2)
    print(f"✓ Neil received assignment from Chuck")
    neil.collect_evidence("S3")
    print(f"✓ Neil collected S3 evidence")
    
    juman.receive_assignment(task3)
    print(f"✓ Juman received assignment from Victor")
    juman.collect_evidence("CloudTrail")
    print(f"✓ Juman collected CloudTrail evidence")
    print()
    
    # Phase 4: Senior auditors create workpapers
    print("Phase 4: Workpaper Creation")
    print("-" * 80)
    
    workpaper1 = Workpaper(
        reference_number="WP-IAM-001",
        control_domain="IAM",
        control_objective="Ensure MFA is enabled for all users",
        testing_procedures=["Review IAM credential report", "Check MFA status"],
        evidence_collected=[],
        analysis="2 out of 5 users do not have MFA enabled",
        conclusion="Control deficiency identified - MFA not universally enforced",
        created_by="Esther",
        created_at=datetime.now()
    )
    
    print(f"✓ Esther created workpaper: {workpaper1.reference_number}")
    
    # Phase 5: Maurice reviews workpapers
    print()
    print("Phase 5: Workpaper Review")
    print("-" * 80)
    
    review = maurice.review_workpaper(workpaper1)
    print(f"✓ Maurice reviewed {workpaper1.reference_number}: {review['status']}")
    print()
    
    # Phase 6: Maurice signs off on final report
    print("Phase 6: Final Report Sign-Off")
    print("-" * 80)
    
    report = AuditReport(
        executive_summary="Audit identified several control deficiencies in IAM and encryption",
        scope="AWS IAM, S3, CloudTrail, and CloudWatch",
        methodology="Risk-based audit using ISACA framework",
        findings_by_domain={
            "IAM": [],
            "Data Encryption": [],
            "Logging": []
        },
        overall_opinion="Qualified opinion due to identified control deficiencies",
        workpaper_index=Index(),
        budget_variance=VarianceReport(
            total_budgeted=200,
            total_actual=210,
            variance=10,
            variance_percentage=5.0
        ),
        generated_at=datetime.now()
    )
    
    sign_off = maurice.sign_off_report(report)
    print(f"✓ Maurice signed off on final report: {sign_off['signature']}")
    print()
    
    # Display audit trail summary
    print("=" * 80)
    print("Audit Trail Summary")
    print("=" * 80)
    print()
    
    all_agents = [maurice, esther, chuck, victor, hillel, neil, juman]
    
    for agent in all_agents:
        trail = agent.get_audit_trail()
        print(f"{agent.name}: {len(trail)} actions logged")
        for entry in trail[:3]:  # Show first 3 actions
            print(f"  - [{entry.action_type}] {entry.action_description}")
        if len(trail) > 3:
            print(f"  ... and {len(trail) - 3} more actions")
        print()
    
    print("=" * 80)
    print("Demonstration Complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
