# Agents Module

This module contains autonomous agents for the AWS Audit Agent System.

## CompanySetupAgent

The `CompanySetupAgent` is responsible for creating a simulated company infrastructure in AWS with intentional security issues for audit demonstration purposes.

### Features

- **Template-based setup**: Loads company configuration from YAML templates
- **Dummy data generation**: Uses Faker library to generate realistic fake data
- **Resource simulation**: Simulates creation of IAM users, S3 buckets, EC2 instances, VPC, and CloudTrail
- **Intentional security issues**: Introduces configurable security issues for audit testing
- **Resource tagging**: Tags all resources for tracking and cleanup
- **Profile generation**: Creates comprehensive company profile documents

### Usage

```python
from src.agents.company_setup import CompanySetupAgent

# Initialize agent
agent = CompanySetupAgent(
    region='us-east-1',
    simulation_tag='audit-demo-2025',
    seed=42
)

# Run complete setup
profile = agent.run_setup(
    template_path='templates/cloudretail_company.yaml',
    output_dir='output'
)

print(f"Created company: {profile.name}")
print(f"Total security issues: {len(profile.intentional_issues)}")
```

### Methods

- `load_template(template_path)`: Load company template from YAML file
- `generate_dummy_data()`: Generate realistic fake data using Faker
- `create_iam_users(dummy_data)`: Create IAM users with intentional issues
- `create_s3_buckets(dummy_data)`: Create S3 buckets with mixed security
- `create_ec2_instances()`: Create EC2 instances with security groups
- `create_vpc()`: Create VPC with basic configuration
- `enable_cloudtrail()`: Enable CloudTrail for audit logging
- `tag_resources()`: Apply simulation tags to all resources
- `generate_profile(dummy_data)`: Generate company profile document
- `save_profile_to_file(profile, output_dir)`: Save profile to JSON file
- `run_setup(template_path, output_dir)`: Run complete setup workflow

### Operating Modes

The agent supports two modes:

**1. Dry Run Mode (Default - Safe)**
```python
agent = CompanySetupAgent(dry_run=True)  # No real resources created
```
- Simulates resource creation without AWS API calls
- Safe for testing and development
- No AWS credentials required
- No costs incurred

**2. Real Mode (Creates Actual AWS Resources)**
```python
agent = CompanySetupAgent(dry_run=False)  # Creates real AWS resources
```
- Creates actual IAM users, S3 buckets, EC2 instances, etc.
- Requires AWS credentials configured
- Stays within Free Tier limits
- **IMPORTANT**: Resources will incur costs if Free Tier is exceeded

### AWS Setup Required

To use Real Mode, you need:

1. **AWS Account** with Free Tier eligibility
2. **AWS Credentials** configured (see `AWS_SETUP_GUIDE.md`)
3. **IAM Permissions** for IAM, S3, EC2, CloudTrail
4. **Budget Alerts** configured to monitor costs

See the complete setup guide: `AWS_SETUP_GUIDE.md`

### Template Format

Templates are YAML files that define:
- Company profile (name, business type, services)
- IAM users with roles and security issues
- S3 buckets with security configurations
- EC2 instances with security groups
- VPC configuration
- CloudTrail settings
- Intentional security issues mapped to ISACA control domains

See `templates/cloudretail_company.yaml` for a complete example.

### Output

The agent generates:
1. Console output showing all created resources and security issues
2. JSON file with complete company profile
3. Structured data for use by audit agents

Example output structure:
```json
{
  "name": "CloudRetail Inc",
  "business_type": "E-commerce Platform",
  "services": [...],
  "infrastructure": {...},
  "security_issues": [...]
}
```

### Requirements Coverage

This agent satisfies requirements 1.1-1.8 from the design specification:
- ✅ 1.1: Company profile with name, description, and services
- ✅ 1.2: Minimal AWS resources within Free Tier limits
- ✅ 1.3: Realistic fake user profiles
- ✅ 1.4: Small sample files under 1GB
- ✅ 1.5: Intentional security issues
- ✅ 1.6: Simulation tags for tracking
- ✅ 1.7: Company profile document output
- ✅ 1.8: Free Tier limit verification

### Examples

See `examples/company_setup_example.py` for detailed usage examples.
