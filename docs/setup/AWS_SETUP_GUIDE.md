# AWS Setup Guide for Audit Agent System

This guide will help you set up an AWS account and configure credentials for the AWS Audit Agent System.

## Prerequisites

- Email address for AWS account
- Credit card (required by AWS, but won't be charged if you stay within Free Tier)
- Python 3.11+ installed
- AWS CLI installed (optional but recommended)

## Step 1: Create AWS Account

1. Go to https://aws.amazon.com/
2. Click "Create an AWS Account"
3. Follow the registration process:
   - Enter email and account name
   - Provide contact information
   - Enter payment information (required but won't be charged for Free Tier usage)
   - Verify identity via phone
   - Select "Basic Support - Free" plan

## Step 2: Create IAM User for the Agent

**IMPORTANT**: Never use your root account credentials for the agent. Create an IAM user instead.

### Option A: Least Privilege (Recommended - More Secure)

Use custom IAM policies that follow the principle of least privilege:

1. Sign in to AWS Console: https://console.aws.amazon.com/
2. Navigate to IAM service
3. **First, create the custom policy:**
   - Click "Policies" → "Create policy"
   - Click "JSON" tab
   - Copy contents from `reference/iam-policies/company-setup-agent-policy.json`
   - Click "Next: Tags" → "Next: Review"
   - Name: `CompanySetupAgentPolicy`
   - Click "Create policy"
4. **Then, create the user:**
   - Click "Users" → "Add users"
   - Username: `company-setup-agent`
   - Access type: ✅ Programmatic access
   - Click "Next: Permissions"
   - Click "Attach existing policies directly"
   - Search for `CompanySetupAgentPolicy`
   - Check the box next to it
   - Click "Next: Tags" → "Next: Review" → "Create user"
5. **IMPORTANT**: Download the CSV file with credentials or copy:
   - Access Key ID
   - Secret Access Key

**Benefits:** Minimal permissions, restricted to specific resource patterns, limited blast radius if compromised.

### Option B: Managed Policies (Simpler but Less Secure)

Use AWS managed policies for quicker setup:

1. Sign in to AWS Console: https://console.aws.amazon.com/
2. Navigate to IAM service
3. Click "Users" → "Add users"
4. User details:
   - Username: `audit-agent-admin`
   - Access type: ✅ Programmatic access
5. Set permissions:
   - Attach existing policies directly
   - Select these policies:
     - `IAMFullAccess` (to create IAM users)
     - `AmazonS3FullAccess` (to create S3 buckets)
     - `AmazonEC2FullAccess` (to create EC2 instances)
     - `AWSCloudTrailFullAccess` (to enable CloudTrail)
6. Add tags (optional):
   - Key: `Purpose`, Value: `AuditAgentSystem`
7. Review and create user
8. **IMPORTANT**: Download the CSV file with credentials or copy:
   - Access Key ID
   - Secret Access Key

**Note:** This grants broader permissions than needed. Use Option A for production or article demonstrations.

See `reference/iam-policies/README.md` for detailed policy documentation.

## Step 3: Configure AWS Credentials

### Option A: Using AWS CLI (Recommended)

```bash
# Install AWS CLI if not already installed
# macOS: brew install awscli
# Linux: pip install awscli
# Windows: Download from https://aws.amazon.com/cli/

# Configure credentials
aws configure

# Enter when prompted:
# AWS Access Key ID: [your-access-key-id]
# AWS Secret Access Key: [your-secret-access-key]
# Default region name: us-east-1
# Default output format: json
```

### Option B: Manual Configuration

Create `~/.aws/credentials` file:

```ini
[default]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
```

Create `~/.aws/config` file:

```ini
[default]
region = us-east-1
output = json
```

### Option C: Environment Variables

```bash
export AWS_ACCESS_KEY_ID=your_access_key_id
export AWS_SECRET_ACCESS_KEY=your_secret_access_key
export AWS_DEFAULT_REGION=us-east-1
```

## Step 4: Verify Credentials

Test that your credentials work:

```bash
# Using AWS CLI
aws sts get-caller-identity

# Should output something like:
# {
#     "UserId": "AIDAXXXXXXXXXXXXXXXXX",
#     "Account": "123456789012",
#     "Arn": "arn:aws:iam::123456789012:user/audit-agent-admin"
# }
```

Or test with Python:

```python
import boto3

# This should not raise an error
sts = boto3.client('sts')
identity = sts.get_caller_identity()
print(f"Account: {identity['Account']}")
print(f"User: {identity['Arn']}")
```

## Step 5: Set Up Budget Alerts

To avoid unexpected charges:

1. Go to AWS Billing Console: https://console.aws.amazon.com/billing/
2. Click "Budgets" → "Create budget"
3. Select "Cost budget"
4. Set budget amount: $5 USD
5. Configure alerts:
   - Alert at 50% ($2.50)
   - Alert at 80% ($4.00)
   - Alert at 100% ($5.00)
6. Enter your email for notifications

## Step 6: Run the Company Setup Agent

### Dry Run Mode (Recommended First)

Test without creating real resources:

```bash
source venv/bin/activate
python examples/company_setup_example.py
```

The agent runs in dry-run mode by default, showing what would be created.

### Real Mode

To create actual AWS resources:

```python
from src.agents.company_setup import CompanySetupAgent

agent = CompanySetupAgent(
    region='us-east-1',
    simulation_tag='audit-demo-2025',
    seed=42,
    dry_run=False  # Set to False for real resource creation
)

profile = agent.run_setup(
    template_path='templates/cloudretail_company.yaml',
    output_dir='output'
)
```

## Free Tier Limits

The template is designed to stay within AWS Free Tier:

| Service | Free Tier Limit | Template Usage |
|---------|----------------|----------------|
| IAM | Unlimited | 5 users |
| S3 | 5 GB storage, 20,000 GET requests | ~1 GB total |
| EC2 | 750 hours/month t2.micro | 2 instances |
| CloudTrail | 1 trail free | 1 trail |
| VPC | Unlimited | Uses default VPC |

**Estimated Monthly Cost**: $0.00 (within Free Tier)

## Important Notes

### What Gets Created

When you run the agent with `dry_run=False`:

- ✅ 5 IAM users with various access levels
- ✅ 3 S3 buckets with sample files (~1 GB total)
- ✅ 2 EC2 t2.micro instances (Free Tier eligible)
- ✅ Security groups for EC2 instances
- ✅ CloudTrail logging to S3
- ✅ All resources tagged with `simulation-id`

### Cleanup

To avoid ongoing charges, you'll need to delete resources when done:

```bash
# Stop EC2 instances
aws ec2 stop-instances --instance-ids i-xxxxx i-yyyyy

# Terminate EC2 instances
aws ec2 terminate-instances --instance-ids i-xxxxx i-yyyyy

# Delete S3 buckets (must be empty first)
aws s3 rm s3://bucket-name --recursive
aws s3 rb s3://bucket-name

# Delete IAM users (must remove policies and access keys first)
aws iam delete-user --user-name username

# Delete CloudTrail
aws cloudtrail delete-trail --name trail-name
```

A cleanup script will be implemented in a later task.

## Troubleshooting

### "Access Denied" Errors

- Verify IAM user has correct policies attached
- Check that credentials are configured correctly
- Ensure you're using IAM user credentials, not root account

### "Bucket Already Exists" Errors

- S3 bucket names must be globally unique
- Modify bucket names in the template to include a unique suffix
- Example: `cloudretail-customer-data-yourname-20251203`

### "Free Tier Exceeded" Warnings

- Check AWS Billing Dashboard
- Verify you're using t2.micro instances (not t2.small or larger)
- Ensure you're not running instances 24/7 (750 hours = 31 days for 1 instance)

### EC2 Instance Launch Failures

- Check if you have a default VPC in your region
- Verify the AMI ID is valid for your region
- Ensure you haven't exceeded EC2 instance limits

## Security Best Practices

1. **Never commit credentials to Git**
   - Add `.aws/` to `.gitignore`
   - Use environment variables or AWS credentials file

2. **Use IAM users, not root account**
   - Root account should have MFA enabled
   - Only use root for account-level tasks

3. **Enable MFA on IAM users**
   - Especially for users with admin access

4. **Rotate access keys regularly**
   - AWS recommends every 90 days

5. **Monitor costs daily**
   - Check AWS Billing Dashboard
   - Set up budget alerts

6. **Clean up resources promptly**
   - Don't leave EC2 instances running
   - Delete S3 buckets when done

## Next Steps

Once your AWS account is set up and credentials are configured:

1. Run the agent in dry-run mode to verify everything works
2. Review the output to understand what will be created
3. Run in real mode to create actual AWS resources
4. Use AWS Console to verify resources were created
5. Proceed with implementing the audit agents (next tasks)

## Support

If you encounter issues:

1. Check AWS Service Health Dashboard: https://status.aws.amazon.com/
2. Review AWS Free Tier usage: https://console.aws.amazon.com/billing/home#/freetier
3. Consult AWS documentation: https://docs.aws.amazon.com/
4. Check CloudTrail logs for API errors

## Cost Monitoring

Monitor your costs to ensure you stay within Free Tier:

```bash
# Check current month costs
aws ce get-cost-and-usage \
  --time-period Start=2025-12-01,End=2025-12-31 \
  --granularity MONTHLY \
  --metrics BlendedCost
```

Or visit: https://console.aws.amazon.com/billing/home#/bills
