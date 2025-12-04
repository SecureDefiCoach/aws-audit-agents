"""Tests for workflow enforcement gates.

These tests verify that proper audit governance is enforced:
- Staff cannot receive assignments without approved audit plan
- Staff cannot collect evidence without an assignment
- Staff cannot execute tests without evidence and approved plan
"""

import pytest
from datetime import datetime
from src.agents.audit_team import SeniorAuditorAgent, StaffAuditorAgent
from src.models.audit_plan import TestProcedure


class TestWorkflowGates:
    """Test workflow enforcement gates."""
    
    def test_staff_cannot_receive_assignment_without_approved_plan(self):
        """Test that staff auditors cannot receive assignments without approved audit plan."""
        hillel = StaffAuditorAgent("Hillel", "Esther")
        
        task = {
            "description": "Collect IAM evidence",
            "service": "IAM"
        }
        
        # Try to receive assignment without approved plan
        result = hillel.receive_assignment(task, audit_plan_approved=False)
        
        assert result["accepted"] is False
        assert result["blocked"] is True
        assert result["reason"] == "Audit plan not approved"
        assert len(hillel.audit_trail) == 1
        assert hillel.audit_trail[0].action_type == "assignment_blocked"
    
    def test_staff_can_receive_assignment_with_approved_plan(self):
        """Test that staff auditors can receive assignments with approved audit plan."""
        hillel = StaffAuditorAgent("Hillel", "Esther")
        
        task = {
            "description": "Collect IAM evidence",
            "service": "IAM"
        }
        
        # Receive assignment with approved plan
        result = hillel.receive_assignment(task, audit_plan_approved=True)
        
        assert result["accepted"] is True
        assert result["blocked"] is False
        assert result["assigned_to"] == "Hillel"
        assert result["assigned_by"] == "Esther"
        assert len(hillel.audit_trail) == 1
        assert hillel.audit_trail[0].action_type == "receive_assignment"
    
    def test_staff_cannot_collect_evidence_without_assignment(self):
        """Test that staff auditors cannot collect evidence without an assignment."""
        hillel = StaffAuditorAgent("Hillel", "Esther")
        
        # Try to collect evidence without assignment
        evidence = hillel.collect_evidence("IAM", has_assignment=False)
        
        assert evidence is None
        assert len(hillel.audit_trail) == 1
        assert hillel.audit_trail[0].action_type == "evidence_collection_blocked"
    
    def test_staff_can_collect_evidence_with_assignment(self):
        """Test that staff auditors can collect evidence with an assignment."""
        hillel = StaffAuditorAgent("Hillel", "Esther")
        
        # Collect evidence with assignment
        evidence = hillel.collect_evidence("IAM", has_assignment=True)
        
        # Evidence is None because it's a placeholder, but should not be blocked
        assert len(hillel.audit_trail) == 2  # collect_evidence + evidence_collected
        assert hillel.audit_trail[0].action_type == "collect_evidence"
        assert hillel.audit_trail[1].action_type == "evidence_collected"
    
    def test_staff_cannot_execute_test_without_approved_plan(self):
        """Test that staff auditors cannot execute tests without approved audit plan."""
        hillel = StaffAuditorAgent("Hillel", "Esther")
        
        procedure = TestProcedure(
            procedure_id="PROC-001",
            control_domain="IAM",
            control_objective="Test MFA",
            procedure_description="Verify MFA enabled",
            evidence_required=["IAM users"],
            assigned_to="Hillel",
            estimated_hours=4.0
        )
        
        # Try to execute test without approved plan
        result = hillel.execute_test(procedure, has_evidence=True, audit_plan_approved=False)
        
        assert result["blocked"] is True
        assert result["reason"] == "Audit plan not approved"
        assert len(hillel.audit_trail) == 1
        assert hillel.audit_trail[0].action_type == "test_execution_blocked"
    
    def test_staff_cannot_execute_test_without_evidence(self):
        """Test that staff auditors cannot execute tests without evidence."""
        hillel = StaffAuditorAgent("Hillel", "Esther")
        
        procedure = TestProcedure(
            procedure_id="PROC-001",
            control_domain="IAM",
            control_objective="Test MFA",
            procedure_description="Verify MFA enabled",
            evidence_required=["IAM users"],
            assigned_to="Hillel",
            estimated_hours=4.0
        )
        
        # Try to execute test without evidence
        result = hillel.execute_test(procedure, has_evidence=False, audit_plan_approved=True)
        
        assert result["blocked"] is True
        assert result["reason"] == "No evidence collected"
        assert len(hillel.audit_trail) == 1
        assert hillel.audit_trail[0].action_type == "test_execution_blocked"
    
    def test_staff_can_execute_test_with_evidence_and_approved_plan(self):
        """Test that staff auditors can execute tests with evidence and approved plan."""
        hillel = StaffAuditorAgent("Hillel", "Esther")
        
        procedure = TestProcedure(
            procedure_id="PROC-001",
            control_domain="IAM",
            control_objective="Test MFA",
            procedure_description="Verify MFA enabled",
            evidence_required=["IAM users"],
            assigned_to="Hillel",
            estimated_hours=4.0
        )
        
        # Execute test with evidence and approved plan
        result = hillel.execute_test(procedure, has_evidence=True, audit_plan_approved=True)
        
        assert result["blocked"] is False
        assert result["procedure_id"] == "PROC-001"
        assert result["executed_by"] == "Hillel"
        assert len(hillel.audit_trail) == 2  # execute_test + test_complete
    
    def test_senior_cannot_assign_task_without_approved_plan(self):
        """Test that senior auditors cannot assign tasks without approved audit plan."""
        esther = SeniorAuditorAgent("Esther", ["IAM"], "Hillel")
        
        task = {
            "description": "Collect IAM evidence",
            "service": "IAM"
        }
        
        # Try to assign task without approved plan
        result = esther.supervise_staff(task, audit_plan_approved=False)
        
        assert result["blocked"] is True
        assert result["reason"] == "Audit plan not approved"
        assert len(esther.audit_trail) == 1
        assert esther.audit_trail[0].action_type == "task_assignment_blocked"
    
    def test_senior_can_assign_task_with_approved_plan(self):
        """Test that senior auditors can assign tasks with approved audit plan."""
        esther = SeniorAuditorAgent("Esther", ["IAM"], "Hillel")
        
        task = {
            "description": "Collect IAM evidence",
            "service": "IAM"
        }
        
        # Assign task with approved plan
        result = esther.supervise_staff(task, audit_plan_approved=True)
        
        assert result["blocked"] is False
        assert result["assigned_by"] == "Esther"
        assert result["assigned_to"] == "Hillel"
        assert result["audit_plan_approved"] is True
        assert len(esther.audit_trail) == 1
        assert esther.audit_trail[0].action_type == "assign_task"
    
    def test_complete_workflow_with_gates(self):
        """Test complete workflow with all gates enforced."""
        esther = SeniorAuditorAgent("Esther", ["IAM"], "Hillel")
        hillel = StaffAuditorAgent("Hillel", "Esther")
        
        task = {
            "description": "Collect IAM evidence",
            "service": "IAM"
        }
        
        procedure = TestProcedure(
            procedure_id="PROC-001",
            control_domain="IAM",
            control_objective="Test MFA",
            procedure_description="Verify MFA enabled",
            evidence_required=["IAM users"],
            assigned_to="Hillel",
            estimated_hours=4.0
        )
        
        # Step 1: Try to assign without approval - BLOCKED
        result1 = esther.supervise_staff(task, audit_plan_approved=False)
        assert result1["blocked"] is True
        
        # Step 2: Assign with approval - SUCCESS
        result2 = esther.supervise_staff(task, audit_plan_approved=True)
        assert result2["blocked"] is False
        
        # Step 3: Receive assignment with approval - SUCCESS
        result3 = hillel.receive_assignment(task, audit_plan_approved=True)
        assert result3["accepted"] is True
        
        # Step 4: Collect evidence with assignment - SUCCESS
        evidence = hillel.collect_evidence("IAM", has_assignment=True)
        # Evidence is None (placeholder) but not blocked
        
        # Step 5: Execute test with evidence and approval - SUCCESS
        result5 = hillel.execute_test(procedure, has_evidence=True, audit_plan_approved=True)
        assert result5["blocked"] is False
        
        # Verify audit trails
        assert len(esther.audit_trail) == 2  # 1 blocked + 1 successful assignment
        assert len(hillel.audit_trail) == 5  # receive + collect + collected + execute + complete
