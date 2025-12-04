"""Unit tests for audit team agents."""
import pytest
from datetime import datetime
from src.agents.audit_team import (
    AuditAgent,
    AuditManagerAgent,
    SeniorAuditorAgent,
    StaffAuditorAgent
)
from src.models.audit_plan import AuditPlan, BudgetAllocation, ExecutionSchedule
from src.models.workpaper import Workpaper, AuditReport, Index, VarianceReport
from src.models.evidence import Evidence


class TestAuditAgent:
    """Test the base AuditAgent class."""
    
    def test_agent_initialization(self):
        """Test that an agent can be initialized with a name."""
        # Create a concrete subclass for testing
        class TestAgent(AuditAgent):
            pass
        
        agent = TestAgent(name="TestAgent")
        assert agent.name == "TestAgent"
        assert agent.audit_trail == []
    
    def test_log_action(self):
        """Test that agents can log actions to the audit trail."""
        class TestAgent(AuditAgent):
            pass
        
        agent = TestAgent(name="TestAgent")
        
        entry = agent.log_action(
            action_type="test_action",
            description="Testing action logging",
            decision_rationale="For unit testing"
        )
        
        assert entry.agent_id == "TestAgent"
        assert entry.action_type == "test_action"
        assert entry.action_description == "Testing action logging"
        assert entry.decision_rationale == "For unit testing"
        assert len(agent.audit_trail) == 1
    
    def test_log_action_with_evidence_refs(self):
        """Test logging actions with evidence references."""
        class TestAgent(AuditAgent):
            pass
        
        agent = TestAgent(name="TestAgent")
        
        entry = agent.log_action(
            action_type="collect_evidence",
            description="Collected IAM evidence",
            evidence_refs=["EVD-001", "EVD-002"]
        )
        
        assert entry.evidence_refs == ["EVD-001", "EVD-002"]
    
    def test_get_audit_trail(self):
        """Test retrieving the audit trail."""
        class TestAgent(AuditAgent):
            pass
        
        agent = TestAgent(name="TestAgent")
        agent.log_action("action1", "First action")
        agent.log_action("action2", "Second action")
        
        trail = agent.get_audit_trail()
        assert len(trail) == 2
        assert trail[0].action_type == "action1"
        assert trail[1].action_type == "action2"


class TestAuditManagerAgent:
    """Test the AuditManagerAgent (Maurice)."""
    
    def test_maurice_initialization(self):
        """Test that Maurice is initialized correctly."""
        maurice = AuditManagerAgent()
        assert maurice.name == "Maurice"
        assert maurice.audit_trail == []
    
    def test_review_audit_plan(self):
        """Test that Maurice can review and approve an audit plan."""
        maurice = AuditManagerAgent()
        
        # Create a minimal audit plan
        schedule = ExecutionSchedule(
            start_date=datetime.now(),
            end_date=datetime.now(),
            phases=[],
            milestones=[]
        )
        budget = BudgetAllocation(total_hours=100, by_domain={}, by_phase={})
        plan = AuditPlan(
            timeline=schedule,
            budget=budget,
            procedures=[],
            resource_allocation={}
        )
        
        approval = maurice.review_audit_plan(plan)
        
        assert approval["approved"] is True
        assert approval["reviewer"] == "Maurice"
        assert "comments" in approval
        assert len(maurice.audit_trail) == 2  # review + approve actions
    
    def test_approve_budget(self):
        """Test that Maurice can approve a budget."""
        maurice = AuditManagerAgent()
        
        budget = BudgetAllocation(
            total_hours=200,
            by_domain={"IAM": 50, "Encryption": 75, "Network": 75},
            by_phase={"Planning": 20, "Execution": 150, "Reporting": 30}
        )
        
        approval = maurice.approve_budget(budget)
        
        assert approval["approved"] is True
        assert approval["reviewer"] == "Maurice"
        assert approval["total_hours"] == 200
        assert len(maurice.audit_trail) == 2  # review + approve actions
    
    def test_review_workpaper(self):
        """Test that Maurice can review a workpaper."""
        maurice = AuditManagerAgent()
        
        workpaper = Workpaper(
            reference_number="WP-IAM-001",
            control_domain="IAM",
            control_objective="Ensure MFA is enabled",
            testing_procedures=["Check MFA status"],
            evidence_collected=[],
            analysis="MFA not enabled for 2 users",
            conclusion="Control deficiency identified",
            created_by="Esther",
            created_at=datetime.now()
        )
        
        review = maurice.review_workpaper(workpaper)
        
        assert review["workpaper_ref"] == "WP-IAM-001"
        assert review["reviewer"] == "Maurice"
        assert review["status"] == "approved"
        assert len(maurice.audit_trail) == 2  # review + approve actions
    
    def test_sign_off_report(self):
        """Test that Maurice can sign off on the final report."""
        maurice = AuditManagerAgent()
        
        report = AuditReport(
            executive_summary="Test summary",
            scope="AWS IAM and S3",
            methodology="Risk-based audit",
            findings_by_domain={"IAM": [], "S3": []},
            overall_opinion="Qualified opinion",
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
        
        assert sign_off["signed_by"] == "Maurice"
        assert sign_off["status"] == "approved"
        assert "Maurice - Audit Manager" in sign_off["signature"]
        assert len(maurice.audit_trail) == 2  # review + sign_off actions


class TestSeniorAuditorAgent:
    """Test the SeniorAuditorAgent class."""
    
    def test_esther_initialization(self):
        """Test that Esther is initialized correctly."""
        esther = SeniorAuditorAgent(
            name="Esther",
            control_domains=["IAM", "Logical Access"],
            staff_auditor="Hillel"
        )
        
        assert esther.name == "Esther"
        assert esther.control_domains == ["IAM", "Logical Access"]
        assert esther.staff_auditor == "Hillel"
    
    def test_chuck_initialization(self):
        """Test that Chuck is initialized correctly."""
        chuck = SeniorAuditorAgent(
            name="Chuck",
            control_domains=["Data Encryption", "Network Security"],
            staff_auditor="Neil"
        )
        
        assert chuck.name == "Chuck"
        assert chuck.control_domains == ["Data Encryption", "Network Security"]
        assert chuck.staff_auditor == "Neil"
    
    def test_victor_initialization(self):
        """Test that Victor is initialized correctly."""
        victor = SeniorAuditorAgent(
            name="Victor",
            control_domains=["Logging", "Monitoring", "Incident Response"],
            staff_auditor="Juman"
        )
        
        assert victor.name == "Victor"
        assert victor.control_domains == ["Logging", "Monitoring", "Incident Response"]
        assert victor.staff_auditor == "Juman"
    
    def test_supervise_staff(self):
        """Test that senior auditors can assign tasks to staff."""
        esther = SeniorAuditorAgent(
            name="Esther",
            control_domains=["IAM"],
            staff_auditor="Hillel"
        )
        
        task = {
            "description": "Collect IAM user list",
            "service": "IAM",
            "deadline": "Week 3"
        }
        
        assignment = esther.supervise_staff(task)
        
        assert assignment["assigned_by"] == "Esther"
        assert assignment["assigned_to"] == "Hillel"
        assert assignment["task"] == task
        assert len(esther.audit_trail) == 1


class TestStaffAuditorAgent:
    """Test the StaffAuditorAgent class."""
    
    def test_hillel_initialization(self):
        """Test that Hillel is initialized correctly."""
        hillel = StaffAuditorAgent(
            name="Hillel",
            senior_auditor="Esther"
        )
        
        assert hillel.name == "Hillel"
        assert hillel.senior_auditor == "Esther"
    
    def test_neil_initialization(self):
        """Test that Neil is initialized correctly."""
        neil = StaffAuditorAgent(
            name="Neil",
            senior_auditor="Chuck"
        )
        
        assert neil.name == "Neil"
        assert neil.senior_auditor == "Chuck"
    
    def test_juman_initialization(self):
        """Test that Juman is initialized correctly."""
        juman = StaffAuditorAgent(
            name="Juman",
            senior_auditor="Victor"
        )
        
        assert juman.name == "Juman"
        assert juman.senior_auditor == "Victor"
    
    def test_receive_assignment(self):
        """Test that staff auditors can receive assignments."""
        hillel = StaffAuditorAgent(
            name="Hillel",
            senior_auditor="Esther"
        )
        
        task = {
            "description": "Collect IAM evidence",
            "service": "IAM"
        }
        
        hillel.receive_assignment(task)
        
        assert len(hillel.audit_trail) == 1
        assert hillel.audit_trail[0].action_type == "receive_assignment"
        assert hillel.audit_trail[0].agent_id == "Hillel"


class TestAgentNamesVisible:
    """Test that all agent names are visible in logs."""
    
    def test_all_agent_names_logged(self):
        """Test that all agents log their names correctly."""
        maurice = AuditManagerAgent()
        esther = SeniorAuditorAgent("Esther", ["IAM"], "Hillel")
        chuck = SeniorAuditorAgent("Chuck", ["Encryption"], "Neil")
        victor = SeniorAuditorAgent("Victor", ["Logging"], "Juman")
        hillel = StaffAuditorAgent("Hillel", "Esther")
        neil = StaffAuditorAgent("Neil", "Chuck")
        juman = StaffAuditorAgent("Juman", "Victor")
        
        # Each agent logs an action
        maurice.log_action("test", "Maurice action")
        esther.log_action("test", "Esther action")
        chuck.log_action("test", "Chuck action")
        victor.log_action("test", "Victor action")
        hillel.log_action("test", "Hillel action")
        neil.log_action("test", "Neil action")
        juman.log_action("test", "Juman action")
        
        # Verify all names are in their respective audit trails
        assert maurice.audit_trail[0].agent_id == "Maurice"
        assert esther.audit_trail[0].agent_id == "Esther"
        assert chuck.audit_trail[0].agent_id == "Chuck"
        assert victor.audit_trail[0].agent_id == "Victor"
        assert hillel.audit_trail[0].agent_id == "Hillel"
        assert neil.audit_trail[0].agent_id == "Neil"
        assert juman.audit_trail[0].agent_id == "Juman"
