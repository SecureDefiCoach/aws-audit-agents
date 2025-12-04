"""VPC client wrapper for network operations."""

import boto3
from typing import Dict, List, Any, Optional
from botocore.exceptions import ClientError


class VPCClient:
    """Client for VPC operations with read-only access by default."""
    
    def __init__(self, region_name: str = 'us-east-1', read_only: bool = True):
        """
        Initialize VPC client.
        
        Args:
            region_name: AWS region name
            read_only: If True, only read operations are allowed
        """
        self.client = boto3.client('ec2', region_name=region_name)
        self.read_only = read_only
    
    def describe_vpcs(self, filters: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        """
        Describe VPCs.
        
        Args:
            filters: Optional filters for VPC query
            
        Returns:
            List of VPC dictionaries
        """
        try:
            params = {}
            if filters:
                params['Filters'] = filters
            
            vpcs = []
            paginator = self.client.get_paginator('describe_vpcs')
            for page in paginator.paginate(**params):
                vpcs.extend(page.get('Vpcs', []))
            return vpcs
        except ClientError as e:
            print(f"Error describing VPCs: {e}")
            return []
    
    def get_vpc(self, vpc_id: str) -> Optional[Dict[str, Any]]:
        """
        Get details for a specific VPC.
        
        Args:
            vpc_id: VPC ID
            
        Returns:
            VPC details or None if error
        """
        try:
            response = self.client.describe_vpcs(VpcIds=[vpc_id])
            vpcs = response.get('Vpcs', [])
            return vpcs[0] if vpcs else None
        except ClientError as e:
            print(f"Error getting VPC {vpc_id}: {e}")
            return None
    
    def describe_subnets(self, filters: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        """
        Describe subnets.
        
        Args:
            filters: Optional filters for subnet query
            
        Returns:
            List of subnet dictionaries
        """
        try:
            params = {}
            if filters:
                params['Filters'] = filters
            
            subnets = []
            paginator = self.client.get_paginator('describe_subnets')
            for page in paginator.paginate(**params):
                subnets.extend(page.get('Subnets', []))
            return subnets
        except ClientError as e:
            print(f"Error describing subnets: {e}")
            return []
    
    def describe_route_tables(self, filters: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        """
        Describe route tables.
        
        Args:
            filters: Optional filters for route table query
            
        Returns:
            List of route table dictionaries
        """
        try:
            params = {}
            if filters:
                params['Filters'] = filters
            
            route_tables = []
            paginator = self.client.get_paginator('describe_route_tables')
            for page in paginator.paginate(**params):
                route_tables.extend(page.get('RouteTables', []))
            return route_tables
        except ClientError as e:
            print(f"Error describing route tables: {e}")
            return []
    
    def describe_internet_gateways(self, filters: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        """
        Describe internet gateways.
        
        Args:
            filters: Optional filters for internet gateway query
            
        Returns:
            List of internet gateway dictionaries
        """
        try:
            params = {}
            if filters:
                params['Filters'] = filters
            
            gateways = []
            paginator = self.client.get_paginator('describe_internet_gateways')
            for page in paginator.paginate(**params):
                gateways.extend(page.get('InternetGateways', []))
            return gateways
        except ClientError as e:
            print(f"Error describing internet gateways: {e}")
            return []
    
    def describe_nat_gateways(self, filters: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        """
        Describe NAT gateways.
        
        Args:
            filters: Optional filters for NAT gateway query
            
        Returns:
            List of NAT gateway dictionaries
        """
        try:
            params = {}
            if filters:
                params['Filters'] = filters
            
            nat_gateways = []
            paginator = self.client.get_paginator('describe_nat_gateways')
            for page in paginator.paginate(**params):
                nat_gateways.extend(page.get('NatGateways', []))
            return nat_gateways
        except ClientError as e:
            print(f"Error describing NAT gateways: {e}")
            return []
    
    def describe_network_acls(self, filters: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        """
        Describe network ACLs.
        
        Args:
            filters: Optional filters for network ACL query
            
        Returns:
            List of network ACL dictionaries
        """
        try:
            params = {}
            if filters:
                params['Filters'] = filters
            
            acls = []
            paginator = self.client.get_paginator('describe_network_acls')
            for page in paginator.paginate(**params):
                acls.extend(page.get('NetworkAcls', []))
            return acls
        except ClientError as e:
            print(f"Error describing network ACLs: {e}")
            return []
    
    def describe_vpc_peering_connections(self, filters: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        """
        Describe VPC peering connections.
        
        Args:
            filters: Optional filters for peering connection query
            
        Returns:
            List of peering connection dictionaries
        """
        try:
            params = {}
            if filters:
                params['Filters'] = filters
            
            connections = []
            paginator = self.client.get_paginator('describe_vpc_peering_connections')
            for page in paginator.paginate(**params):
                connections.extend(page.get('VpcPeeringConnections', []))
            return connections
        except ClientError as e:
            print(f"Error describing VPC peering connections: {e}")
            return []
    
    def describe_vpc_endpoints(self, filters: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        """
        Describe VPC endpoints.
        
        Args:
            filters: Optional filters for VPC endpoint query
            
        Returns:
            List of VPC endpoint dictionaries
        """
        try:
            params = {}
            if filters:
                params['Filters'] = filters
            
            endpoints = []
            paginator = self.client.get_paginator('describe_vpc_endpoints')
            for page in paginator.paginate(**params):
                endpoints.extend(page.get('VpcEndpoints', []))
            return endpoints
        except ClientError as e:
            print(f"Error describing VPC endpoints: {e}")
            return []
    
    def describe_flow_logs(self, filters: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        """
        Describe VPC flow logs.
        
        Args:
            filters: Optional filters for flow log query
            
        Returns:
            List of flow log dictionaries
        """
        try:
            params = {}
            if filters:
                params['Filters'] = filters
            
            flow_logs = []
            paginator = self.client.get_paginator('describe_flow_logs')
            for page in paginator.paginate(**params):
                flow_logs.extend(page.get('FlowLogs', []))
            return flow_logs
        except ClientError as e:
            print(f"Error describing flow logs: {e}")
            return []
