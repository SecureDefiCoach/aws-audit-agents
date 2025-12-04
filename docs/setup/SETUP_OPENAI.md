# OpenAI API Setup Instructions

## Step 1: Get Your API Key

If you don't have it handy:
1. Go to https://platform.openai.com/api-keys
2. Log in with your OpenAI account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-...`)

## Step 2: Set the API Key

### Option A: Temporary (this session only)
```bash
export OPENAI_API_KEY='sk-your-key-here'
```

### Option B: Permanent (recommended)
```bash
# Add to your shell config
echo 'export OPENAI_API_KEY="sk-your-key-here"' >> ~/.zshrc

# Reload config
source ~/.zshrc
```

## Step 3: Test the Setup

```bash
python test_openai_setup.py
```

This will:
- ✅ Verify your API key works
- ✅ Test GPT-4 Turbo connection
- ✅ Show you Esther's reasoning quality
- ✅ Estimate cost per API call
- ✅ Confirm you're ready to build agents

## Expected Output

```
================================================================================
OpenAI API Setup Test
================================================================================
✅ API key found: sk-proj-ab...

🧪 Testing API connection with GPT-4...

✅ API connection successful!

📊 Model used: gpt-4-turbo-2024-04-09
💰 Tokens used: 245 (input: 45, output: 200)
💵 Estimated cost: $0.0065

🤖 Esther's response:
--------------------------------------------------------------------------------
When auditing an AWS account, I would prioritize these three IAM risks:

1. **Missing MFA on privileged accounts**: Root and administrative users 
   without multi-factor authentication are vulnerable to credential compromise.

2. **Overly permissive policies**: IAM policies granting broad permissions 
   (e.g., s3:*, iam:*) violate least privilege and increase blast radius.

3. **Inactive or unused access keys**: Long-lived credentials that aren't 
   rotated or are attached to inactive users pose security risks.
--------------------------------------------------------------------------------

✅ Quality check: Found 5 audit concepts: mfa, least privilege, root, access key, policy
✅ Response quality: EXCELLENT - Shows strong audit knowledge

================================================================================
✅ READY TO BUILD LLM-BASED AGENTS!
================================================================================

Next steps:
  1. Implement base AuditAgent class
  2. Build Esther with GPT-4 reasoning
  3. Test against CloudRetail AWS account
```

## Cost Estimates with GPT-4 Turbo

### Pricing
- **Input**: $0.01 per 1K tokens (~750 words)
- **Output**: $0.03 per 1K tokens (~750 words)

### Typical Audit Run
- **Risk assessment**: 20 calls × 300 tokens = 6K tokens → $0.24
- **Audit planning**: 30 calls × 400 tokens = 12K tokens → $0.48
- **Evidence analysis**: 50 calls × 500 tokens = 25K tokens → $1.00
- **Workpaper creation**: 20 calls × 600 tokens = 12K tokens → $0.48
- **Agent communication**: 30 calls × 200 tokens = 6K tokens → $0.24

**Total per audit**: ~$2.50

### Your $10 Budget
- **Development** (5-10 test runs): $5-7
- **Final demo** (1 run): $2.50
- **Total**: $7.50-9.50

**You have enough!** 🎉

## Available Models

You can use any of these:

### GPT-4 Turbo (Recommended)
```python
model="gpt-4-turbo"  # Latest, best reasoning
```
- **Cost**: $0.01 input, $0.03 output per 1K tokens
- **Speed**: 2-3 seconds
- **Quality**: Excellent

### GPT-4o (Faster, Cheaper)
```python
model="gpt-4o"  # Optimized version
```
- **Cost**: $0.005 input, $0.015 output per 1K tokens (50% cheaper!)
- **Speed**: 1-2 seconds
- **Quality**: Very good

### GPT-3.5 Turbo (Budget Option)
```python
model="gpt-3.5-turbo"  # Cheapest
```
- **Cost**: $0.0005 input, $0.0015 output per 1K tokens (90% cheaper!)
- **Speed**: 1 second
- **Quality**: Good (but may struggle with complex reasoning)

## Recommendation

Start with **GPT-4 Turbo** for best results. If you need to stretch your $10:
- Use **GPT-4o** for most tasks (50% cheaper, still excellent)
- Use **GPT-4 Turbo** only for complex reasoning (risk assessment, finding analysis)

## Troubleshooting

### Error: "Incorrect API key"
- Check your key starts with `sk-`
- Make sure you copied the entire key
- Try creating a new key

### Error: "Rate limit exceeded"
- You're making too many requests
- Wait 1 minute and try again
- We'll add rate limiting in the code

### Error: "Insufficient quota"
- Check your billing at https://platform.openai.com/account/billing
- Add more credits if needed
- Your $10 should be plenty for this project

## Next Steps

Once the test passes:
1. ✅ API key is working
2. ✅ GPT-4 reasoning is excellent
3. ✅ Ready to build agents

Let's start with **Task 1**: Implement base AuditAgent class!
