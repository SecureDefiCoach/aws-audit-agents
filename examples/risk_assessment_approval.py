"""Interactive example demonstrating human-in-the-loop risk assessment approval.

This example shows the proper audit workflow:
1. Senior auditors perform risk assessment
2. Maurice presents it for human review
3. Human approves or rejects
4. Only after approval can audit planning proceed
"""

from datetime import datetime
from src.agents.audit_team import SeniorAuditorAgent, AuditManagerAgent
from src.models.company import CompanyProfile, InfrastructureConfig, SecurityIssue, InformationAsset


def main():
    print("\n" + "=" * 80)
    print("INTERACTIVE RISK ASSESSMENT APPROVAL WORKFLOW")
    print("=" * 80)
    print()
    print("This demonstrates the proper audit cycle with human oversight:")
    print("  1. Senior auditors perform risk assessment")
    print("  2. Maurice (Audit Manager) presents for your review")
    print("  3. You approve or reject the assessment")
    print("  4. Only after approval can audit planning proceed")
    print()
    input("Press Enter to begin...")
    print()
    
    # Step 1: Create company profile with assets and issues
    print("Step 1: Loading CloudRetail Inc Company Profile")
    print("-" * 80)
    
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
            ),
            SecurityIssue(
                issue_type="cloudtrail_single_region",
                resource_id="cloudtrail-main",
                control_domain="Logging",
                severity="medium",
                description="CloudTrail only enabled in one region"
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
                description="Contains customer profiles, order history, payment data"
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
                description="Full administrative access to AWS environment"
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
                description="Handles payment transactions - PCI-DSS scope"
            )
        ]
    )
    
    print(f"✓ Company: {company.name}")
    print(f"  Business Type: {company.business_type}")
    print(f"  Information Assets: {len(company.information_assets)}")
    print(f"  Security Issues: {len(company.intentional_issues)}")
    print()
    input("Press Enter to continue...")
    print()
    
    # Step 2: Senior auditors perform risk assessment
    print("Step 2: Senior Auditors Performing Risk Assessment")
    print("-" * 80)
    print()
    
    # Initialize audit team
    maurice = AuditManagerAgent()
    
    esther = SeniorAuditorAgent(
        name="Esther",
        control_domains=["IAM", "Logical Access"],
        staff_auditor="Hillel"
    )
    
    chuck = SeniorAuditorAgent(
        name="Chuck",
        control_domains=["Data Encryption", "Network Security"],
        staff_auditor="Neil"
    )
    
    victor = SeniorAuditorAgent(
        name="Victor",
        control_domains=["Logging", "Monitoring"],
        staff_auditor="Juman"
    )
    
    print("Esther (IAM & Logical Access Lead) - Assessing risks...")
    esther_risks = esther.assess_risk(company)
    print(f"  ✓ Identified {len(esther_risks.inherent_risks)} risks in IAM domain")
    print()
    
    print("Chuck (Data Encryption & Network Security Lead) - Assessing risks...")
    chuck_risks = chuck.assess_risk(company)
    print(f"  ✓ Identified {len(chuck_risks.inherent_risks)} risks in Encryption/Network domains")
    print()
    
    print("Victor (Logging & Monitoring Lead) - Assessing risks...")
    victor_risks = victor.assess_risk(company)
    print(f"  ✓ Identified {len(victor_risks.inherent_risks)} risks in Logging domain")
    print()
    
    # Combine risk assessments
    from src.models.risk import RiskAssessment
    
    combined_assessment = RiskAssessment(
        inherent_risks=esther_risks.inherent_risks + chuck_risks.inherent_risks + victor_risks.inherent_risks,
        residual_risks=esther_risks.residual_risks + chuck_risks.residual_risks + victor_risks.residual_risks,
        prioritized_domains=esther_risks.prioritized_domains + chuck_risks.prioritized_domains + victor_risks.prioritized_domains,
        risk_matrix={**esther_risks.risk_matrix, **chuck_risks.risk_matrix, **victor_risks.risk_matrix}
    )
    
    print(f"Combined Risk Assessment:")
    print(f"  Total Risks: {len(combined_assessment.inherent_risks)}")
    print(f"  High-Risk: {len([r for r in combined_assessment.residual_risks if r.risk_level == 'high'])}")
    print(f"  Medium-Risk: {len([r for r in combined_assessment.residual_risks if r.risk_level == 'medium'])}")
    print()
    input("Press Enter to present to Maurice for review...")
    print()
    
    # Step 3: Maurice reviews and presents for human approval
    print("Step 3: Maurice Reviews Risk Assessment")
    print("-" * 80)
    print()
    
    # This will prompt for human input
    review_result = maurice.review_risk_assessment(combined_assessment, company.name, interactive=True)
    
    # Step 4: Check approval status and proceed accordingly
    if review_result["approved"]:
        print()
        print("=" * 80)
        print("NEXT STEPS")
        print("=" * 80)
        print()
        print("✓ Risk assessment approved!")
        print()
        print("The audit team can now proceed to:")
        print("  1. Create detailed audit plan based on approved risks")
        print("  2. Develop specific test procedures for high-risk areas")
        print("  3. Allocate budget and resources")
        print("  4. Present audit plan to Maurice for approval")
        print()
        print("High-risk areas that will receive priority:")
        for risk in [r for r in combined_assessment.residual_risks if r.risk_level == "high"]:
            print(f"  • {risk.control_domain}: {risk.description}")
        print()
        
    else:
        print()
        print("=" * 80)
        print("REVISION REQUIRED")
        print("=" * 80)
        print()
        print("✗ Risk assessment requires revision")
        print()
        print("The audit team will:")
        print("  1. Review Maurice's feedback")
        print("  2. Revise the risk assessment")
        print("  3. Re-submit for approval")
        print()
        print(f"Feedback: {review_result['comments']}")
        print()
    
    # Show audit trail
    print()
    print("=" * 80)
    print("AUDIT TRAIL")
    print("=" * 80)
    print()
    print(f"Maurice's Actions ({len(maurice.audit_trail)} entries):")
    for entry in maurice.audit_trail:
        print(f"  [{entry.timestamp.strftime('%H:%M:%S')}] {entry.action_type}")
        print(f"    {entry.action_description}")
    print()


if __name__ == "__main__":
    main()
