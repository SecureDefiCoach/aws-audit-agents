"""Budget client wrapper for cost monitoring operations."""

import boto3
from typing import Dict, List, Any, Optional
from botocore.exceptions import ClientError


class BudgetClient:
    """Client for AWS Budgets operations with read-only access by default."""
    
    def __init__(self, region_name: str = 'us-east-1', read_only: bool = True):
        """
        Initialize Budget client.
        
        Args:
            region_name: AWS region name (Budgets is global but requires region)
            read_only: If True, only read operations are allowed
        """
        self.client = boto3.client('budgets', region_name=region_name)
        self.ce_client = boto3.client('ce', region_name=region_name)  # Cost Explorer
        self.read_only = read_only
    
    def describe_budgets(self, account_id: str) -> List[Dict[str, Any]]:
        """
        Describe all budgets for an account.
        
        Args:
            account_id: AWS account ID
            
        Returns:
            List of budget dictionaries
        """
        try:
            budgets = []
            paginator = self.client.get_paginator('describe_budgets')
            for page in paginator.paginate(AccountId=account_id):
                budgets.extend(page.get('Budgets', []))
            return budgets
        except ClientError as e:
            print(f"Error describing budgets: {e}")
            return []
    
    def describe_budget(self, account_id: str, budget_name: str) -> Optional[Dict[str, Any]]:
        """
        Get details for a specific budget.
        
        Args:
            account_id: AWS account ID
            budget_name: Budget name
            
        Returns:
            Budget details or None if error
        """
        try:
            response = self.client.describe_budget(
                AccountId=account_id,
                BudgetName=budget_name
            )
            return response.get('Budget')
        except ClientError as e:
            print(f"Error describing budget {budget_name}: {e}")
            return None
    
    def describe_notifications_for_budget(
        self,
        account_id: str,
        budget_name: str
    ) -> List[Dict[str, Any]]:
        """
        Get notifications configured for a budget.
        
        Args:
            account_id: AWS account ID
            budget_name: Budget name
            
        Returns:
            List of notification dictionaries
        """
        try:
            notifications = []
            paginator = self.client.get_paginator('describe_notifications_for_budget')
            for page in paginator.paginate(
                AccountId=account_id,
                BudgetName=budget_name
            ):
                notifications.extend(page.get('Notifications', []))
            return notifications
        except ClientError as e:
            print(f"Error describing notifications for budget {budget_name}: {e}")
            return []
    
    def describe_subscribers_for_notification(
        self,
        account_id: str,
        budget_name: str,
        notification: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Get subscribers for a budget notification.
        
        Args:
            account_id: AWS account ID
            budget_name: Budget name
            notification: Notification configuration
            
        Returns:
            List of subscriber dictionaries
        """
        try:
            subscribers = []
            paginator = self.client.get_paginator('describe_subscribers_for_notification')
            for page in paginator.paginate(
                AccountId=account_id,
                BudgetName=budget_name,
                Notification=notification
            ):
                subscribers.extend(page.get('Subscribers', []))
            return subscribers
        except ClientError as e:
            print(f"Error describing subscribers for budget {budget_name}: {e}")
            return []
    
    def get_cost_and_usage(
        self,
        start_date: str,
        end_date: str,
        granularity: str = 'MONTHLY',
        metrics: Optional[List[str]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Get cost and usage data using Cost Explorer.
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            granularity: Time granularity (DAILY, MONTHLY, HOURLY)
            metrics: List of metrics to retrieve (defaults to ['UnblendedCost'])
            
        Returns:
            Cost and usage data or None if error
        """
        try:
            if metrics is None:
                metrics = ['UnblendedCost']
            
            response = self.ce_client.get_cost_and_usage(
                TimePeriod={
                    'Start': start_date,
                    'End': end_date
                },
                Granularity=granularity,
                Metrics=metrics
            )
            return response
        except ClientError as e:
            print(f"Error getting cost and usage: {e}")
            return None
    
    def get_cost_forecast(
        self,
        start_date: str,
        end_date: str,
        metric: str = 'UNBLENDED_COST',
        granularity: str = 'MONTHLY'
    ) -> Optional[Dict[str, Any]]:
        """
        Get cost forecast using Cost Explorer.
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            metric: Metric to forecast (UNBLENDED_COST, BLENDED_COST, etc.)
            granularity: Time granularity (DAILY, MONTHLY)
            
        Returns:
            Cost forecast data or None if error
        """
        try:
            response = self.ce_client.get_cost_forecast(
                TimePeriod={
                    'Start': start_date,
                    'End': end_date
                },
                Metric=metric,
                Granularity=granularity
            )
            return response
        except ClientError as e:
            print(f"Error getting cost forecast: {e}")
            return None
    
    def get_dimension_values(
        self,
        start_date: str,
        end_date: str,
        dimension: str,
        search_string: Optional[str] = None
    ) -> List[str]:
        """
        Get dimension values for cost analysis.
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            dimension: Dimension name (SERVICE, LINKED_ACCOUNT, etc.)
            search_string: Optional search filter
            
        Returns:
            List of dimension values
        """
        try:
            params = {
                'TimePeriod': {
                    'Start': start_date,
                    'End': end_date
                },
                'Dimension': dimension
            }
            
            if search_string:
                params['SearchString'] = search_string
            
            response = self.ce_client.get_dimension_values(**params)
            return [item['Value'] for item in response.get('DimensionValues', [])]
        except ClientError as e:
            print(f"Error getting dimension values: {e}")
            return []
    
    def get_tags(
        self,
        start_date: str,
        end_date: str,
        tag_key: Optional[str] = None
    ) -> List[str]:
        """
        Get tag values for cost allocation.
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            tag_key: Optional tag key to filter by
            
        Returns:
            List of tag values
        """
        try:
            params = {
                'TimePeriod': {
                    'Start': start_date,
                    'End': end_date
                }
            }
            
            if tag_key:
                params['TagKey'] = tag_key
            
            response = self.ce_client.get_tags(**params)
            return response.get('Tags', [])
        except ClientError as e:
            print(f"Error getting tags: {e}")
            return []
