# Logging and Monitoring Control Testing Procedures

## Overview
This document provides standardized procedures for testing logging and monitoring controls in AWS environments. These procedures can be used by any auditor assigned to test logging controls.

## Control Domain
- **Domain**: Logging and Monitoring
- **Applicable To**: All auditors testing logging controls
- **Reference**: ISACA IT Audit Programs

## Key Control Objectives

### 1. CloudTrail Enabled and Configured
**Control Objective**: All AWS API activity is logged

**Testing Procedures**:
1. Verify CloudTrail is enabled in all regions
2. Confirm multi-region trail exists
3. Check management event logging is enabled
4. Verify data event logging for sensitive resources
5. Confirm log file validation is enabled
6. Check log encryption (SSE-KMS)

**Evidence to Request**:
- CloudTrail configuration screenshots
- List of all trails with settings
- S3 bucket configuration for log storage
- KMS key policies for log encryption
- CloudTrail status report

**Expected Results**:
- At least one multi-region trail enabled
- Management events logged
- Data events logged for sensitive S3 buckets
- Log file validation enabled
- Logs encrypted with KMS

**Risk Rating if Failed**: High

---

### 2. Log Retention and Storage
**Control Objective**: Logs are retained for adequate periods and stored securely

**Testing Procedures**:
1. Review S3 bucket lifecycle policies for log storage
2. Verify retention period meets requirements (90+ days)
3. Check S3 bucket versioning and MFA delete
4. Verify bucket encryption
5. Review bucket access policies
6. Check for log backup procedures

**Evidence to Request**:
- S3 bucket lifecycle policies
- Bucket versioning configuration
- Bucket encryption settings
- Bucket access policies
- Log retention policy documentation
- Backup procedures

**Expected Results**:
- Logs retained for minimum 90 days (1 year recommended)
- S3 bucket versioning enabled
- MFA delete enabled on log bucket
- Bucket encryption enabled
- Restrictive bucket policies
- Logs backed up to separate location

**Risk Rating if Failed**: High

---

### 3. Log Monitoring and Alerting
**Control Objective**: Logs are actively monitored for security events

**Testing Procedures**:
1. Review CloudWatch metric filters
2. Verify alarms for critical security events
3. Check SNS topic configurations
4. Test alert delivery
5. Review alert response procedures
6. Verify 24/7 monitoring coverage

**Evidence to Request**:
- CloudWatch metric filter configurations
- CloudWatch alarm definitions
- SNS topic subscriptions
- Sample alert notifications
- Alert response procedures
- Recent alert response examples
- Monitoring coverage documentation

**Critical Events to Monitor**:
- Root account usage
- Unauthorized API calls
- Console sign-in failures
- IAM policy changes
- Security group changes
- Network ACL changes
- CloudTrail configuration changes
- S3 bucket policy changes

**Expected Results**:
- Metric filters for all critical events
- Alarms configured and active
- Alerts delivered to appropriate personnel
- Alert response procedures documented
- Evidence of alert response
- 24/7 monitoring coverage

**Risk Rating if Failed**: High

---

### 4. VPC Flow Logs
**Control Objective**: Network traffic is logged for security analysis

**Testing Procedures**:
1. Verify VPC Flow Logs enabled for all VPCs
2. Check flow log retention period
3. Review flow log storage location
4. Verify flow log analysis procedures
5. Check for rejected traffic monitoring

**Evidence to Request**:
- VPC Flow Log configurations
- List of VPCs with/without flow logs
- Flow log retention settings
- Flow log analysis procedures
- Sample flow log analysis reports
- Rejected traffic monitoring

**Expected Results**:
- Flow logs enabled for all production VPCs
- Retention period adequate (30+ days)
- Logs stored securely
- Regular flow log analysis performed
- Rejected traffic monitored and investigated

**Risk Rating if Failed**: Medium

---

### 5. CloudWatch Logs Configuration
**Control Objective**: Application and system logs are centralized and retained

**Testing Procedures**:
1. Identify all log groups
2. Review log retention settings
3. Verify log encryption
4. Check log group access policies
5. Review log streaming configurations

**Evidence to Request**:
- CloudWatch log group inventory
- Retention settings for each log group
- Encryption configurations
- Log group access policies
- Log streaming configurations

**Expected Results**:
- All applications sending logs to CloudWatch
- Appropriate retention periods set
- Logs encrypted at rest
- Restrictive access policies
- Critical logs streamed to SIEM if applicable

**Risk Rating if Failed**: Medium

---

### 6. Log Integrity and Protection
**Control Objective**: Logs cannot be tampered with or deleted

**Testing Procedures**:
1. Verify CloudTrail log file validation
2. Check S3 bucket policies prevent deletion
3. Review IAM policies for log access
4. Verify MFA delete on log buckets
5. Check for log integrity monitoring

**Evidence to Request**:
- CloudTrail log file validation status
- S3 bucket policies for log storage
- IAM policies granting log access
- MFA delete configuration
- Log integrity monitoring procedures

**Expected Results**:
- Log file validation enabled
- Bucket policies prevent unauthorized deletion
- Minimal IAM access to logs
- MFA delete required
- Log integrity monitored

**Risk Rating if Failed**: High

---

### 7. Incident Response Logging
**Control Objective**: Adequate logging exists to support incident investigation

**Testing Procedures**:
1. Review incident response procedures
2. Verify log sources cover all critical systems
3. Check log detail level is sufficient
4. Test log search and analysis capabilities
5. Review past incident investigations

**Evidence to Request**:
- Incident response procedures
- Log source inventory
- Log detail/verbosity settings
- Log search tool documentation
- Past incident investigation reports

**Expected Results**:
- Comprehensive incident response procedures
- All critical systems logging
- Sufficient log detail for investigations
- Effective log search capabilities
- Evidence of successful investigations

**Risk Rating if Failed**: Medium

---

### 8. Third-Party Log Integration
**Control Objective**: Logs are integrated with SIEM or log management platform

**Testing Procedures**:
1. Identify SIEM or log management platform
2. Verify AWS logs are forwarded
3. Check log forwarding reliability
4. Review correlation rules
5. Test alert generation from SIEM

**Evidence to Request**:
- SIEM platform documentation
- Log forwarding configurations
- Log forwarding reliability metrics
- SIEM correlation rules
- Sample SIEM alerts

**Expected Results**:
- SIEM platform implemented
- AWS logs forwarded reliably
- Correlation rules for AWS events
- SIEM alerts configured
- Regular SIEM monitoring

**Risk Rating if Failed**: Medium (Low if no SIEM requirement)

---

## Evidence Collection Guidelines

### Log Samples to Request

1. **CloudTrail Logs**:
   - Last 90 days of activity
   - Specific event types (IAM changes, security group changes)
   - Root account activity
   - Failed authentication attempts

2. **VPC Flow Logs**:
   - Sample from each VPC
   - Rejected traffic examples
   - Last 30 days

3. **CloudWatch Logs**:
   - Application log samples
   - System log samples
   - Error log samples

### Working with Company Representatives

When requesting logs from Chuck:

1. **Specify Time Periods**:
   - Exact start and end dates/times
   - Include timezone
   - Request continuous periods (no gaps)

2. **Specify Format**:
   - JSON for CloudTrail
   - CSV for flow logs
   - Original format preferred

3. **Specify Scope**:
   - Which accounts
   - Which regions
   - Which services
   - Which event types

4. **Request Configurations**:
   - Screenshots of settings
   - Policy documents
   - Architecture diagrams

## Log Analysis Techniques

### CloudTrail Analysis

**Key Fields to Review**:
- eventTime: When event occurred
- eventName: What action was performed
- userIdentity: Who performed the action
- sourceIPAddress: Where it came from
- errorCode: If action failed
- requestParameters: What was requested
- responseElements: What was returned

**Analysis Steps**:
1. Sort by eventTime to check continuity
2. Filter by eventName for specific actions
3. Group by userIdentity to see user activity
4. Check errorCode for failed attempts
5. Review sourceIPAddress for unusual locations

### VPC Flow Log Analysis

**Key Fields to Review**:
- srcaddr: Source IP address
- dstaddr: Destination IP address
- srcport: Source port
- dstport: Destination port
- protocol: Protocol number
- action: ACCEPT or REJECT
- bytes: Amount of data transferred

**Analysis Steps**:
1. Filter for REJECT actions
2. Identify unusual ports
3. Check for large data transfers
4. Look for unusual source IPs
5. Identify scanning activity

## Workpaper Documentation

Every logging control test must include:

1. **Control Objective**: What you're testing
2. **Procedure**: Steps you performed
3. **Evidence**: Logs reviewed (with date ranges and sources)
4. **Analysis**: Your evaluation of log completeness and monitoring
5. **Findings**: What you discovered
6. **Conclusion**: Effective, ineffective, or needs improvement
7. **Issues**: Any deficiencies with risk ratings

## Common Logging Issues

### Critical Issues (High Risk)
- CloudTrail not enabled
- CloudTrail disabled in some regions
- No log monitoring or alerting
- Logs not encrypted
- No log file validation
- Logs can be deleted by unauthorized users

### Significant Issues (Medium Risk)
- Short retention periods (< 30 days)
- VPC Flow Logs not enabled
- No SIEM integration
- Incomplete log coverage
- No incident response procedures
- Alerts not tested

### Minor Issues (Low Risk)
- Retention could be longer
- Some non-critical logs missing
- Documentation gaps
- Alert tuning needed

## Risk Assessment Considerations

### High-Risk Indicators
- No CloudTrail logging
- No log monitoring
- Logs can be tampered with
- Very short retention (< 7 days)
- No incident response capability

### Medium-Risk Indicators
- Partial logging coverage
- Basic monitoring but no automation
- Retention meets minimum only
- Limited log analysis capability

### Low-Risk Indicators
- Comprehensive logging
- Active monitoring with automation
- Long retention periods
- SIEM integration
- Regular log analysis
- Proven incident response

## Tools and Queries

### Useful AWS CLI Commands

```bash
# List CloudTrail trails
aws cloudtrail describe-trails

# Get trail status
aws cloudtrail get-trail-status --name [trail-name]

# List VPC Flow Logs
aws ec2 describe-flow-logs

# List CloudWatch log groups
aws logs describe-log-groups

# Query CloudWatch Logs
aws logs filter-log-events --log-group-name [name] --start-time [timestamp]

# Lookup CloudTrail events
aws cloudtrail lookup-events --lookup-attributes AttributeKey=EventName,AttributeValue=[event]
```

### AWS Console Locations

- CloudTrail: CloudTrail → Trails
- VPC Flow Logs: VPC → Your VPCs → Flow Logs
- CloudWatch Logs: CloudWatch → Logs → Log groups
- CloudWatch Alarms: CloudWatch → Alarms

## Professional Standards

- Verify log completeness and continuity
- Check for gaps in logging
- Test monitoring and alerting
- Validate log integrity controls
- Document all findings with evidence
- Escalate critical logging gaps immediately
- Maintain objectivity in analysis
