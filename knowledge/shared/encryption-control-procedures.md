# Encryption Control Testing Procedures

## Overview
This document provides standardized procedures for testing encryption controls in AWS environments. These procedures can be used by any auditor assigned to test encryption controls.

## Control Domain
- **Domain**: Data Encryption
- **Applicable To**: All auditors testing encryption controls
- **Reference**: ISACA IT Audit Programs

## Key Control Objectives

### 1. S3 Bucket Encryption at Rest
**Control Objective**: All S3 data is encrypted at rest

**Testing Procedures**:
1. Obtain complete S3 bucket inventory
2. Check encryption status for each bucket
3. Verify encryption method (SSE-S3, SSE-KMS, SSE-C)
4. Review bucket policies requiring encryption
5. Test that unencrypted uploads are rejected
6. Identify any unencrypted buckets

**Evidence to Request**:
- Complete S3 bucket list with encryption status
- Bucket encryption configurations
- Bucket policies
- Test results showing encryption enforcement
- Business justification for any unencrypted buckets

**Expected Results**:
- All buckets have default encryption enabled
- SSE-KMS preferred for sensitive data
- Bucket policies enforce encryption
- No unencrypted objects in sensitive buckets

**Risk Rating if Failed**: High (for sensitive data), Medium (for non-sensitive)

---

### 2. EBS Volume Encryption
**Control Objective**: All EBS volumes are encrypted

**Testing Procedures**:
1. Obtain complete EBS volume inventory
2. Check encryption status for each volume
3. Verify encryption by default is enabled
4. Review KMS key usage
5. Identify any unencrypted volumes
6. Check snapshots are encrypted

**Evidence to Request**:
- EBS volume inventory with encryption status
- Account-level encryption by default setting
- KMS key configurations
- Snapshot encryption status
- Business justification for unencrypted volumes

**Expected Results**:
- All volumes encrypted
- Encryption by default enabled at account level
- Appropriate KMS keys used
- All snapshots encrypted

**Risk Rating if Failed**: High

---

### 3. RDS Database Encryption
**Control Objective**: All database data is encrypted at rest

**Testing Procedures**:
1. Obtain RDS instance inventory
2. Check encryption status for each instance
3. Verify automated backups are encrypted
4. Check read replicas are encrypted
5. Review KMS key usage
6. Identify any unencrypted databases

**Evidence to Request**:
- RDS instance inventory with encryption status
- Backup encryption configurations
- Read replica encryption status
- KMS key policies
- Business justification for unencrypted databases

**Expected Results**:
- All RDS instances encrypted
- Backups encrypted
- Read replicas encrypted
- Appropriate KMS keys used

**Risk Rating if Failed**: High

---

### 4. Encryption Key Management
**Control Objective**: Encryption keys are properly managed and protected

**Testing Procedures**:
1. Review KMS key inventory
2. Check key policies and access controls
3. Verify key rotation is enabled
4. Review key usage and grants
5. Check for customer-managed vs AWS-managed keys
6. Verify key deletion protection

**Evidence to Request**:
- KMS key inventory
- Key policies for each key
- Key rotation status
- Key usage reports
- Key grants
- Key deletion settings

**Expected Results**:
- Customer-managed keys for sensitive data
- Appropriate key policies (least privilege)
- Automatic key rotation enabled
- Key deletion protection enabled
- Regular key usage audits

**Risk Rating if Failed**: High

---

### 5. Encryption in Transit
**Control Objective**: Data is encrypted during transmission

**Testing Procedures**:
1. Review load balancer configurations
2. Check SSL/TLS certificate usage
3. Verify TLS version requirements (1.2+)
4. Review S3 bucket policies requiring HTTPS
5. Check API Gateway SSL configurations
6. Test that HTTP is redirected to HTTPS

**Evidence to Request**:
- Load balancer listener configurations
- SSL/TLS certificate inventory
- Certificate expiration dates
- S3 bucket policies
- API Gateway configurations
- Test results showing HTTPS enforcement

**Expected Results**:
- All public endpoints use HTTPS
- TLS 1.2 or higher required
- Valid SSL certificates
- HTTP redirects to HTTPS
- S3 bucket policies deny HTTP

**Risk Rating if Failed**: High (for sensitive data), Medium (for non-sensitive)

---

### 6. Certificate Management
**Control Objective**: SSL/TLS certificates are properly managed

**Testing Procedures**:
1. Obtain certificate inventory
2. Check certificate expiration dates
3. Verify certificate issuers (trusted CAs)
4. Review certificate renewal procedures
5. Check for self-signed certificates
6. Verify certificate monitoring/alerting

**Evidence to Request**:
- Certificate inventory with expiration dates
- Certificate renewal procedures
- Certificate monitoring configurations
- Recent certificate renewals
- Justification for any self-signed certificates

**Expected Results**:
- All certificates from trusted CAs
- No expired certificates
- Certificates renewed before expiration
- Automated renewal where possible
- Alerts for expiring certificates
- No self-signed certificates in production

**Risk Rating if Failed**: Medium

---

### 7. Secrets Management
**Control Objective**: Secrets and credentials are encrypted and managed securely

**Testing Procedures**:
1. Review use of AWS Secrets Manager or Parameter Store
2. Check for hardcoded credentials in code
3. Verify secrets are encrypted
4. Review secret rotation policies
5. Check secret access controls
6. Verify secrets are not in CloudFormation templates

**Evidence to Request**:
- Secrets Manager inventory
- Parameter Store inventory
- Code review results (no hardcoded secrets)
- Secret rotation configurations
- Secret access policies
- CloudFormation template review

**Expected Results**:
- Secrets stored in Secrets Manager or Parameter Store
- No hardcoded credentials
- Secrets encrypted with KMS
- Automatic rotation enabled where possible
- Least privilege access to secrets
- Secrets not exposed in templates or logs

**Risk Rating if Failed**: High

---

### 8. Data Classification and Encryption Standards
**Control Objective**: Encryption requirements match data sensitivity

**Testing Procedures**:
1. Review data classification policy
2. Verify encryption standards for each classification
3. Check that sensitive data uses appropriate encryption
4. Review encryption algorithm standards
5. Verify compliance with regulatory requirements

**Evidence to Request**:
- Data classification policy
- Encryption standards documentation
- Data inventory with classifications
- Encryption implementation for sensitive data
- Compliance requirement documentation

**Expected Results**:
- Clear data classification policy
- Encryption standards defined
- Sensitive data encrypted appropriately
- Strong encryption algorithms (AES-256)
- Compliance requirements met

**Risk Rating if Failed**: High (for sensitive data)

---

## Evidence Collection Guidelines

### Inventory Requests

1. **S3 Buckets**:
   - Bucket name
   - Encryption status
   - Encryption type
   - KMS key ID (if applicable)
   - Data classification

2. **EBS Volumes**:
   - Volume ID
   - Encryption status
   - KMS key ID
   - Attached instance
   - Data classification

3. **RDS Instances**:
   - Instance identifier
   - Encryption status
   - KMS key ID
   - Backup encryption status
   - Data classification

4. **KMS Keys**:
   - Key ID
   - Key alias
   - Key state
   - Rotation status
   - Key policy
   - Usage (which resources)

### Working with Company Representatives

When requesting encryption evidence from Chuck:

1. **Request Complete Inventories**:
   - All resources, not just samples
   - Include encryption status
   - Include data classifications

2. **Request Configurations**:
   - Screenshots of encryption settings
   - Policy documents
   - KMS key policies

3. **Request Test Results**:
   - Evidence that encryption is enforced
   - Test results showing unencrypted uploads fail

## Testing Techniques

### S3 Encryption Testing

1. **Review Bucket Encryption**:
   - Check default encryption setting
   - Verify encryption type
   - Review bucket policy

2. **Test Enforcement**:
   - Attempt unencrypted upload (should fail)
   - Verify policy denies unencrypted PutObject

3. **Sample Object Testing**:
   - Select sample objects
   - Verify encryption metadata
   - Check encryption key used

### EBS Encryption Testing

1. **Review Volume Encryption**:
   - Check encryption flag
   - Verify KMS key
   - Check snapshot encryption

2. **Test Account Settings**:
   - Verify encryption by default
   - Attempt to create unencrypted volume (should fail)

### RDS Encryption Testing

1. **Review Instance Encryption**:
   - Check encryption flag
   - Verify KMS key
   - Check backup encryption

2. **Review Read Replicas**:
   - Verify replicas are encrypted
   - Check same encryption as source

## Workpaper Documentation

Every encryption control test must include:

1. **Control Objective**: What you're testing
2. **Procedure**: Steps you performed
3. **Evidence**: Inventories and configurations reviewed
4. **Sample**: If sampling, document selection
5. **Findings**: Encrypted vs unencrypted resources
6. **Analysis**: Risk assessment of unencrypted data
7. **Conclusion**: Effective, ineffective, or needs improvement
8. **Issues**: Any unencrypted sensitive data with risk ratings

## Common Encryption Issues

### Critical Issues (High Risk)
- Sensitive data unencrypted at rest
- No encryption in transit for sensitive data
- Hardcoded credentials in code
- Weak encryption algorithms
- No key rotation
- Overly permissive key policies

### Significant Issues (Medium Risk)
- Some non-sensitive data unencrypted
- Encryption not enforced by policy
- Manual key rotation only
- Self-signed certificates in production
- Expiring certificates

### Minor Issues (Low Risk)
- Inconsistent encryption methods
- Documentation gaps
- Some AWS-managed keys where customer-managed preferred
- Certificate renewal process could be automated

## Risk Assessment Considerations

### High-Risk Indicators
- Sensitive data unencrypted
- No encryption in transit
- Secrets in code or logs
- No key management
- Weak encryption algorithms

### Medium-Risk Indicators
- Partial encryption implementation
- Some encryption not enforced
- Manual key management
- Limited key rotation

### Low-Risk Indicators
- Comprehensive encryption
- Encryption enforced by policy
- Automated key management
- Regular key rotation
- Strong encryption algorithms

## Tools and Queries

### Useful AWS CLI Commands

```bash
# List S3 buckets with encryption
aws s3api list-buckets
aws s3api get-bucket-encryption --bucket [bucket-name]

# List EBS volumes with encryption status
aws ec2 describe-volumes --query 'Volumes[*].[VolumeId,Encrypted]'

# List RDS instances with encryption status
aws rds describe-db-instances --query 'DBInstances[*].[DBInstanceIdentifier,StorageEncrypted]'

# List KMS keys
aws kms list-keys
aws kms describe-key --key-id [key-id]

# Get key rotation status
aws kms get-key-rotation-status --key-id [key-id]

# List certificates
aws acm list-certificates
```

### AWS Console Locations

- S3 Encryption: S3 → Buckets → Properties → Default encryption
- EBS Encryption: EC2 → Volumes → Encryption column
- RDS Encryption: RDS → Databases → Configuration → Encryption
- KMS Keys: KMS → Customer managed keys
- Certificates: Certificate Manager → Certificates

## Professional Standards

- Identify all unencrypted sensitive data
- Assess risk based on data classification
- Verify encryption is enforced, not optional
- Check key management practices
- Document all findings with evidence
- Escalate unencrypted sensitive data immediately
- Maintain objectivity in risk assessment
