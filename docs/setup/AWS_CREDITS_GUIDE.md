# AWS Credits and Cost Management Guide

This guide provides information on obtaining AWS credits and minimizing costs for the AWS Audit Agent System demonstration.

## AWS Credit Programs

### 1. AWS Activate (For Startups)
**Best for:** Startups affiliated with accelerators, incubators, or VCs

- **Website:** https://aws.amazon.com/activate/
- **Credits:** $1,000 - $100,000 depending on tier
- **Requirements:**
  - Affiliation with AWS Activate Provider (accelerator, incubator, VC)
  - Or membership in AWS Partner Network
  - Company must be less than 10 years old
- **Application:** Through your accelerator/incubator or directly if eligible
- **Timeline:** Varies by provider, typically 2-4 weeks

**Tiers:**
- **Portfolio:** $1,000 credits (via participating providers)
- **Portfolio Plus:** $5,000 credits (via select providers)
- **Founders:** $25,000 credits (via select providers)
- **Advanced:** $100,000 credits (for high-growth startups)

### 2. AWS Educate
**Best for:** Students, educators, and educational institutions

- **Website:** https://aws.amazon.com/education/awseducate/
- **Credits:** $30-$100 per year
- **Requirements:**
  - Valid .edu email address OR
  - Educator verification through institution
- **Application:** Self-service registration
- **Timeline:** Immediate approval for .edu emails

**Benefits:**
- AWS credits
- Free training content
- Access to AWS services
- Career pathways

### 3. AWS Community Builders Program
**Best for:** Active AWS community contributors

- **Website:** https://aws.amazon.com/developer/community/community-builders/
- **Credits:** $500-$1,000+ per year
- **Requirements:**
  - Active AWS community participation
  - Blog posts, videos, tutorials, or open-source projects
  - Social media presence discussing AWS
  - Application and acceptance required
- **Application:** Opens periodically (check website)
- **Timeline:** Applications reviewed quarterly

**What they look for:**
- Regular AWS-related content creation
- Community engagement
- Technical expertise
- Willingness to share knowledge

### 4. AWS User Group Leaders
**Best for:** AWS user group organizers

- **Website:** https://aws.amazon.com/developer/community/usergroups/
- **Credits:** Varies, typically $500-$1,000 per year
- **Requirements:**
  - Lead or co-lead an active AWS user group
  - Regular meetups (monthly or quarterly)
  - Minimum attendance requirements
- **Application:** Through AWS user group program
- **Timeline:** Ongoing for active leaders

### 5. AWS Open Source Credits
**Best for:** Open-source projects with significant usage

- **Website:** https://aws.amazon.com/blogs/opensource/aws-promotional-credits-open-source-projects/
- **Credits:** Varies based on project needs
- **Requirements:**
  - Open-source project with OSI-approved license
  - Significant community usage/traction
  - Clear AWS infrastructure needs
- **Application:** Email aws-oss-credits@amazon.com
- **Timeline:** Case-by-case review

### 6. AWS Research Credits
**Best for:** Academic researchers

- **Website:** https://aws.amazon.com/grants/
- **Credits:** Varies, can be substantial for research projects
- **Requirements:**
  - Academic affiliation
  - Research proposal
  - Faculty sponsorship
- **Application:** Through AWS Cloud Credits for Research Program
- **Timeline:** Quarterly review cycles

## Alternative Funding Options

### GitHub Sponsors
If you make this project open source:

- **Website:** https://github.com/sponsors
- **Setup:** Enable GitHub Sponsors on your repository
- **Funding:** Community donations to cover AWS costs
- **Requirements:** Open-source project, active development

### Patreon / Ko-fi
For ongoing project support:

- **Patreon:** https://www.patreon.com/
- **Ko-fi:** https://ko-fi.com/
- **Use case:** Monthly supporters for AWS costs
- **Requirements:** Regular content/updates

## Cost Minimization Strategies

If you need to pay out of pocket, here's how to minimize costs:

### Strategy 1: Quick Demo Run (< $1)
```bash
# 1. Create resources
python -m src.agents.company_setup --dry-run=false

# 2. Run audit immediately (implement later)
python -m src.orchestrator.run_audit

# 3. Take screenshots

# 4. Delete everything
python -m src.agents.cleanup --simulation-id=audit-demo-2025

# Total time: < 1 hour
# Total cost: ~$0.10
```

### Strategy 2: Stop EC2 When Not Using
```bash
# Stop instances (no compute charges, only storage)
aws ec2 stop-instances --instance-ids i-xxxxx i-yyyyy

# Restart when needed
aws ec2 start-instances --instance-ids i-xxxxx i-yyyyy

# Cost while stopped: ~$0.10/month for EBS storage
```

### Strategy 3: Use Spot Instances
Modify the code to use EC2 Spot Instances (up to 90% cheaper):

```python
# In create_ec2_instances()
response = self.ec2_client.run_instances(
    ImageId=ami,
    InstanceType=instance_type,
    MinCount=1,
    MaxCount=1,
    InstanceMarketOptions={
        'MarketType': 'spot',
        'SpotOptions': {
            'MaxPrice': '0.01',  # $0.01/hour max
            'SpotInstanceType': 'one-time'
        }
    },
    # ... rest of config
)
```

### Strategy 4: Use Smaller Regions
Some regions are cheaper than others:

- **Cheapest:** us-east-1 (N. Virginia)
- **Also cheap:** us-east-2 (Ohio)
- **More expensive:** us-west-1, eu-west-1

## Realistic Cost Estimates

### Scenario 1: One-Time Demo (Recommended)
- **Duration:** 1 hour
- **Services:** IAM (free), S3 (1GB), EC2 (2 × t2.micro), CloudTrail
- **Cost:** ~$0.10
- **Use case:** Quick demo, screenshots, article

### Scenario 2: One Week Development
- **Duration:** 7 days
- **Services:** Same as above, instances running 24/7
- **Cost:** ~$2-3
- **Use case:** Active development and testing

### Scenario 3: One Month Showcase
- **Duration:** 30 days
- **Services:** Same as above, instances stopped when not in use
- **Cost:** ~$5-10
- **Use case:** Long-term demonstration, multiple presentations

### Scenario 4: Free Tier Only
- **Duration:** 12 months
- **Services:** Stay within all Free Tier limits
- **Cost:** $0
- **Limitations:**
  - 750 hours/month EC2 (1 instance 24/7 or 2 instances 12 hours/day)
  - 5GB S3 storage
  - 1 CloudTrail trail

## Recommended Approach

### For This Project:

1. **Immediate (No Credits):**
   - Run quick demo (< 1 hour)
   - Cost: ~$0.10
   - Get screenshots and data for article

2. **Short-term (1-2 weeks):**
   - Apply to AWS Community Builders
   - Make project open source
   - Write blog post about the project
   - Cost while waiting: ~$2-5

3. **Long-term (After credits):**
   - Use credits for extended development
   - Create video demonstrations
   - Present at meetups/conferences

## Application Tips

### For AWS Community Builders:

**Strengthen your application:**
1. **Create content about this project:**
   - Blog post: "Building an AWS Audit Agent System"
   - Video: Demo walkthrough
   - GitHub: Open-source the code

2. **Show community engagement:**
   - Share on Twitter/LinkedIn
   - Answer AWS questions on Stack Overflow
   - Participate in AWS subreddit

3. **Demonstrate expertise:**
   - Technical depth in your content
   - Real-world use cases
   - Best practices and security focus

**Timeline:**
- Applications typically open quarterly
- Review takes 4-6 weeks
- Credits issued upon acceptance

### For AWS Educate:

**If you have .edu email:**
1. Sign up immediately (instant approval)
2. Get $30-100 credits
3. Enough for this demo project

**If you're an educator:**
1. Get verification from your institution
2. Apply through AWS Educate portal
3. Typically approved within 1-2 weeks

## Contact Information

### AWS Support
- **General:** https://aws.amazon.com/contact-us/
- **Credits:** aws-activate@amazon.com (for Activate program)
- **Community:** aws-community@amazon.com

### Kiro/Anthropic
Since this showcases Kiro capabilities:
- Check Kiro documentation for developer programs
- Contact Kiro support about showcase projects
- Mention it's for community education/article

## Budget Tracking

Set up AWS Budget alerts regardless of credit status:

```bash
# Via AWS Console:
# Billing → Budgets → Create budget
# Set threshold: $5
# Alerts at: $1, $3, $5
```

## Summary

**Best Options for This Project:**

1. ✅ **AWS Community Builders** - Best long-term option if you create content
2. ✅ **AWS Educate** - Quick option if you have .edu email
3. ✅ **Quick Demo Run** - Cheapest option (~$0.10) if paying out of pocket
4. ✅ **Open Source + Sponsors** - Community-funded option

**Not Recommended:**
- ❌ AWS Activate (requires startup/VC affiliation)
- ❌ Waiting for credits before starting (just run quick demo)

## Next Steps

1. **Immediate:** Run quick demo with minimal cost (~$0.10)
2. **This Week:** Apply to AWS Community Builders
3. **This Month:** Create content about the project
4. **Ongoing:** Use credits for extended development

The project is designed to be cost-effective. Even without credits, you can run a complete demonstration for less than $1.

---

**Questions?** Check the AWS Credits FAQ: https://aws.amazon.com/activate/faq/
