"""
Company Setup Agent for AWS Audit Agent System.

This agent creates a simulated company infrastructure in AWS with intentional
security issues for audit demonstration purposes.
"""

import yaml
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

from src.utils.faker_generator import FakerGenerator
from src.models.company import CompanyProfile, SecurityIssue, InfrastructureConfig
from src.aws.iam_client import IAMClient
from src.aws.s3_client import S3Client
from src.aws.ec2_client import EC2Client
from src.aws.vpc_client import VPCClient
from src.aws.cloudtrail_client import CloudTrailClient

import boto3
from botocore.exceptions import ClientError


class CompanySetupAgent:
    """
    Agent responsible for setting up simulated company infrastructure.
    
    Creates AWS resources based on a template, introduces intentional security
    issues, and generates a company profile document for audit purposes.
    """
    
    def __init__(
        self,
        region: str = 'us-east-1',
        simulation_tag: str = 'audit-demo-2025',
        seed: int = 42,
        dry_run: bool = False
    ):
        """
        Initialize the Company Setup Agent.
        
        Args:
            region: AWS region for resource creation
            simulation_tag: Tag to apply to all created resources
            seed: Random seed for Faker generator
            dry_run: If True, simulate without creating real resources
        """
        self.region = region
        self.simulation_tag = simulation_tag
        self.faker = FakerGenerator(seed=seed)
        self.dry_run = dry_run
        self.template_data: Optional[Dict[str, Any]] = None
        self.created_resources: Dict[str, List[str]] = {
            'iam_users': [],
            's3_buckets': [],
            'ec2_instances': [],
            'vpc_id': None,
            'cloudtrail_name': None
        }
        
        # Initialize AWS clients (only if not dry run)
        if not dry_run:
            self.iam_client = boto3.client('iam', region_name=region)
            self.s3_client = boto3.client('s3', region_name=region)
            self.ec2_client = boto3.client('ec2', region_name=region)
            self.cloudtrail_client = boto3.client('cloudtrail', region_name=region)
        else:
            print("[CompanySetupAgent] Running in DRY RUN mode - no real resources will be created")
            self.iam_client = None
            self.s3_client = None
            self.ec2_client = None
            self.cloudtrail_client = None
    
    def load_template(self, template_path: str) -> Dict[str, Any]:
        """
        Load company template from YAML file.
        
        Args:
            template_path: Path to YAML template file
            
        Returns:
            Parsed template data as dictionary
            
        Raises:
            FileNotFoundError: If template file doesn't exist
            yaml.YAMLError: If template is invalid YAML
        """
        path = Path(template_path)
        if not path.exists():
            raise FileNotFoundError(f"Template file not found: {template_path}")
        
        with open(path, 'r') as f:
            self.template_data = yaml.safe_load(f)
        
        print(f"[CompanySetupAgent] Loaded template: {template_path}")
        return self.template_data
    
    def generate_dummy_data(self) -> Dict[str, Any]:
        """
        Generate dummy data using Faker for template placeholders.
        
        Uses the loaded template to determine what dummy data to generate.
        Enhances template data with realistic fake information.
        
        Returns:
            Dictionary containing generated dummy data
            
        Raises:
            ValueError: If template not loaded
        """
        if not self.template_data:
            raise ValueError("Template must be loaded before generating dummy data")
        
        dummy_data = {
            'generated_at': datetime.now().isoformat(),
            'users': [],
            'files': {}
        }
        
        # Generate dummy user data for IAM users
        iam_users = self.template_data.get('iam_users', [])
        for user_config in iam_users:
            # Extract name from email or username
            username = user_config.get('username', '')
            role = user_config.get('role', 'User')
            department = user_config.get('department', 'General')
            
            # Generate realistic name based on username
            if '-' in username:
                parts = username.split('-')
                first_name = parts[1].capitalize() if len(parts) > 1 else 'User'
            else:
                first_name = username.capitalize()
            
            full_name = f"{first_name} {self.faker.faker.last_name()}"
            
            dummy_data['users'].append({
                'username': username,
                'full_name': full_name,
                'role': role,
                'department': department,
                'email': user_config.get('email', f"{username}@example.com")
            })
        
        # Generate dummy file content for S3 buckets
        s3_buckets = self.template_data.get('s3_buckets', [])
        for bucket_config in s3_buckets:
            bucket_name = bucket_config.get('name', '')
            sample_files = bucket_config.get('sample_files', [])
            size_mb = bucket_config.get('size_mb', 10)
            
            dummy_data['files'][bucket_name] = []
            
            for file_path in sample_files:
                # Determine content type from file extension
                if file_path.endswith('.json'):
                    content_type = 'json'
                elif file_path.endswith('.csv'):
                    content_type = 'csv'
                elif file_path.endswith('.log'):
                    content_type = 'log'
                else:
                    content_type = 'text'
                
                # Generate small sample content (keep under Free Tier limits)
                content = self.faker.generate_file_content(
                    content_type=content_type,
                    size_kb=min(10, size_mb // len(sample_files))  # Small files
                )
                
                dummy_data['files'][bucket_name].append({
                    'path': file_path,
                    'content': content,
                    'size_bytes': len(content.encode('utf-8'))
                })
        
        print(f"[CompanySetupAgent] Generated dummy data for {len(dummy_data['users'])} users")
        print(f"[CompanySetupAgent] Generated dummy files for {len(dummy_data['files'])} buckets")
        
        return dummy_data

    
    def create_iam_users(self, dummy_data: Dict[str, Any]) -> List[str]:
        """
        Create IAM users with intentional security issues.
        
        Args:
            dummy_data: Generated dummy data containing user information
            
        Returns:
            List of created IAM user ARNs
        """
        if not self.template_data:
            raise ValueError("Template must be loaded first")
        
        iam_users = self.template_data.get('iam_users', [])
        created_users = []
        
        print(f"[CompanySetupAgent] Creating {len(iam_users)} IAM users...")
        
        for user_config in iam_users:
            username = user_config.get('username')
            access_level = user_config.get('access_level')
            create_access_key = user_config.get('create_access_key', False)
            custom_policy = user_config.get('custom_policy')
            security_issues = user_config.get('security_issues', [])
            
            if self.dry_run:
                # Simulate IAM user creation
                user_arn = f"arn:aws:iam::123456789012:user/{username}"
                print(f"  - [DRY RUN] Would create user: {username} (Access: {access_level})")
            else:
                try:
                    # Create the IAM user
                    response = self.iam_client.create_user(
                        UserName=username,
                        Tags=[
                            {'Key': 'simulation-id', 'Value': self.simulation_tag},
                            {'Key': 'created-by', 'Value': 'CompanySetupAgent'},
                            {'Key': 'Name', 'Value': username}
                        ]
                    )
                    user_arn = response['User']['Arn']
                    print(f"  - Created user: {username} (Access: {access_level})")
                    
                    # Attach managed policy based on access level
                    if access_level and access_level != 'Custom':
                        policy_arn = f"arn:aws:iam::aws:policy/{access_level}"
                        try:
                            self.iam_client.attach_user_policy(
                                UserName=username,
                                PolicyArn=policy_arn
                            )
                            print(f"    ✓ Attached policy: {access_level}")
                        except ClientError as e:
                            print(f"    ⚠️  Could not attach policy {access_level}: {e}")
                    
                    # Create custom inline policy if specified
                    if custom_policy:
                        policy_document = {
                            "Version": "2012-10-17",
                            "Statement": [{
                                "Effect": "Allow",
                                "Action": custom_policy,
                                "Resource": "*"
                            }]
                        }
                        self.iam_client.put_user_policy(
                            UserName=username,
                            PolicyName=f"{username}-custom-policy",
                            PolicyDocument=json.dumps(policy_document)
                        )
                        print(f"    ✓ Created custom policy with {len(custom_policy)} actions")
                    
                    # Create access key if specified (intentional security issue)
                    if create_access_key:
                        key_response = self.iam_client.create_access_key(UserName=username)
                        access_key_id = key_response['AccessKey']['AccessKeyId']
                        print(f"    🔑 Created access key: {access_key_id}")
                    
                except ClientError as e:
                    if e.response['Error']['Code'] == 'EntityAlreadyExists':
                        print(f"  - User {username} already exists, skipping...")
                        user_arn = f"arn:aws:iam::123456789012:user/{username}"
                    else:
                        print(f"  - Error creating user {username}: {e}")
                        continue
            
            # Log intentional security issues
            for issue in security_issues:
                print(f"    ⚠️  Intentional issue: {issue.get('type')} - {issue.get('description')}")
            
            created_users.append(user_arn)
            self.created_resources['iam_users'].append(username)
        
        print(f"[CompanySetupAgent] ✓ Created {len(created_users)} IAM users")
        return created_users
    
    def create_s3_buckets(self, dummy_data: Dict[str, Any]) -> List[str]:
        """
        Create S3 buckets with mixed security configurations.
        
        Args:
            dummy_data: Generated dummy data containing file content
            
        Returns:
            List of created S3 bucket names
        """
        if not self.template_data:
            raise ValueError("Template must be loaded first")
        
        s3_buckets = self.template_data.get('s3_buckets', [])
        created_buckets = []
        
        print(f"[CompanySetupAgent] Creating {len(s3_buckets)} S3 buckets...")
        
        for bucket_config in s3_buckets:
            bucket_name = bucket_config.get('name')
            purpose = bucket_config.get('purpose')
            security_config = bucket_config.get('security_configuration', {})
            security_issues = bucket_config.get('security_issues', [])
            
            if self.dry_run:
                print(f"  - [DRY RUN] Would create bucket: {bucket_name}")
                print(f"    Purpose: {purpose}")
                print(f"    Encryption: {security_config.get('encryption', False)}")
                print(f"    Versioning: {security_config.get('versioning', False)}")
            else:
                try:
                    # Create the S3 bucket
                    if self.region == 'us-east-1':
                        self.s3_client.create_bucket(Bucket=bucket_name)
                    else:
                        self.s3_client.create_bucket(
                            Bucket=bucket_name,
                            CreateBucketConfiguration={'LocationConstraint': self.region}
                        )
                    print(f"  - Created bucket: {bucket_name}")
                    print(f"    Purpose: {purpose}")
                    
                    # Apply tags
                    self.s3_client.put_bucket_tagging(
                        Bucket=bucket_name,
                        Tagging={
                            'TagSet': [
                                {'Key': 'simulation-id', 'Value': self.simulation_tag},
                                {'Key': 'created-by', 'Value': 'CompanySetupAgent'},
                                {'Key': 'Name', 'Value': bucket_name}
                            ]
                        }
                    )
                    
                    # Configure encryption (or intentionally leave it off)
                    if security_config.get('encryption', False):
                        encryption_type = security_config.get('encryption_type', 'AES256')
                        self.s3_client.put_bucket_encryption(
                            Bucket=bucket_name,
                            ServerSideEncryptionConfiguration={
                                'Rules': [{
                                    'ApplyServerSideEncryptionByDefault': {
                                        'SSEAlgorithm': encryption_type
                                    }
                                }]
                            }
                        )
                        print(f"    ✓ Encryption enabled: {encryption_type}")
                    else:
                        print(f"    ⚠️  Encryption: DISABLED (intentional)")
                    
                    # Configure versioning
                    if security_config.get('versioning', False):
                        self.s3_client.put_bucket_versioning(
                            Bucket=bucket_name,
                            VersioningConfiguration={'Status': 'Enabled'}
                        )
                        print(f"    ✓ Versioning enabled")
                    else:
                        print(f"    ⚠️  Versioning: DISABLED (intentional)")
                    
                    # Configure public access block
                    if security_config.get('public_access_block', True):
                        self.s3_client.put_public_access_block(
                            Bucket=bucket_name,
                            PublicAccessBlockConfiguration={
                                'BlockPublicAcls': True,
                                'IgnorePublicAcls': True,
                                'BlockPublicPolicy': True,
                                'RestrictPublicBuckets': True
                            }
                        )
                        print(f"    ✓ Public access blocked")
                    else:
                        print(f"    ⚠️  Public access: ALLOWED (intentional)")
                    
                    # Upload sample files
                    if bucket_name in dummy_data.get('files', {}):
                        files = dummy_data['files'][bucket_name]
                        print(f"    📄 Uploading {len(files)} sample files...")
                        for file_info in files:
                            self.s3_client.put_object(
                                Bucket=bucket_name,
                                Key=file_info['path'],
                                Body=file_info['content'].encode('utf-8')
                            )
                            print(f"       - {file_info['path']} ({file_info['size_bytes']} bytes)")
                    
                except ClientError as e:
                    if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                        print(f"  - Bucket {bucket_name} already exists, skipping...")
                    else:
                        print(f"  - Error creating bucket {bucket_name}: {e}")
                        continue
            
            # Log intentional security issues
            for issue in security_issues:
                print(f"    ⚠️  Intentional issue: {issue.get('type')} - {issue.get('description')}")
            
            created_buckets.append(bucket_name)
            self.created_resources['s3_buckets'].append(bucket_name)
        
        print(f"[CompanySetupAgent] ✓ Created {len(created_buckets)} S3 buckets")
        return created_buckets
    
    def create_ec2_instances(self) -> List[str]:
        """
        Create EC2 instances with security groups.
        
        NOTE: EC2 instances are expensive even on Free Tier. This method creates
        t2.micro instances which are Free Tier eligible (750 hours/month).
        
        Returns:
            List of created EC2 instance IDs
        """
        if not self.template_data:
            raise ValueError("Template must be loaded first")
        
        ec2_instances = self.template_data.get('ec2_instances', [])
        created_instances = []
        
        print(f"[CompanySetupAgent] Creating {len(ec2_instances)} EC2 instances...")
        print(f"  ⚠️  WARNING: EC2 instances will incur costs if Free Tier is exceeded")
        
        for instance_config in ec2_instances:
            instance_name = instance_config.get('name')
            instance_type = instance_config.get('instance_type')
            purpose = instance_config.get('purpose')
            ami = instance_config.get('ami')
            security_group_config = instance_config.get('security_group', {})
            security_issues = instance_config.get('security_issues', [])
            
            if self.dry_run:
                instance_id = f"i-{self.faker.faker.hexify(text='^^^^^^^^^^^^^^^^')}"
                print(f"  - [DRY RUN] Would create instance: {instance_name} ({instance_id})")
                print(f"    Type: {instance_type}")
                print(f"    Purpose: {purpose}")
            else:
                try:
                    # First, create security group
                    sg_name = security_group_config.get('name', f"{instance_name}-sg")
                    sg_description = f"Security group for {instance_name}"
                    
                    # Get VPC ID (use default VPC if we haven't created one)
                    vpc_id = self.created_resources.get('vpc_id')
                    if not vpc_id:
                        # Get default VPC
                        vpcs = self.ec2_client.describe_vpcs(
                            Filters=[{'Name': 'isDefault', 'Values': ['true']}]
                        )
                        if vpcs['Vpcs']:
                            vpc_id = vpcs['Vpcs'][0]['VpcId']
                    
                    # Create security group
                    try:
                        sg_response = self.ec2_client.create_security_group(
                            GroupName=sg_name,
                            Description=sg_description,
                            VpcId=vpc_id,
                            TagSpecifications=[{
                                'ResourceType': 'security-group',
                                'Tags': [
                                    {'Key': 'simulation-id', 'Value': self.simulation_tag},
                                    {'Key': 'Name', 'Value': sg_name}
                                ]
                            }]
                        )
                        sg_id = sg_response['GroupId']
                        print(f"  - Created security group: {sg_name} ({sg_id})")
                        
                        # Add inbound rules
                        inbound_rules = security_group_config.get('inbound_rules', [])
                        for rule in inbound_rules:
                            protocol = rule.get('protocol')
                            port = rule.get('port')
                            source = rule.get('source')
                            
                            self.ec2_client.authorize_security_group_ingress(
                                GroupId=sg_id,
                                IpPermissions=[{
                                    'IpProtocol': protocol,
                                    'FromPort': port,
                                    'ToPort': port,
                                    'IpRanges': [{'CidrIp': source}]
                                }]
                            )
                            print(f"    ✓ Added rule: {protocol}:{port} from {source}")
                    
                    except ClientError as e:
                        if e.response['Error']['Code'] == 'InvalidGroup.Duplicate':
                            # Security group already exists, get its ID
                            sgs = self.ec2_client.describe_security_groups(
                                Filters=[{'Name': 'group-name', 'Values': [sg_name]}]
                            )
                            sg_id = sgs['SecurityGroups'][0]['GroupId']
                            print(f"  - Using existing security group: {sg_name} ({sg_id})")
                        else:
                            raise
                    
                    # Get latest Amazon Linux 2 AMI if not specified
                    if not ami:
                        images = self.ec2_client.describe_images(
                            Owners=['amazon'],
                            Filters=[
                                {'Name': 'name', 'Values': ['amzn2-ami-hvm-*-x86_64-gp2']},
                                {'Name': 'state', 'Values': ['available']}
                            ]
                        )
                        if images['Images']:
                            # Sort by creation date and get latest
                            sorted_images = sorted(images['Images'], 
                                                 key=lambda x: x['CreationDate'], 
                                                 reverse=True)
                            ami = sorted_images[0]['ImageId']
                    
                    # Launch EC2 instance
                    response = self.ec2_client.run_instances(
                        ImageId=ami,
                        InstanceType=instance_type,
                        MinCount=1,
                        MaxCount=1,
                        SecurityGroupIds=[sg_id],
                        TagSpecifications=[{
                            'ResourceType': 'instance',
                            'Tags': [
                                {'Key': 'simulation-id', 'Value': self.simulation_tag},
                                {'Key': 'Name', 'Value': instance_name},
                                {'Key': 'Purpose', 'Value': purpose}
                            ]
                        }]
                    )
                    
                    instance_id = response['Instances'][0]['InstanceId']
                    print(f"  - Created instance: {instance_name} ({instance_id})")
                    print(f"    Type: {instance_type}")
                    print(f"    AMI: {ami}")
                    print(f"    Purpose: {purpose}")
                    
                except ClientError as e:
                    print(f"  - Error creating instance {instance_name}: {e}")
                    continue
            
            # Log intentional security issues
            for issue in security_issues:
                print(f"    ⚠️  Intentional issue: {issue.get('type')} - {issue.get('description')}")
            
            created_instances.append(instance_id)
            self.created_resources['ec2_instances'].append(instance_id)
        
        print(f"[CompanySetupAgent] ✓ Created {len(created_instances)} EC2 instances")
        return created_instances
    
    def create_vpc(self) -> str:
        """
        Create VPC with basic configuration.
        
        NOTE: VPC creation is optional. If skipped, the default VPC will be used.
        Creating a custom VPC is more complex and may not be necessary for the demo.
        
        Returns:
            Created VPC ID or None if using default VPC
        """
        if not self.template_data:
            raise ValueError("Template must be loaded first")
        
        vpc_config = self.template_data.get('vpc_configuration', {})
        
        print(f"[CompanySetupAgent] VPC Configuration...")
        
        vpc_name = vpc_config.get('name')
        cidr_block = vpc_config.get('cidr_block')
        subnets = vpc_config.get('subnets', [])
        security_issues = vpc_config.get('security_issues', [])
        
        if self.dry_run:
            vpc_id = f"vpc-{self.faker.faker.hexify(text='^^^^^^^^^^^^^^^^')}"
            print(f"  - [DRY RUN] Would create VPC: {vpc_name} ({vpc_id})")
            print(f"    CIDR Block: {cidr_block}")
        else:
            # For simplicity, use the default VPC
            # Creating a custom VPC with subnets, route tables, etc. is complex
            print(f"  - Using default VPC (custom VPC creation is complex)")
            print(f"    Note: Template specifies {vpc_name} with {cidr_block}")
            
            try:
                vpcs = self.ec2_client.describe_vpcs(
                    Filters=[{'Name': 'isDefault', 'Values': ['true']}]
                )
                if vpcs['Vpcs']:
                    vpc_id = vpcs['Vpcs'][0]['VpcId']
                    print(f"    ✓ Using default VPC: {vpc_id}")
                else:
                    print(f"    ⚠️  No default VPC found")
                    vpc_id = None
            except ClientError as e:
                print(f"    ⚠️  Error getting default VPC: {e}")
                vpc_id = None
        
        # Log intentional security issues from template
        for issue in security_issues:
            print(f"    ⚠️  Intentional issue: {issue.get('type')} - {issue.get('description')}")
        
        self.created_resources['vpc_id'] = vpc_id
        
        print(f"[CompanySetupAgent] ✓ VPC configured")
        return vpc_id
    
    def enable_cloudtrail(self) -> str:
        """
        Enable CloudTrail for audit logging.
        
        NOTE: CloudTrail requires an S3 bucket to be created first.
        
        Returns:
            CloudTrail trail name
        """
        if not self.template_data:
            raise ValueError("Template must be loaded first")
        
        cloudtrail_config = self.template_data.get('cloudtrail', {})
        
        print(f"[CompanySetupAgent] Enabling CloudTrail...")
        
        trail_name = cloudtrail_config.get('name')
        s3_bucket = cloudtrail_config.get('s3_bucket')
        include_global = cloudtrail_config.get('include_global_events', True)
        multi_region = cloudtrail_config.get('is_multi_region', False)
        log_validation = cloudtrail_config.get('log_file_validation', False)
        security_issues = cloudtrail_config.get('security_issues', [])
        
        if self.dry_run:
            print(f"  - [DRY RUN] Would create trail: {trail_name}")
            print(f"    S3 Bucket: {s3_bucket}")
            print(f"    Include Global Events: {include_global}")
            print(f"    Multi-Region: {multi_region}")
            print(f"    Log File Validation: {log_validation}")
        else:
            try:
                # Create CloudTrail trail
                response = self.cloudtrail_client.create_trail(
                    Name=trail_name,
                    S3BucketName=s3_bucket,
                    IncludeGlobalServiceEvents=include_global,
                    IsMultiRegionTrail=multi_region,
                    EnableLogFileValidation=log_validation,
                    TagsList=[
                        {'Key': 'simulation-id', 'Value': self.simulation_tag},
                        {'Key': 'created-by', 'Value': 'CompanySetupAgent'}
                    ]
                )
                
                print(f"  - Created trail: {trail_name}")
                print(f"    S3 Bucket: {s3_bucket}")
                print(f"    Include Global Events: {include_global}")
                print(f"    Multi-Region: {multi_region}")
                print(f"    Log File Validation: {log_validation}")
                
                # Start logging
                self.cloudtrail_client.start_logging(Name=trail_name)
                print(f"    ✓ Logging started")
                
            except ClientError as e:
                if e.response['Error']['Code'] == 'TrailAlreadyExistsException':
                    print(f"  - Trail {trail_name} already exists, skipping...")
                else:
                    print(f"  - Error creating trail {trail_name}: {e}")
                    print(f"    Note: CloudTrail requires proper S3 bucket permissions")
        
        # Log intentional security issues
        for issue in security_issues:
            print(f"    ⚠️  Intentional issue: {issue.get('type')} - {issue.get('description')}")
        
        self.created_resources['cloudtrail_name'] = trail_name
        
        print(f"[CompanySetupAgent] ✓ CloudTrail configured: {trail_name}")
        return trail_name
    
    def tag_resources(self) -> None:
        """
        Apply simulation tags to all created resources.
        
        NOTE: Most resources are already tagged during creation. This method
        verifies and reports on tagging status.
        """
        print(f"[CompanySetupAgent] Verifying resource tags: {self.simulation_tag}")
        
        # Count total resources
        total_resources = (
            len(self.created_resources['iam_users']) +
            len(self.created_resources['s3_buckets']) +
            len(self.created_resources['ec2_instances']) +
            (1 if self.created_resources['vpc_id'] else 0) +
            (1 if self.created_resources['cloudtrail_name'] else 0)
        )
        
        print(f"  - Total resources: {total_resources}")
        print(f"    Tag: simulation-id = {self.simulation_tag}")
        print(f"    Tag: created-by = CompanySetupAgent")
        print(f"    Tag: created-at = {datetime.now().isoformat()}")
        
        # Log resource counts by type
        if self.created_resources['iam_users']:
            print(f"    ✓ Tagged {len(self.created_resources['iam_users'])} IAM users")
        if self.created_resources['s3_buckets']:
            print(f"    ✓ Tagged {len(self.created_resources['s3_buckets'])} S3 buckets")
        if self.created_resources['ec2_instances']:
            print(f"    ✓ Tagged {len(self.created_resources['ec2_instances'])} EC2 instances")
        if self.created_resources['vpc_id']:
            print(f"    ✓ VPC: {self.created_resources['vpc_id']}")
        if self.created_resources['cloudtrail_name']:
            print(f"    ✓ CloudTrail: {self.created_resources['cloudtrail_name']}")
        
        print(f"[CompanySetupAgent] ✓ All resources tagged")

    
    def generate_profile(self, dummy_data: Dict[str, Any]) -> CompanyProfile:
        """
        Generate company profile document.
        
        Creates a CompanyProfile object containing all information about the
        simulated company, its infrastructure, and intentional security issues.
        
        Args:
            dummy_data: Generated dummy data
            
        Returns:
            CompanyProfile object with complete company information
        """
        if not self.template_data:
            raise ValueError("Template must be loaded first")
        
        print(f"[CompanySetupAgent] Generating company profile...")
        
        # Extract company profile data
        company_data = self.template_data.get('company_profile', {})
        
        # Build infrastructure config
        infrastructure = InfrastructureConfig(
            iam_users=self.template_data.get('iam_users', []),
            s3_buckets=self.template_data.get('s3_buckets', []),
            ec2_instances=self.template_data.get('ec2_instances', []),
            vpc_config=self.template_data.get('vpc_configuration', {}),
            cloudtrail_config=self.template_data.get('cloudtrail', {}),
            region=self.region
        )
        
        # Collect all intentional security issues
        intentional_issues = []
        
        # Issues from IAM users
        for user in self.template_data.get('iam_users', []):
            for issue in user.get('security_issues', []):
                intentional_issues.append(SecurityIssue(
                    issue_type=issue.get('type'),
                    resource_id=user.get('username'),
                    control_domain=issue.get('control_domain'),
                    severity=issue.get('severity'),
                    description=issue.get('description')
                ))
        
        # Issues from S3 buckets
        for bucket in self.template_data.get('s3_buckets', []):
            for issue in bucket.get('security_issues', []):
                intentional_issues.append(SecurityIssue(
                    issue_type=issue.get('type'),
                    resource_id=bucket.get('name'),
                    control_domain=issue.get('control_domain'),
                    severity=issue.get('severity'),
                    description=issue.get('description')
                ))
        
        # Issues from EC2 instances
        for instance in self.template_data.get('ec2_instances', []):
            for issue in instance.get('security_issues', []):
                intentional_issues.append(SecurityIssue(
                    issue_type=issue.get('type'),
                    resource_id=instance.get('name'),
                    control_domain=issue.get('control_domain'),
                    severity=issue.get('severity'),
                    description=issue.get('description')
                ))
        
        # Issues from VPC
        vpc_config = self.template_data.get('vpc_configuration', {})
        for issue in vpc_config.get('security_issues', []):
            intentional_issues.append(SecurityIssue(
                issue_type=issue.get('type'),
                resource_id=vpc_config.get('name'),
                control_domain=issue.get('control_domain'),
                severity=issue.get('severity'),
                description=issue.get('description')
            ))
        
        # Issues from CloudTrail
        cloudtrail_config = self.template_data.get('cloudtrail', {})
        for issue in cloudtrail_config.get('security_issues', []):
            intentional_issues.append(SecurityIssue(
                issue_type=issue.get('type'),
                resource_id=cloudtrail_config.get('name'),
                control_domain=issue.get('control_domain'),
                severity=issue.get('severity'),
                description=issue.get('description')
            ))
        
        # Issues from CloudWatch
        cloudwatch_config = self.template_data.get('cloudwatch', {})
        for issue in cloudwatch_config.get('security_issues', []):
            intentional_issues.append(SecurityIssue(
                issue_type=issue.get('type'),
                resource_id='CloudWatch',
                control_domain=issue.get('control_domain'),
                severity=issue.get('severity'),
                description=issue.get('description')
            ))
        
        # Create company profile
        profile = CompanyProfile(
            name=company_data.get('name', 'Unknown Company'),
            business_type=company_data.get('business_type', 'Unknown'),
            services=company_data.get('services', []),
            infrastructure=infrastructure,
            intentional_issues=intentional_issues,
            created_at=datetime.now()
        )
        
        # Print summary
        print(f"  Company: {profile.name}")
        print(f"  Business Type: {profile.business_type}")
        print(f"  Services: {len(profile.services)}")
        print(f"  IAM Users: {len(infrastructure.iam_users)}")
        print(f"  S3 Buckets: {len(infrastructure.s3_buckets)}")
        print(f"  EC2 Instances: {len(infrastructure.ec2_instances)}")
        print(f"  Intentional Security Issues: {len(intentional_issues)}")
        
        # Group issues by control domain
        issues_by_domain = {}
        for issue in intentional_issues:
            domain = issue.control_domain
            if domain not in issues_by_domain:
                issues_by_domain[domain] = []
            issues_by_domain[domain].append(issue)
        
        print(f"\n  Security Issues by Control Domain:")
        for domain, issues in sorted(issues_by_domain.items()):
            print(f"    - {domain}: {len(issues)} issues")
        
        print(f"\n[CompanySetupAgent] ✓ Company profile generated")
        
        return profile
    
    def save_profile_to_file(self, profile: CompanyProfile, output_dir: str = 'output') -> str:
        """
        Save company profile to JSON file.
        
        Args:
            profile: CompanyProfile object to save
            output_dir: Directory to save the profile file
            
        Returns:
            Path to saved profile file
        """
        from pathlib import Path
        
        # Create output directory if it doesn't exist
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"company_profile_{timestamp}.json"
        filepath = output_path / filename
        
        # Convert profile to dictionary
        profile_dict = {
            'name': profile.name,
            'business_type': profile.business_type,
            'services': profile.services,
            'created_at': profile.created_at.isoformat(),
            'infrastructure': {
                'region': profile.infrastructure.region,
                'iam_users': len(profile.infrastructure.iam_users),
                's3_buckets': len(profile.infrastructure.s3_buckets),
                'ec2_instances': len(profile.infrastructure.ec2_instances),
                'vpc_configured': bool(profile.infrastructure.vpc_config),
                'cloudtrail_enabled': bool(profile.infrastructure.cloudtrail_config)
            },
            'security_issues': [
                {
                    'issue_type': issue.issue_type,
                    'resource_id': issue.resource_id,
                    'control_domain': issue.control_domain,
                    'severity': issue.severity,
                    'description': issue.description
                }
                for issue in profile.intentional_issues
            ],
            'created_resources': self.created_resources
        }
        
        # Save to file
        with open(filepath, 'w') as f:
            json.dump(profile_dict, f, indent=2)
        
        print(f"[CompanySetupAgent] Company profile saved to: {filepath}")
        
        return str(filepath)
    
    def run_setup(self, template_path: str, output_dir: str = 'output') -> CompanyProfile:
        """
        Run complete company setup workflow.
        
        This is a convenience method that executes all setup steps in order:
        1. Load template
        2. Generate dummy data
        3. Create IAM users
        4. Create S3 buckets
        5. Create EC2 instances
        6. Create VPC
        7. Enable CloudTrail
        8. Tag resources
        9. Generate profile
        10. Save profile to file
        
        Args:
            template_path: Path to company template YAML file
            output_dir: Directory to save output files
            
        Returns:
            CompanyProfile object
        """
        print("=" * 80)
        print("AWS AUDIT AGENT SYSTEM - COMPANY SETUP")
        print("=" * 80)
        print()
        
        # Step 1: Load template
        self.load_template(template_path)
        print()
        
        # Step 2: Generate dummy data
        dummy_data = self.generate_dummy_data()
        print()
        
        # Step 3: Create IAM users
        self.create_iam_users(dummy_data)
        print()
        
        # Step 4: Create S3 buckets
        self.create_s3_buckets(dummy_data)
        print()
        
        # Step 5: Create EC2 instances
        self.create_ec2_instances()
        print()
        
        # Step 6: Create VPC
        self.create_vpc()
        print()
        
        # Step 7: Enable CloudTrail
        self.enable_cloudtrail()
        print()
        
        # Step 8: Tag resources
        self.tag_resources()
        print()
        
        # Step 9: Generate profile
        profile = self.generate_profile(dummy_data)
        print()
        
        # Step 10: Save profile
        self.save_profile_to_file(profile, output_dir)
        print()
        
        print("=" * 80)
        print("COMPANY SETUP COMPLETE")
        print("=" * 80)
        
        return profile
