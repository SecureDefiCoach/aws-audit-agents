"""S3 client wrapper for bucket operations."""

import boto3
from typing import Dict, List, Any, Optional
from botocore.exceptions import ClientError


class S3Client:
    """Client for S3 operations with read-only access by default."""
    
    def __init__(self, region_name: str = 'us-east-1', read_only: bool = True):
        """
        Initialize S3 client.
        
        Args:
            region_name: AWS region name
            read_only: If True, only read operations are allowed
        """
        self.client = boto3.client('s3', region_name=region_name)
        self.read_only = read_only
    
    def list_buckets(self) -> List[Dict[str, Any]]:
        """
        List all S3 buckets.
        
        Returns:
            List of bucket dictionaries
        """
        try:
            response = self.client.list_buckets()
            return response.get('Buckets', [])
        except ClientError as e:
            print(f"Error listing buckets: {e}")
            return []
    
    def get_bucket_encryption(self, bucket_name: str) -> Optional[Dict[str, Any]]:
        """
        Get encryption configuration for a bucket.
        
        Args:
            bucket_name: S3 bucket name
            
        Returns:
            Encryption configuration or None if not configured/error
        """
        try:
            response = self.client.get_bucket_encryption(Bucket=bucket_name)
            return response.get('ServerSideEncryptionConfiguration')
        except ClientError as e:
            if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
                return None
            print(f"Error getting encryption for bucket {bucket_name}: {e}")
            return None
    
    def get_bucket_versioning(self, bucket_name: str) -> Optional[Dict[str, Any]]:
        """
        Get versioning configuration for a bucket.
        
        Args:
            bucket_name: S3 bucket name
            
        Returns:
            Versioning configuration or None if error
        """
        try:
            response = self.client.get_bucket_versioning(Bucket=bucket_name)
            return {
                'Status': response.get('Status', 'Disabled'),
                'MFADelete': response.get('MFADelete', 'Disabled')
            }
        except ClientError as e:
            print(f"Error getting versioning for bucket {bucket_name}: {e}")
            return None
    
    def get_bucket_logging(self, bucket_name: str) -> Optional[Dict[str, Any]]:
        """
        Get logging configuration for a bucket.
        
        Args:
            bucket_name: S3 bucket name
            
        Returns:
            Logging configuration or None if not configured/error
        """
        try:
            response = self.client.get_bucket_logging(Bucket=bucket_name)
            return response.get('LoggingEnabled')
        except ClientError as e:
            print(f"Error getting logging for bucket {bucket_name}: {e}")
            return None
    
    def get_bucket_policy(self, bucket_name: str) -> Optional[str]:
        """
        Get bucket policy.
        
        Args:
            bucket_name: S3 bucket name
            
        Returns:
            Policy document as string or None if not configured/error
        """
        try:
            response = self.client.get_bucket_policy(Bucket=bucket_name)
            return response.get('Policy')
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchBucketPolicy':
                return None
            print(f"Error getting policy for bucket {bucket_name}: {e}")
            return None
    
    def get_bucket_acl(self, bucket_name: str) -> Optional[Dict[str, Any]]:
        """
        Get bucket ACL.
        
        Args:
            bucket_name: S3 bucket name
            
        Returns:
            ACL configuration or None if error
        """
        try:
            response = self.client.get_bucket_acl(Bucket=bucket_name)
            return {
                'Owner': response.get('Owner'),
                'Grants': response.get('Grants', [])
            }
        except ClientError as e:
            print(f"Error getting ACL for bucket {bucket_name}: {e}")
            return None
    
    def get_public_access_block(self, bucket_name: str) -> Optional[Dict[str, Any]]:
        """
        Get public access block configuration for a bucket.
        
        Args:
            bucket_name: S3 bucket name
            
        Returns:
            Public access block configuration or None if not configured/error
        """
        try:
            response = self.client.get_public_access_block(Bucket=bucket_name)
            return response.get('PublicAccessBlockConfiguration')
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchPublicAccessBlockConfiguration':
                return None
            print(f"Error getting public access block for bucket {bucket_name}: {e}")
            return None
    
    def get_bucket_location(self, bucket_name: str) -> Optional[str]:
        """
        Get bucket location/region.
        
        Args:
            bucket_name: S3 bucket name
            
        Returns:
            Region name or None if error
        """
        try:
            response = self.client.get_bucket_location(Bucket=bucket_name)
            location = response.get('LocationConstraint')
            # us-east-1 returns None
            return location if location else 'us-east-1'
        except ClientError as e:
            print(f"Error getting location for bucket {bucket_name}: {e}")
            return None
    
    def get_bucket_tagging(self, bucket_name: str) -> List[Dict[str, str]]:
        """
        Get bucket tags.
        
        Args:
            bucket_name: S3 bucket name
            
        Returns:
            List of tag dictionaries or empty list if not configured/error
        """
        try:
            response = self.client.get_bucket_tagging(Bucket=bucket_name)
            return response.get('TagSet', [])
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchTagSet':
                return []
            print(f"Error getting tags for bucket {bucket_name}: {e}")
            return []
    
    def list_objects(self, bucket_name: str, max_keys: int = 1000) -> List[Dict[str, Any]]:
        """
        List objects in a bucket.
        
        Args:
            bucket_name: S3 bucket name
            max_keys: Maximum number of keys to return
            
        Returns:
            List of object dictionaries
        """
        try:
            response = self.client.list_objects_v2(
                Bucket=bucket_name,
                MaxKeys=max_keys
            )
            return response.get('Contents', [])
        except ClientError as e:
            print(f"Error listing objects in bucket {bucket_name}: {e}")
            return []
