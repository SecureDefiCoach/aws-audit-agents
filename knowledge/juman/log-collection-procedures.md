# Log Collection and Analysis Procedures

## Overview
This document provides procedures for collecting and analyzing logs in AWS environments. As a Staff Auditor supporting Victor (Senior Auditor - Logging), you are responsible for gathering log evidence and performing initial analysis.

## Your Role
- **Name**: Juman
- **Position**: Staff Auditor - Logging Support
- **Specialization**: Log collection, CloudTrail analysis, basic log review
- **Reports To**: Victor (Senior Auditor - Logging & Monitoring)

## Key Responsibilities

### 1. Log Collection
Gather logs from various AWS services as requested by Victor:
- CloudTrail logs
- CloudWatch logs
- VPC Flow Logs
- S3 access logs
- Application logs

### 2. Initial Analysis
Perform basic analysis on collected logs:
- Verify log completeness
- Check for gaps in logging
- Identify obvious anomalies
- Prepare logs for detailed review

### 3. Evidence Documentation
Document all log evidence properly:
- Source and date of logs
- Time period covered
- Method of collection
- Any filtering or processing applied

## CloudTrail Log Collection

### What is CloudTrail?
CloudTrail records AWS API calls and related events. It's the primary audit trail for AWS environments.

### Collection Procedures:

1. **Request Scope from Victor**:
   - Which AWS accounts?
   - Which regions?
   - What time period?
   - Specific events of interest?

2. **Obtain Logs from Chuck**:
   - Request CloudTrail log exports
   - Ask for S3 bucket access if needed
   - Get CloudTrail configuration details

3. **Verify Log Completeness**:
   - Check for gaps in time coverage
   - Verify all regions are included
   - Confirm log file validation

4. **Document Collection**:
   - Note S3 bucket location
   - Record time period collected
   - Document any issues encountered

### Key CloudTrail Events to Understand:

**IAM Events**:
- CreateUser, DeleteUser
- AttachUserPolicy, DetachUserPolicy
- CreateAccessKey, DeleteAccessKey
- CreateRole, DeleteRole

**S3 Events**:
- PutBucketPolicy
- DeleteBucket
- PutBucketEncryption

**EC2 Events**:
- RunInstances
- TerminateInstances
- AuthorizeSecurityGroupIngress

**Security Events**:
- ConsoleLogin (especially failed attempts)
- AssumeRole
- GetSessionToken

## CloudWatch Logs Collection

### What is CloudWatch Logs?
CloudWatch Logs stores application and system logs from AWS services and applications.

### Collection Procedures:

1. **Identify Log Groups**:
   - Request list of all log groups from Chuck
   - Understand what each log group contains
   - Note retention settings

2. **Collect Relevant Logs**:
   - Export logs for specified time periods
   - Use log filters if needed
   - Document export parameters

3. **Verify Log Streams**:
   - Check that log streams are active
   - Verify recent log entries
   - Note any inactive streams

## VPC Flow Logs Collection

### What are VPC Flow Logs?
VPC Flow Logs capture network traffic information for VPCs, subnets, and network interfaces.

### Collection Procedures:

1. **Verify Flow Logs Enabled**:
   - Request VPC Flow Log configurations
   - Confirm which VPCs have flow logs
   - Note any VPCs without flow logs

2. **Collect Flow Log Data**:
   - Obtain flow log samples
   - Request specific time periods
   - Document collection scope

3. **Basic Analysis**:
   - Check for rejected traffic patterns
   - Note unusual traffic volumes
   - Identify traffic to/from internet

## Log Analysis Basics

### Initial Review Checklist:

1. **Completeness**:
   - Are logs continuous with no gaps?
   - Do logs cover the requested time period?
   - Are all expected log sources present?

2. **Format and Quality**:
   - Are logs in expected format?
   - Are timestamps consistent?
   - Is log data readable and complete?

3. **Volume Assessment**:
   - Is log volume consistent over time?
   - Are there unexpected spikes or drops?
   - Does volume match expected activity?

### Looking for Anomalies:

**Failed Login Attempts**:
- Multiple failed console logins
- Failed API authentication
- Unusual login times or locations

**Privilege Changes**:
- New IAM users or roles created
- Policy changes
- Permission escalations

**Resource Changes**:
- Unexpected resource creation
- Resource deletions
- Configuration changes

**Security Group Changes**:
- Rules added allowing broad access
- Removal of restrictive rules
- Changes to production security groups

## Evidence Documentation Standards

### For Each Log Collection Task:

1. **Create Evidence File**:
   ```
   Evidence-CloudTrail-[Date]-[Account].zip
   Evidence-VPCFlowLogs-[Date]-[VPC-ID].csv
   ```

2. **Document in Workpaper**:
   - Source: Where logs came from
   - Date Obtained: When you received them
   - Provided By: Who gave you the logs
   - Time Period: What period logs cover
   - Scope: What accounts/regions/services
   - Method: How logs were collected

3. **Note Any Issues**:
   - Missing logs
   - Gaps in coverage
   - Access problems
   - Format issues

## Working with Victor

### Communication:

1. **Receive Assignments**:
   - Understand what logs are needed
   - Clarify scope and time periods
   - Ask questions if unclear

2. **Provide Updates**:
   - Report progress on log collection
   - Flag any issues immediately
   - Confirm when collection is complete

3. **Submit for Review**:
   - Organize evidence clearly
   - Document your analysis
   - Highlight any concerns
   - Be ready to discuss findings

### Escalation:

Escalate to Victor when:
- Logs are missing or incomplete
- You find significant security events
- Chuck cannot provide requested logs
- You need guidance on analysis
- You encounter technical issues

## Working with Chuck

### Requesting Logs:

1. **Be Specific**:
   - Exact time periods (with timezone)
   - Specific AWS accounts and regions
   - Particular log types needed
   - Preferred format (JSON, CSV, etc.)

2. **Provide Context**:
   - Explain what control you're testing
   - Why these logs are needed
   - How they'll be used

3. **Follow Up**:
   - Confirm receipt of logs
   - Verify completeness
   - Ask clarifying questions
   - Thank Chuck for assistance

## Common Log Collection Issues

### Issue: Logs Not Available
**Cause**: Logging not enabled or retention expired
**Action**: Document the gap, notify Victor, request configuration evidence

### Issue: Logs Too Large
**Cause**: Long time period or high-volume environment
**Action**: Request filtered logs or samples, discuss scope with Victor

### Issue: Access Denied
**Cause**: Permissions issue
**Action**: Work with Chuck to get proper access or alternative export

### Issue: Log Format Unclear
**Cause**: Unfamiliar log structure
**Action**: Request documentation, ask Chuck for explanation, escalate to Victor

## Tools and Commands

### Useful AWS CLI Commands (if you have access):

```bash
# List CloudTrail trails
aws cloudtrail describe-trails

# List CloudWatch log groups
aws logs describe-log-groups

# List VPC Flow Logs
aws ec2 describe-flow-logs

# Query CloudWatch Logs
aws logs filter-log-events --log-group-name [name] --start-time [timestamp]
```

### Log Analysis Tools:

- Text editors for viewing log files
- Spreadsheet software for CSV analysis
- JSON viewers for CloudTrail logs
- Log aggregation tools (if available)

## Quality Standards

- Collect complete log sets (no partial data)
- Verify log integrity
- Document collection method
- Preserve original log files
- Note any processing or filtering
- Maintain chain of custody

## Professional Conduct

- Be thorough in log collection
- Document everything
- Ask questions when unsure
- Escalate issues promptly
- Respect data confidentiality
- Maintain objectivity
- Follow Victor's guidance

## Learning Resources

To improve your log analysis skills:
- Study CloudTrail event reference
- Learn common AWS API calls
- Understand VPC Flow Log format
- Practice log filtering and searching
- Review security incident examples
