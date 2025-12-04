# Gemini Prompt: Agent Framework Infographic (Day 1)

## 🎯 Today's Focus: The Agent Framework

Simple, focused infographic showing the core structure of a single autonomous agent.

---

## 📋 Prompt for Google Gemini

```
Create a clean, professional infographic showing the framework of a single autonomous AI agent. Keep it simple and focused - this is Day 1 of a series.

## Title
"Autonomous AI Agent Framework"

## Core Concept
A self-thinking AI agent with three integrated components working together:

### Component 1: 🧠 REASONING ENGINE
- **What**: GPT-5 API connection
- **Purpose**: Think and make decisions
- **How**: Receives goals, reasons about approach, adapts based on results
- **Example**: Given "Test IAM control" → figures out what to check and how

### Component 2: 📚 KNOWLEDGE BASE  
- **What**: Markdown files in file system
- **Purpose**: Store procedures and guidelines
- **Location**: knowledge/[agent-name]/ folder
- **Example**: risk-assessment-procedure.md, iam-control-procedures.md
- **How**: Agent reads these files to know HOW to perform tasks

### Component 3: 🔧 ACTION TOOLS
- **What**: AWS CLI commands (via Python Boto3)
- **Purpose**: Take actions in AWS environment
- **Examples**: 
  - query_iam (check users, roles, MFA)
  - query_cloudtrail (check audit logs)
  - create_workpaper (document findings)
- **Access**: Read-only to AWS services

## Visual Layout

Show ONE agent in the center with three connected parts:

```
        [AGENT NAME: Esther]
        Senior Auditor - IAM
                |
    ┌───────────┼───────────┐
    |           |           |
    ▼           ▼           ▼
  🧠 BRAIN    📚 MEMORY   🔧 HANDS
  
  GPT-5 API   Knowledge   AWS CLI
  Reasoning   Base Files  Tools
```

## The Autonomous Loop

Show a simple circular flow:
1. Receive Goal
2. Think (GPT-5)
3. Read Procedures (Knowledge)
4. Execute Actions (AWS CLI)
5. Analyze Results (GPT-5)
6. Document (Workpaper)
7. Complete or Continue

## Key Message

**"Self-thinking AI agents that reason, learn, and act autonomously"**

## What Makes This Special

Show 3 key differentiators:
- ✓ **Self-Thinking**: No step-by-step scripts, agents reason about goals
- ✓ **Knowledge-Driven**: Reads procedures like a human would
- ✓ **Action-Capable**: Directly interacts with AWS environment

## Simple Example

Show a mini workflow:
```
Goal: "Check if MFA is enabled"
    ↓
🧠 Think: "I need to query IAM and check each user"
    ↓
📚 Read: Consults iam-control-procedures.md
    ↓
🔧 Act: Executes query_iam(operation="list_mfa_devices")
    ↓
🧠 Analyze: "5 users don't have MFA enabled"
    ↓
📝 Document: Creates workpaper with finding
```

## Design Guidelines

**Keep It Simple**:
- Focus on ONE agent, not the whole team
- Show the 3 components clearly
- Use simple icons (brain, book, wrench)
- Clean, minimal design
- Easy to understand in 30 seconds

**Color Scheme**:
- Blue (#667eea) for reasoning/brain
- Purple (#764ba2) for knowledge/memory
- Green (#4caf50) for actions/tools
- White/light gray background

**Layout**:
- Agent name at top
- Three components in a row or triangle
- Simple workflow loop at bottom
- Minimal text, maximum clarity

**Size**: 
- Square or 16:9 ratio
- Suitable for social media and presentations
- High resolution

## What NOT to Include

❌ Don't show the whole team (that's for later)
❌ Don't show complex workflows (keep it simple)
❌ Don't include too much technical detail
❌ Don't overwhelm with text

## Perfect For

✓ Social media post (LinkedIn, Twitter)
✓ Blog post header image
✓ Presentation intro slide
✓ Documentation visual
✓ Day 1 of infographic series
```

---

## 🎯 Ultra-Simple Version (Use This!)

```
Create a simple, clean infographic titled "Autonomous AI Agent Framework"

Show ONE agent with THREE parts:

1. 🧠 REASONING ENGINE
   - GPT-5 API
   - Thinks & decides

2. 📚 KNOWLEDGE BASE
   - Markdown files
   - Procedures & guidelines

3. 🔧 ACTION TOOLS
   - AWS CLI
   - Takes actions

Add a simple loop showing:
Goal → Think → Read → Act → Document → Complete

Use colors: Blue (brain), Purple (knowledge), Green (actions)

Keep it minimal and easy to understand. This is Day 1 of a series.
```

---

---

## 📅 Infographic Series Plan

**Day 1** (Today): Agent Framework - The 3 components  
**Day 2**: Knowledge Base - How agents learn from procedures  
**Day 3**: Action Tools - AWS CLI integration  
**Day 4**: Reasoning Engine - GPT-5 decision making  
**Day 5**: The Team - 7 agents working together  
**Day 6**: Workflow - The 6 audit phases  
**Day 7**: Results - Before/after comparison  

---

**Created**: December 4, 2025  
**Purpose**: Day 1 infographic - Simple agent framework  
**Series**: Daily infographics building up the complete picture  
**Tool**: Google Gemini or similar AI image generation
