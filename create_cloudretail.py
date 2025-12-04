#!/usr/bin/env python3
"""
Create CloudRetail Inc - Real AWS Resources

This script creates actual AWS resources for the audit demonstration.
Make sure you have:
1. AWS credentials configured (aws configure)
2. Appropriate IAM permissions
3. Budget alerts set up

Estimated cost: $0-5 depending on how long resources run
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from src.agents.company_setup import CompanySetupAgent


def main():
    """Create CloudRetail Inc with real AWS resources."""
    
    print("=" * 80)
    print("CREATING CLOUDRETAIL INC - REAL AWS RESOURCES")
    print("=" * 80)
    print()
    print("⚠️  WARNING: This will create REAL AWS resources!")
    print("⚠️  Resources created:")
    print("   - 5 IAM users")
    print("   - 3 S3 buckets (~1 GB)")
    print("   - 2 EC2 t2.micro instances")
    print("   - Security groups")
    print("   - CloudTrail logging")
    print()
    print("💰 Estimated cost: $0-5 (should be within Free Tier)")
    print()
    
    # Confirm with user
    response = input("Do you want to proceed? (yes/no): ").strip().lower()
    
    if response != 'yes':
        print("\n❌ Cancelled. No resources created.")
        return
    
    print("\n✅ Proceeding with resource creation...")
    print()
    
    # Initialize agent with real mode
    agent = CompanySetupAgent(
        region='us-east-2',  # Ohio
        simulation_tag='audit-demo-2025',
        seed=42,
        dry_run=False  # CREATE REAL RESOURCES
    )
    
    # Run complete setup
    try:
        profile = agent.run_setup(
            template_path='templates/cloudretail_company.yaml',
            output_dir='output'
        )
        
        print()
        print("=" * 80)
        print("✅ SUCCESS! CloudRetail Inc has been created!")
        print("=" * 80)
        print()
        print(f"Company: {profile.name}")
        print(f"Business Type: {profile.business_type}")
        print(f"Total Security Issues: {len(profile.intentional_issues)}")
        print()
        print("📋 Next Steps:")
        print("1. Check AWS Console to verify resources")
        print("2. Review output/company_profile_*.json")
        print("3. Proceed with implementing audit agents (Tasks 9-13)")
        print()
        print("💡 Remember to clean up resources when done to avoid charges!")
        print()
        
    except Exception as e:
        print()
        print("=" * 80)
        print("❌ ERROR: Failed to create resources")
        print("=" * 80)
        print(f"\nError: {e}")
        print()
        print("Troubleshooting:")
        print("1. Check AWS credentials: aws sts get-caller-identity")
        print("2. Verify IAM permissions are attached")
        print("3. Check AWS Console for any existing resources with same names")
        print()
        sys.exit(1)


if __name__ == '__main__':
    main()
