"""IAM client wrapper for user and role operations."""

import boto3
from typing import Dict, List, Any, Optional
from botocore.exceptions import ClientError


class IAMClient:
    """Client for IAM operations with read-only access by default."""
    
    def __init__(self, region_name: str = 'us-east-1', read_only: bool = True):
        """
        Initialize IAM client.
        
        Args:
            region_name: AWS region name
            read_only: If True, only read operations are allowed
        """
        self.client = boto3.client('iam', region_name=region_name)
        self.read_only = read_only
    
    def get_credential_report(self) -> Optional[bytes]:
        """
        Get IAM credential report.
        
        Returns:
            Credential report content or None if error
        """
        try:
            # Generate report first
            self.client.generate_credential_report()
            
            # Retrieve the report
            response = self.client.get_credential_report()
            return response.get('Content')
        except ClientError as e:
            print(f"Error getting credential report: {e}")
            return None
    
    def list_users(self) -> List[Dict[str, Any]]:
        """
        List all IAM users.
        
        Returns:
            List of user dictionaries
        """
        try:
            users = []
            paginator = self.client.get_paginator('list_users')
            for page in paginator.paginate():
                users.extend(page.get('Users', []))
            return users
        except ClientError as e:
            print(f"Error listing users: {e}")
            return []
    
    def get_user(self, user_name: str) -> Optional[Dict[str, Any]]:
        """
        Get details for a specific user.
        
        Args:
            user_name: IAM user name
            
        Returns:
            User details or None if error
        """
        try:
            response = self.client.get_user(UserName=user_name)
            return response.get('User')
        except ClientError as e:
            print(f"Error getting user {user_name}: {e}")
            return None
    
    def list_roles(self) -> List[Dict[str, Any]]:
        """
        List all IAM roles.
        
        Returns:
            List of role dictionaries
        """
        try:
            roles = []
            paginator = self.client.get_paginator('list_roles')
            for page in paginator.paginate():
                roles.extend(page.get('Roles', []))
            return roles
        except ClientError as e:
            print(f"Error listing roles: {e}")
            return []
    
    def get_role(self, role_name: str) -> Optional[Dict[str, Any]]:
        """
        Get details for a specific role.
        
        Args:
            role_name: IAM role name
            
        Returns:
            Role details or None if error
        """
        try:
            response = self.client.get_role(RoleName=role_name)
            return response.get('Role')
        except ClientError as e:
            print(f"Error getting role {role_name}: {e}")
            return None
    
    def list_user_policies(self, user_name: str) -> List[str]:
        """
        List inline policies for a user.
        
        Args:
            user_name: IAM user name
            
        Returns:
            List of policy names
        """
        try:
            response = self.client.list_user_policies(UserName=user_name)
            return response.get('PolicyNames', [])
        except ClientError as e:
            print(f"Error listing policies for user {user_name}: {e}")
            return []
    
    def list_attached_user_policies(self, user_name: str) -> List[Dict[str, Any]]:
        """
        List attached managed policies for a user.
        
        Args:
            user_name: IAM user name
            
        Returns:
            List of attached policy dictionaries
        """
        try:
            response = self.client.list_attached_user_policies(UserName=user_name)
            return response.get('AttachedPolicies', [])
        except ClientError as e:
            print(f"Error listing attached policies for user {user_name}: {e}")
            return []
    
    def get_user_policy(self, user_name: str, policy_name: str) -> Optional[Dict[str, Any]]:
        """
        Get an inline policy document for a user.
        
        Args:
            user_name: IAM user name
            policy_name: Policy name
            
        Returns:
            Policy document or None if error
        """
        try:
            response = self.client.get_user_policy(
                UserName=user_name,
                PolicyName=policy_name
            )
            return response.get('PolicyDocument')
        except ClientError as e:
            print(f"Error getting policy {policy_name} for user {user_name}: {e}")
            return None
    
    def list_access_keys(self, user_name: str) -> List[Dict[str, Any]]:
        """
        List access keys for a user.
        
        Args:
            user_name: IAM user name
            
        Returns:
            List of access key metadata
        """
        try:
            response = self.client.list_access_keys(UserName=user_name)
            return response.get('AccessKeyMetadata', [])
        except ClientError as e:
            print(f"Error listing access keys for user {user_name}: {e}")
            return []
    
    def list_mfa_devices(self, user_name: str) -> List[Dict[str, Any]]:
        """
        List MFA devices for a user.
        
        Args:
            user_name: IAM user name
            
        Returns:
            List of MFA device dictionaries
        """
        try:
            response = self.client.list_mfa_devices(UserName=user_name)
            return response.get('MFADevices', [])
        except ClientError as e:
            print(f"Error listing MFA devices for user {user_name}: {e}")
            return []
    
    def get_account_summary(self) -> Optional[Dict[str, int]]:
        """
        Get account summary with usage statistics.
        
        Returns:
            Account summary dictionary or None if error
        """
        try:
            response = self.client.get_account_summary()
            return response.get('SummaryMap')
        except ClientError as e:
            print(f"Error getting account summary: {e}")
            return None
