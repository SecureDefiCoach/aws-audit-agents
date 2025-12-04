# Security Best Practices - AWS Audit Agent System

This document outlines the security best practices implemented in the AWS Audit Agent System.

## Principle of Least Privilege

The system follows the principle of least privilege by providing two custom IAM policies with minimal permissions:

### 1. Company Setup Agent Policy

**Purpose:** Create simulated company infrastructure

**Key Restrictions:**
- ✅ Can only create IAM users matching specific patterns (admin-*, dev-*, analyst-*, contractor-*, support-*)
- ✅ Can only create S3 buckets with "cloudretail-" prefix
- ✅ Can only launch EC2 instances in us-east-1 and us-east-2
- ✅ Cannot modify existing VPCs (uses default VPC)
- ✅ Can only manage CloudTrail trails with "cloudretail-" prefix
- ✅ All resources must be tagged with simulation-id

**What This Prevents:**
- ❌ Cannot create arbitrary IAM users
- ❌ Cannot create S3 buckets outside naming convention
- ❌ Cannot launch instances in other regions
- ❌ Cannot modify production resources
- ❌ Cannot access untagged resources

### 2. Audit Agent Read-Only Policy

**Purpose:** Collect evidence for audit procedures

**Key Restrictions:**
- ✅ Read-only access to IAM, S3, EC2, VPC, CloudTrail, CloudWatch
- ✅ Cannot create, modify, or delete any resources
- ✅ Cannot access credentials or secrets
- ✅ Cannot perform any write operations

**What This Prevents:**
- ❌ Cannot modify infrastructure
- ❌ Cannot delete evidence
- ❌ Cannot escalate privileges
- ❌ Cannot access sensitive data

## Security Layers

### Layer 1: IAM Policies (Preventive)
- Custom policies with minimal permissions
- Resource-based restrictions (naming patterns, regions)
- Tag-based access control

### Layer 2: Resource Tagging (Detective)
- All resources tagged with `simulation-id`
- Easy identification of demo resources
- Supports automated cleanup

### Layer 3: Region Restrictions (Preventive)
- Limited to us-east-1 and us-east-2
- Prevents accidental resource creation in expensive regions
- Reduces attack surface

### Layer 4: Naming Conventions (Preventive)
- Enforced naming patterns for all resources
- Prevents collision with production resources
- Clear identification of demo resources

### Layer 5: Budget Alerts (Detective)
- $1 and $5 thresholds
- Email notifications
- Early warning system

## Comparison: Managed vs Custom Policies

| Security Aspect | AWS Managed Policies | Custom Policies |
|----------------|---------------------|-----------------|
| **IAM Permissions** | Full access to all IAM | Only specific user patterns |
| **S3 Permissions** | Full access to all buckets | Only "cloudretail-*" buckets |
| **EC2 Permissions** | All regions, all instance types | us-east-1/2 only, tagged instances |
| **VPC Permissions** | Full VPC management | Read-only access |
| **Blast Radius** | Entire AWS account | Limited to tagged resources |
| **Setup Time** | 2 minutes | 5 minutes |
| **Security Level** | ⚠️ Moderate | ✅ High |
| **Best Practice** | ❌ No | ✅ Yes |

## Credential Management

### Do's ✅
- Store credentials in `~/.aws/credentials` file
- Use environment variables for temporary access
- Rotate access keys every 90 days
- Enable MFA on IAM users
- Use separate users for setup vs audit
- Delete access keys when not in use

### Don'ts ❌
- Never commit credentials to Git
- Never use root account credentials
- Never share access keys
- Never embed credentials in code
- Never use same credentials for multiple purposes
- Never leave credentials in plain text files

## Resource Isolation

All demo resources are isolated through:

1. **Naming Conventions:**
   - IAM users: `admin-*`, `dev-*`, etc.
   - S3 buckets: `cloudretail-*`
   - CloudTrail: `cloudretail-*`

2. **Tagging:**
   - `simulation-id`: `audit-demo-2025`
   - `created-by`: `CompanySetupAgent`
   - `created-at`: timestamp

3. **Region Restriction:**
   - Only us-east-1 and us-east-2
   - No global resource creation

## Audit Trail

All actions are logged through:

1. **CloudTrail:** AWS API calls
2. **Agent Logs:** Application-level actions
3. **Resource Tags:** Creation metadata
4. **Budget Alerts:** Cost monitoring

## Incident Response

If credentials are compromised:

1. **Immediate Actions:**
   - Disable access keys in IAM console
   - Rotate credentials
   - Review CloudTrail logs for unauthorized activity

2. **Assessment:**
   - Check for unauthorized resources
   - Review budget for unexpected charges
   - Identify affected resources by tags

3. **Remediation:**
   - Delete unauthorized resources
   - Update IAM policies if needed
   - Generate new access keys
   - Update budget alerts

4. **Prevention:**
   - Enable MFA on all IAM users
   - Implement IP-based access restrictions
   - Set up CloudWatch alarms for suspicious activity

## Cleanup Security

When implementing the cleanup agent (Task 22):

1. **Verification Required:**
   - Confirm resources have simulation tag
   - Verify resource naming patterns
   - Check creation timestamps

2. **Deletion Order:**
   - Delete in dependency order
   - Log all deletions
   - Verify complete removal

3. **Safeguards:**
   - Cannot delete untagged resources
   - Cannot delete resources outside naming patterns
   - Requires explicit confirmation

## Compliance Considerations

This security approach aligns with:

- **NIST Cybersecurity Framework:** Identify, Protect, Detect, Respond, Recover
- **CIS AWS Foundations Benchmark:** IAM best practices
- **AWS Well-Architected Framework:** Security pillar
- **ISACA COBIT:** Access control and monitoring

## Recommendations for Production

If adapting this system for production use:

1. **Use AWS Organizations:** Separate demo account from production
2. **Implement SCPs:** Service Control Policies for additional guardrails
3. **Enable AWS Config:** Track configuration changes
4. **Use AWS SSO:** Centralized identity management
5. **Implement VPC Endpoints:** Private connectivity to AWS services
6. **Enable GuardDuty:** Threat detection
7. **Use Secrets Manager:** Secure credential storage
8. **Implement CloudWatch Alarms:** Real-time monitoring

## Security Checklist

Before running the agent:

- [ ] Custom IAM policies created and attached
- [ ] Access keys stored securely (not in code)
- [ ] Budget alerts configured ($1 and $5 thresholds)
- [ ] MFA enabled on root account
- [ ] CloudTrail enabled in account
- [ ] Region set to us-east-1 or us-east-2
- [ ] Simulation tag configured
- [ ] Credentials file has proper permissions (chmod 600)

After running the agent:

- [ ] Verify resources created with correct tags
- [ ] Check budget dashboard for costs
- [ ] Review CloudTrail logs for expected activity
- [ ] Confirm no unauthorized resources created
- [ ] Document access key IDs used
- [ ] Plan cleanup timeline

## Conclusion

By implementing least privilege IAM policies, the AWS Audit Agent System demonstrates:

1. **Security Awareness:** Understanding of AWS security best practices
2. **Professional Standards:** Following industry guidelines
3. **Risk Management:** Limiting blast radius of potential incidents
4. **Compliance:** Aligning with audit and security frameworks

This approach adds credibility to the demonstration and shows that the system is designed with security in mind from the start.
