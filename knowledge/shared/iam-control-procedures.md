# IAM Control Testing Procedures

## Overview
This document provides standardized procedures for testing Identity and Access Management (IAM) controls in AWS environments. These procedures can be used by any auditor assigned to test IAM controls.

## Control Domain
- **Domain**: Identity and Access Management (IAM)
- **Applicable To**: All auditors testing IAM controls
- **Reference**: ISACA IT Audit Programs

## Key Control Objectives

### 1. Root Account Protection
**Control Objective**: Root account access is restricted and monitored

**Testing Procedures**:
1. Verify root account MFA is enabled
2. Confirm root account access keys do not exist
3. Review CloudTrail logs for root account usage
4. Verify root account email is monitored
5. Check that root account is not used for daily operations

**Evidence to Request**:
- Root account MFA status screenshot
- Root account access key inventory (should be empty)
- CloudTrail logs showing root account activity (last 90 days)
- Root account usage policy documentation

**Expected Results**:
- MFA enabled on root account
- No access keys for root account
- Minimal or no root account usage
- All root usage has business justification

**Risk Rating if Failed**: High

---

### 2. MFA Enforcement
**Control Objective**: Multi-factor authentication is required for all users

**Testing Procedures**:
1. Obtain list of all IAM users
2. Check MFA status for each user
3. Review IAM policies requiring MFA
4. Test that users without MFA cannot access resources
5. Verify MFA device types are approved

**Evidence to Request**:
- Complete IAM user list with MFA status
- IAM policies requiring MFA
- Test results showing MFA enforcement
- MFA device inventory

**Sample Selection**:
- If < 20 users: Test all users
- If 20-50 users: Test 25 users (minimum)
- If > 50 users: Test 30 users or 50%, whichever is greater

**Expected Results**:
- 100% of users have MFA enabled
- Policies enforce MFA for console and API access
- Only approved MFA device types in use

**Risk Rating if Failed**: High

---

### 3. Least Privilege Access
**Control Objective**: Users have only the permissions they need

**Testing Procedures**:
1. Select sample of IAM users and roles
2. Review attached policies for each
3. Identify overly permissive policies (e.g., AdministratorAccess)
4. Verify business justification for elevated permissions
5. Check for unused permissions (AWS Access Analyzer)
6. Review last access information

**Evidence to Request**:
- IAM user and role inventory with attached policies
- Access Analyzer findings
- Last accessed information for users/roles
- Business justification for admin access
- Access review/recertification records

**Sample Selection**:
- All users with AdministratorAccess or PowerUserAccess
- Random sample of 20-30 regular users
- All service roles

**Expected Results**:
- No unnecessary admin access
- Policies follow least privilege principle
- Regular access reviews performed
- Unused permissions identified and removed

**Risk Rating if Failed**: Medium to High

---

### 4. Password Policy
**Control Objective**: Strong password requirements are enforced

**Testing Procedures**:
1. Review account password policy settings
2. Verify minimum password length (14+ characters recommended)
3. Check complexity requirements
4. Verify password expiration settings
5. Check password reuse prevention
6. Test password policy enforcement

**Evidence to Request**:
- Password policy configuration screenshot
- Password policy documentation
- Test results showing policy enforcement

**Expected Results**:
- Minimum 14 character passwords
- Complexity requirements enabled
- Password expiration ≤ 90 days
- Password reuse prevention (24 passwords)
- Policy cannot be bypassed

**Risk Rating if Failed**: Medium

---

### 5. Access Key Rotation
**Control Objective**: Access keys are rotated regularly

**Testing Procedures**:
1. Obtain list of all access keys with creation dates
2. Identify keys older than 90 days
3. Review key rotation policy
4. Check for inactive keys
5. Verify automated rotation where possible

**Evidence to Request**:
- Access key inventory with ages
- Key rotation policy documentation
- Automated rotation configurations
- Inactive key removal procedures

**Expected Results**:
- All keys rotated within 90 days
- Inactive keys disabled or deleted
- Automated rotation implemented where possible
- Key rotation policy documented and followed

**Risk Rating if Failed**: Medium

---

### 6. IAM Role Usage
**Control Objective**: Roles are used instead of long-term credentials where possible

**Testing Procedures**:
1. Review application and service authentication methods
2. Identify use of IAM roles vs. access keys
3. Check EC2 instance profiles
4. Review Lambda execution roles
5. Verify cross-account access uses roles

**Evidence to Request**:
- EC2 instances with/without instance profiles
- Lambda functions with execution roles
- Application authentication methods
- Cross-account access configurations

**Expected Results**:
- EC2 instances use instance profiles
- Lambda functions use execution roles
- Applications use roles when possible
- Cross-account access uses roles, not keys

**Risk Rating if Failed**: Medium

---

### 7. Inactive User Accounts
**Control Objective**: Inactive accounts are disabled or removed

**Testing Procedures**:
1. Obtain user last activity report
2. Identify users inactive > 90 days
3. Review account deactivation procedures
4. Verify terminated employee access is revoked
5. Check for orphaned accounts

**Evidence to Request**:
- User activity report (last 90 days)
- Account deactivation procedures
- Termination checklist
- Recent terminations and access revocation evidence

**Expected Results**:
- Inactive accounts (90+ days) are disabled
- Terminated employee access revoked same day
- Regular account reviews performed
- Orphaned accounts identified and removed

**Risk Rating if Failed**: Medium

---

### 8. Privileged Access Monitoring
**Control Objective**: Privileged actions are logged and monitored

**Testing Procedures**:
1. Review CloudTrail configuration for IAM events
2. Check CloudWatch alarms for privileged actions
3. Verify monitoring of policy changes
4. Test alert delivery for critical events
5. Review incident response procedures

**Evidence to Request**:
- CloudTrail configuration for IAM events
- CloudWatch alarms for IAM changes
- Sample alerts from privileged actions
- Incident response runbooks
- Recent alert response examples

**Expected Results**:
- All IAM events logged in CloudTrail
- Alerts configured for critical changes
- Alerts are delivered and reviewed
- Incident response procedures exist
- Evidence of alert response

**Risk Rating if Failed**: High

---

## Evidence Collection Guidelines

### Working with Company Representatives

When requesting evidence from Chuck (or other company IT staff):

1. **Be Specific**: 
   - "Please provide IAM user list with MFA status as of [date]"
   - Not: "Send me IAM information"

2. **Request Screenshots**:
   - Console screenshots with timestamps
   - Configuration pages showing settings
   - Policy documents

3. **Request Exports**:
   - CSV exports of user lists
   - JSON policy documents
   - CloudTrail log samples

4. **Define Time Periods**:
   - Specify exact dates and times
   - Include timezone
   - Request point-in-time snapshots

### Organizing Evidence

1. Create evidence folder: `evidence/iam/[control-id]/`
2. Name files descriptively: `IAM-Users-MFA-Status-2025-12-04.csv`
3. Document source and date in workpaper
4. Keep original files unmodified
5. Create separate analysis files

## Workpaper Documentation

Every IAM control test must include:

1. **Control Objective**: What you're testing
2. **Procedure**: Steps you performed
3. **Evidence**: What you reviewed (with file references)
4. **Sample**: If sampling, document selection method and size
5. **Findings**: What you discovered
6. **Analysis**: Your evaluation of the control
7. **Conclusion**: Effective, ineffective, or needs improvement
8. **Issues**: Any deficiencies identified with risk ratings

## Common IAM Issues

### Critical Issues (High Risk)
- Root account without MFA
- Root account with access keys
- No MFA enforcement
- Overly permissive policies (AdministratorAccess to all)
- No CloudTrail logging of IAM events

### Significant Issues (Medium Risk)
- Weak password policy
- Access keys not rotated
- Inactive accounts not disabled
- No least privilege implementation
- Missing access reviews

### Minor Issues (Low Risk)
- Password policy could be stronger
- Some unused permissions
- Documentation gaps
- Inconsistent naming conventions

## Risk Assessment Considerations

When assessing IAM control risks:

### High-Risk Indicators
- No MFA on privileged accounts
- Shared credentials
- No access monitoring
- Weak password requirements
- No access reviews

### Medium-Risk Indicators
- Partial MFA implementation
- Some overly permissive policies
- Infrequent access reviews
- Manual key rotation

### Low-Risk Indicators
- Comprehensive MFA
- Least privilege implemented
- Regular access reviews
- Automated controls
- Strong monitoring

## Tools and Queries

### Useful AWS CLI Commands

```bash
# List all users with MFA status
aws iam get-credential-report

# List access keys with age
aws iam list-access-keys --user-name [username]

# Get password policy
aws iam get-account-password-policy

# List users
aws iam list-users

# Get user's attached policies
aws iam list-attached-user-policies --user-name [username]

# Get role's attached policies
aws iam list-attached-role-policies --role-name [rolename]
```

### AWS Console Locations

- IAM Dashboard: IAM → Dashboard
- Users: IAM → Users
- Roles: IAM → Roles
- Policies: IAM → Policies
- Password Policy: IAM → Account settings
- Credential Report: IAM → Credential report

## Professional Standards

- Maintain independence and objectivity
- Base conclusions on evidence
- Document all work thoroughly
- Communicate findings clearly
- Follow up on issues
- Respect confidentiality
- Escalate significant issues promptly
