"""Complete audit workflow with human-in-the-loop approvals.

This example demonstrates the full audit cycle with proper governance:
1. Senior auditors perform risk assessment
2. YOU approve risk assessment
3. Senior auditors create audit plan
4. YOU approve audit plan
5. Only then can testing proceed
"""

from datetime import datetime
from src.agents.audit_team import SeniorAuditorAgent, AuditManagerAgent
from src.models.company import CompanyProfile, InfrastructureConfig, SecurityIssue, InformationAsset


def main():
    print("\n" + "=" * 80)
    print("COMPLETE AUDIT WORKFLOW WITH APPROVALS")
    print("=" * 80)
    print()
    print("This demonstrates proper audit governance with human oversight:")
    print("  Phase 1: Risk Assessment → Your Approval")
    print("  Phase 2: Audit Planning → Your Approval")
    print("  Phase 3: Test Execution → Only after approvals")
    print()
    input("Press Enter to begin...")
    print()
    
    # Setup: Create company profile
    print("=" * 80)
    print("SETUP: CloudRetail Inc Company Profile")
    print("=" * 80)
    print()
    
    company = CompanyProfile(
        name="CloudRetail Inc",
        business_type="E-commerce Platform",
        services=["Online Store", "Payment Processing", "Customer Portal"],
        infrastructure=InfrastructureConfig(),
        intentional_issues=[
            SecurityIssue(
                issue_type="missing_mfa",
                resource_id="admin-john",
                control_domain="IAM",
                severity="high",
                description="Administrator account without MFA enabled"
            ),
            SecurityIssue(
                issue_type="unencrypted_bucket",
                resource_id="cloudretail-customer-data",
                control_domain="Data Encryption",
                severity="high",
                description="Customer data bucket without encryption at rest"
            ),
            SecurityIssue(
                issue_type="unrestricted_ssh",
                resource_id="cloudretail-web-server",
                control_domain="Network Security",
                severity="high",
                description="SSH port 22 open to internet (0.0.0.0/0)"
            )
        ],
        created_at=datetime.now(),
        information_assets=[
            InformationAsset(
                asset_id="ASSET-001",
                asset_name="Customer Database",
                asset_type="S3 Bucket",
                location="cloudretail-customer-data",
                data_classification="PII",
                confidentiality_impact="high",
                integrity_impact="high",
                availability_impact="high",
                business_process="Customer Account Management",
                description="Customer PII and order data"
            ),
            InformationAsset(
                asset_id="ASSET-002",
                asset_name="Administrator Account",
                asset_type="IAM User",
                location="admin-john",
                data_classification="Confidential",
                confidentiality_impact="high",
                integrity_impact="high",
                availability_impact="high",
                business_process="IT Operations",
                description="Admin access to AWS"
            ),
            InformationAsset(
                asset_id="ASSET-003",
                asset_name="Payment Processing System",
                asset_type="Application",
                location="cloudretail-web-server",
                data_classification="Financial",
                confidentiality_impact="high",
                integrity_impact="high",
                availability_impact="high",
                business_process="Payment Processing",
                description="Payment transactions"
            )
        ]
    )
    
    print(f"Company: {company.name}")
    print(f"Assets: {len(company.information_assets)}")
    print(f"Known Issues: {len(company.intentional_issues)}")
    print()
    input("Press Enter to start Phase 1: Risk Assessment...")
    print()
    
    # Initialize audit team
    maurice = AuditManagerAgent()
    esther = SeniorAuditorAgent("Esther", ["IAM", "Logical Access"], "Hillel")
    chuck = SeniorAuditorAgent("Chuck", ["Data Encryption", "Network Security"], "Neil")
    
    # PHASE 1: RISK ASSESSMENT
    print("=" * 80)
    print("PHASE 1: RISK ASSESSMENT")
    print("=" * 80)
    print()
    
    print("Senior auditors performing risk assessment...")
    print()
    
    esther_risks = esther.assess_risk(company)
    print(f"✓ Esther: {len(esther_risks.inherent_risks)} risks in IAM")
    
    chuck_risks = chuck.assess_risk(company)
    print(f"✓ Chuck: {len(chuck_risks.inherent_risks)} risks in Encryption/Network")
    print()
    
    # Combine assessments
    from src.models.risk import RiskAssessment
    combined_risks = RiskAssessment(
        inherent_risks=esther_risks.inherent_risks + chuck_risks.inherent_risks,
        residual_risks=esther_risks.residual_risks + chuck_risks.residual_risks,
        prioritized_domains=esther_risks.prioritized_domains + chuck_risks.prioritized_domains,
        risk_matrix={**esther_risks.risk_matrix, **chuck_risks.risk_matrix}
    )
    
    input("Press Enter to present risk assessment to Maurice for your approval...")
    print()
    
    # APPROVAL GATE 1: Risk Assessment
    risk_review = maurice.review_risk_assessment(combined_risks, company.name, interactive=True)
    
    if not risk_review["approved"]:
        print()
        print("❌ WORKFLOW STOPPED")
        print("Risk assessment was not approved. Audit cannot proceed.")
        print("The team will revise based on your feedback and re-submit.")
        return
    
    # PHASE 2: AUDIT PLANNING
    print()
    input("Press Enter to start Phase 2: Audit Planning...")
    print()
    
    print("=" * 80)
    print("PHASE 2: AUDIT PLANNING")
    print("=" * 80)
    print()
    
    print("Senior auditors creating audit plan based on approved risks...")
    print()
    
    esther_plan = esther.create_audit_plan(esther_risks)
    print(f"✓ Esther: {len(esther_plan.procedures)} test procedures, {esther_plan.budget.total_hours} hours")
    
    chuck_plan = chuck.create_audit_plan(chuck_risks)
    print(f"✓ Chuck: {len(chuck_plan.procedures)} test procedures, {chuck_plan.budget.total_hours} hours")
    print()
    
    # Combine audit plans
    from src.models.audit_plan import AuditPlan, BudgetAllocation
    
    combined_plan = AuditPlan(
        timeline=esther_plan.timeline,  # Use one timeline
        budget=BudgetAllocation(
            total_hours=esther_plan.budget.total_hours + chuck_plan.budget.total_hours,
            by_domain={**esther_plan.budget.by_domain, **chuck_plan.budget.by_domain},
            by_phase=esther_plan.budget.by_phase
        ),
        procedures=esther_plan.procedures + chuck_plan.procedures,
        resource_allocation={**esther_plan.resource_allocation, **chuck_plan.resource_allocation}
    )
    
    input("Press Enter to present audit plan to Maurice for your approval...")
    print()
    
    # APPROVAL GATE 2: Audit Plan
    plan_review = maurice.review_audit_plan(combined_plan, company.name, interactive=True)
    
    if not plan_review["approved"]:
        print()
        print("❌ WORKFLOW STOPPED")
        print("Audit plan was not approved. Testing cannot proceed.")
        print("The team will revise based on your feedback and re-submit.")
        return
    
    # PHASE 3: TEST EXECUTION (Only if approved)
    print()
    print("=" * 80)
    print("PHASE 3: TEST EXECUTION")
    print("=" * 80)
    print()
    print("✓ Both risk assessment and audit plan approved!")
    print("✓ Audit team is now authorized to execute test procedures")
    print()
    print("The team can now:")
    print("  1. Collect evidence from AWS services")
    print("  2. Execute the approved test procedures")
    print("  3. Evaluate controls and document findings")
    print("  4. Create workpapers for review")
    print()
    print(f"Authorized test procedures: {len(combined_plan.procedures)}")
    print(f"Authorized budget: {combined_plan.budget.total_hours} hours")
    print()
    
    # Show what would be tested
    print("Test procedures that will be executed:")
    for i, proc in enumerate(combined_plan.procedures[:5], 1):  # Show first 5
        print(f"  {i}. {proc.control_objective}")
        print(f"     Domain: {proc.control_domain}")
        print(f"     Assigned to: {proc.assigned_to}")
    
    if len(combined_plan.procedures) > 5:
        print(f"  ... and {len(combined_plan.procedures) - 5} more procedures")
    print()
    
    # Show audit trail
    print("=" * 80)
    print("AUDIT TRAIL SUMMARY")
    print("=" * 80)
    print()
    print(f"Maurice's Actions: {len(maurice.audit_trail)} entries")
    print("Key decisions:")
    for entry in maurice.audit_trail:
        if "approve" in entry.action_type or "reject" in entry.action_type:
            print(f"  • {entry.action_type}: {entry.action_description}")
    print()
    
    print("=" * 80)
    print("WORKFLOW COMPLETE")
    print("=" * 80)
    print()
    print("✓ Risk assessment approved")
    print("✓ Audit plan approved")
    print("✓ Test execution authorized")
    print()
    print("The audit can now proceed with proper governance and oversight.")
    print()


if __name__ == "__main__":
    main()
