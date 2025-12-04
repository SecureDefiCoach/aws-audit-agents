# Major Phases of Audit Execution

## Overview

This document outlines the major phases of a professional IT audit execution, specifically for AWS infrastructure audits. These phases follow industry-standard audit methodology and ensure comprehensive, evidence-based audit work.

---

## Phase 1: Risk Assessment & Planning

### 1.1 Understanding the Business
**Owner**: Maurice (Audit Manager) + Esther (Senior Auditor)

**Activities**:
- Review company's business model and operations
- Identify critical business processes relying on AWS
- Understand company's risk appetite and tolerance
- Review prior audit findings (if any)

**Key Questions**:
- What does the company do?
- What AWS services are critical to operations?
- What are the biggest risks to the business?
- What regulatory requirements apply?

**Deliverable**: Business context documentation

---

### 1.2 Company Inventory Request
**Owner**: Esther (Senior Auditor)
**Collaborator**: Chuck (IT Manager)

**Activities**:
- Request complete inventory of AWS infrastructure
- Ask for: AWS services in use, data classifications, critical systems, user populations
- Understand AWS footprint and architecture
- Document company's security posture

**Evidence Collected**:
- AWS service inventory
- Architecture diagrams
- User and role listings
- Data classification matrix

**Deliverable**: AWS environment inventory

---

### 1.3 Risk Assessment
**Owner**: Esther (Senior Auditor)

**Activities**:
- Assess risks across all control domains:
  - **IAM & Logical Access**: Unauthorized access, excessive privileges, lack of MFA
  - **Data Protection**: Unencrypted data, poor key management, data exposure
  - **Network Security**: Overly permissive security groups, public exposure
  - **Logging & Monitoring**: Missing CloudTrail, insufficient retention, no alerting
  - **Change Management**: Uncontrolled changes, no approval process

**Risk Scoring**:
- **Likelihood** (1-5): Remote → Almost Certain
- **Impact** (1-5): Negligible → Critical
- **Risk Score** = Likelihood × Impact
- **Risk Levels**: 
  - 1-5: Low
  - 6-12: Medium
  - 13-20: High
  - 21-25: Critical

**Key Decisions**:
- Calculate risk scores for all control areas
- Consider budget constraints
- **Select 3-5 high-risk controls for testing**
- Document rationale for control selection

**Deliverable**: Risk Assessment Workpaper (WP-RISK-001)

---

### 1.4 Risk Assessment Review & Approval
**Owner**: Maurice (Audit Manager)
**Reviewer**: Esther (Senior Auditor)

**Activities**:
- Review Esther's risk assessment for completeness
- Evaluate control selection considering:
  - Risk scores
  - Budget constraints
  - Coverage across domains
  - Materiality
- Discuss and reach agreement on final control selection
- **Approve final set of 3-5 controls to test**

**Critical Checkpoint**: ✓ Cannot proceed to testing without approval

**Deliverable**: Approved risk assessment with agreed-upon controls

---

### 1.5 Audit Planning
**Owner**: Esther (Senior Auditor)

**Activities**:
- Extract testing procedures from ISACA for selected controls
- Assign controls to auditors based on:
  - **Senior Auditors**: Complex controls requiring judgment
  - **Staff Auditors**: Straightforward evidence collection
- Create audit timeline and milestones
- Estimate audit hours per control
- Document audit plan

**Deliverable**: Audit Plan (WP-PLAN-001) with control assignments

---

## Phase 2: Control Testing (Fieldwork)

### 2.1 Initial Meeting with Auditee
**Owner**: Assigned Auditor (e.g., Hillel)
**Collaborator**: Chuck (IT Manager)

**Activities**:
- Schedule meeting with Chuck
- Explain which control is being tested
- Discuss how the control works at CloudRetail
- Identify what evidence is needed
- Agree on evidence to be provided

**Communication**:
- Professional meeting request
- Clear explanation of control objective
- Specific evidence requests
- Timeline expectations

**Deliverable**: Meeting summary + Evidence request list

---

### 2.2 Evidence Collection
**Owner**: Chuck (IT Manager)
**Recipient**: Assigned Auditor

**Activities**:
- Chuck retrieves requested evidence from AWS
- Organizes and documents evidence
- Provides evidence with context and explanations
- Answers follow-up questions

**Evidence Types** (by reliability):
1. **Physical Examination** (Highest): Auditor directly queries AWS APIs
2. **AWS-Generated Logs** (High): CloudTrail, Config, CloudWatch
3. **Internal Documentation** (Moderate): Policies, procedures, diagrams
4. **Inquiry** (Lowest): Interviews, discussions (must be corroborated)

**Deliverable**: Evidence package with proper documentation

---

### 2.3 Control Testing
**Owner**: Assigned Auditor (e.g., Hillel)

**Activities**:
- Review evidence provided by Chuck
- Perform testing procedures from ISACA audit program
- Collect additional evidence directly via AWS APIs (physical examination)
- Analyze evidence against control objectives
- Identify any control weaknesses or gaps
- Document findings with supporting evidence

**Testing Approach**:
- Start with high-reliability evidence (physical examination)
- Use inquiry to understand context
- Corroborate inquiry with physical examination
- Document all evidence sources

**Key Questions**:
- Is the control designed effectively?
- Is the control implemented as designed?
- Is the control operating consistently?
- Is there evidence of control monitoring?

**Deliverable**: Control testing workpaper (draft) with preliminary findings

---

### 2.4 Issue Validation with Auditee
**Owner**: Assigned Auditor
**Collaborator**: Chuck (IT Manager)

**Activities** (if issues found):
- Communicate identified issues to Chuck
- Explain the control weakness or gap
- Request Chuck to verify the facts
- Ensure mutual understanding of the issue
- Document Chuck's response

**Important**: Issues are NOT official until audit manager reviews and approves

**Deliverable**: Validated issue documentation

---

### 2.5 Workpaper Completion
**Owner**: Assigned Auditor

**Activities**:
- Document validated issues in workpaper
- Include evidence showing control is working OR why not
- Ensure all findings are supported by evidence
- Complete analysis and conclusion
- Reference all evidence collected
- Assess evidence sufficiency and appropriateness

**Workpaper Components**:
- Control objective
- Testing procedures performed
- Evidence collected (with reliability assessment)
- Analysis of findings
- Conclusion on control effectiveness
- Issues identified (if any)

**Deliverable**: Complete control testing workpaper

---

## Phase 3: Workpaper Review & Quality Assurance

### 3.1 Senior Auditor Review
**Owner**: Esther (Senior Auditor)
**Preparer**: Hillel (Staff Auditor)

**Activities**:
- Review staff auditor's workpapers for quality
- Check completeness of evidence
- Verify analysis supports conclusions
- Ensure evidence reliability is properly assessed
- Check for proper corroboration of low-reliability evidence
- Ensure professional standards are met
- Request clarifications or improvements if needed

**Quality Checks**:
- ✓ All testing procedures completed
- ✓ Evidence is sufficient and appropriate
- ✓ Analysis is logical and well-supported
- ✓ Conclusions are reasonable
- ✓ Documentation is clear and professional

**Deliverable**: Approved workpapers OR feedback for revision

---

### 3.2 Workpaper Revision (if needed)
**Owner**: Assigned Auditor

**Activities**:
- Address senior auditor's feedback
- Collect additional evidence if needed
- Improve analysis or documentation
- Resubmit for approval

**Deliverable**: Revised workpaper

---

### 3.3 Audit Manager Review
**Owner**: Maurice (Audit Manager)

**Activities**:
- Review all completed workpapers
- Validate that issues are legitimate
- Ensure evidence supports findings
- Check professional quality across all workpapers
- Verify consistency in conclusions
- **Approve issues as official findings**

**Critical Rule**: Issues only become official after Maurice's approval

**Quality Checks**:
- ✓ Evidence hierarchy properly applied
- ✓ High-reliability evidence used for key findings
- ✓ Low-reliability evidence properly corroborated
- ✓ All findings supported by sufficient evidence
- ✓ Professional standards maintained

**Critical Checkpoint**: ✓ Issues not official until Maurice approves

**Deliverable**: Officially approved findings + Quality-assured workpapers

---

## Phase 4: Remediation Planning

### 4.1 Findings Discussion with Auditee
**Owner**: Esther (Senior Auditor)
**Collaborator**: Chuck (IT Manager)

**Activities**:
- Present validated findings to Chuck
- Discuss each issue and its impact
- Explain risk implications
- Request remediation plans from Chuck
- Request timelines for fixes
- Document Chuck's commitments

**Tone**: Professional, constructive, collaborative

**Deliverable**: Remediation plans with timelines for each issue

---

## Phase 5: Audit Reporting

### 5.1 Draft Audit Report
**Owner**: Esther (Senior Auditor)

**Activities**:
- Summarize all testing work performed
- List all controls tested
- Document all validated issues with:
  - Issue description
  - Risk rating
  - Impact assessment
  - Root cause analysis
  - Remediation plan
  - Timeline for remediation
- Provide recommendations
- Include executive summary

**Report Structure**:
1. Executive Summary
2. Audit Scope and Objectives
3. Methodology
4. Controls Tested
5. Findings and Recommendations
6. Remediation Plans
7. Conclusion
8. Appendices (detailed workpapers)

**Deliverable**: Draft audit report

---

### 5.2 Report Review
**Owner**: Maurice (Audit Manager)

**Activities**:
- Review draft report for accuracy
- Verify all findings are supported by workpapers
- Check tone and professionalism
- Ensure completeness
- Verify remediation plans are reasonable
- Make edits or request revisions

**Quality Checks**:
- ✓ All findings supported by evidence
- ✓ Risk ratings are appropriate
- ✓ Recommendations are actionable
- ✓ Tone is professional and constructive
- ✓ Report is clear and well-organized

**Deliverable**: Approved report OR feedback for revision

---

### 5.3 Report Finalization & Sign-Off
**Owner**: Maurice (Audit Manager)

**Activities**:
- Final review of report
- Ensure all revisions incorporated
- Sign off on audit report
- Authorize release to management

**Critical Checkpoint**: ✓ Report not official until Maurice signs

**Deliverable**: **Final Audit Report** (Official)

---

### 5.4 Closing Meeting
**Owner**: Maurice (Audit Manager) + Esther (Senior Auditor)
**Audience**: CloudRetail Management + Chuck (IT Manager)

**Activities**:
- Present final audit report
- Discuss findings and recommendations
- Review remediation plans and timelines
- Answer questions
- Obtain management acknowledgment
- Discuss follow-up audit (if needed)

**Deliverable**: Signed management response letter

---

## Phase 6: Follow-Up (Optional)

### 6.1 Remediation Tracking
**Owner**: Maurice (Audit Manager)

**Activities**:
- Track remediation progress
- Request status updates from Chuck
- Verify completion of remediation actions
- Perform follow-up testing if needed

**Deliverable**: Remediation status report

---

### 6.2 Follow-Up Audit (if needed)
**Owner**: Assigned Auditor

**Activities**:
- Test remediated controls
- Verify issues have been resolved
- Document results
- Update audit report

**Deliverable**: Follow-up audit report

---

## Key Workflow Principles

### 1. Evidence-Based
- Every finding must be supported by evidence
- Evidence must be from reliable sources
- Evidence hierarchy must be followed
- Low-reliability evidence must be corroborated

### 2. Hierarchical Review
- Staff auditors → Senior auditors → Audit manager
- Each level reviews work from below
- Issues only official after manager approval
- Quality assurance at every level

### 3. Company Collaboration
- Auditors request evidence from auditee
- Auditee provides evidence and context
- Issues are discussed and validated with auditee
- Remediation plans developed collaboratively

### 4. Professional Standards
- All workpapers meet quality standards
- Analysis supports conclusions
- Documentation is clear and complete
- Tone is professional and constructive

### 5. Budget Conscious
- Risk assessment considers budget constraints
- Only 3-5 high-risk controls selected
- Efficient use of audit resources
- Focus on material risks

---

## Critical Checkpoints Summary

| Checkpoint | Phase | Owner | Requirement |
|-----------|-------|-------|-------------|
| ✓ Risk Assessment Approved | Phase 1 | Maurice | 3-5 controls selected, cannot proceed without approval |
| ✓ Evidence Collected | Phase 2 | Chuck + Auditor | All requested evidence provided, cannot test without evidence |
| ✓ Workpapers Reviewed | Phase 3 | Esther + Maurice | All workpapers approved, issues not official until Maurice approves |
| ✓ Remediation Plans Obtained | Phase 4 | Esther + Chuck | Plans documented with timelines, cannot finalize report without plans |
| ✓ Report Signed Off | Phase 5 | Maurice | Report reviewed and approved, not official until Maurice signs |

---

## Timeline Example (3-5 Controls)

| Phase | Duration | Activities |
|-------|----------|-----------|
| Phase 1: Risk Assessment & Planning | 2-3 weeks | Business understanding, inventory, risk assessment, planning |
| Phase 2: Control Testing (Fieldwork) | 3-4 weeks | Evidence collection, testing, issue validation |
| Phase 3: Workpaper Review & QA | 1-2 weeks | Senior review, manager review, revisions |
| Phase 4: Remediation Planning | 1 week | Findings discussion, remediation plans |
| Phase 5: Audit Reporting | 1-2 weeks | Draft report, review, finalization, closing meeting |
| **Total** | **8-12 weeks** | **Complete audit cycle** |

---

## Success Criteria

The audit is successful when:

✅ Risk assessment completed and approved (3-5 controls selected)  
✅ All selected controls tested with sufficient evidence  
✅ All workpapers reviewed and approved by Esther and Maurice  
✅ All issues validated with Chuck  
✅ Remediation plans obtained for all issues  
✅ Audit report drafted, reviewed, and signed off by Maurice  
✅ Professional standards maintained throughout  
✅ Budget constraints respected  
✅ Closing meeting completed with management acknowledgment  

---

## Agent Roles by Phase

### Maurice (Audit Manager)
- **Phase 1**: Review and approve risk assessment
- **Phase 3**: Review all workpapers, approve official findings
- **Phase 5**: Review and sign off on audit report
- **Phase 5**: Lead closing meeting

### Esther (Senior Auditor - IAM)
- **Phase 1**: Perform risk assessment, create audit plan
- **Phase 2**: May perform complex control testing
- **Phase 3**: Review staff auditor workpapers
- **Phase 4**: Meet with Chuck for remediation planning
- **Phase 5**: Draft audit report

### Victor (Senior Auditor - Logging)
- **Phase 1**: Provide input on logging/monitoring risks
- **Phase 2**: Test logging and monitoring controls
- **Phase 3**: Review staff auditor workpapers
- **Phase 4**: Coordinate remediation for logging issues

### Hillel (Staff Auditor - IAM)
- **Phase 2**: Collect evidence, test assigned controls
- **Phase 2**: Document findings in workpapers
- **Phase 3**: Revise workpapers based on feedback

### Neil (Staff Auditor - Encryption/Network)
- **Phase 2**: Test encryption and network controls
- **Phase 2**: Collect evidence and document findings

### Juman (Staff Auditor - Logging)
- **Phase 2**: Collect logging evidence
- **Phase 2**: Support Victor in logging control testing

### Chuck (IT Manager - Auditee)
- **Phase 1**: Provide company inventory
- **Phase 2**: Meet with auditors, provide evidence
- **Phase 2**: Verify facts when issues identified
- **Phase 4**: Develop remediation plans
- **Phase 5**: Attend closing meeting

---

**This document provides the complete roadmap for executing a professional IT audit of AWS infrastructure.**

---
**Created**: December 4, 2025  
**Purpose**: Define major phases of audit execution  
**Audience**: All audit team members and stakeholders
