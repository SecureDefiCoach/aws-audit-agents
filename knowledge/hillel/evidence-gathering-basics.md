# Evidence Gathering Basics

## Purpose
This guide helps staff auditors collect audit evidence from AWS services accurately and efficiently.

## What is Audit Evidence?

Audit evidence is information used to support audit findings and conclusions. Good evidence is:
- **Relevant**: Relates to the control being tested
- **Reliable**: From trustworthy sources
- **Sufficient**: Enough to support the conclusion
- **Timely**: Current and up-to-date

## Types of Evidence

### 1. Configuration Evidence
- AWS service settings and configurations
- IAM policies and permissions
- Security group rules
- Encryption settings
- Logging configurations

**How to Collect**:
- Use AWS Console (take screenshots)
- Use AWS CLI (save command output)
- Export to JSON/CSV when possible
- Use AWS Config for historical data

### 2. Log Evidence
- CloudTrail logs
- CloudWatch logs
- S3 access logs
- VPC flow logs
- Application logs

**How to Collect**:
- Query logs for specific time periods
- Filter for relevant events
- Export log data
- Document query parameters used

### 3. Interview Evidence
- Discussions with system owners
- Walkthroughs of processes
- Explanations of controls
- Demonstrations of procedures

**How to Collect**:
- Take detailed notes
- Document who, when, what
- Request follow-up documentation
- Verify understanding

### 4. Documentation Evidence
- Policies and procedures
- Architecture diagrams
- Change management records
- Incident reports
- Previous audit reports

**How to Collect**:
- Request from client
- Verify version and date
- Check for approvals
- Note any gaps or inconsistencies

## Evidence Collection Process

### Step 1: Understand What You Need
- Review the control objective
- Read the testing procedures
- Identify required evidence types
- Clarify any questions with senior auditor

### Step 2: Plan Your Collection
- Determine where evidence is located
- Identify tools needed (Console, CLI, API)
- Check access permissions
- Estimate time required

### Step 3: Collect the Evidence
- Follow testing procedures exactly
- Document collection method
- Take clear screenshots
- Save raw data files
- Note any issues or limitations

### Step 4: Label and Store Evidence
- Assign unique evidence ID (EVD-XXX-###)
- Include collection date and time
- Note who collected it
- Store in proper folder
- Update evidence log

### Step 5: Document in Workpaper
- Reference evidence by ID
- Describe what evidence shows
- Note any observations
- Flag any concerns for senior auditor

## Using AWS Tools

### AWS Console
**Best for**: Quick checks, screenshots, visual evidence

**Tips**:
- Use full-screen for screenshots
- Include timestamps
- Show relevant filters/settings
- Capture multiple views if needed

### AWS CLI
**Best for**: Bulk data collection, automation, detailed queries

**Common Commands**:
```bash
# List IAM users
aws iam list-users

# Get S3 bucket encryption
aws s3api get-bucket-encryption --bucket bucket-name

# List security groups
aws ec2 describe-security-groups

# Get CloudTrail status
aws cloudtrail describe-trails
```

**Tips**:
- Save command output to files
- Use --output json for structured data
- Document the exact command used
- Include AWS region in documentation

### AWS Config
**Best for**: Historical configurations, compliance checks

**Tips**:
- Query for specific time periods
- Check configuration history
- Review compliance status
- Export results

## Evidence Quality Checklist

Before submitting evidence, verify:
- [ ] Evidence ID is unique and follows naming convention
- [ ] Collection date and time are documented
- [ ] Collection method is noted
- [ ] Evidence is relevant to control objective
- [ ] Evidence is complete (not partial)
- [ ] Screenshots are clear and readable
- [ ] Files are properly named
- [ ] Evidence is stored in correct folder
- [ ] Evidence log is updated

## Common Mistakes to Avoid

### ❌ Don't Do This
- Collect evidence without understanding why
- Take unclear or partial screenshots
- Forget to document collection method
- Mix up evidence from different controls
- Lose track of evidence IDs
- Collect outdated evidence
- Skip documentation steps

### ✅ Do This Instead
- Ask questions if unsure
- Take clear, complete screenshots
- Document everything
- Keep evidence organized by control
- Use consistent naming conventions
- Verify evidence is current
- Follow procedures exactly

## When to Ask for Help

Contact your senior auditor if:
- You don't understand what evidence to collect
- You can't access required AWS services
- Evidence doesn't match expectations
- You find something concerning
- You're stuck or running behind schedule
- You need clarification on procedures

## Evidence Storage

### Folder Structure
```
output/evidence/
├── EVD-IAM-001.json
├── EVD-IAM-002.json
├── EVD-S3-001.json
└── ...
```

### File Naming
- Use evidence ID as filename
- Include extension (.json, .csv, .txt, .png)
- No spaces in filenames
- Use consistent format

### Evidence Log
Maintain a log with:
- Evidence ID
- Control domain
- Description
- Collection date
- Collected by
- File location

## Quality Standards

Your evidence should be:
- **Complete**: All required data collected
- **Accurate**: No errors or omissions
- **Clear**: Easy to understand
- **Organized**: Properly labeled and stored
- **Documented**: Collection method noted
- **Timely**: Collected during audit period

## Remember
- Quality is more important than speed
- When in doubt, ask questions
- Document everything
- Double-check your work
- Keep evidence organized
- Maintain professional standards
