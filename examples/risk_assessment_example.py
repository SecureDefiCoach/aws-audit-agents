"""Example demonstrating asset-based risk assessment.

This example shows how senior auditors assess risks by:
1. Identifying information assets
2. Understanding impact (confidentiality, integrity, availability)
3. Identifying vulnerabilities
4. Calculating risk = impact × likelihood
"""

from datetime import datetime
from src.agents.audit_team import SeniorAuditorAgent, AuditManagerAgent
from src.models.company import CompanyProfile, InfrastructureConfig, SecurityIssue, InformationAsset


def main():
    print("=" * 80)
    print("Asset-Based Risk Assessment Demonstration")
    print("=" * 80)
    print()
    
    # Step 1: Define information assets
    print("Step 1: Defining Critical Information Assets")
    print("-" * 80)
    
    information_assets = [
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
    
    for asset in information_assets:
        print(f"\n{asset.asset_name} ({asset.asset_id})")
        print(f"  Type: {asset.asset_type}")
        print(f"  Location: {asset.location}")
        print(f"  Classification: {asset.data_classification}")
        print(f"  Impact if Compromised: {asset.confidentiality_impact.upper()}")
        print(f"  Impact if Modified: {asset.integrity_impact.upper()}")
        print(f"  Impact if Unavailable: {asset.availability_impact.upper()}")
        print(f"  Business Process: {asset.business_process}")
    
    print()
    print()
    
    # Step 2: Create company profile with assets and vulnerabilities
    print("Step 2: Identifying Security Vulnerabilities")
    print("-" * 80)
    
    security_issues = [
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
    ]
    
    for issue in security_issues:
        print(f"\n{issue.description}")
        print(f"  Resource: {issue.resource_id}")
        print(f"  Control Domain: {issue.control_domain}")
        print(f"  Severity: {issue.severity.upper()}")
    
    print()
    print()
    
    # Step 3: Create company profile
    company = CompanyProfile(
        name="CloudRetail Inc",
        business_type="E-commerce",
        services=["Online Store", "Payment Processing", "Customer Portal"],
        infrastructure=InfrastructureConfig(),
        intentional_issues=security_issues,
        created_at=datetime.now(),
        information_assets=information_assets
    )
    
    # Step 4: Senior auditors perform risk assessment
    print("Step 3: Performing Risk Assessment")
    print("-" * 80)
    print()
    
    # Esther assesses IAM risks
    print("Esther (IAM & Logical Access Lead):")
    esther = SeniorAuditorAgent(
        name="Esther",
        control_domains=["IAM", "Logical Access"],
        staff_auditor="Hillel"
    )
    
    esther_risks = esther.assess_risk(company)
    
    print(f"\nRisk Assessment Results:")
    print(f"  Inherent Risks Identified: {len(esther_risks.inherent_risks)}")
    print(f"  Residual Risks: {len(esther_risks.residual_risks)}")
    print()
    
    for risk in esther_risks.inherent_risks:
        print(f"  Risk ID: {risk.risk_id}")
        print(f"  Description: {risk.description}")
        print(f"  Impact: {risk.impact.upper()}")
        print(f"  Likelihood: {risk.likelihood.upper()}")
        print(f"  Risk Level: {risk.risk_level.upper()}")
        print()
    
    # Chuck assesses encryption and network risks
    print("\nChuck (Data Encryption & Network Security Lead):")
    chuck = SeniorAuditorAgent(
        name="Chuck",
        control_domains=["Data Encryption", "Network Security"],
        staff_auditor="Neil"
    )
    
    chuck_risks = chuck.assess_risk(company)
    
    print(f"\nRisk Assessment Results:")
    print(f"  Inherent Risks Identified: {len(chuck_risks.inherent_risks)}")
    print(f"  Residual Risks: {len(chuck_risks.residual_risks)}")
    print()
    
    for risk in chuck_risks.inherent_risks:
        print(f"  Risk ID: {risk.risk_id}")
        print(f"  Description: {risk.description}")
        print(f"  Impact: {risk.impact.upper()}")
        print(f"  Likelihood: {risk.likelihood.upper()}")
        print(f"  Risk Level: {risk.risk_level.upper()}")
        print()
    
    # Step 5: Show how assets drive risk prioritization
    print()
    print("Step 4: Risk Prioritization Based on Asset Impact")
    print("-" * 80)
    print()
    
    all_risks = esther_risks.inherent_risks + chuck_risks.inherent_risks
    high_risks = [r for r in all_risks if r.risk_level == "high"]
    
    print(f"Total Risks Identified: {len(all_risks)}")
    print(f"High-Risk Issues: {len(high_risks)}")
    print()
    
    print("High-Risk Issues Requiring Immediate Attention:")
    for risk in high_risks:
        print(f"\n  • {risk.description}")
        print(f"    Domain: {risk.control_domain}")
        print(f"    Why High Risk: Affects critical {risk.control_domain} assets")
    
    print()
    print()
    
    # Step 6: Show audit trail
    print("Step 5: Audit Trail (Transparency)")
    print("-" * 80)
    print()
    
    print("Esther's Actions:")
    for entry in esther.audit_trail:
        print(f"  [{entry.timestamp.strftime('%H:%M:%S')}] {entry.action_type}")
        print(f"    {entry.action_description}")
        if entry.decision_rationale:
            print(f"    Rationale: {entry.decision_rationale}")
        print()
    
    print("Chuck's Actions:")
    for entry in chuck.audit_trail:
        print(f"  [{entry.timestamp.strftime('%H:%M:%S')}] {entry.action_type}")
        print(f"    {entry.action_description}")
        if entry.decision_rationale:
            print(f"    Rationale: {entry.decision_rationale}")
        print()
    
    # Summary
    print("=" * 80)
    print("Key Takeaways")
    print("=" * 80)
    print()
    print("1. Information Assets Drive Risk Assessment")
    print("   - We identified WHAT needs protection (customer data, admin access, payment system)")
    print("   - We assessed IMPACT if compromised/unavailable (all HIGH impact)")
    print()
    print("2. Vulnerabilities + Asset Impact = Risk")
    print("   - Missing MFA on admin account + High impact admin access = HIGH RISK")
    print("   - Unencrypted bucket + High impact customer data = HIGH RISK")
    print("   - Open SSH + High impact payment system = HIGH RISK")
    print()
    print("3. Risk-Based Prioritization")
    print(f"   - {len(high_risks)} high-risk issues identified")
    print("   - These will receive priority in audit plan and resource allocation")
    print()
    print("4. Complete Transparency")
    print(f"   - {len(esther.audit_trail) + len(chuck.audit_trail)} audit trail entries")
    print("   - All decisions documented with rationale")
    print()


if __name__ == "__main__":
    main()
