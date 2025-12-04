"""CloudTrail client wrapper for logging operations."""

import boto3
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from botocore.exceptions import ClientError


class CloudTrailClient:
    """Client for CloudTrail operations with read-only access by default."""
    
    def __init__(self, region_name: str = 'us-east-1', read_only: bool = True):
        """
        Initialize CloudTrail client.
        
        Args:
            region_name: AWS region name
            read_only: If True, only read operations are allowed
        """
        self.client = boto3.client('cloudtrail', region_name=region_name)
        self.read_only = read_only
    
    def describe_trails(self) -> List[Dict[str, Any]]:
        """
        Describe CloudTrail trails.
        
        Returns:
            List of trail dictionaries
        """
        try:
            response = self.client.describe_trails()
            return response.get('trailList', [])
        except ClientError as e:
            print(f"Error describing trails: {e}")
            return []
    
    def get_trail_status(self, trail_name: str) -> Optional[Dict[str, Any]]:
        """
        Get status for a specific trail.
        
        Args:
            trail_name: CloudTrail trail name or ARN
            
        Returns:
            Trail status or None if error
        """
        try:
            response = self.client.get_trail_status(Name=trail_name)
            return {
                'IsLogging': response.get('IsLogging', False),
                'LatestDeliveryTime': response.get('LatestDeliveryTime'),
                'LatestNotificationTime': response.get('LatestNotificationTime'),
                'StartLoggingTime': response.get('StartLoggingTime'),
                'StopLoggingTime': response.get('StopLoggingTime'),
                'LatestCloudWatchLogsDeliveryTime': response.get('LatestCloudWatchLogsDeliveryTime'),
                'LatestDigestDeliveryTime': response.get('LatestDigestDeliveryTime')
            }
        except ClientError as e:
            print(f"Error getting trail status for {trail_name}: {e}")
            return None
    
    def get_event_selectors(self, trail_name: str) -> Optional[Dict[str, Any]]:
        """
        Get event selectors for a trail.
        
        Args:
            trail_name: CloudTrail trail name or ARN
            
        Returns:
            Event selectors or None if error
        """
        try:
            response = self.client.get_event_selectors(TrailName=trail_name)
            return {
                'EventSelectors': response.get('EventSelectors', []),
                'AdvancedEventSelectors': response.get('AdvancedEventSelectors', [])
            }
        except ClientError as e:
            print(f"Error getting event selectors for {trail_name}: {e}")
            return None
    
    def lookup_events(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        max_results: int = 50,
        lookup_attributes: Optional[List[Dict[str, str]]] = None
    ) -> List[Dict[str, Any]]:
        """
        Lookup CloudTrail events.
        
        Args:
            start_time: Start time for event lookup (defaults to 7 days ago)
            end_time: End time for event lookup (defaults to now)
            max_results: Maximum number of events to return
            lookup_attributes: Optional filters for event lookup
            
        Returns:
            List of event dictionaries
        """
        try:
            params = {'MaxResults': max_results}
            
            if start_time:
                params['StartTime'] = start_time
            else:
                params['StartTime'] = datetime.now() - timedelta(days=7)
            
            if end_time:
                params['EndTime'] = end_time
            
            if lookup_attributes:
                params['LookupAttributes'] = lookup_attributes
            
            events = []
            paginator = self.client.get_paginator('lookup_events')
            for page in paginator.paginate(**params):
                events.extend(page.get('Events', []))
                if len(events) >= max_results:
                    break
            
            return events[:max_results]
        except ClientError as e:
            print(f"Error looking up events: {e}")
            return []
    
    def list_tags(self, resource_id_list: List[str]) -> List[Dict[str, Any]]:
        """
        List tags for CloudTrail resources.
        
        Args:
            resource_id_list: List of trail ARNs
            
        Returns:
            List of resource tag dictionaries
        """
        try:
            response = self.client.list_tags(ResourceIdList=resource_id_list)
            return response.get('ResourceTagList', [])
        except ClientError as e:
            print(f"Error listing tags: {e}")
            return []
    
    def get_insight_selectors(self, trail_name: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get insight selectors for a trail.
        
        Args:
            trail_name: CloudTrail trail name or ARN
            
        Returns:
            Insight selectors or None if error
        """
        try:
            response = self.client.get_insight_selectors(TrailName=trail_name)
            return response.get('InsightSelectors', [])
        except ClientError as e:
            print(f"Error getting insight selectors for {trail_name}: {e}")
            return None
    
    def list_public_keys(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """
        List public keys for CloudTrail digest verification.
        
        Args:
            start_time: Start time for key lookup
            end_time: End time for key lookup
            
        Returns:
            List of public key dictionaries
        """
        try:
            params = {}
            if start_time:
                params['StartTime'] = start_time
            if end_time:
                params['EndTime'] = end_time
            
            response = self.client.list_public_keys(**params)
            return response.get('PublicKeyList', [])
        except ClientError as e:
            print(f"Error listing public keys: {e}")
            return []
