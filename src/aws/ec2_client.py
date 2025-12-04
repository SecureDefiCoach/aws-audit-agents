"""EC2 client wrapper for instance operations."""

import boto3
from typing import Dict, List, Any, Optional
from botocore.exceptions import ClientError


class EC2Client:
    """Client for EC2 operations with read-only access by default."""
    
    def __init__(self, region_name: str = 'us-east-1', read_only: bool = True):
        """
        Initialize EC2 client.
        
        Args:
            region_name: AWS region name
            read_only: If True, only read operations are allowed
        """
        self.client = boto3.client('ec2', region_name=region_name)
        self.read_only = read_only
    
    def describe_instances(self, filters: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        """
        Describe EC2 instances.
        
        Args:
            filters: Optional filters for instance query
            
        Returns:
            List of instance dictionaries
        """
        try:
            params = {}
            if filters:
                params['Filters'] = filters
            
            instances = []
            paginator = self.client.get_paginator('describe_instances')
            for page in paginator.paginate(**params):
                for reservation in page.get('Reservations', []):
                    instances.extend(reservation.get('Instances', []))
            return instances
        except ClientError as e:
            print(f"Error describing instances: {e}")
            return []
    
    def get_instance(self, instance_id: str) -> Optional[Dict[str, Any]]:
        """
        Get details for a specific instance.
        
        Args:
            instance_id: EC2 instance ID
            
        Returns:
            Instance details or None if error
        """
        try:
            response = self.client.describe_instances(InstanceIds=[instance_id])
            reservations = response.get('Reservations', [])
            if reservations and reservations[0].get('Instances'):
                return reservations[0]['Instances'][0]
            return None
        except ClientError as e:
            print(f"Error getting instance {instance_id}: {e}")
            return None
    
    def describe_security_groups(self, filters: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        """
        Describe security groups.
        
        Args:
            filters: Optional filters for security group query
            
        Returns:
            List of security group dictionaries
        """
        try:
            params = {}
            if filters:
                params['Filters'] = filters
            
            security_groups = []
            paginator = self.client.get_paginator('describe_security_groups')
            for page in paginator.paginate(**params):
                security_groups.extend(page.get('SecurityGroups', []))
            return security_groups
        except ClientError as e:
            print(f"Error describing security groups: {e}")
            return []
    
    def get_security_group(self, group_id: str) -> Optional[Dict[str, Any]]:
        """
        Get details for a specific security group.
        
        Args:
            group_id: Security group ID
            
        Returns:
            Security group details or None if error
        """
        try:
            response = self.client.describe_security_groups(GroupIds=[group_id])
            groups = response.get('SecurityGroups', [])
            return groups[0] if groups else None
        except ClientError as e:
            print(f"Error getting security group {group_id}: {e}")
            return None
    
    def describe_volumes(self, filters: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        """
        Describe EBS volumes.
        
        Args:
            filters: Optional filters for volume query
            
        Returns:
            List of volume dictionaries
        """
        try:
            params = {}
            if filters:
                params['Filters'] = filters
            
            volumes = []
            paginator = self.client.get_paginator('describe_volumes')
            for page in paginator.paginate(**params):
                volumes.extend(page.get('Volumes', []))
            return volumes
        except ClientError as e:
            print(f"Error describing volumes: {e}")
            return []
    
    def describe_snapshots(self, owner_ids: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Describe EBS snapshots.
        
        Args:
            owner_ids: Optional list of owner IDs (defaults to 'self')
            
        Returns:
            List of snapshot dictionaries
        """
        try:
            params = {'OwnerIds': owner_ids if owner_ids else ['self']}
            
            snapshots = []
            paginator = self.client.get_paginator('describe_snapshots')
            for page in paginator.paginate(**params):
                snapshots.extend(page.get('Snapshots', []))
            return snapshots
        except ClientError as e:
            print(f"Error describing snapshots: {e}")
            return []
    
    def describe_images(self, owner_ids: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Describe AMIs.
        
        Args:
            owner_ids: Optional list of owner IDs (defaults to 'self')
            
        Returns:
            List of image dictionaries
        """
        try:
            params = {'Owners': owner_ids if owner_ids else ['self']}
            
            response = self.client.describe_images(**params)
            return response.get('Images', [])
        except ClientError as e:
            print(f"Error describing images: {e}")
            return []
    
    def describe_key_pairs(self) -> List[Dict[str, Any]]:
        """
        Describe EC2 key pairs.
        
        Returns:
            List of key pair dictionaries
        """
        try:
            response = self.client.describe_key_pairs()
            return response.get('KeyPairs', [])
        except ClientError as e:
            print(f"Error describing key pairs: {e}")
            return []
    
    def describe_network_interfaces(self, filters: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        """
        Describe network interfaces.
        
        Args:
            filters: Optional filters for network interface query
            
        Returns:
            List of network interface dictionaries
        """
        try:
            params = {}
            if filters:
                params['Filters'] = filters
            
            interfaces = []
            paginator = self.client.get_paginator('describe_network_interfaces')
            for page in paginator.paginate(**params):
                interfaces.extend(page.get('NetworkInterfaces', []))
            return interfaces
        except ClientError as e:
            print(f"Error describing network interfaces: {e}")
            return []
