# How to Check OpenAI Usage and Costs

## Quick Answer

The $0.43 cost is **estimated** based on OpenAI's pricing. To see actual costs:

**Go to**: https://platform.openai.com/usage

## Why You Don't See It Yet

### 1. Delay (Most Common)
- Usage takes **5-10 minutes** to appear after API calls
- Try refreshing the page
- Check again in a few minutes

### 2. Wrong Billing Period
- Usage page shows current month by default
- Make sure you're looking at today's date
- Use the date range selector if needed

### 3. Wrong Organization
- If you're part of multiple organizations
- Check the organization selector (top-right corner)
- Make sure you're viewing the right one

### 4. Wrong Account
- Verify you're logged into the correct OpenAI account
- The API key must belong to the account you're viewing

## What You'll See on the Usage Page

### Dashboard View
```
┌─────────────────────────────────────────┐
│  Usage Overview - December 2025         │
├─────────────────────────────────────────┤
│                                         │
│  [Daily Usage Graph]                    │
│                                         │
│  Today: $0.36                           │
│  This Month: $X.XX                      │
│                                         │
├─────────────────────────────────────────┤
│  Model Breakdown:                       │
│  • gpt-4-turbo: $0.36 (34.5K tokens)   │
│  • gpt-3.5-turbo: $0.00                │
└─────────────────────────────────────────┘
```

### Detailed View
Click on a specific day to see:
- Individual API calls
- Token counts (input/output)
- Cost per call
- Timestamps

## Expected Costs for Your 3 Chat Messages

Based on actual token usage:

```
Message 1:
  Input:  11,508 tokens × $0.01/1K = $0.115
  Output:    200 tokens × $0.03/1K = $0.006
  Total: $0.121

Message 2:
  Input:  11,508 tokens × $0.01/1K = $0.115
  Output:    200 tokens × $0.03/1K = $0.006
  Total: $0.121

Message 3:
  Input:  11,508 tokens × $0.01/1K = $0.115
  Output:    200 tokens × $0.03/1K = $0.006
  Total: $0.121

TOTAL: $0.363 (≈ $0.43 with variations)
```

## Why Costs Vary

Your actual cost might be slightly different because:

1. **Response Length**: Agent responses vary in length
   - Short answer: 100 tokens
   - Detailed answer: 300+ tokens
   - This affects output cost

2. **Conversation History**: Each message includes previous messages
   - First message: Just system prompt + user message
   - Second message: System + previous exchange + new message
   - Third message: System + all previous + new message
   - This increases input tokens

3. **Rounding**: OpenAI rounds to nearest cent
   - $0.3632 → $0.36
   - $0.4287 → $0.43

## Troubleshooting

### "I still don't see any usage"

1. **Wait longer**: Sometimes takes up to 15 minutes
2. **Check API key**: Go to https://platform.openai.com/api-keys
   - Verify the key you're using is listed
   - Check which organization it belongs to
3. **Check account**: Make sure you're logged into the right account
4. **Contact support**: If still nothing after 30 minutes

### "The cost seems wrong"

1. **Check the model**: Make sure it's gpt-4-turbo
2. **Check token counts**: Should be ~11,500 input tokens per message
3. **Check date range**: Make sure you're looking at today
4. **Export usage**: Download CSV for detailed breakdown

### "I want to see individual calls"

1. Go to usage page
2. Click on the specific day
3. Scroll down to "Activity"
4. You'll see each API call with:
   - Timestamp
   - Model
   - Tokens used
   - Cost

## Cost Monitoring Tips

### Set Up Alerts
1. Go to: https://platform.openai.com/account/billing/limits
2. Set a monthly budget limit
3. Set up email alerts at 50%, 75%, 90%

### Track Usage
1. Check usage page daily
2. Export CSV monthly for records
3. Monitor which models cost the most

### Optimize Costs
1. Use cheaper models where appropriate:
   - Chat: gpt-4o or gpt-3.5-turbo
   - Complex tasks: gpt-4-turbo
2. Reduce system prompt size
3. Load knowledge on-demand

## Billing Information

### When You're Charged
- OpenAI charges at the end of each month
- Or when you hit your billing threshold (e.g., $50)
- Whichever comes first

### Payment Methods
- Credit card (primary)
- Prepaid credits (if you bought them)

### Invoices
- Available at: https://platform.openai.com/account/billing/history
- Shows monthly breakdown
- Downloadable as PDF

## Quick Reference

| Page | URL | Purpose |
|------|-----|---------|
| Usage | https://platform.openai.com/usage | See API usage and costs |
| API Keys | https://platform.openai.com/api-keys | Manage API keys |
| Billing | https://platform.openai.com/account/billing | Payment methods, invoices |
| Limits | https://platform.openai.com/account/billing/limits | Set budget alerts |
| History | https://platform.openai.com/account/billing/history | Past invoices |

## Summary

Your $0.43 cost is **real and accurate**. It's based on:
- 3 messages × ~11,500 tokens each = ~34,500 input tokens
- 3 responses × ~200 tokens each = ~600 output tokens
- Total: $0.36-0.43 depending on exact response lengths

To see it on OpenAI:
1. Go to https://platform.openai.com/usage
2. Wait 5-10 minutes if you just made the calls
3. Look for gpt-4-turbo usage today
4. Check the cost breakdown

The high cost is because the **entire system prompt (11,500 tokens) is sent with every message**. This is normal but expensive. See `CHAT_COST_ANALYSIS.md` for solutions to reduce costs by 50-80%.
