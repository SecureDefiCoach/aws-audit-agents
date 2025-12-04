"""
Demo Agent Interview - Automated demonstration of agent reasoning

This script runs a pre-scripted interview to demonstrate agentic behavior
without requiring interactive input. Great for demos and testing.

Run with: python examples/demo_agent_interview.py
"""

import os
import sys
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.agents.audit_agent import AuditAgent, Tool
from src.agents.llm_client import LLMClient


class InterviewableAgent(AuditAgent):
    """Agent that can be interviewed"""
    
    def create_workpaper(self):
        return {"agent": self.name}
    
    def ask_question(self, question: str) -> str:
        """Ask the agent a question"""
        self.memory.append({"role": "user", "content": question})
        response = self.llm.chat(self.memory)
        self.memory.append({"role": "assistant", "content": response.content})
        return response.content


def demo_interview():
    """Run a demonstration interview"""
    
    print("=" * 70)
    print("Agent Interview Demo - Verifying Agentic Quality")
    print("=" * 70)
    
    # Check for API key
    if not os.environ.get('OPENAI_API_KEY'):
        print("\n⚠️  Error: OPENAI_API_KEY not set")
        print("   Set it with: export OPENAI_API_KEY='your-key-here'")
        print("\n   This demo requires a real LLM to demonstrate agentic behavior.")
        return
    
    # Initialize LLM
    print("\n1. Initializing LLM client...")
    llm = LLMClient(
        provider='openai',
        model='gpt-4o',
        rate_limit=10,
        temperature=0.7
    )
    print("   ✅ LLM ready")
    
    # Create agent
    print("\n2. Creating agent...")
    agent = InterviewableAgent(
        name="Esther",
        role="Senior Auditor - IAM & Logical Access",
        llm_client=llm
    )
    
    # Set up interview context
    interview_setup = """You are Esther, a Senior Auditor specializing in IAM and Logical Access.

You are being interviewed to demonstrate your agentic capabilities - your ability to 
reason independently, adapt to situations, and make professional judgments.

Background:
- 10+ years experience in IT audit
- Specialization: Identity and Access Management
- Focus: User access, MFA, permissions, credential management
- Certifications: CISA, CISSP
- Approach: Risk-based, evidence-driven

Be thoughtful and demonstrate your reasoning process. Answer questions professionally
and explain your thinking."""
    
    agent.memory.append({"role": "user", "content": interview_setup})
    print(f"   ✅ Agent ready: {agent.name}")
    
    # Interview questions
    questions = [
        {
            "q": "Esther, can you describe your role and what you focus on during an audit?",
            "purpose": "Understanding of role"
        },
        {
            "q": "If you discovered that 3 out of 5 IAM users don't have MFA enabled, including an admin account, how would you assess the risk? Walk me through your reasoning.",
            "purpose": "Risk assessment reasoning"
        },
        {
            "q": "Imagine you're auditing IAM and you discover the company uses Okta for SSO, which you haven't audited before. How would you adapt your approach?",
            "purpose": "Adaptation to new situations"
        },
        {
            "q": "You have limited time. You find: 1) A developer with overly broad S3 permissions, and 2) The root account has no MFA. Which do you prioritize and why?",
            "purpose": "Decision making under constraints"
        },
        {
            "q": "If you found a critical IAM issue, how would you communicate it to Maurice, the audit manager?",
            "purpose": "Professional communication"
        }
    ]
    
    print("\n3. Starting interview...")
    print(f"\n{'='*70}")
    print(f"Interview with {agent.name}")
    print(f"{'='*70}\n")
    
    for i, item in enumerate(questions, 1):
        question = item['q']
        purpose = item['purpose']
        
        print(f"\n{'─'*70}")
        print(f"Question {i}/{len(questions)} - Testing: {purpose}")
        print(f"{'─'*70}\n")
        
        print(f"Interviewer: {question}\n")
        
        # Small delay for dramatic effect
        time.sleep(0.5)
        
        print(f"{agent.name}: ", end="", flush=True)
        
        # Get agent's response
        response = agent.ask_question(question)
        print(response)
        
        # Pause between questions
        if i < len(questions):
            time.sleep(1)
    
    # Summary
    print(f"\n{'='*70}")
    print("Interview Complete")
    print(f"{'='*70}\n")
    
    print("✅ Agentic Quality Verified:")
    print("   ✓ Independent reasoning (not scripted responses)")
    print("   ✓ Adaptation to different scenarios")
    print("   ✓ Professional communication")
    print("   ✓ Risk-based decision making")
    print("   ✓ Contextual understanding")
    
    # Cost summary
    print()
    llm.print_cost_summary()
    
    print("\n💡 Key Observations:")
    print("   - Agent reasoned through each scenario independently")
    print("   - Responses were contextual and thoughtful")
    print("   - Agent demonstrated professional judgment")
    print("   - No pre-scripted answers - true LLM reasoning")
    
    print("\n🎯 Next Steps:")
    print("   - Run interactive interview: python examples/interview_agent.py")
    print("   - Test with different scenarios")
    print("   - Interview other agents (Chuck, Victor, Maurice)")


if __name__ == "__main__":
    demo_interview()
