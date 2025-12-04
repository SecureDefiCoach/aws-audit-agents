# Network Security Control Testing Procedures

## Overview
This document provides standardized procedures for testing network security controls in AWS environments. These procedures can be used by any auditor assigned to test network controls.

## Control Domain
- **Domain**: Network Security
- **Applicable To**: All auditors testing network controls
- **Reference**: ISACA IT Audit Programs

## Key Control Objectives

### 1. Security Group Configuration
**Control Objective**: Security groups follow least privilege and deny unnecessary access

**Testing Procedures**:
1. Obtain complete security group inventory
2. Review all inbound rules
3. Review all outbound rules
4. Identify overly permissive rules (0.0.0.0/0)
5. Check for unused security groups
6. Verify security group descriptions exist

**Evidence to Request**:
- Complete security group inventory
- Security group rules for each group
- Security group associations (which resources)
- Network architecture diagrams
- Security group standards documentation

**Critical Rules to Review**:
- SSH (port 22) from 0.0.0.0/0
- RDP (port 3389) from 0.0.0.0/0
- Database ports (3306, 5432, 1433) from 0.0.0.0/0
- All ports (0-65535) from 0.0.0.0/0
- Outbound all traffic when not needed

**Expected Results**:
- No SSH/RDP from internet (0.0.0.0/0)
- No database ports from internet
- Inbound rules limited to specific IPs/ranges
- Outbound rules follow least privilege
- All rules have descriptions
- No unused security groups

**Risk Rating if Failed**: High (for critical services), Medium (for others)

---

### 2. Network ACL Configuration
**Control Objective**: Network ACLs provide subnet-level protection

**Testing Procedures**:
1. Obtain NACL inventory for all VPCs
2. Review NACL rules for each subnet
3. Check rule ordering and precedence
4. Verify appropriate allow/deny rules
5. Identify overly permissive NACLs
6. Check for conflicting rules

**Evidence to Request**:
- NACL configurations for all VPCs
- Subnet associations
- NACL rule sets
- Network architecture showing subnet design

**Expected Results**:
- NACLs configured for each subnet
- Rules follow least privilege
- No conflicting rules
- Rule ordering is correct
- Appropriate deny rules in place

**Risk Rating if Failed**: Medium

---

### 3. VPC Configuration and Isolation
**Control Objective**: VPCs are properly configured and isolated

**Testing Procedures**:
1. Review VPC inventory
2. Check VPC CIDR blocks for conflicts
3. Verify subnet design (public vs private)
4. Review route tables
5. Check VPC peering configurations
6. Verify network isolation between environments

**Evidence to Request**:
- VPC inventory with CIDR blocks
- Subnet configurations (public/private)
- Route table configurations
- VPC peering connections
- Network architecture diagrams
- Environment isolation documentation

**Expected Results**:
- Separate VPCs for different environments (prod, dev, test)
- No CIDR conflicts
- Clear public/private subnet separation
- Appropriate route tables
- Controlled VPC peering
- Network isolation enforced

**Risk Rating if Failed**: Medium to High

---

### 4. Internet Gateway and NAT Configuration
**Control Objective**: Internet access is controlled and monitored

**Testing Procedures**:
1. Identify all internet gateways
2. Review which subnets have internet access
3. Check NAT gateway/instance configurations
4. Verify private subnets use NAT for outbound
5. Review route tables for internet routes
6. Check for unintended internet exposure

**Evidence to Request**:
- Internet gateway inventory
- NAT gateway/instance configurations
- Route tables showing internet routes
- Subnet classifications (public/private)
- Network architecture diagrams

**Expected Results**:
- Internet gateways only in public subnets
- Private subnets use NAT for outbound
- No direct internet access for private resources
- Appropriate route table configurations
- Controlled internet exposure

**Risk Rating if Failed**: High

---

### 5. VPN and Direct Connect Security
**Control Objective**: Remote connectivity is secure and properly configured

**Testing Procedures**:
1. Review VPN configurations
2. Check VPN encryption settings
3. Verify VPN authentication methods
4. Review Direct Connect configurations
5. Check for redundancy
6. Verify monitoring of connections

**Evidence to Request**:
- VPN configuration details
- VPN encryption settings
- Authentication methods
- Direct Connect configurations
- Connection monitoring procedures
- Redundancy documentation

**Expected Results**:
- Strong VPN encryption (AES-256)
- Multi-factor authentication for VPN
- Redundant connections where required
- Connection monitoring in place
- Proper routing configurations

**Risk Rating if Failed**: High

---

### 6. Public IP Address Management
**Control Objective**: Public IP addresses are minimized and controlled

**Testing Procedures**:
1. Identify all resources with public IPs
2. Review business justification for public IPs
3. Check for unnecessary public exposure
4. Verify Elastic IP usage
5. Review public IP assignment procedures

**Evidence to Request**:
- Inventory of resources with public IPs
- Business justification for each
- Elastic IP inventory
- Public IP assignment procedures
- Network architecture showing public resources

**Expected Results**:
- Minimal public IP usage
- Business justification for all public IPs
- No unnecessary public exposure
- Elastic IPs properly managed
- Public IP assignment controlled

**Risk Rating if Failed**: Medium

---

### 7. Network Segmentation
**Control Objective**: Network is properly segmented by function and sensitivity

**Testing Procedures**:
1. Review network architecture
2. Verify segmentation by tier (web, app, database)
3. Check segmentation by environment (prod, dev, test)
4. Review security group rules between segments
5. Verify micro-segmentation where appropriate

**Evidence to Request**:
- Network architecture diagrams
- Subnet design documentation
- Security group rules between tiers
- Segmentation standards
- Traffic flow diagrams

**Expected Results**:
- Clear network segmentation
- Separate subnets for different tiers
- Controlled traffic between segments
- Environment isolation
- Appropriate security group rules

**Risk Rating if Failed**: Medium to High

---

### 8. Network Monitoring and Logging
**Control Objective**: Network traffic is monitored and logged

**Testing Procedures**:
1. Verify VPC Flow Logs are enabled
2. Review flow log retention
3. Check for network monitoring tools
4. Verify intrusion detection/prevention
5. Review network alert configurations

**Evidence to Request**:
- VPC Flow Log configurations
- Flow log retention settings
- Network monitoring tool documentation
- IDS/IPS configurations
- Network alert procedures
- Sample network alerts

**Expected Results**:
- VPC Flow Logs enabled for all VPCs
- Adequate retention period (30+ days)
- Network monitoring tools deployed
- IDS/IPS where appropriate
- Network alerts configured
- Regular log review

**Risk Rating if Failed**: Medium

---

## Evidence Collection Guidelines

### Security Group Analysis

When reviewing security groups:

1. **Identify High-Risk Rules**:
   - Any rule with source 0.0.0.0/0
   - SSH (22) or RDP (3389) from internet
   - Database ports from internet
   - All ports open

2. **Document Each High-Risk Rule**:
   - Security group ID and name
   - Rule details (protocol, port, source)
   - Associated resources
   - Business justification (if any)

3. **Risk Assessment**:
   - Critical: Database or admin access from internet
   - High: SSH/RDP from internet
   - Medium: Other services from internet
   - Low: Outbound restrictions missing

### Working with Company Representatives

When requesting network evidence from Chuck:

1. **Request Complete Inventories**:
   - All security groups with rules
   - All NACLs with rules
   - All VPCs with subnets
   - All internet gateways and NAT gateways

2. **Request Architecture Diagrams**:
   - Network topology
   - Traffic flows
   - Segmentation design

3. **Request Justifications**:
   - Why certain rules exist
   - Business need for public access
   - Compensating controls

## Testing Techniques

### Security Group Testing

1. **Systematic Review**:
   - Export all security groups to spreadsheet
   - Filter for 0.0.0.0/0 rules
   - Identify critical ports (22, 3389, 3306, 5432)
   - Document each high-risk rule

2. **Resource Association**:
   - Identify which resources use risky security groups
   - Assess criticality of exposed resources
   - Determine if exposure is necessary

3. **Rule Validation**:
   - Request business justification
   - Check for compensating controls
   - Verify monitoring is in place

### Network Architecture Review

1. **Diagram Analysis**:
   - Verify segmentation
   - Check isolation between environments
   - Identify internet-facing resources
   - Review traffic flows

2. **Route Table Analysis**:
   - Check for unintended internet routes
   - Verify private subnets use NAT
   - Confirm no direct internet access for private resources

## Workpaper Documentation

Every network control test must include:

1. **Control Objective**: What you're testing
2. **Procedure**: Steps you performed
3. **Evidence**: Configurations reviewed
4. **Findings**: High-risk rules or configurations
5. **Analysis**: Risk assessment for each finding
6. **Business Justification**: Company's explanation (if any)
7. **Compensating Controls**: Other controls that mitigate risk
8. **Conclusion**: Effective, ineffective, or needs improvement
9. **Issues**: Any deficiencies with risk ratings

## Common Network Security Issues

### Critical Issues (High Risk)
- Database ports open to internet (0.0.0.0/0)
- SSH/RDP open to internet without MFA
- No network segmentation
- Production and development in same network
- No VPC Flow Logs
- Overly permissive security groups on critical resources

### Significant Issues (Medium Risk)
- Some unnecessary public IPs
- Weak network segmentation
- Missing NACLs
- No network monitoring
- Inconsistent security group standards
- Missing security group descriptions

### Minor Issues (Low Risk)
- Unused security groups not removed
- Inconsistent naming conventions
- Documentation gaps
- Some outbound rules could be more restrictive

## Risk Assessment Considerations

### High-Risk Indicators
- Critical services exposed to internet
- No network segmentation
- No network monitoring
- Flat network architecture
- No VPC Flow Logs

### Medium-Risk Indicators
- Some unnecessary internet exposure
- Basic segmentation only
- Limited network monitoring
- Some overly permissive rules

### Low-Risk Indicators
- Minimal internet exposure
- Strong network segmentation
- Comprehensive monitoring
- Least privilege security groups
- Regular security group reviews

## Tools and Queries

### Useful AWS CLI Commands

```bash
# List all security groups
aws ec2 describe-security-groups

# Find security groups with 0.0.0.0/0
aws ec2 describe-security-groups --query 'SecurityGroups[?IpPermissions[?IpRanges[?CidrIp==`0.0.0.0/0`]]]'

# List all NACLs
aws ec2 describe-network-acls

# List all VPCs
aws ec2 describe-vpcs

# List all subnets
aws ec2 describe-subnets

# List internet gateways
aws ec2 describe-internet-gateways

# List NAT gateways
aws ec2 describe-nat-gateways

# List VPC Flow Logs
aws ec2 describe-flow-logs
```

### AWS Console Locations

- Security Groups: EC2 → Security Groups
- NACLs: VPC → Network ACLs
- VPCs: VPC → Your VPCs
- Subnets: VPC → Subnets
- Route Tables: VPC → Route Tables
- Internet Gateways: VPC → Internet Gateways
- NAT Gateways: VPC → NAT Gateways
- VPC Flow Logs: VPC → Your VPCs → Flow Logs

## Professional Standards

- Identify all high-risk network exposures
- Assess risk based on resource criticality
- Request business justification for risky configurations
- Consider compensating controls
- Document all findings with evidence
- Escalate critical exposures immediately
- Maintain objectivity in risk assessment
- Verify network segmentation is effective
