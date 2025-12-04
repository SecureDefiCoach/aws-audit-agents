"""Example demonstrating Senior Auditor agent functionality.

This example shows how Esther, Chuck, and Victor (Senior Auditors) work together
to assess risks, create audit plans, collect evidence, execute tests, evaluate
controls, and create workpapers.
"""

from datetime import datetime
from src.agents.audit_team import SeniorAuditorAgent
from src.models.company import CompanyProfile, InfrastructureConfig, SecurityIssue
from src.models.evidence import Evidence
from src.models.audit_plan import TestProcedure


def main():
    print("=" * 80)
    print("AWS Audit Agent System - Senior Auditor Demonstration")
    print("=" * 80)
    print()
    
    # Create a simulated company profile with intentional security issues
    print("Step 1: Creating CloudRetail Inc company profile...")
    company = CompanyProfile(
        name="CloudRetail Inc",
        business_type="E-commerce",
        services=["Online Store", "Payment Processing", "Customer Portal"],
        infrastructure=InfrastructureConfig(
            iam_users=[],
            s3_buckets=[],
            ec2_instances=[],
            vpc_config={}
        ),
        intentional_issues=[
            SecurityIssue(
                issue_type="missing_mfa",
                resource_id="user-admin",
                control_domain="IAM",
                severity="high",
                description="Administrator account without MFA enabled"
            ),
            SecurityIssue(
                issue_type="overly_permissive_policy",
                resource_id="user-developer",
                control_domain="IAM",
                severity="medium",
                description="Developer with admin-like permissions"
            ),
            SecurityIssue(
                issue_type="unencrypted_bucket",
                resource_id="bucket-customer-data",
                control_domain="Data Encryption",
                severity="high",
                description="Customer data bucket without encryption"
            ),
            SecurityIssue(
                issue_type="unrestricted_security_group",
                resource_id="sg-web-server",
                control_domain="Network Security",
                severity="high",
                description="Security group allows 0.0.0.0/0 access"
            ),
            SecurityIssue(
                issue_type="cloudtrail_disabled",
                resource_id="cloudtrail-main",
                control_domain="Logging",
                severity="medium",
                description="CloudTrail not enabled in all regions"
            )
        ],
        created_at=datetime.now()
    )
    print(f"✓ Created company: {company.name}")
    print(f"  Business Type: {company.business_type}")
    print(f"  Services: {', '.join(company.services)}")
    print(f"  Intentional Issues: {len(company.intentional_issues)}")
    print()
    
    # Initialize the three senior auditors
    print("Step 2: Initializing Senior Auditors...")
    esther = SeniorAuditorAgent(
        name="Esther",
        control_domains=["IAM", "Logical Access"],
        staff_auditor="Hillel"
    )
    print(f"✓ Esther - Lead Auditor for {', '.join(esther.control_domains)}")
    print(f"  Staff Auditor: {esther.staff_auditor}")
    
    chuck = SeniorAuditorAgent(
        name="Chuck",
        control_domains=["Data Encryption", "Network Security"],
        staff_auditor="Neil"
    )
    print(f"✓ Chuck - Lead Auditor for {', '.join(chuck.control_domains)}")
    print(f"  Staff Auditor: {chuck.staff_auditor}")
    
    victor = SeniorAuditorAgent(
        name="Victor",
        control_domains=["Logging", "Monitoring", "Incident Response"],
        staff_auditor="Juman"
    )
    print(f"✓ Victor - Lead Auditor for {', '.join(victor.control_domains)}")
    print(f"  Staff Auditor: {victor.staff_auditor}")
    print()
    
    # Step 3: Each senior auditor assesses risks in their domains
    print("Step 3: Performing Risk Assessments...")
    print()
    
    print("Esther's Risk Assessment (IAM):")
    esther_risks = esther.assess_risk(company)
    iam_risks = [r for r in esther_risks.inherent_risks if r.control_domain in esther.control_domains]
    print(f"  Inherent Risks Identified: {len(iam_risks)}")
    for risk in iam_risks:
        print(f"    - {risk.description} (Risk Level: {risk.risk_level.upper()})")
    print()
    
    print("Chuck's Risk Assessment (Encryption & Network):")
    chuck_risks = chuck.assess_risk(company)
    chuck_domain_risks = [r for r in chuck_risks.inherent_risks if r.control_domain in chuck.control_domains]
    print(f"  Inherent Risks Identified: {len(chuck_domain_risks)}")
    for risk in chuck_domain_risks:
        print(f"    - {risk.description} (Risk Level: {risk.risk_level.upper()})")
    print()
    
    print("Victor's Risk Assessment (Logging):")
    victor_risks = victor.assess_risk(company)
    victor_domain_risks = [r for r in victor_risks.inherent_risks if r.control_domain in victor.control_domains]
    print(f"  Inherent Risks Identified: {len(victor_domain_risks)}")
    for risk in victor_domain_risks:
        print(f"    - {risk.description} (Risk Level: {risk.risk_level.upper()})")
    print()
    
    # Step 4: Create audit plans
    print("Step 4: Creating Audit Plans...")
    print()
    
    print("Esther's Audit Plan:")
    esther_plan = esther.create_audit_plan(esther_risks)
    print(f"  Total Hours: {esther_plan.budget.total_hours}")
    print(f"  Procedures: {len(esther_plan.procedures)}")
    print(f"  Timeline: {esther_plan.timeline.start_date.strftime('%Y-%m-%d')} to {esther_plan.timeline.end_date.strftime('%Y-%m-%d')}")
    print()
    
    print("Chuck's Audit Plan:")
    chuck_plan = chuck.create_audit_plan(chuck_risks)
    print(f"  Total Hours: {chuck_plan.budget.total_hours}")
    print(f"  Procedures: {len(chuck_plan.procedures)}")
    print(f"  Timeline: {chuck_plan.timeline.start_date.strftime('%Y-%m-%d')} to {chuck_plan.timeline.end_date.strftime('%Y-%m-%d')}")
    print()
    
    print("Victor's Audit Plan:")
    victor_plan = victor.create_audit_plan(victor_risks)
    print(f"  Total Hours: {victor_plan.budget.total_hours}")
    print(f"  Procedures: {len(victor_plan.procedures)}")
    print(f"  Timeline: {victor_plan.timeline.start_date.strftime('%Y-%m-%d')} to {victor_plan.timeline.end_date.strftime('%Y-%m-%d')}")
    print()
    
    # Step 5: Demonstrate task assignment
    print("Step 5: Assigning Tasks to Staff Auditors...")
    print()
    
    task = {
        "description": "Collect IAM user list and MFA status",
        "service": "IAM",
        "deadline": "Week 3"
    }
    assignment = esther.supervise_staff(task)
    print(f"✓ Esther assigned task to {assignment['assigned_to']}")
    print(f"  Task: {task['description']}")
    print()
    
    # Step 6: Execute a test with mock evidence
    print("Step 6: Executing Testing Procedures...")
    print()
    
    # Use the first procedure from Esther's plan
    procedure = esther_plan.procedures[0]
    print(f"Testing: {procedure.control_objective}")
    print(f"Procedure: {procedure.procedure_description}")
    print()
    
    # Create mock evidence (simulating what would be collected from AWS)
    evidence = Evidence(
        evidence_id="EVD-IAM-001",
        source="IAM",
        collection_method="direct",
        collected_at=datetime.now(),
        collected_by="Esther",
        data={
            "users": [
                {"UserName": "admin"},
                {"UserName": "developer"},
                {"UserName": "readonly-user"}
            ],
            "mfa_status": {
                "admin": False,  # Missing MFA!
                "developer": True,
                "readonly-user": True
            }
        },
        storage_path="evidence/iam/EVD-IAM-001.json",
        control_domain="IAM"
    )
    
    test_result = esther.execute_test(procedure, evidence)
    print(f"Test Result: {'PASSED' if test_result['passed'] else 'FAILED'}")
    print(f"Findings:")
    for finding in test_result['findings']:
        print(f"  - {finding}")
    if test_result['affected_resources']:
        print(f"Affected Resources: {', '.join(test_result['affected_resources'])}")
    print()
    
    # Step 7: Evaluate the control
    print("Step 7: Evaluating Control Effectiveness...")
    print()
    
    finding = esther.evaluate_control(test_result)
    print(f"Finding ID: {finding.finding_id}")
    print(f"Control Domain: {finding.control_domain}")
    print(f"Result: {finding.result.upper()}")
    print(f"Risk Rating: {finding.risk_rating.upper()}")
    print(f"Affected Resources: {len(finding.affected_resources)}")
    print(f"Recommendations:")
    for rec in finding.recommendations:
        print(f"  - {rec}")
    print()
    
    # Step 8: Create workpaper
    print("Step 8: Creating Workpaper...")
    print()
    
    workpaper = esther.create_workpaper(finding, [evidence])
    print(f"Workpaper Reference: {workpaper.reference_number}")
    print(f"Control Domain: {workpaper.control_domain}")
    print(f"Created By: {workpaper.created_by}")
    print(f"Created At: {workpaper.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    print("Analysis:")
    print(workpaper.analysis)
    print()
    print("Conclusion:")
    print(workpaper.conclusion)
    print()
    
    # Step 9: Display audit trails
    print("Step 9: Audit Trail Summary...")
    print()
    
    print(f"Esther's Audit Trail: {len(esther.audit_trail)} actions logged")
    print("Recent actions:")
    for entry in esther.audit_trail[-5:]:
        print(f"  [{entry.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {entry.action_type}: {entry.action_description}")
    print()
    
    print(f"Chuck's Audit Trail: {len(chuck.audit_trail)} actions logged")
    print("Recent actions:")
    for entry in chuck.audit_trail[-3:]:
        print(f"  [{entry.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {entry.action_type}: {entry.action_description}")
    print()
    
    print(f"Victor's Audit Trail: {len(victor.audit_trail)} actions logged")
    print("Recent actions:")
    for entry in victor.audit_trail[-3:]:
        print(f"  [{entry.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {entry.action_type}: {entry.action_description}")
    print()
    
    # Summary
    print("=" * 80)
    print("Demonstration Complete!")
    print("=" * 80)
    print()
    print("Summary:")
    print(f"  - 3 Senior Auditors (Esther, Chuck, Victor) assessed risks in their domains")
    print(f"  - Total risks identified: {len(esther_risks.inherent_risks) + len(chuck_risks.inherent_risks) + len(victor_risks.inherent_risks)}")
    print(f"  - Total audit procedures planned: {len(esther_plan.procedures) + len(chuck_plan.procedures) + len(victor_plan.procedures)}")
    print(f"  - Total budgeted hours: {esther_plan.budget.total_hours + chuck_plan.budget.total_hours + victor_plan.budget.total_hours}")
    print(f"  - 1 test executed with finding: {finding.result.upper()} ({finding.risk_rating.upper()} risk)")
    print(f"  - 1 workpaper created: {workpaper.reference_number}")
    print(f"  - Total audit trail entries: {len(esther.audit_trail) + len(chuck.audit_trail) + len(victor.audit_trail)}")
    print()
    print("All agent actions are logged with agent names visible for transparency.")
    print()


if __name__ == "__main__":
    main()
