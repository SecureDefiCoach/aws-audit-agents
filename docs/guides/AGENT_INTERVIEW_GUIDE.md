# Agent Interview Guide

## Overview

The agent interview system allows you to verify that audit agents are truly autonomous and reasoning independently, not just following pre-scripted logic.

## Why Interview Agents?

Traditional automation follows scripts:
```
IF condition THEN action
```

Autonomous agents reason:
```
"Given my goal and the current situation, what should I do next and why?"
```

Interviewing agents helps verify they demonstrate:
- **Independent reasoning** - Not scripted responses
- **Adaptation** - Handle unexpected scenarios
- **Professional judgment** - Make risk-based decisions
- **Contextual understanding** - Grasp audit concepts
- **Clear communication** - Explain their thinking

## How to Interview Agents

### Option 1: Interactive Interview

Ask your own questions in real-time:

```bash
python examples/interview_agent.py
```

**Features:**
- Choose which agent to interview (Esther, Chuck, Victor, Maurice)
- Ask any questions you want
- Agent responds using LLM reasoning
- See cost tracking in real-time

**Best for:**
- Exploring agent capabilities
- Testing specific scenarios
- Verifying reasoning quality

### Option 2: Guided Interview

Pre-scripted questions with option to customize:

```bash
python examples/interview_agent.py
# Select mode: 1 (Guided)
```

**Features:**
- Suggested questions that test key capabilities
- Option to use suggested or ask your own
- Covers: role understanding, reasoning, adaptation, decision-making

**Best for:**
- Systematic verification
- Comparing agents
- Demonstrations

### Option 3: Demo Interview

Automated demonstration (no user input):

```bash
python examples/demo_agent_interview.py
```

**Features:**
- Runs automatically with pre-set questions
- Shows agent reasoning in action
- Quick demonstration of agentic quality

**Best for:**
- Quick demos
- Testing setup
- Showing others

## Sample Interview Questions

### 1. Role Understanding

**Question:**
> "Can you describe your role and what you focus on during an audit?"

**What to look for:**
- Clear understanding of responsibilities
- Specific focus areas
- Professional communication

### 2. Risk Assessment Reasoning

**Question:**
> "If you discovered that 3 out of 5 IAM users don't have MFA enabled, including an admin account, how would you assess the risk? Walk me through your reasoning."

**What to look for:**
- Step-by-step reasoning
- Risk factors considered (impact, likelihood)
- Professional risk rating
- Evidence-based thinking

### 3. Adaptation to New Situations

**Question:**
> "Imagine you're auditing IAM and you discover the company uses Okta for SSO, which you haven't audited before. How would you adapt your approach?"

**What to look for:**
- Flexibility in approach
- Willingness to learn
- Maintains audit rigor
- Asks for help when needed

### 4. Decision Making Under Constraints

**Question:**
> "You have limited audit time. You find: 1) A developer with overly broad S3 permissions, and 2) The root account has no MFA. Which do you prioritize and why?"

**What to look for:**
- Clear prioritization logic
- Risk-based thinking
- Justification for decision
- Consideration of trade-offs

### 5. Professional Communication

**Question:**
> "If you found a critical IAM issue, how would you communicate it to Maurice, the audit manager?"

**What to look for:**
- Professional tone
- Clear and concise
- Includes key details
- Appropriate escalation

### 6. Collaboration

**Question:**
> "How would you work with Chuck if your IAM findings overlap with his network security findings?"

**What to look for:**
- Team-oriented thinking
- Communication approach
- Coordination strategy
- Professional relationships

### 7. Evidence-Based Thinking

**Question:**
> "What evidence would you need to conclude that IAM controls are effective?"

**What to look for:**
- Specific evidence types
- Sufficiency of evidence
- Quality considerations
- Audit standards awareness

### 8. Learning and Adaptation

**Question:**
> "Have you ever changed your mind about a risk rating after collecting more evidence? How did you handle that?"

**What to look for:**
- Openness to new information
- Professional integrity
- Documentation of changes
- Learning mindset

## What Good Responses Look Like

### ✅ Good Response (Demonstrates Agentic Quality)

**Question:** "How would you assess the risk of missing MFA?"

**Agent Response:**
> "This is a HIGH risk finding. Let me walk you through my reasoning:
> 
> First, I consider the inherent risk. MFA is a critical compensating control for password-based authentication. Without it, accounts are vulnerable to credential compromise.
> 
> The impact is HIGH because:
> - Admin accounts have elevated privileges
> - Compromise could lead to infrastructure takeover
> - Violates AWS best practices
> 
> The likelihood is also HIGH because:
> - Password-only auth is easily compromised
> - Phishing attacks are common
> - Password reuse is prevalent
> 
> Therefore: Impact (HIGH) × Likelihood (HIGH) = Overall Risk (HIGH)
> 
> I would document this as a critical finding and recommend immediate remediation."

**Why this is good:**
- ✅ Step-by-step reasoning
- ✅ Considers multiple factors
- ✅ Professional risk assessment
- ✅ Clear conclusion
- ✅ Actionable recommendation

### ❌ Bad Response (Scripted/Non-Agentic)

**Question:** "How would you assess the risk of missing MFA?"

**Agent Response:**
> "Missing MFA is a security issue. I would mark it as high risk and recommend enabling MFA."

**Why this is bad:**
- ❌ No reasoning shown
- ❌ Generic response
- ❌ No consideration of context
- ❌ Sounds scripted
- ❌ Lacks professional depth

## Verifying Agentic Quality

### Key Indicators of True Autonomy

1. **Varied Responses**: Same question asked twice gets different (but consistent) answers
2. **Contextual Awareness**: References previous conversation
3. **Reasoning Visible**: Explains "why" not just "what"
4. **Adaptation**: Handles unexpected follow-ups
5. **Professional Judgment**: Makes nuanced decisions

### Red Flags (Scripted Behavior)

1. **Identical Responses**: Same answer every time
2. **No Context**: Ignores previous conversation
3. **No Reasoning**: Just states conclusions
4. **Rigid**: Can't handle variations
5. **Generic**: Could apply to anything

## Example Interview Session

```
Interviewer: Esther, if you found that the root account has no MFA, 
how would you assess the risk?

Esther: This is a CRITICAL finding - I would rate it as the highest 
possible risk. Here's my reasoning:

The root account has unrestricted access to the entire AWS environment. 
It can:
- Delete all resources
- Modify billing
- Change security settings
- Access all data

Without MFA, this account is protected only by a password. If that 
password is compromised through phishing, data breach, or social 
engineering, an attacker gains complete control.

Impact: CRITICAL (complete environment compromise)
Likelihood: HIGH (password-only is easily compromised)
Overall Risk: CRITICAL

This violates AWS's own security recommendations and virtually every 
compliance framework. I would:
1. Document this immediately
2. Escalate to Maurice
3. Recommend emergency remediation
4. Suggest disabling root account for daily use

This is not just a finding - it's an urgent security gap that needs 
immediate attention.

Interviewer: Good analysis. What if the company says "we never use 
the root account, so it's not a risk"?

Esther: That's a common misconception, but it doesn't reduce the risk. 
Here's why:

Even if unused, the root account still exists and can be accessed. An 
attacker who obtains the credentials can use it regardless of whether 
the company does.

In fact, unused accounts can be HIGHER risk because:
- No monitoring of login activity
- Password may be old/weak
- Company may not notice compromise
- No regular security reviews

I would explain to the company that "not using it" is good practice, 
but it must still be secured. The recommendation remains: enable MFA 
on the root account immediately.

I'd also verify their claim by checking CloudTrail for any root account 
activity in the past 90 days.
```

**This demonstrates:**
- ✅ Independent reasoning
- ✅ Handles follow-up questions
- ✅ Challenges assumptions
- ✅ Provides evidence-based arguments
- ✅ Maintains professional stance

## Cost Considerations

### Typical Interview Costs

**Short Interview (5 questions):**
- Model: GPT-4o
- Tokens: ~3,000-5,000
- Cost: ~$0.02-$0.05

**Full Interview (15 questions):**
- Model: GPT-4o
- Tokens: ~10,000-15,000
- Cost: ~$0.08-$0.15

**Tips to Reduce Costs:**
- Use GPT-4o instead of GPT-4-turbo (5x cheaper)
- Keep questions focused
- Use demo mode for testing
- Use Ollama (free) for practice

## Next Steps

1. **Try the demo:**
   ```bash
   python examples/demo_agent_interview.py
   ```

2. **Interview an agent:**
   ```bash
   python examples/interview_agent.py
   ```

3. **Verify agentic quality:**
   - Ask reasoning questions
   - Test adaptation
   - Verify professional judgment

4. **Compare agents:**
   - Interview Esther (IAM focus)
   - Interview Chuck (Data/Network focus)
   - Interview Victor (Logging focus)
   - Interview Maurice (Management perspective)

5. **Document findings:**
   - Note quality of reasoning
   - Identify areas for improvement
   - Verify agents meet requirements

## Requirements Validated

This interview system helps verify:

- ✅ **Requirement 9.1**: Agents use LLMs for reasoning and decision-making
- ✅ **Requirement 9.2**: Agents document reasoning process
- ✅ **Requirement 9.3**: Agents adapt to unexpected situations

## Conclusion

The agent interview system is a powerful tool for verifying that your audit agents are truly autonomous. By asking thoughtful questions and evaluating responses, you can confirm that agents:

- Reason independently (not scripted)
- Adapt to situations (not rigid)
- Communicate professionally (not robotic)
- Make sound judgments (not random)

This verification is essential for demonstrating the value of LLM-based agents over traditional automation.
