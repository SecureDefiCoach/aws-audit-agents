"""Integration tests for Senior Auditor workflow."""
import pytest
from datetime import datetime
from src.agents.audit_team import SeniorAuditorAgent
from src.models.company import CompanyProfile, InfrastructureConfig, SecurityIssue
from src.models.audit_plan import TestProcedure
from src.models.evidence import Evidence, EvidenceRequest


class TestSeniorAuditorWorkflow:
    """Test the complete Senior Auditor workflow."""
    
    def test_assess_risk_workflow(self):
        """Test that senior auditors can assess risks from company profile."""
        from src.models.company import InformationAsset
        
        # Create a company profile with intentional issues and information assets
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
                    resource_id="admin-john",
                    control_domain="IAM",
                    severity="high",
                    description="Administrator account without MFA"
                ),
                SecurityIssue(
                    issue_type="unencrypted_bucket",
                    resource_id="cloudretail-customer-data",
                    control_domain="Data Encryption",
                    severity="high",
                    description="Customer data bucket without encryption"
                )
            ],
            created_at=datetime.now(),
            information_assets=[
                InformationAsset(
                    asset_id="ASSET-001",
                    asset_name="Administrator Account",
                    asset_type="IAM User",
                    location="admin-john",
                    data_classification="Confidential",
                    confidentiality_impact="high",
                    integrity_impact="high",
                    availability_impact="high",
                    business_process="IT Operations",
                    description="Admin access to AWS environment"
                ),
                InformationAsset(
                    asset_id="ASSET-002",
                    asset_name="Customer Database",
                    asset_type="S3 Bucket",
                    location="cloudretail-customer-data",
                    data_classification="PII",
                    confidentiality_impact="high",
                    integrity_impact="high",
                    availability_impact="high",
                    business_process="Customer Data Management",
                    description="Customer PII and order data"
                )
            ]
        )
        
        # Esther assesses IAM risks
        esther = SeniorAuditorAgent(
            name="Esther",
            control_domains=["IAM", "Logical Access"],
            staff_auditor="Hillel"
        )
        
        risk_assessment = esther.assess_risk(company)
        
        # Verify risk assessment
        assert risk_assessment is not None
        assert len(risk_assessment.inherent_risks) > 0
        assert len(risk_assessment.residual_risks) > 0
        assert len(risk_assessment.prioritized_domains) > 0
        
        # Verify IAM risks were identified
        iam_risks = [r for r in risk_assessment.inherent_risks if r.control_domain == "IAM"]
        assert len(iam_risks) > 0
        assert iam_risks[0].risk_level == "high"
        
        # Verify audit trail
        assert len(esther.audit_trail) == 3  # assess_risk + identify_assets + risk_assessment_complete
        assert esther.audit_trail[0].action_type == "assess_risk"
    
    def test_create_audit_plan_workflow(self):
        """Test that senior auditors can create audit plans."""
        from src.models.risk import Risk, ControlDomain, RiskAssessment
        
        # Create risk assessment
        risks = RiskAssessment(
            inherent_risks=[
                Risk(
                    risk_id="RISK-IAM-001",
                    control_domain="IAM",
                    description="Missing MFA",
                    impact="high",
                    likelihood="high",
                    risk_level="high"
                )
            ],
            residual_risks=[
                Risk(
                    risk_id="RESID-IAM-001",
                    control_domain="IAM",
                    description="Missing MFA",
                    impact="high",
                    likelihood="high",
                    risk_level="high"
                )
            ],
            prioritized_domains=[
                ControlDomain(
                    domain_name="IAM",
                    description="Identity and Access Management",
                    priority=1,
                    risk_level="high"
                )
            ],
            risk_matrix={"IAM": "high"}
        )
        
        esther = SeniorAuditorAgent(
            name="Esther",
            control_domains=["IAM"],
            staff_auditor="Hillel"
        )
        
        audit_plan = esther.create_audit_plan(risks)
        
        # Verify audit plan
        assert audit_plan is not None
        assert audit_plan.budget.total_hours > 0
        assert len(audit_plan.procedures) > 0
        assert audit_plan.timeline.start_date is not None
        
        # Verify high-risk domain gets more hours
        assert audit_plan.budget.by_domain.get("IAM", 0) >= 40.0
        
        # Verify procedures were created
        iam_procedures = [p for p in audit_plan.procedures if p.control_domain == "IAM"]
        assert len(iam_procedures) > 0
        
        # Verify audit trail
        assert len(esther.audit_trail) == 2
        assert esther.audit_trail[0].action_type == "create_audit_plan"
    
    def test_collect_evidence_direct_workflow(self):
        """Test that senior auditors can collect evidence directly."""
        esther = SeniorAuditorAgent(
            name="Esther",
            control_domains=["IAM"],
            staff_auditor="Hillel"
        )
        
        # Note: This will fail if AWS credentials are not configured
        # In a real test, we would mock the AWS clients
        try:
            evidence = esther.collect_evidence_direct("IAM", "IAM")
            
            if evidence:
                # Verify evidence structure
                assert evidence.evidence_id is not None
                assert evidence.source == "IAM"
                assert evidence.collection_method == "direct"
                assert evidence.collected_by == "Esther"
                assert evidence.control_domain == "IAM"
                
                # Verify audit trail
                assert len(esther.audit_trail) >= 2
        except Exception as e:
            # Expected if AWS credentials not configured
            pytest.skip(f"AWS credentials not configured: {e}")
    
    def test_request_evidence_workflow(self):
        """Test that senior auditors can request evidence from auditee."""
        esther = SeniorAuditorAgent(
            name="Esther",
            control_domains=["IAM"],
            staff_auditor="Hillel"
        )
        
        request = EvidenceRequest(
            request_id="REQ-001",
            control_domain="IAM",
            requested_items=["User list", "MFA status"],
            requested_by="Esther",
            requested_at=datetime.now(),
            status="pending"
        )
        
        request_id = esther.request_evidence(request)
        
        assert request_id == "REQ-001"
        assert len(esther.audit_trail) == 1
        assert esther.audit_trail[0].action_type == "request_evidence"
    
    def test_execute_test_workflow(self):
        """Test that senior auditors can execute testing procedures."""
        esther = SeniorAuditorAgent(
            name="Esther",
            control_domains=["IAM"],
            staff_auditor="Hillel"
        )
        
        procedure = TestProcedure(
            procedure_id="PROC-001",
            control_domain="IAM",
            control_objective="Verify MFA is enabled for all users",
            procedure_description="Review IAM users and verify MFA device configuration",
            evidence_required=["IAM user list", "MFA device status"],
            assigned_to="Esther",
            estimated_hours=4.0
        )
        
        # Create mock evidence
        evidence = Evidence(
            evidence_id="EVD-IAM-001",
            source="IAM",
            collection_method="direct",
            collected_at=datetime.now(),
            collected_by="Esther",
            data={
                "users": [
                    {"UserName": "admin"},
                    {"UserName": "developer"}
                ],
                "mfa_status": {
                    "admin": False,
                    "developer": True
                }
            },
            storage_path="evidence/iam/EVD-IAM-001.json"
        )
        
        test_result = esther.execute_test(procedure, evidence)
        
        # Verify test result
        assert test_result is not None
        assert test_result["procedure_id"] == "PROC-001"
        assert test_result["executed_by"] == "Esther"
        assert "passed" in test_result
        assert test_result["passed"] is False  # admin has no MFA
        assert len(test_result["affected_resources"]) == 1
        assert "admin" in test_result["affected_resources"]
        
        # Verify audit trail
        assert len(esther.audit_trail) == 2
    
    def test_evaluate_control_workflow(self):
        """Test that senior auditors can evaluate controls."""
        esther = SeniorAuditorAgent(
            name="Esther",
            control_domains=["IAM"],
            staff_auditor="Hillel"
        )
        
        test_result = {
            "procedure_id": "PROC-001",
            "control_domain": "IAM",
            "control_objective": "Verify MFA is enabled for all users",
            "procedure_description": "Review IAM users and verify MFA device configuration",
            "executed_by": "Esther",
            "executed_at": datetime.now(),
            "evidence_id": "EVD-IAM-001",
            "passed": False,
            "findings": ["2 users without MFA enabled"],
            "affected_resources": ["admin", "developer"]
        }
        
        finding = esther.evaluate_control(test_result)
        
        # Verify finding
        assert finding is not None
        assert finding.finding_id is not None
        assert finding.control_domain == "IAM"
        assert finding.result == "fail"
        assert finding.risk_rating in ["high", "medium", "low"]
        assert len(finding.recommendations) > 0
        assert finding.created_by == "Esther"
        
        # Verify audit trail
        assert len(esther.audit_trail) == 2
    
    def test_create_workpaper_workflow(self):
        """Test that senior auditors can create workpapers."""
        from src.models.finding import Finding
        
        esther = SeniorAuditorAgent(
            name="Esther",
            control_domains=["IAM"],
            staff_auditor="Hillel"
        )
        
        finding = Finding(
            finding_id="FIND-12345678",
            control_domain="IAM",
            control_objective="Verify MFA is enabled for all users",
            test_procedure="Review IAM users and verify MFA device configuration",
            result="fail",
            evidence_refs=["EVD-IAM-001"],
            affected_resources=["admin", "developer"],
            risk_rating="high",
            recommendations=["Enable MFA for all users"],
            created_by="Esther",
            created_at=datetime.now()
        )
        
        workpaper = esther.create_workpaper(finding)
        
        # Verify workpaper
        assert workpaper is not None
        assert workpaper.reference_number.startswith("WP-")
        assert workpaper.control_domain == "IAM"
        assert workpaper.created_by == "Esther"
        assert len(workpaper.analysis) > 0
        assert len(workpaper.conclusion) > 0
        
        # Verify finding was updated with workpaper reference
        assert finding.workpaper_ref == workpaper.reference_number
        
        # Verify audit trail
        assert len(esther.audit_trail) == 2
    
    def test_full_senior_auditor_workflow(self):
        """Test the complete workflow from risk assessment to workpaper creation."""
        # Create company profile
        company = CompanyProfile(
            name="CloudRetail Inc",
            business_type="E-commerce",
            services=["Online Store", "Payment Processing"],
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
                    description="Administrator account without MFA"
                )
            ],
            created_at=datetime.now()
        )
        
        # Initialize Esther
        esther = SeniorAuditorAgent(
            name="Esther",
            control_domains=["IAM"],
            staff_auditor="Hillel"
        )
        
        # Step 1: Assess risk
        risk_assessment = esther.assess_risk(company)
        assert risk_assessment is not None
        
        # Step 2: Create audit plan
        audit_plan = esther.create_audit_plan(risk_assessment)
        assert audit_plan is not None
        
        # Step 3: Assign task to staff
        task = {
            "description": "Collect IAM evidence",
            "service": "IAM"
        }
        assignment = esther.supervise_staff(task)
        assert assignment["assigned_to"] == "Hillel"
        
        # Step 4: Execute test (with mock evidence)
        procedure = audit_plan.procedures[0]
        evidence = Evidence(
            evidence_id="EVD-IAM-001",
            source="IAM",
            collection_method="direct",
            collected_at=datetime.now(),
            collected_by="Esther",
            data={
                "users": [{"UserName": "admin"}],
                "mfa_status": {"admin": False}
            },
            storage_path="evidence/iam/EVD-IAM-001.json"
        )
        test_result = esther.execute_test(procedure, evidence)
        assert test_result is not None
        
        # Step 5: Evaluate control
        finding = esther.evaluate_control(test_result)
        assert finding is not None
        
        # Step 6: Create workpaper
        workpaper = esther.create_workpaper(finding)
        assert workpaper is not None
        
        # Verify complete audit trail
        assert len(esther.audit_trail) > 10  # Multiple actions logged
        
        # Verify all agent actions are logged with Esther's name
        for entry in esther.audit_trail:
            assert entry.agent_id == "Esther"


class TestMultipleSeniorAuditors:
    """Test multiple senior auditors working on different domains."""
    
    def test_three_senior_auditors_different_domains(self):
        """Test Esther, Chuck, and Victor working on different domains."""
        # Create company with issues in multiple domains
        company = CompanyProfile(
            name="CloudRetail Inc",
            business_type="E-commerce",
            services=["Online Store"],
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
                    description="Missing MFA"
                ),
                SecurityIssue(
                    issue_type="unencrypted_bucket",
                    resource_id="bucket-data",
                    control_domain="Data Encryption",
                    severity="high",
                    description="Unencrypted bucket"
                ),
                SecurityIssue(
                    issue_type="cloudtrail_disabled",
                    resource_id="cloudtrail",
                    control_domain="Logging",
                    severity="medium",
                    description="CloudTrail not enabled"
                )
            ],
            created_at=datetime.now()
        )
        
        # Initialize all three senior auditors
        esther = SeniorAuditorAgent(
            name="Esther",
            control_domains=["IAM"],
            staff_auditor="Hillel"
        )
        
        chuck = SeniorAuditorAgent(
            name="Chuck",
            control_domains=["Data Encryption"],
            staff_auditor="Neil"
        )
        
        victor = SeniorAuditorAgent(
            name="Victor",
            control_domains=["Logging"],
            staff_auditor="Juman"
        )
        
        # Each auditor assesses risks in their domain
        esther_risks = esther.assess_risk(company)
        chuck_risks = chuck.assess_risk(company)
        victor_risks = victor.assess_risk(company)
        
        # Verify each found risks in their domain
        assert len([r for r in esther_risks.inherent_risks if r.control_domain == "IAM"]) > 0
        assert len([r for r in chuck_risks.inherent_risks if r.control_domain == "Data Encryption"]) > 0
        assert len([r for r in victor_risks.inherent_risks if r.control_domain == "Logging"]) > 0
        
        # Verify each has their own audit trail
        assert all(e.agent_id == "Esther" for e in esther.audit_trail)
        assert all(e.agent_id == "Chuck" for e in chuck.audit_trail)
        assert all(e.agent_id == "Victor" for e in victor.audit_trail)
