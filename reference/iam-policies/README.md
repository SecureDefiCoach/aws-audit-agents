# IAM Policies - Least Privilege Approach

This folder contains IAM policies following the principle of least privilege for the AWS Audit Agent System.

## Policies

### 1. company-setup-agent-policy.json

**Purpose:** Minimal permissions needed to create the simulated company infrastructure.

**Permissions:**
- **IAM:** Create/delete users with specific name patterns (admin-*, dev-*, etc.)
- **S3:** Create/manage buckets with "cloudretail-" prefix only
- **EC2:** Launch/terminate t2.micro instances in us-east-1/us-east-2 only
- **Security Groups:** Create/manage security groups
- **VPC:** Read-only access (uses default VPC)
- **CloudTrail:** Create/manage trails with "cloudretail-" prefix only
- **Tagging:** Tag resources with simulation-id tag
- **Cost Monitoring:** Read-only access to billing

**Restrictions:**
- Cannot create IAM users outside naming pattern
- Cannot create S3 buckets outside "cloudretail-" prefix
- Cannot launch instances outside specified regions
- Cannot modify existing VPCs
- Cannot access resources without simulation tag

### 2. audit-agent-readonly-policy.json

**Purpose:** Read-only permissions for audit agents to collect evidence.

**Permissions:**
- **IAM:** Read user information, policies, access keys, MFA status
- **S3:** Read bucket configurations and objects
- **EC2:** Read instance and security group information
- **VPC:** Read network configurations
- **CloudTrail:** Read trail configurations and events
- **CloudWatch:** Read alarms and logs
- **Cost Monitoring:** Read-only access to billing

**Restrictions:**
- No write permissions to any service
- Cannot create, modify, or delete resources
- Cannot access credentials or secrets

## Setup Instructions

### Option 1: Use Custom Policies (Recommended - Least Privilege)

1. **Create Company Setup User:**
   ```bash
   # In AWS Console:
   # IAM → Users → Add users
   # Username: company-setup-agent
   # Access type: Programmatic access
   # Permissions: Create custom policy
   # Copy contents of company-setup-agent-policy.json
   ```

2. **Create Audit Agent User:**
   ```bash
   # In AWS Console:
   # IAM → Users → Add users
   # Username: audit-agent-readonly
   # Access type: Programmatic access
   # Permissions: Create custom policy
   # Copy contents of audit-agent-readonly-policy.json
   ```

### Option 2: Use AWS Managed Policies (Simpler but Less Secure)

If you prefer simplicity over security for this demo:

**Company Setup Agent:**
- IAMFullAccess
- AmazonS3FullAccess
- AmazonEC2FullAccess
- AWSCloudTrailFullAccess

**Audit Agent:**
- ViewOnlyAccess
- CloudTrailReadOnlyAccess

⚠️ **Note:** Managed policies grant broader permissions than needed.

## Creating Custom Policies in AWS Console

1. Go to IAM → Policies → Create policy
2. Click "JSON" tab
3. Paste the policy JSON
4. Click "Next: Tags"
5. Click "Next: Review"
6. Name: `CompanySetupAgentPolicy` or `AuditAgentReadOnlyPolicy`
7. Description: "Least privilege policy for AWS Audit Agent System"
8. Click "Create policy"

## Attaching Policies to Users

1. Go to IAM → Users → [username]
2. Click "Add permissions"
3. Click "Attach existing policies directly"
4. Search for your custom policy name
5. Check the box next to it
6. Click "Next: Review"
7. Click "Add permissions"

## Security Benefits

### Least Privilege Advantages:

1. **Limited Blast Radius:** If credentials are compromised, damage is contained
2. **Resource Isolation:** Can only affect resources with specific naming patterns
3. **Region Restriction:** Cannot create resources in unauthorized regions
4. **Tag-Based Control:** Can only manage tagged resources
5. **Audit Trail:** Clear separation between setup and audit activities

### Comparison:

| Aspect | Managed Policies | Custom Policies |
|--------|-----------------|-----------------|
| Setup Time | 2 minutes | 5 minutes |
| Security | Moderate | High |
| Permissions | Broad | Minimal |
| Blast Radius | Large | Small |
| Best Practice | ❌ | ✅ |

## Testing Policies

After creating the policies, test them:

```python
# Test company setup agent
from src.agents.company_setup import CompanySetupAgent

agent = CompanySetupAgent(
    region='us-east-2',
    simulation_tag='audit-demo-2025',
    dry_run=False
)

# Should succeed with custom policy
profile = agent.run_setup(
    template_path='templates/cloudretail_company.yaml',
    output_dir='output'
)
```

## Troubleshooting

### "Access Denied" Errors

If you get access denied errors:

1. **Check policy is attached:** IAM → Users → [username] → Permissions
2. **Verify JSON syntax:** Policies → [policy name] → Edit
3. **Check resource ARNs:** Ensure bucket/user names match patterns
4. **Verify region:** Ensure you're in us-east-1 or us-east-2

### Common Issues

**Issue:** Cannot create IAM user "test-user"
**Solution:** User name must match pattern (admin-*, dev-*, etc.)

**Issue:** Cannot create S3 bucket "my-bucket"
**Solution:** Bucket name must start with "cloudretail-"

**Issue:** Cannot launch EC2 in us-west-2
**Solution:** Policy restricts to us-east-1 and us-east-2 only

## Cleanup Policy

For the cleanup agent (Task 22), you'll need a separate policy that allows deletion of tagged resources. This will be created when implementing that task.

## Recommendations

For this demonstration project:

1. **Development/Testing:** Use managed policies for speed
2. **Production/Article:** Use custom policies to demonstrate security best practices
3. **Screenshots:** Show the custom policies in your article to highlight security awareness

The custom policies demonstrate that you understand AWS security and follow industry best practices, which adds credibility to your audit agent system.
