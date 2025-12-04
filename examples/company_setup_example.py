#!/usr/bin/env python3
"""
Example usage of CompanySetupAgent.

This example demonstrates how to use the CompanySetupAgent to create
a simulated company infrastructure for audit demonstration.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.company_setup import CompanySetupAgent


def example_basic_usage():
    """Basic usage example - DRY RUN mode (safe, no real resources)."""
    print("Example 1: Basic Usage (DRY RUN MODE)")
    print("-" * 60)
    print("This mode simulates resource creation without using AWS.")
    print()
    
    # Initialize agent in dry-run mode (default)
    agent = CompanySetupAgent(
        region='us-east-1',
        simulation_tag='audit-demo-2025',
        seed=42,
        dry_run=True  # Safe mode - no real AWS resources created
    )
    
    # Run complete setup
    profile = agent.run_setup(
        template_path='templates/cloudretail_company.yaml',
        output_dir='output'
    )
    
    print(f"\nCreated company: {profile.name}")
    print(f"Total security issues: {len(profile.intentional_issues)}")


def example_real_aws_mode():
    """Example with REAL AWS resource creation."""
    print("\n\nExample 2: REAL AWS MODE")
    print("-" * 60)
    print("⚠️  WARNING: This will create REAL AWS resources!")
    print("⚠️  Ensure you have:")
    print("   - AWS credentials configured")
    print("   - Appropriate IAM permissions")
    print("   - Budget alerts set up")
    print()
    
    # Uncomment to run with real AWS resources
    # agent = CompanySetupAgent(
    #     region='us-east-1',
    #     simulation_tag='audit-demo-2025',
    #     seed=42,
    #     dry_run=False  # CREATES REAL AWS RESOURCES
    # )
    # 
    # profile = agent.run_setup(
    #     template_path='templates/cloudretail_company.yaml',
    #     output_dir='output'
    # )
    # 
    # print(f"\nCreated company: {profile.name}")
    # print(f"Total security issues: {len(profile.intentional_issues)}")
    # print("\n⚠️  Remember to clean up resources to avoid charges!")
    
    print("(Commented out for safety - uncomment to run)")


def example_step_by_step():
    """Step-by-step usage example."""
    print("\n\nExample 2: Step-by-Step Usage")
    print("-" * 60)
    
    # Initialize agent
    agent = CompanySetupAgent(
        region='us-east-1',
        simulation_tag='audit-demo-custom',
        seed=123
    )
    
    # Step 1: Load template
    template = agent.load_template('templates/cloudretail_company.yaml')
    print(f"Loaded template for: {template['company_profile']['name']}")
    
    # Step 2: Generate dummy data
    dummy_data = agent.generate_dummy_data()
    print(f"Generated data for {len(dummy_data['users'])} users")
    
    # Step 3: Create resources (simulated)
    agent.create_iam_users(dummy_data)
    agent.create_s3_buckets(dummy_data)
    agent.create_ec2_instances()
    agent.create_vpc()
    agent.enable_cloudtrail()
    
    # Step 4: Tag resources
    agent.tag_resources()
    
    # Step 5: Generate profile
    profile = agent.generate_profile(dummy_data)
    
    # Step 6: Save to file
    filepath = agent.save_profile_to_file(profile, 'output')
    print(f"\nProfile saved to: {filepath}")


def example_custom_seed():
    """Example with custom seed for different dummy data."""
    print("\n\nExample 3: Custom Seed for Different Data")
    print("-" * 60)
    
    # Different seeds produce different dummy data
    for seed in [42, 100, 200]:
        agent = CompanySetupAgent(
            region='us-east-1',
            simulation_tag=f'audit-demo-seed-{seed}',
            seed=seed
        )
        
        agent.load_template('templates/cloudretail_company.yaml')
        dummy_data = agent.generate_dummy_data()
        
        print(f"\nSeed {seed}:")
        print(f"  First user: {dummy_data['users'][0]['full_name']}")


if __name__ == '__main__':
    # Run dry-run example (safe)
    example_basic_usage()
    
    # Show real AWS mode example (commented out for safety)
    example_real_aws_mode()
    
    # Uncomment to run other examples:
    # example_step_by_step()
    # example_custom_seed()
