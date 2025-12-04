# Control Testing Procedures

## Purpose
This guide provides senior auditors with procedures for testing AWS controls effectively and documenting findings professionally.

## General Testing Approach

### 1. Understand the Control
Before testing, ensure you understand:
- **Control Objective**: What risk is being mitigated?
- **Control Design**: How is the control supposed to work?
- **Control Owner**: Who is responsible for the control?
- **Control Frequency**: How often does the control operate?

### 2. Plan Your Testing
- Review ISACA testing procedures for this control
- Identify what evidence you need to collect
- Determine if interviews are required
- Plan your testing approach and timeline
- Coordinate with staff auditors if delegation is needed

### 3. Execute Testing Procedures
Follow the ISACA testing steps exactly:
- Collect required evidence from AWS
- Conduct interviews with control owners
- Document observations in real-time
- Note any exceptions or unusual findings
- Gather additional evidence if needed

### 4. Analyze Results
- Compare actual state vs. expected state
- Evaluate control design effectiveness
- Assess control operating effectiveness
- Identify any control deficiencies
- Consider root causes of issues

### 5. Document Findings
- Create workpaper with all required sections
- Reference all evidence collected
- Provide thorough analysis
- State clear conclusion (Pass/Fail/Deficiency)
- Include recommendations if deficiencies found

## Control Testing by Domain

### IAM Controls
**Key Testing Areas**:
- Root account security (MFA, usage monitoring)
- User access management (least privilege, reviews)
- MFA enforcement on privileged accounts
- Password policies and complexity
- Access key rotation
- Role-based access control (RBAC)

**Evidence to Collect**:
- IAM user list with MFA status
- IAM policies and permissions
- Root account activity logs
- Access key age reports
- Password policy configuration
- Role trust relationships

**Common Findings**:
- Users without MFA enabled
- Overly permissive policies
- Inactive users not disabled
- Access keys not rotated
- Root account used for daily operations

### Encryption Controls
**Key Testing Areas**:
- S3 bucket encryption (default encryption)
- EBS volume encryption
- RDS database encryption
- Encryption in transit (SSL/TLS)
- KMS key management
- Key rotation policies

**Evidence to Collect**:
- S3 bucket encryption settings
- EBS volume encryption status
- RDS instance encryption config
- KMS key policies and rotation
- SSL/TLS certificate configurations

**Common Findings**:
- Unencrypted S3 buckets
- EBS volumes without encryption
- KMS keys not rotated
- Weak encryption algorithms
- Missing encryption in transit

### Network Security Controls
**Key Testing Areas**:
- Security group configurations
- Network ACLs
- VPC design and segmentation
- Public vs. private subnets
- Internet gateway usage
- VPC flow logs

**Evidence to Collect**:
- Security group rules
- NACL configurations
- VPC architecture diagrams
- Public IP assignments
- Flow log settings
- Route table configurations

**Common Findings**:
- Overly permissive security groups (0.0.0.0/0)
- Missing network segmentation
- Unnecessary public exposure
- Flow logs not enabled
- Unrestricted SSH/RDP access

### Logging & Monitoring Controls
**Key Testing Areas**:
- CloudTrail configuration
- CloudWatch log groups
- S3 access logging
- VPC flow logs
- Log retention policies
- Security monitoring and alerting

**Evidence to Collect**:
- CloudTrail trail configurations
- CloudWatch log group settings
- S3 bucket logging status
- Log retention periods
- CloudWatch alarms and metrics
- SNS notification configurations

**Common Findings**:
- CloudTrail not enabled in all regions
- Insufficient log retention
- Missing critical alarms
- Logs not centralized
- No log integrity validation

## Interview Techniques

### Preparing for Interviews
- Review control documentation beforehand
- Prepare specific questions
- Schedule interview in advance
- Explain purpose and scope
- Set expectations for time needed

### Conducting Interviews
- Start with open-ended questions
- Listen actively and take notes
- Ask follow-up questions
- Request examples and demonstrations
- Verify understanding
- Thank interviewee for their time

### Documenting Interviews
- Document date, time, and participants
- Summarize key points discussed
- Note any discrepancies with documentation
- Include direct quotes when relevant
- Have interviewee review notes if possible
- Store interview notes with workpaper

### Sample Interview Questions
**For Control Owners**:
- "Can you walk me through how this control works?"
- "How do you know the control is operating effectively?"
- "What happens if the control fails?"
- "How often do you review this control?"
- "Have there been any exceptions or issues?"

**For System Administrators**:
- "How is this configured in AWS?"
- "Who has access to modify these settings?"
- "How do you monitor for changes?"
- "What alerts are in place?"
- "Can you show me an example?"

## Evidence Collection Best Practices

### Direct Evidence (Preferred)
- Collect directly from AWS console or API
- Take screenshots with timestamps
- Export configurations to JSON/CSV
- Run AWS CLI commands and save output
- Use AWS Config for historical data

### Indirect Evidence (When Necessary)
- Request evidence from client
- Verify authenticity and completeness
- Cross-check with other sources
- Document limitations
- Consider reliability in analysis

### Evidence Documentation
- Label all evidence with unique IDs
- Include collection date and method
- Note who collected the evidence
- Store in proper evidence folder
- Reference in workpaper

## Quality Standards

### Your Workpaper Should Be
- **Thorough**: All testing steps completed
- **Clear**: Another auditor could understand it
- **Objective**: Facts, not opinions
- **Professional**: Audit-quality documentation
- **Conclusive**: Clear Pass/Fail determination

### Before Submitting for Review
- [ ] All testing procedures completed
- [ ] All evidence collected and referenced
- [ ] Analysis is thorough and objective
- [ ] Conclusion is supported by evidence
- [ ] Workpaper is professionally formatted
- [ ] No spelling or grammar errors
- [ ] Cross-references are correct

## Escalation Procedures

### When to Escalate to Maurice
- Significant control deficiencies found
- Unable to obtain required evidence
- Scope limitations encountered
- Disagreement with client
- Need for additional resources
- Ethical concerns

### How to Escalate
1. Document the issue clearly
2. Provide relevant context
3. Suggest potential solutions
4. Request specific guidance
5. Follow up on decisions

## Remember
- Professional skepticism is essential
- Document everything
- Quality over speed
- Ask questions when unsure
- Maintain independence and objectivity
