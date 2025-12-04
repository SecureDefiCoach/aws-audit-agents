"""Audit team agent classes for performing AWS audits.

This module contains the base classes and specific implementations for the audit team:
- Maurice (Audit Manager)
- Esther, Chuck, Victor (Senior Auditors)
- Hillel, Neil, Juman (Staff Auditors)
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
import logging

from ..models.audit_trail import AuditTrailEntry
from ..models.audit_plan import AuditPlan, BudgetAllocation, TestProcedure
from ..models.risk import RiskAssessment
from ..models.company import CompanyProfile
from ..models.evidence import Evidence, EvidenceRequest
from ..models.finding import Finding
from ..models.workpaper import Workpaper, AuditReport


# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class AuditAction:
    """Represents an action taken by an audit agent."""
    action_type: str
    description: str
    decision_rationale: Optional[str] = None
    evidence_refs: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class AuditAgent(ABC):
    """Base class for all audit agents.
    
    All audit agents have a name and can log their actions to the audit trail.
    This ensures transparency and traceability of all audit activities.
    """
    
    def __init__(self, name: str, time_simulator=None):
        """Initialize the audit agent.
        
        Args:
            name: The agent's name (e.g., "Maurice", "Esther")
            time_simulator: Optional TimeSimulator for simulated timestamps
        """
        self.name = name
        self.time_simulator = time_simulator
        self.audit_trail: List[AuditTrailEntry] = []
        
    def log_action(
        self,
        action_type: str,
        description: str,
        decision_rationale: Optional[str] = None,
        evidence_refs: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> AuditTrailEntry:
        """Log an action to the audit trail.
        
        All agent actions are logged with the agent's name visible for
        transparency and demonstration purposes.
        
        Args:
            action_type: Type of action (e.g., "review", "collect_evidence", "evaluate")
            description: Human-readable description of the action
            decision_rationale: Optional explanation of why this action was taken
            evidence_refs: Optional list of evidence IDs referenced
            metadata: Optional additional metadata
            
        Returns:
            The created AuditTrailEntry
        """
        timestamp = self._get_simulated_time()
        
        entry = AuditTrailEntry(
            timestamp=timestamp,
            agent_id=self.name,
            action_type=action_type,
            action_description=description,
            decision_rationale=decision_rationale,
            evidence_refs=evidence_refs or [],
            metadata=metadata or {}
        )
        
        self.audit_trail.append(entry)
        
        # Log to console with agent name visible
        logger.info(f"[{self.name}] {action_type}: {description}")
        
        return entry
    
    def _get_simulated_time(self) -> datetime:
        """Get the current simulated time or real time if no simulator."""
        if self.time_simulator:
            return self.time_simulator.get_simulated_time()
        return datetime.now()
    
    def get_audit_trail(self) -> List[AuditTrailEntry]:
        """Get all audit trail entries for this agent."""
        return self.audit_trail.copy()


class AuditManagerAgent(AuditAgent):
    """Audit Manager agent (Maurice).
    
    Maurice is responsible for:
    - Reviewing and approving the audit plan
    - Approving budget allocations
    - Reviewing workpapers created by the team
    - Signing off on the final audit report
    """
    
    def __init__(self, time_simulator=None):
        """Initialize Maurice, the Audit Manager."""
        super().__init__(name="Maurice", time_simulator=time_simulator)
        
    def review_audit_plan(self, plan: AuditPlan, company_name: str = "", interactive: bool = False) -> Dict[str, Any]:
        """Review and approve audit plan with optional human-in-the-loop.
        
        This method presents the audit plan for review and approval
        before test execution can begin.
        
        Args:
            plan: The audit plan to review
            company_name: Name of company being audited
            interactive: If True, prompts for human approval. If False, auto-approves (for testing)
            
        Returns:
            Review decision with approval status
        """
        self.log_action(
            action_type="review_audit_plan",
            description=f"Reviewing audit plan for {company_name}: {len(plan.procedures)} test procedures, {plan.budget.total_hours} hours",
            decision_rationale="Ensuring plan covers all high-risk areas and test procedures are appropriate before execution"
        )
        
        # If not interactive, auto-approve for backward compatibility
        if not interactive:
            plan.approved = True
            plan.approved_by = self.name
            plan.approved_at = self._get_simulated_time()
            
            approval = {
                "approved": True,
                "reviewer": self.name,
                "comments": "Audit plan is comprehensive and risk-based. Approved for execution.",
                "reviewed_at": self._get_simulated_time()
            }
            
            self.log_action(
                action_type="approve_audit_plan",
                description="Audit plan approved",
                decision_rationale="Plan adequately addresses identified risks and allocates resources appropriately"
            )
            
            return approval
        
        # Present audit plan summary
        print("\n" + "=" * 80)
        print(f"AUDIT PLAN REVIEW - {company_name}")
        print("=" * 80)
        print(f"\nReviewer: {self.name} (Audit Manager)")
        print(f"Date: {self._get_simulated_time().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        print("TIMELINE:")
        print(f"  Start Date: {plan.timeline.start_date.strftime('%Y-%m-%d')}")
        print(f"  End Date: {plan.timeline.end_date.strftime('%Y-%m-%d')}")
        print(f"  Duration: {(plan.timeline.end_date - plan.timeline.start_date).days} days")
        print(f"  Phases: {len(plan.timeline.phases)}")
        for phase in plan.timeline.phases:
            print(f"    - {phase.phase_name}: {phase.start_date.strftime('%Y-%m-%d')} to {phase.end_date.strftime('%Y-%m-%d')}")
        print()
        
        print("BUDGET:")
        print(f"  Total Hours: {plan.budget.total_hours}")
        print(f"  Allocation by Domain:")
        for domain, hours in sorted(plan.budget.by_domain.items(), key=lambda x: x[1], reverse=True):
            print(f"    - {domain}: {hours} hours")
        print()
        
        print(f"TEST PROCEDURES ({len(plan.procedures)} total):")
        print()
        
        # Group procedures by domain
        by_domain = {}
        for proc in plan.procedures:
            if proc.control_domain not in by_domain:
                by_domain[proc.control_domain] = []
            by_domain[proc.control_domain].append(proc)
        
        for domain, procs in sorted(by_domain.items()):
            print(f"  {domain} ({len(procs)} procedures):")
            for proc in procs:
                print(f"    • {proc.control_objective}")
                print(f"      Procedure: {proc.procedure_description}")
                print(f"      Assigned to: {proc.assigned_to}")
                print(f"      Estimated: {proc.estimated_hours} hours")
                print(f"      Evidence: {', '.join(proc.evidence_required)}")
                print()
        
        print("=" * 80)
        print("APPROVAL REQUIRED")
        print("=" * 80)
        print()
        print("The audit plan must be approved before test execution can begin.")
        print("Review the test procedures above to ensure they are appropriate.")
        print()
        
        # Human-in-the-loop: Get approval
        while True:
            response = input("Do you approve this audit plan? (yes/no/comments): ").strip().lower()
            
            if response in ['yes', 'y', 'approve', 'approved']:
                # Approve the audit plan
                plan.approved = True
                plan.approved_by = self.name
                plan.approved_at = self._get_simulated_time()
                plan.review_comments = "Audit plan approved. Authorized to proceed with test execution."
                
                approval = {
                    "approved": True,
                    "reviewer": self.name,
                    "comments": "Audit plan is comprehensive and risk-based. Approved for execution.",
                    "reviewed_at": self._get_simulated_time(),
                    "procedure_count": len(plan.procedures),
                    "total_hours": plan.budget.total_hours
                }
                
                self.log_action(
                    action_type="approve_audit_plan",
                    description=f"Audit plan approved: {len(plan.procedures)} test procedures authorized for execution",
                    decision_rationale="Plan adequately addresses identified risks and test procedures are appropriate"
                )
                
                print()
                print("✓ Audit plan APPROVED")
                print(f"  Approved by: {self.name}")
                print(f"  Date: {plan.approved_at.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"  Authorized: {len(plan.procedures)} test procedures")
                print()
                
                return approval
                
            elif response in ['no', 'n', 'reject', 'rejected']:
                # Reject the audit plan
                comments = input("Please provide feedback for revision: ").strip()
                
                plan.approved = False
                plan.review_comments = comments
                
                approval = {
                    "approved": False,
                    "reviewer": self.name,
                    "comments": comments,
                    "reviewed_at": self._get_simulated_time(),
                    "action_required": "Revise audit plan based on feedback"
                }
                
                self.log_action(
                    action_type="reject_audit_plan",
                    description="Audit plan requires revision",
                    decision_rationale=f"Feedback: {comments}"
                )
                
                print()
                print("✗ Audit plan REJECTED - Requires revision")
                print(f"  Feedback: {comments}")
                print()
                
                return approval
                
            elif response in ['comments', 'comment', 'c']:
                # Provide comments but continue review
                comment = input("Enter your comments: ").strip()
                print(f"\nComment noted: {comment}\n")
                continue
                
            else:
                print("Invalid response. Please enter 'yes', 'no', or 'comments'")
                continue
    
    def approve_budget(self, budget: BudgetAllocation) -> Dict[str, Any]:
        """Approve the budget allocation.
        
        Args:
            budget: The budget allocation to approve
            
        Returns:
            Approval decision with comments
        """
        self.log_action(
            action_type="review_budget",
            description=f"Reviewing budget allocation of {budget.total_hours} total hours",
            decision_rationale="Ensuring budget is realistic and aligned with audit scope"
        )
        
        approval = {
            "approved": True,
            "reviewer": self.name,
            "total_hours": budget.total_hours,
            "comments": "Budget allocation is reasonable for the scope of work. Approved.",
            "approved_at": self._get_simulated_time()
        }
        
        self.log_action(
            action_type="approve_budget",
            description=f"Budget of {budget.total_hours} hours approved",
            decision_rationale="Budget provides adequate time for thorough testing of high-risk areas"
        )
        
        return approval
    
    def review_workpaper(self, workpaper: Workpaper) -> Dict[str, Any]:
        """Review a workpaper created by the audit team.
        
        Args:
            workpaper: The workpaper to review
            
        Returns:
            Review result with feedback
        """
        self.log_action(
            action_type="review_workpaper",
            description=f"Reviewing workpaper {workpaper.reference_number} for {workpaper.control_domain}",
            decision_rationale="Ensuring workpaper contains sufficient evidence and clear conclusions"
        )
        
        review = {
            "workpaper_ref": workpaper.reference_number,
            "reviewer": self.name,
            "status": "approved",
            "comments": "Workpaper is well-documented with clear evidence trail and sound conclusions.",
            "reviewed_at": self._get_simulated_time()
        }
        
        self.log_action(
            action_type="approve_workpaper",
            description=f"Workpaper {workpaper.reference_number} approved",
            decision_rationale="Evidence supports conclusions and documentation meets professional standards"
        )
        
        return review
    
    def review_risk_assessment(self, risk_assessment: RiskAssessment, company_name: str = "", interactive: bool = False) -> Dict[str, Any]:
        """Review and approve risk assessment with optional human-in-the-loop.
        
        This method presents the risk assessment for review and approval
        before proceeding to audit planning.
        
        Args:
            risk_assessment: The risk assessment to review
            company_name: Name of company being assessed
            interactive: If True, prompts for human approval. If False, auto-approves (for testing)
            
        Returns:
            Review decision with approval status
        """
        from ..models.risk import RiskAssessment
        
        total_risks = len(risk_assessment.inherent_risks)
        high_risks = len([r for r in risk_assessment.residual_risks if r.risk_level == "high"])
        
        self.log_action(
            action_type="review_risk_assessment",
            description=f"Reviewing risk assessment for {company_name}: {total_risks} risks identified, {high_risks} high-risk",
            decision_rationale="Ensuring risk assessment is comprehensive and prioritization is appropriate before creating audit plan"
        )
        
        # If not interactive, auto-approve for backward compatibility
        if not interactive:
            risk_assessment.approved = True
            risk_assessment.approved_by = self.name
            risk_assessment.approved_at = self._get_simulated_time()
            
            review = {
                "approved": True,
                "reviewer": self.name,
                "comments": "Risk assessment is comprehensive and appropriately prioritized. Approved to proceed with audit planning.",
                "reviewed_at": self._get_simulated_time(),
                "high_risk_count": high_risks,
                "total_risk_count": total_risks
            }
            
            self.log_action(
                action_type="approve_risk_assessment",
                description=f"Risk assessment approved: {high_risks} high-risk areas will receive priority attention",
                decision_rationale="Risk assessment provides solid foundation for risk-based audit planning"
            )
            
            return review
        
        # Present risk assessment summary
        print("\n" + "=" * 80)
        print(f"RISK ASSESSMENT REVIEW - {company_name}")
        print("=" * 80)
        print(f"\nReviewer: {self.name} (Audit Manager)")
        print(f"Date: {self._get_simulated_time().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        print("SUMMARY:")
        print(f"  Total Inherent Risks: {len(risk_assessment.inherent_risks)}")
        print(f"  Total Residual Risks: {len(risk_assessment.residual_risks)}")
        print(f"  High-Risk Areas: {high_risks}")
        print(f"  Medium-Risk Areas: {len([r for r in risk_assessment.residual_risks if r.risk_level == 'medium'])}")
        print(f"  Low-Risk Areas: {len([r for r in risk_assessment.residual_risks if r.risk_level == 'low'])}")
        print()
        
        print("PRIORITIZED CONTROL DOMAINS:")
        for i, domain in enumerate(risk_assessment.prioritized_domains, 1):
            print(f"  {i}. {domain.domain_name} - Risk Level: {domain.risk_level.upper()}")
        print()
        
        print("HIGH-RISK ISSUES REQUIRING ATTENTION:")
        high_risk_items = [r for r in risk_assessment.residual_risks if r.risk_level == "high"]
        if high_risk_items:
            for risk in high_risk_items:
                print(f"\n  • {risk.description}")
                print(f"    Domain: {risk.control_domain}")
                print(f"    Impact: {risk.impact.upper()} | Likelihood: {risk.likelihood.upper()}")
        else:
            print("  None identified")
        print()
        
        print("=" * 80)
        print("APPROVAL REQUIRED")
        print("=" * 80)
        print()
        print("The risk assessment must be approved before proceeding to audit planning.")
        print()
        
        # Human-in-the-loop: Get approval
        while True:
            response = input("Do you approve this risk assessment? (yes/no/comments): ").strip().lower()
            
            if response in ['yes', 'y', 'approve', 'approved']:
                # Approve the risk assessment
                risk_assessment.approved = True
                risk_assessment.approved_by = self.name
                risk_assessment.approved_at = self._get_simulated_time()
                risk_assessment.review_comments = "Risk assessment approved. Proceed with audit planning."
                
                review = {
                    "approved": True,
                    "reviewer": self.name,
                    "comments": "Risk assessment is comprehensive and appropriately prioritized. Approved to proceed with audit planning.",
                    "reviewed_at": self._get_simulated_time(),
                    "high_risk_count": high_risks,
                    "total_risk_count": total_risks
                }
                
                self.log_action(
                    action_type="approve_risk_assessment",
                    description=f"Risk assessment approved: {high_risks} high-risk areas will receive priority attention",
                    decision_rationale="Risk assessment provides solid foundation for risk-based audit planning"
                )
                
                print()
                print("✓ Risk assessment APPROVED")
                print(f"  Approved by: {self.name}")
                print(f"  Date: {risk_assessment.approved_at.strftime('%Y-%m-%d %H:%M:%S')}")
                print()
                
                return review
                
            elif response in ['no', 'n', 'reject', 'rejected']:
                # Reject the risk assessment
                comments = input("Please provide feedback for revision: ").strip()
                
                risk_assessment.approved = False
                risk_assessment.review_comments = comments
                
                review = {
                    "approved": False,
                    "reviewer": self.name,
                    "comments": comments,
                    "reviewed_at": self._get_simulated_time(),
                    "action_required": "Revise risk assessment based on feedback"
                }
                
                self.log_action(
                    action_type="reject_risk_assessment",
                    description="Risk assessment requires revision",
                    decision_rationale=f"Feedback: {comments}"
                )
                
                print()
                print("✗ Risk assessment REJECTED - Requires revision")
                print(f"  Feedback: {comments}")
                print()
                
                return review
                
            elif response in ['comments', 'comment', 'c']:
                # Provide comments but continue review
                comment = input("Enter your comments: ").strip()
                print(f"\nComment noted: {comment}\n")
                continue
                
            else:
                print("Invalid response. Please enter 'yes', 'no', or 'comments'")
                continue
    
    def sign_off_report(self, report: AuditReport) -> Dict[str, Any]:
        """Sign off on the final audit report.
        
        Args:
            report: The final audit report
            
        Returns:
            Sign-off with signature
        """
        total_findings = sum(len(findings) for findings in report.findings_by_domain.values())
        
        self.log_action(
            action_type="review_final_report",
            description=f"Reviewing final audit report with {total_findings} findings across {len(report.findings_by_domain)} domains",
            decision_rationale="Final review to ensure report is complete, accurate, and professionally presented"
        )
        
        sign_off = {
            "signed_by": self.name,
            "signature": f"{self.name} - Audit Manager",
            "status": "approved",
            "comments": "Final audit report is complete and ready for distribution.",
            "signed_at": self._get_simulated_time()
        }
        
        self.log_action(
            action_type="sign_off_report",
            description="Final audit report signed off",
            decision_rationale="Report provides clear audit opinion supported by comprehensive evidence and workpapers"
        )
        
        return sign_off


class SeniorAuditorAgent(AuditAgent):
    """Senior Auditor agent (Esther, Chuck, or Victor).
    
    Senior auditors are responsible for:
    - Assessing risk in their assigned control domains
    - Creating audit plans for their areas
    - Supervising staff auditors
    - Collecting evidence (both direct and via requests)
    - Executing testing procedures
    - Evaluating controls and creating findings
    - Creating workpapers
    """
    
    def __init__(
        self,
        name: str,
        control_domains: List[str],
        staff_auditor: str,
        time_simulator=None
    ):
        """Initialize a Senior Auditor.
        
        Args:
            name: The auditor's name ("Esther", "Chuck", or "Victor")
            control_domains: List of control domains this auditor leads
            staff_auditor: Name of the staff auditor reporting to this senior
            time_simulator: Optional TimeSimulator for simulated timestamps
        """
        super().__init__(name=name, time_simulator=time_simulator)
        self.control_domains = control_domains
        self.staff_auditor = staff_auditor
        
    def assess_risk(self, company: CompanyProfile) -> RiskAssessment:
        """Assess risks for the company in assigned control domains.
        
        Performs asset-based risk assessment by:
        1. Identifying information assets in assigned domains
        2. Assessing impact (confidentiality, integrity, availability)
        3. Identifying threats and vulnerabilities
        4. Calculating risk = impact × likelihood
        
        Args:
            company: The company profile to assess
            
        Returns:
            Risk assessment for assigned domains
        """
        from ..models.risk import Risk, ControlDomain
        
        self.log_action(
            action_type="assess_risk",
            description=f"Assessing risks for {company.name} in domains: {', '.join(self.control_domains)}",
            decision_rationale="Analyzing information assets, impact, and vulnerabilities to identify inherent and residual risks"
        )
        
        # Log information assets being assessed
        relevant_assets = [a for a in company.information_assets if self._is_asset_in_domain(a)]
        if relevant_assets:
            asset_summary = ", ".join([f"{a.asset_name} ({a.data_classification})" for a in relevant_assets])
            self.log_action(
                action_type="identify_assets",
                description=f"Identified {len(relevant_assets)} information assets in scope: {asset_summary}",
                decision_rationale="Understanding what assets need protection to assess impact of security issues"
            )
        
        inherent_risks = []
        residual_risks = []
        prioritized_domains = []
        risk_matrix = {}
        
        # Analyze intentional security issues in context of information assets
        for issue in company.intentional_issues:
            if issue.control_domain in self.control_domains:
                # Find affected assets to determine true impact
                affected_assets = [a for a in company.information_assets 
                                 if issue.resource_id in a.location]
                
                # Calculate impact based on affected assets
                if affected_assets:
                    # Use highest impact from affected assets
                    max_impact = self._calculate_asset_impact(affected_assets)
                    impact_level = max_impact
                    asset_names = ", ".join([a.asset_name for a in affected_assets])
                    risk_description = f"{issue.description} - Affects: {asset_names}"
                else:
                    # No specific asset identified, use issue severity
                    impact_level = issue.severity
                    risk_description = issue.description
                
                # Create inherent risk
                inherent_risk = Risk(
                    risk_id=f"RISK-{issue.control_domain}-{len(inherent_risks)+1:03d}",
                    control_domain=issue.control_domain,
                    description=risk_description,
                    impact=impact_level,
                    likelihood="high",  # Intentional issues are likely to be exploited
                    risk_level=impact_level,  # Risk = Impact × Likelihood (high × high = high)
                    mitigation_controls=[]
                )
                inherent_risks.append(inherent_risk)
                
                # Residual risk is same as inherent since controls are weak
                residual_risk = Risk(
                    risk_id=f"RESID-{issue.control_domain}-{len(residual_risks)+1:03d}",
                    control_domain=issue.control_domain,
                    description=f"Residual: {risk_description}",
                    impact=impact_level,
                    likelihood="high",
                    risk_level=impact_level,
                    mitigation_controls=[]
                )
                residual_risks.append(residual_risk)
        
        # Create prioritized control domains based on risk levels
        domain_risk_counts = {}
        for risk in residual_risks:
            domain = risk.control_domain
            if domain not in domain_risk_counts:
                domain_risk_counts[domain] = {"high": 0, "medium": 0, "low": 0}
            domain_risk_counts[domain][risk.risk_level] += 1
        
        # Prioritize domains by risk (high risks first)
        priority = 1
        for domain in self.control_domains:
            if domain in domain_risk_counts:
                counts = domain_risk_counts[domain]
                # Determine overall domain risk level
                if counts["high"] > 0:
                    domain_risk = "high"
                elif counts["medium"] > 0:
                    domain_risk = "medium"
                else:
                    domain_risk = "low"
            else:
                domain_risk = "low"
            
            control_domain = ControlDomain(
                domain_name=domain,
                description=f"Control domain for {domain}",
                priority=priority,
                risk_level=domain_risk,
                control_objectives=[]
            )
            prioritized_domains.append(control_domain)
            risk_matrix[domain] = domain_risk
            priority += 1
        
        # Sort by risk level (high first)
        risk_order = {"high": 0, "medium": 1, "low": 2}
        prioritized_domains.sort(key=lambda d: (risk_order[d.risk_level], d.priority))
        
        # Update priorities after sorting
        for i, domain in enumerate(prioritized_domains):
            domain.priority = i + 1
        
        assessment = RiskAssessment(
            inherent_risks=inherent_risks,
            residual_risks=residual_risks,
            prioritized_domains=prioritized_domains,
            risk_matrix=risk_matrix
        )
        
        self.log_action(
            action_type="risk_assessment_complete",
            description=f"Completed risk assessment: {len(inherent_risks)} inherent risks, {len(residual_risks)} residual risks",
            decision_rationale=f"Identified {len([r for r in residual_risks if r.risk_level == 'high'])} high-risk areas requiring priority attention",
            metadata={
                "company": company.name,
                "domains": self.control_domains,
                "high_risk_count": len([r for r in residual_risks if r.risk_level == "high"]),
                "medium_risk_count": len([r for r in residual_risks if r.risk_level == "medium"]),
                "low_risk_count": len([r for r in residual_risks if r.risk_level == "low"])
            }
        )
        
        return assessment
    
    def create_audit_plan(self, risks: RiskAssessment) -> AuditPlan:
        """Create an audit plan based on risk assessment.
        
        Args:
            risks: The risk assessment results
            
        Returns:
            Audit plan for assigned domains
        """
        from ..models.audit_plan import AuditPhase, Milestone, ExecutionSchedule
        from datetime import timedelta
        import uuid
        
        self.log_action(
            action_type="create_audit_plan",
            description=f"Creating audit plan for domains: {', '.join(self.control_domains)}",
            decision_rationale="Prioritizing testing procedures based on risk levels"
        )
        
        # Create timeline with phases
        start_date = self._get_simulated_time()
        
        # Planning phase (1 week)
        planning_phase = AuditPhase(
            phase_name="Planning",
            start_date=start_date,
            end_date=start_date + timedelta(weeks=1),
            activities=["Risk assessment", "Audit plan creation", "Resource allocation"]
        )
        
        # Fieldwork phase (3 weeks)
        fieldwork_phase = AuditPhase(
            phase_name="Fieldwork",
            start_date=planning_phase.end_date,
            end_date=planning_phase.end_date + timedelta(weeks=3),
            activities=["Evidence collection", "Testing procedures", "Control evaluation"]
        )
        
        # Reporting phase (2 weeks)
        reporting_phase = AuditPhase(
            phase_name="Reporting",
            start_date=fieldwork_phase.end_date,
            end_date=fieldwork_phase.end_date + timedelta(weeks=2),
            activities=["Workpaper creation", "Report drafting", "Management review"]
        )
        
        # Create milestones
        milestones = [
            Milestone(
                milestone_name="Risk Assessment Complete",
                target_date=planning_phase.end_date,
                description="Complete risk assessment and finalize audit plan"
            ),
            Milestone(
                milestone_name="Evidence Collection Complete",
                target_date=fieldwork_phase.start_date + timedelta(weeks=2),
                description="Complete evidence collection for all control domains"
            ),
            Milestone(
                milestone_name="Testing Complete",
                target_date=fieldwork_phase.end_date,
                description="Complete all testing procedures and control evaluations"
            ),
            Milestone(
                milestone_name="Draft Report Complete",
                target_date=reporting_phase.end_date - timedelta(weeks=1),
                description="Complete draft audit report for review"
            )
        ]
        
        schedule = ExecutionSchedule(
            start_date=start_date,
            end_date=reporting_phase.end_date,
            phases=[planning_phase, fieldwork_phase, reporting_phase],
            milestones=milestones
        )
        
        # Allocate budget based on risk levels
        total_hours = 0.0
        by_domain = {}
        
        for domain in risks.prioritized_domains:
            if domain.domain_name in self.control_domains:
                # Allocate more hours to high-risk domains
                if domain.risk_level == "high":
                    hours = 40.0
                elif domain.risk_level == "medium":
                    hours = 24.0
                else:
                    hours = 16.0
                
                by_domain[domain.domain_name] = hours
                total_hours += hours
        
        by_phase = {
            "Planning": total_hours * 0.15,
            "Fieldwork": total_hours * 0.65,
            "Reporting": total_hours * 0.20
        }
        
        budget = BudgetAllocation(
            total_hours=total_hours,
            by_domain=by_domain,
            by_phase=by_phase
        )
        
        # Create testing procedures for each domain
        procedures = []
        for domain in risks.prioritized_domains:
            if domain.domain_name in self.control_domains:
                # Create procedures based on domain
                if "IAM" in domain.domain_name or "Logical Access" in domain.domain_name:
                    procedures.extend([
                        TestProcedure(
                            procedure_id=str(uuid.uuid4()),
                            control_domain=domain.domain_name,
                            control_objective="Verify MFA is enabled for all users",
                            procedure_description="Review IAM users and verify MFA device configuration",
                            evidence_required=["IAM user list", "MFA device status"],
                            assigned_to=self.staff_auditor,
                            estimated_hours=4.0
                        ),
                        TestProcedure(
                            procedure_id=str(uuid.uuid4()),
                            control_domain=domain.domain_name,
                            control_objective="Verify least privilege access",
                            procedure_description="Review IAM policies for overly permissive permissions",
                            evidence_required=["IAM policies", "User permissions"],
                            assigned_to=self.name,
                            estimated_hours=6.0
                        )
                    ])
                elif "Encryption" in domain.domain_name or "Data" in domain.domain_name:
                    procedures.extend([
                        TestProcedure(
                            procedure_id=str(uuid.uuid4()),
                            control_domain=domain.domain_name,
                            control_objective="Verify S3 bucket encryption",
                            procedure_description="Review S3 buckets and verify encryption is enabled",
                            evidence_required=["S3 bucket list", "Encryption configuration"],
                            assigned_to=self.staff_auditor,
                            estimated_hours=4.0
                        )
                    ])
                elif "Network" in domain.domain_name:
                    procedures.extend([
                        TestProcedure(
                            procedure_id=str(uuid.uuid4()),
                            control_domain=domain.domain_name,
                            control_objective="Verify security group configurations",
                            procedure_description="Review security groups for unrestricted access",
                            evidence_required=["Security group rules", "Network configurations"],
                            assigned_to=self.staff_auditor,
                            estimated_hours=5.0
                        )
                    ])
                elif "Logging" in domain.domain_name or "Monitoring" in domain.domain_name:
                    procedures.extend([
                        TestProcedure(
                            procedure_id=str(uuid.uuid4()),
                            control_domain=domain.domain_name,
                            control_objective="Verify CloudTrail is enabled",
                            procedure_description="Review CloudTrail configuration and logging status",
                            evidence_required=["CloudTrail status", "Log configuration"],
                            assigned_to=self.staff_auditor,
                            estimated_hours=3.0
                        )
                    ])
        
        resource_allocation = by_domain.copy()
        
        plan = AuditPlan(
            timeline=schedule,
            budget=budget,
            procedures=procedures,
            resource_allocation=resource_allocation
        )
        
        self.log_action(
            action_type="audit_plan_created",
            description=f"Audit plan created: {len(procedures)} procedures, {total_hours} total hours, {len(self.control_domains)} domains",
            decision_rationale=f"Allocated more resources to high-risk domains: {', '.join([d.domain_name for d in risks.prioritized_domains if d.risk_level == 'high'])}",
            metadata={
                "total_hours": total_hours,
                "procedure_count": len(procedures),
                "domain_count": len(self.control_domains),
                "timeline_weeks": 6
            }
        )
        
        return plan
    
    def supervise_staff(self, task: Dict[str, Any], audit_plan_approved: bool = True) -> Dict[str, Any]:
        """Assign a task to the staff auditor.
        
        Args:
            task: Task details to assign
            audit_plan_approved: Whether the audit plan has been approved (default True for backward compatibility)
            
        Returns:
            Assignment confirmation
        """
        # Check if audit plan is approved before assigning tasks
        if not audit_plan_approved:
            self.log_action(
                action_type="task_assignment_blocked",
                description=f"Cannot assign task to {self.staff_auditor}: {task.get('description', 'N/A')}",
                decision_rationale="Audit plan must be approved before assigning tasks to staff"
            )
            return {
                "assigned_by": self.name,
                "assigned_to": self.staff_auditor,
                "task": task,
                "blocked": True,
                "reason": "Audit plan not approved"
            }
        
        self.log_action(
            action_type="assign_task",
            description=f"Assigning task to {self.staff_auditor}: {task.get('description', 'N/A')}",
            decision_rationale=f"Delegating evidence collection to {self.staff_auditor} for efficiency",
            metadata={"assigned_to": self.staff_auditor, "task": task}
        )
        
        assignment = {
            "assigned_by": self.name,
            "assigned_to": self.staff_auditor,
            "task": task,
            "assigned_at": self._get_simulated_time(),
            "blocked": False,
            "audit_plan_approved": audit_plan_approved
        }
        
        return assignment
    
    def collect_evidence_direct(self, service: str, control_domain: str = None) -> Evidence:
        """Collect evidence directly from an AWS service.
        
        Args:
            service: AWS service name (e.g., "CloudTrail", "VPC", "S3", "EC2")
            control_domain: Optional control domain for evidence organization
            
        Returns:
            Collected evidence
        """
        import uuid
        from ..aws.iam_client import IAMClient
        from ..aws.s3_client import S3Client
        from ..aws.ec2_client import EC2Client
        from ..aws.vpc_client import VPCClient
        from ..aws.cloudtrail_client import CloudTrailClient
        
        self.log_action(
            action_type="collect_evidence",
            description=f"Collecting evidence directly from {service}",
            decision_rationale=f"Direct collection appropriate for {service} evidence"
        )
        
        evidence_data = {}
        evidence_id = f"EVD-{service.upper()}-{uuid.uuid4().hex[:8]}"
        
        try:
            if service.lower() == "iam":
                client = IAMClient()
                evidence_data = {
                    "users": client.list_users(),
                    "roles": client.list_roles(),
                    "account_summary": client.get_account_summary()
                }
                # Get MFA status for each user
                mfa_status = {}
                for user in evidence_data["users"]:
                    user_name = user.get("UserName")
                    mfa_devices = client.list_mfa_devices(user_name)
                    mfa_status[user_name] = len(mfa_devices) > 0
                evidence_data["mfa_status"] = mfa_status
                
            elif service.lower() == "s3":
                client = S3Client()
                buckets = client.list_buckets()
                evidence_data = {"buckets": []}
                for bucket in buckets:
                    bucket_name = bucket.get("Name")
                    bucket_info = {
                        "name": bucket_name,
                        "creation_date": str(bucket.get("CreationDate")),
                        "encryption": client.get_bucket_encryption(bucket_name),
                        "versioning": client.get_bucket_versioning(bucket_name),
                        "logging": client.get_bucket_logging(bucket_name),
                        "public_access_block": client.get_public_access_block(bucket_name)
                    }
                    evidence_data["buckets"].append(bucket_info)
                    
            elif service.lower() == "ec2":
                client = EC2Client()
                evidence_data = {
                    "instances": client.describe_instances(),
                    "security_groups": client.describe_security_groups(),
                    "volumes": client.describe_volumes()
                }
                
            elif service.lower() == "vpc":
                client = VPCClient()
                evidence_data = {
                    "vpcs": client.describe_vpcs(),
                    "subnets": client.describe_subnets(),
                    "route_tables": client.describe_route_tables(),
                    "security_groups": client.describe_security_groups(),
                    "network_acls": client.describe_network_acls()
                }
                
            elif service.lower() == "cloudtrail":
                client = CloudTrailClient()
                trails = client.describe_trails()
                evidence_data = {"trails": []}
                for trail in trails:
                    trail_name = trail.get("Name")
                    trail_info = {
                        "name": trail_name,
                        "arn": trail.get("TrailARN"),
                        "status": client.get_trail_status(trail_name),
                        "event_selectors": client.get_event_selectors(trail_name)
                    }
                    evidence_data["trails"].append(trail_info)
                # Get recent events
                evidence_data["recent_events"] = client.lookup_events(max_results=10)
                
            else:
                self.log_action(
                    action_type="evidence_collection_error",
                    description=f"Unknown service: {service}",
                    decision_rationale="Service not supported for evidence collection"
                )
                return None
                
        except Exception as e:
            self.log_action(
                action_type="evidence_collection_error",
                description=f"Error collecting evidence from {service}: {str(e)}",
                decision_rationale="Continuing with remaining evidence collection despite error"
            )
            evidence_data = {"error": str(e), "service": service}
        
        evidence = Evidence(
            evidence_id=evidence_id,
            source=service,
            collection_method="direct",
            collected_at=self._get_simulated_time(),
            collected_by=self.name,
            data=evidence_data,
            storage_path=f"evidence/{service.lower()}/{evidence_id}.json",
            control_domain=control_domain
        )
        
        self.log_action(
            action_type="evidence_collected",
            description=f"Evidence collected from {service}: {len(evidence_data)} data points",
            decision_rationale=f"Evidence stored for analysis in {control_domain or 'general'} domain",
            evidence_refs=[evidence_id],
            metadata={"service": service, "method": "direct", "evidence_id": evidence_id}
        )
        
        return evidence
    
    def request_evidence(self, request: EvidenceRequest) -> str:
        """Request evidence from an auditee agent.
        
        Args:
            request: Evidence request details
            
        Returns:
            Request ID for tracking
        """
        self.log_action(
            action_type="request_evidence",
            description=f"Requesting evidence for {request.control_domain}: {', '.join(request.requested_items)}",
            decision_rationale="Using auditee agent to demonstrate agent-to-agent evidence collection",
            metadata={"request_id": request.request_id, "items": request.requested_items}
        )
        
        return request.request_id
    
    def execute_test(self, procedure: TestProcedure, evidence: Evidence, audit_plan_approved: bool = True) -> Dict[str, Any]:
        """Execute a testing procedure using collected evidence.
        
        Args:
            procedure: The testing procedure to execute
            evidence: Evidence to analyze
            audit_plan_approved: Whether the audit plan has been approved (default True for backward compatibility)
            
        Returns:
            Test results with pass/fail status and details
        """
        # Check if audit plan is approved before executing
        if not audit_plan_approved:
            self.log_action(
                action_type="test_execution_blocked",
                description=f"Cannot execute test: {procedure.procedure_description}",
                decision_rationale="Audit plan must be approved before test execution can begin"
            )
            return {
                "procedure_id": procedure.procedure_id,
                "executed_by": self.name,
                "executed_at": self._get_simulated_time(),
                "passed": False,
                "findings": ["Test execution blocked - audit plan not approved"],
                "affected_resources": [],
                "blocked": True
            }
        
        self.log_action(
            action_type="execute_test",
            description=f"Executing test procedure: {procedure.procedure_description}",
            decision_rationale=f"Testing {procedure.control_objective}",
            evidence_refs=[evidence.evidence_id] if evidence else []
        )
        
        test_result = {
            "procedure_id": procedure.procedure_id,
            "control_domain": procedure.control_domain,
            "control_objective": procedure.control_objective,
            "procedure_description": procedure.procedure_description,
            "executed_by": self.name,
            "executed_at": self._get_simulated_time(),
            "evidence_id": evidence.evidence_id if evidence else None,
            "passed": False,
            "findings": [],
            "affected_resources": []
        }
        
        if not evidence or not evidence.data:
            test_result["findings"].append("No evidence available for testing")
            self.log_action(
                action_type="test_complete",
                description=f"Test incomplete - no evidence available",
                metadata=test_result
            )
            return test_result
        
        # Execute test based on control objective
        if "MFA" in procedure.control_objective:
            # Test MFA enablement
            mfa_status = evidence.data.get("mfa_status", {})
            users_without_mfa = [user for user, has_mfa in mfa_status.items() if not has_mfa]
            
            if users_without_mfa:
                test_result["passed"] = False
                test_result["findings"].append(f"{len(users_without_mfa)} users without MFA enabled")
                test_result["affected_resources"] = users_without_mfa
            else:
                test_result["passed"] = True
                test_result["findings"].append("All users have MFA enabled")
                
        elif "least privilege" in procedure.control_objective.lower():
            # Test for overly permissive policies
            users = evidence.data.get("users", [])
            overly_permissive = []
            
            for user in users:
                user_name = user.get("UserName", "")
                # Check if user has admin-like permissions (simplified check)
                if "admin" in user_name.lower() or "root" in user_name.lower():
                    overly_permissive.append(user_name)
            
            if overly_permissive:
                test_result["passed"] = False
                test_result["findings"].append(f"{len(overly_permissive)} users with potentially excessive permissions")
                test_result["affected_resources"] = overly_permissive
            else:
                test_result["passed"] = True
                test_result["findings"].append("No overly permissive user accounts identified")
                
        elif "encryption" in procedure.control_objective.lower():
            # Test S3 bucket encryption
            buckets = evidence.data.get("buckets", [])
            unencrypted_buckets = []
            
            for bucket in buckets:
                if not bucket.get("encryption"):
                    unencrypted_buckets.append(bucket.get("name"))
            
            if unencrypted_buckets:
                test_result["passed"] = False
                test_result["findings"].append(f"{len(unencrypted_buckets)} buckets without encryption")
                test_result["affected_resources"] = unencrypted_buckets
            else:
                test_result["passed"] = True
                test_result["findings"].append("All buckets have encryption enabled")
                
        elif "security group" in procedure.control_objective.lower():
            # Test security group configurations
            security_groups = evidence.data.get("security_groups", [])
            unrestricted_groups = []
            
            for sg in security_groups:
                for rule in sg.get("IpPermissions", []):
                    for ip_range in rule.get("IpRanges", []):
                        if ip_range.get("CidrIp") == "0.0.0.0/0":
                            unrestricted_groups.append(sg.get("GroupId"))
                            break
            
            if unrestricted_groups:
                test_result["passed"] = False
                test_result["findings"].append(f"{len(unrestricted_groups)} security groups with unrestricted access")
                test_result["affected_resources"] = list(set(unrestricted_groups))
            else:
                test_result["passed"] = True
                test_result["findings"].append("No security groups with unrestricted access")
                
        elif "CloudTrail" in procedure.control_objective:
            # Test CloudTrail enablement
            trails = evidence.data.get("trails", [])
            active_trails = [t for t in trails if t.get("status", {}).get("IsLogging")]
            
            if not active_trails:
                test_result["passed"] = False
                test_result["findings"].append("CloudTrail is not enabled or not logging")
                test_result["affected_resources"] = ["CloudTrail"]
            else:
                test_result["passed"] = True
                test_result["findings"].append(f"CloudTrail is enabled with {len(active_trails)} active trail(s)")
        
        else:
            # Generic test - just check if evidence exists
            test_result["passed"] = True
            test_result["findings"].append("Evidence collected and reviewed")
        
        self.log_action(
            action_type="test_complete",
            description=f"Test {'passed' if test_result['passed'] else 'failed'} for {procedure.control_domain}: {', '.join(test_result['findings'])}",
            decision_rationale=f"Test results based on analysis of {evidence.source} evidence",
            evidence_refs=[evidence.evidence_id],
            metadata={
                "passed": test_result["passed"],
                "finding_count": len(test_result["findings"]),
                "affected_resource_count": len(test_result["affected_resources"])
            }
        )
        
        return test_result
    
    def evaluate_control(self, test_result: Dict[str, Any]) -> Finding:
        """Evaluate a control based on test results.
        
        Args:
            test_result: Results from testing procedure
            
        Returns:
            Finding (pass or fail)
        """
        import uuid
        
        self.log_action(
            action_type="evaluate_control",
            description=f"Evaluating control for {test_result.get('control_domain')}: {test_result.get('control_objective')}",
            decision_rationale="Comparing test results against control criteria"
        )
        
        # Determine risk rating based on findings
        affected_count = len(test_result.get("affected_resources", []))
        passed = test_result.get("passed", False)
        
        if not passed:
            if affected_count > 5:
                risk_rating = "high"
            elif affected_count > 2:
                risk_rating = "medium"
            else:
                risk_rating = "low"
        else:
            risk_rating = "low"
        
        # Create recommendations based on findings
        recommendations = []
        if not passed:
            findings_text = "; ".join(test_result.get("findings", []))
            
            if "MFA" in test_result.get("control_objective", ""):
                recommendations.append("Enable MFA for all IAM users")
                recommendations.append("Implement MFA enforcement policy")
            elif "encryption" in test_result.get("control_objective", "").lower():
                recommendations.append("Enable default encryption for all S3 buckets")
                recommendations.append("Review and update bucket policies to require encryption")
            elif "security group" in test_result.get("control_objective", "").lower():
                recommendations.append("Restrict security group rules to specific IP ranges")
                recommendations.append("Remove 0.0.0.0/0 access from security groups")
            elif "CloudTrail" in test_result.get("control_objective", ""):
                recommendations.append("Enable CloudTrail in all regions")
                recommendations.append("Configure CloudTrail log file validation")
            else:
                recommendations.append(f"Address identified issues: {findings_text}")
        else:
            recommendations.append("Continue monitoring control effectiveness")
        
        finding = Finding(
            finding_id=f"FIND-{uuid.uuid4().hex[:8].upper()}",
            control_domain=test_result.get("control_domain", "Unknown"),
            control_objective=test_result.get("control_objective", "Unknown"),
            test_procedure=test_result.get("procedure_description", "Unknown"),
            result="pass" if passed else "fail",
            evidence_refs=[test_result.get("evidence_id")] if test_result.get("evidence_id") else [],
            affected_resources=test_result.get("affected_resources", []),
            risk_rating=risk_rating,
            recommendations=recommendations,
            created_by=self.name,
            created_at=self._get_simulated_time()
        )
        
        self.log_action(
            action_type="evaluation_complete",
            description=f"Control evaluation complete: {finding.result.upper()} - Risk: {risk_rating.upper()}",
            decision_rationale=f"Based on test results, control is {'effective' if passed else 'ineffective'} with {risk_rating} risk",
            evidence_refs=finding.evidence_refs,
            metadata={
                "finding_id": finding.finding_id,
                "result": finding.result,
                "risk_rating": risk_rating,
                "affected_resource_count": len(finding.affected_resources)
            }
        )
        
        return finding
    
    def create_workpaper(self, finding: Finding, evidence_list: List[Evidence] = None) -> Workpaper:
        """Create a workpaper documenting the finding.
        
        Args:
            finding: The finding to document
            evidence_list: Optional list of evidence objects referenced in the finding
            
        Returns:
            Created workpaper
        """
        self.log_action(
            action_type="create_workpaper",
            description=f"Creating workpaper for {finding.control_domain} - {finding.result}",
            decision_rationale="Documenting testing procedures, evidence, and conclusions",
            evidence_refs=finding.evidence_refs
        )
        
        # Generate workpaper reference number
        domain_abbrev = "".join([word[0] for word in finding.control_domain.split()]).upper()
        if len(domain_abbrev) > 3:
            domain_abbrev = domain_abbrev[:3]
        
        # Use finding ID for uniqueness
        ref_number = f"WP-{domain_abbrev}-{finding.finding_id[-6:]}"
        
        # Create analysis text
        if finding.result == "pass":
            analysis = f"""
Control Objective: {finding.control_objective}

Testing Performed:
{finding.test_procedure}

Evidence Reviewed:
- Evidence IDs: {', '.join(finding.evidence_refs)}
- Collection method: Direct AWS API access
- Collected by: {finding.created_by}

Analysis:
Testing procedures were executed to evaluate the effectiveness of controls related to {finding.control_domain}.
The evidence collected demonstrates that the control objective is being met.

Observations:
- No deficiencies identified
- Control is operating effectively
- {len(finding.evidence_refs)} piece(s) of evidence support this conclusion
"""
            conclusion = f"Based on testing performed, the control for '{finding.control_objective}' is EFFECTIVE. No exceptions noted."
        else:
            analysis = f"""
Control Objective: {finding.control_objective}

Testing Performed:
{finding.test_procedure}

Evidence Reviewed:
- Evidence IDs: {', '.join(finding.evidence_refs)}
- Collection method: Direct AWS API access
- Collected by: {finding.created_by}

Analysis:
Testing procedures were executed to evaluate the effectiveness of controls related to {finding.control_domain}.
The evidence collected indicates control deficiencies that require management attention.

Deficiencies Identified:
- {len(finding.affected_resources)} affected resource(s)
- Risk Rating: {finding.risk_rating.upper()}
- Affected Resources: {', '.join(finding.affected_resources[:5])}{'...' if len(finding.affected_resources) > 5 else ''}

Recommendations:
{chr(10).join([f'- {rec}' for rec in finding.recommendations])}
"""
            conclusion = f"Based on testing performed, the control for '{finding.control_objective}' is INEFFECTIVE. {len(finding.affected_resources)} exception(s) noted with {finding.risk_rating} risk rating."
        
        workpaper = Workpaper(
            reference_number=ref_number,
            control_domain=finding.control_domain,
            control_objective=finding.control_objective,
            testing_procedures=[finding.test_procedure],
            evidence_collected=evidence_list or [],
            analysis=analysis.strip(),
            conclusion=conclusion,
            created_by=self.name,
            created_at=self._get_simulated_time(),
            cross_references=[]
        )
        
        # Update finding with workpaper reference
        finding.workpaper_ref = ref_number
        
        self.log_action(
            action_type="workpaper_created",
            description=f"Workpaper {ref_number} created for {finding.control_domain}: {finding.result.upper()}",
            decision_rationale=f"Documented {'effective' if finding.result == 'pass' else 'ineffective'} control with supporting evidence and {'recommendations' if finding.result == 'fail' else 'observations'}",
            evidence_refs=finding.evidence_refs,
            metadata={
                "workpaper_ref": ref_number,
                "finding_id": finding.finding_id,
                "result": finding.result,
                "risk_rating": finding.risk_rating
            }
        )
        
        return workpaper
    
    def _is_asset_in_domain(self, asset) -> bool:
        """Check if an information asset is relevant to this auditor's domains."""
        # Map asset types to control domains
        domain_mappings = {
            "IAM User": ["IAM", "Logical Access"],
            "S3 Bucket": ["Data Encryption", "Logging"],
            "EC2 Instance": ["Network Security", "Asset Management"],
            "Application": ["Network Security", "Data Encryption"],
            "Database": ["Data Encryption", "Disaster Recovery"]
        }
        
        asset_domains = domain_mappings.get(asset.asset_type, [])
        return any(domain in self.control_domains for domain in asset_domains)
    
    def _calculate_asset_impact(self, assets) -> str:
        """Calculate the highest impact level from a list of assets."""
        impact_order = {"high": 3, "medium": 2, "low": 1}
        max_impact = "low"
        max_score = 0
        
        for asset in assets:
            # Consider all three impact types (CIA triad)
            for impact in [asset.confidentiality_impact, asset.integrity_impact, asset.availability_impact]:
                score = impact_order.get(impact, 0)
                if score > max_score:
                    max_score = score
                    max_impact = impact
        
        return max_impact


class StaffAuditorAgent(AuditAgent):
    """Staff Auditor agent (Hillel, Neil, or Juman).
    
    Staff auditors are responsible for:
    - Receiving assignments from their senior auditor
    - Collecting evidence from AWS services
    - Executing testing procedures
    - Documenting findings
    """
    
    def __init__(
        self,
        name: str,
        senior_auditor: str,
        time_simulator=None
    ):
        """Initialize a Staff Auditor.
        
        Args:
            name: The auditor's name ("Hillel", "Neil", or "Juman")
            senior_auditor: Name of the senior auditor this staff reports to
            time_simulator: Optional TimeSimulator for simulated timestamps
        """
        super().__init__(name=name, time_simulator=time_simulator)
        self.senior_auditor = senior_auditor
        
    def receive_assignment(self, task: Dict[str, Any], audit_plan_approved: bool = True) -> Dict[str, Any]:
        """Receive a task assignment from senior auditor.
        
        Args:
            task: Task details assigned by senior auditor
            audit_plan_approved: Whether the audit plan has been approved (default True for backward compatibility)
            
        Returns:
            Assignment result with status
        """
        # Check if audit plan is approved before accepting assignment
        if not audit_plan_approved:
            self.log_action(
                action_type="assignment_blocked",
                description=f"Cannot accept assignment from {self.senior_auditor}: {task.get('description', 'N/A')}",
                decision_rationale="Audit plan must be approved before staff can receive assignments"
            )
            return {
                "accepted": False,
                "blocked": True,
                "reason": "Audit plan not approved",
                "task": task
            }
        
        self.log_action(
            action_type="receive_assignment",
            description=f"Received assignment from {self.senior_auditor}: {task.get('description', 'N/A')}",
            decision_rationale=f"Accepting task assignment from {self.senior_auditor}",
            metadata={"assigned_by": self.senior_auditor, "task": task}
        )
        
        return {
            "accepted": True,
            "blocked": False,
            "task": task,
            "assigned_to": self.name,
            "assigned_by": self.senior_auditor
        }
    
    def collect_evidence(self, service: str, has_assignment: bool = True) -> Evidence:
        """Collect evidence from an AWS service.
        
        Args:
            service: AWS service name
            has_assignment: Whether staff has received an approved assignment (default True for backward compatibility)
            
        Returns:
            Collected evidence or None if blocked
        """
        # Check if staff has an approved assignment before collecting evidence
        if not has_assignment:
            self.log_action(
                action_type="evidence_collection_blocked",
                description=f"Cannot collect evidence from {service}",
                decision_rationale="Staff must have an approved assignment before collecting evidence"
            )
            return None
        
        self.log_action(
            action_type="collect_evidence",
            description=f"Collecting evidence from {service}",
            decision_rationale=f"Gathering evidence as assigned by {self.senior_auditor}"
        )
        
        # Placeholder - actual implementation in later tasks
        self.log_action(
            action_type="evidence_collected",
            description=f"Evidence collected from {service}",
            metadata={"service": service, "collected_by": self.name}
        )
        
        return None
    
    def execute_test(self, procedure: TestProcedure, has_evidence: bool = True, audit_plan_approved: bool = True) -> Dict[str, Any]:
        """Execute a testing procedure.
        
        Args:
            procedure: The testing procedure to execute
            has_evidence: Whether evidence has been collected (default True for backward compatibility)
            audit_plan_approved: Whether the audit plan has been approved (default True for backward compatibility)
            
        Returns:
            Test results
        """
        # Check if audit plan is approved before executing tests
        if not audit_plan_approved:
            self.log_action(
                action_type="test_execution_blocked",
                description=f"Cannot execute test: {procedure.procedure_description}",
                decision_rationale="Audit plan must be approved before test execution"
            )
            return {
                "procedure_id": procedure.procedure_id,
                "executed_by": self.name,
                "executed_at": self._get_simulated_time(),
                "blocked": True,
                "reason": "Audit plan not approved"
            }
        
        # Check if evidence has been collected before executing tests
        if not has_evidence:
            self.log_action(
                action_type="test_execution_blocked",
                description=f"Cannot execute test: {procedure.procedure_description}",
                decision_rationale="Evidence must be collected before test execution"
            )
            return {
                "procedure_id": procedure.procedure_id,
                "executed_by": self.name,
                "executed_at": self._get_simulated_time(),
                "blocked": True,
                "reason": "No evidence collected"
            }
        
        self.log_action(
            action_type="execute_test",
            description=f"Executing test: {procedure.procedure_description}",
            decision_rationale=f"Performing testing as assigned by {self.senior_auditor}"
        )
        
        # Placeholder - actual implementation in later tasks
        test_result = {
            "procedure_id": procedure.procedure_id,
            "executed_by": self.name,
            "executed_at": self._get_simulated_time(),
            "blocked": False
        }
        
        self.log_action(
            action_type="test_complete",
            description=f"Test completed for {procedure.control_domain}",
            metadata=test_result
        )
        
        return test_result
    
    def document_finding(self, result: Dict[str, Any]) -> Finding:
        """Document a finding based on test results.
        
        Args:
            result: Test result to document
            
        Returns:
            Documented finding
        """
        self.log_action(
            action_type="document_finding",
            description="Documenting test results as finding",
            decision_rationale="Creating initial finding documentation for senior auditor review"
        )
        
        # Placeholder - actual implementation in later tasks
        self.log_action(
            action_type="finding_documented",
            description="Finding documented and ready for review"
        )
        
        return None
