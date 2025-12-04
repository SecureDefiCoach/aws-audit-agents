"""
Interactive Agent Interview System

This script allows you to interview audit agents to verify their agentic quality.
You can ask them questions about their work, reasoning, and decision-making process.

The agent will respond using LLM reasoning, demonstrating autonomous behavior.

Run with: python examples/interview_agent.py
"""

import os
import sys
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.agents.audit_agent import AuditAgent, Tool
from src.agents.llm_client import LLMClient


class InterviewableAgent(AuditAgent):
    """Agent that can be interviewed"""
    
    def __init__(self, name, role, llm_client, background=None):
        super().__init__(name, role, llm_client)
        self.background = background or {}
        self.interview_mode = False
    
    def create_workpaper(self):
        """Create workpaper (required by base class)"""
        return {"agent": self.name, "role": self.role}
    
    def start_interview(self):
        """Enter interview mode"""
        self.interview_mode = True
        
        # Set up interview context
        interview_prompt = f"""You are being interviewed to verify your agentic capabilities.

The interviewer wants to understand:
- How you reason and make decisions
- How you adapt to unexpected situations
- How you would approach audit tasks
- Your understanding of your role and responsibilities

Background about you:
{self._format_background()}

Be thoughtful, professional, and demonstrate your reasoning capabilities.
Answer questions directly and explain your thought process.
If you don't know something, say so honestly.

The interview is starting now. Wait for the first question."""
        
        self.memory.append({"role": "user", "content": interview_prompt})
        
        print(f"\n{'='*70}")
        print(f"Interview with {self.name} - {self.role}")
        print(f"{'='*70}")
        print(f"\n{self.name} is ready for interview.")
        print("Type your questions. Type 'exit' to end the interview.\n")
    
    def _format_background(self):
        """Format background information"""
        if not self.background:
            return "No specific background provided."
        
        lines = []
        for key, value in self.background.items():
            lines.append(f"- {key}: {value}")
        return "\n".join(lines)
    
    def ask_question(self, question: str) -> str:
        """
        Ask the agent a question and get their response.
        
        Args:
            question: The question to ask
        
        Returns:
            Agent's response
        """
        if not self.interview_mode:
            raise ValueError("Agent is not in interview mode. Call start_interview() first.")
        
        # Add question to memory
        self.memory.append({"role": "user", "content": question})
        
        # Get LLM response
        response = self.llm.chat(self.memory)
        
        # Add response to memory
        self.memory.append({"role": "assistant", "content": response.content})
        
        # Log the interaction
        self._log_action(
            action_type="interview_question",
            description=f"Answered question: {question[:50]}...",
            details={"question": question, "answer": response.content}
        )
        
        return response.content
    
    def end_interview(self):
        """End the interview"""
        self.interview_mode = False
        
        print(f"\n{'='*70}")
        print(f"Interview Complete")
        print(f"{'='*70}")
        print(f"Questions asked: {len([a for a in self.action_history if a.action_type == 'interview_question'])}")
        print(f"Total conversation turns: {len(self.memory)}")


def create_sample_agents():
    """Create sample agents with different backgrounds"""
    
    # Check for API key
    if not os.environ.get('OPENAI_API_KEY'):
        print("\n⚠️  Error: OPENAI_API_KEY not set")
        print("   Set it with: export OPENAI_API_KEY='your-key-here'")
        print("\n   This interview system requires a real LLM to demonstrate agentic behavior.")
        sys.exit(1)
    
    # Initialize LLM client
    llm = LLMClient(
        provider='openai',
        model='gpt-4o',  # Good balance of cost and quality
        rate_limit=10,
        temperature=0.7
    )
    
    agents = {}
    
    # Esther - IAM Auditor
    agents['esther'] = InterviewableAgent(
        name="Esther",
        role="Senior Auditor - IAM & Logical Access",
        llm_client=llm,
        background={
            "Specialization": "Identity and Access Management",
            "Focus Areas": "User access, MFA, permissions, credential management",
            "Experience": "10+ years in IT audit",
            "Certifications": "CISA, CISSP",
            "Approach": "Risk-based, evidence-driven"
        }
    )
    
    # Chuck - Data Protection Auditor
    agents['chuck'] = InterviewableAgent(
        name="Chuck",
        role="Senior Auditor - Data Protection & Network Security",
        llm_client=llm,
        background={
            "Specialization": "Data encryption and network security",
            "Focus Areas": "S3 encryption, EC2 security groups, VPC configuration",
            "Experience": "8+ years in cloud security",
            "Certifications": "CISA, AWS Security Specialty",
            "Approach": "Defense-in-depth, least privilege"
        }
    )
    
    # Victor - Logging Auditor
    agents['victor'] = InterviewableAgent(
        name="Victor",
        role="Senior Auditor - Logging & Monitoring",
        llm_client=llm,
        background={
            "Specialization": "Logging, monitoring, and incident response",
            "Focus Areas": "CloudTrail, CloudWatch, log retention, alerting",
            "Experience": "7+ years in security operations",
            "Certifications": "CISA, GCIH",
            "Approach": "Detective controls, continuous monitoring"
        }
    )
    
    # Maurice - Audit Manager
    agents['maurice'] = InterviewableAgent(
        name="Maurice",
        role="Audit Manager",
        llm_client=llm,
        background={
            "Specialization": "Audit management and quality review",
            "Focus Areas": "Workpaper review, risk assessment, team coordination",
            "Experience": "15+ years in audit leadership",
            "Certifications": "CISA, CIA, CPA",
            "Approach": "Quality-focused, mentorship-oriented"
        }
    )
    
    return agents, llm


def interactive_interview(agent: InterviewableAgent):
    """Run an interactive interview session"""
    
    agent.start_interview()
    
    while True:
        # Get question from user
        try:
            question = input(f"\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n")
            break
        
        if not question:
            continue
        
        if question.lower() in ['exit', 'quit', 'done', 'bye']:
            break
        
        # Get agent's response
        print(f"\n{agent.name}: ", end="", flush=True)
        response = agent.ask_question(question)
        print(response)
    
    agent.end_interview()


def guided_interview(agent: InterviewableAgent):
    """Run a guided interview with suggested questions"""
    
    agent.start_interview()
    
    # Suggested questions to verify agentic quality
    questions = [
        # Understanding of role
        "Can you describe your role and what you're responsible for in an audit?",
        
        # Reasoning capability
        "If you discovered that a production database has no encryption at rest, how would you assess the risk? Walk me through your thinking.",
        
        # Adaptation
        "Imagine you're auditing IAM and you find that the company uses a third-party identity provider you've never seen before. How would you adapt your approach?",
        
        # Decision making
        "You have limited audit time. You find both: 1) Missing MFA on a developer account, and 2) Root account with no MFA. Which do you investigate first and why?",
        
        # Tool usage
        "What tools or information would you need to assess whether CloudTrail is properly configured?",
        
        # Communication
        "If you found a critical security issue, how would you communicate it to the audit manager? What would you include?",
        
        # Learning
        "Have you ever changed your mind about a risk rating after collecting more evidence? How did you handle that?",
        
        # Collaboration
        "How would you work with other auditors if your findings overlap with theirs?"
    ]
    
    print("\n📋 This is a guided interview with suggested questions.")
    print("   Press Enter to use the suggested question, or type your own.\n")
    
    for i, suggested_q in enumerate(questions, 1):
        print(f"\n{'─'*70}")
        print(f"Question {i}/{len(questions)}")
        print(f"{'─'*70}")
        print(f"\nSuggested: {suggested_q}")
        
        # Get user input
        try:
            user_input = input(f"\nYour question (or press Enter for suggested): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n")
            break
        
        if user_input.lower() in ['exit', 'quit', 'done']:
            break
        
        # Use suggested question if user pressed Enter
        question = user_input if user_input else suggested_q
        
        # Get agent's response
        print(f"\n{agent.name}: ", end="", flush=True)
        response = agent.ask_question(question)
        print(response)
        
        # Ask if user wants to continue
        if i < len(questions):
            try:
                continue_input = input(f"\nContinue to next question? (y/n): ").strip().lower()
                if continue_input == 'n':
                    break
            except (EOFError, KeyboardInterrupt):
                print("\n")
                break
    
    agent.end_interview()


def main():
    """Main interview program"""
    
    print("=" * 70)
    print("Agent Interview System - Verify Agentic Quality")
    print("=" * 70)
    
    # Create agents
    print("\n📋 Loading agents...")
    agents, llm = create_sample_agents()
    print(f"   ✅ {len(agents)} agents ready for interview")
    
    # Select agent
    print("\n👥 Available agents:")
    for key, agent in agents.items():
        print(f"   {key}: {agent.name} - {agent.role}")
    
    while True:
        try:
            agent_choice = input("\nSelect agent to interview (or 'exit'): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n")
            break
        
        if agent_choice in ['exit', 'quit', 'done']:
            break
        
        if agent_choice not in agents:
            print(f"❌ Unknown agent: {agent_choice}")
            continue
        
        agent = agents[agent_choice]
        
        # Select interview mode
        print("\n📝 Interview modes:")
        print("   1. Guided interview (suggested questions)")
        print("   2. Free-form interview (ask anything)")
        
        try:
            mode = input("\nSelect mode (1 or 2): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n")
            break
        
        if mode == '1':
            guided_interview(agent)
        elif mode == '2':
            interactive_interview(agent)
        else:
            print("❌ Invalid mode")
            continue
        
        # Print cost summary
        print("\n💰 Interview cost:")
        llm.print_cost_summary()
        
        # Ask if user wants to interview another agent
        try:
            another = input("\nInterview another agent? (y/n): ").strip().lower()
            if another != 'y':
                break
        except (EOFError, KeyboardInterrupt):
            print("\n")
            break
    
    print("\n✅ Interview system closed")
    print("\n💡 Tip: Review the agent's responses to verify:")
    print("   - Independent reasoning (not scripted)")
    print("   - Adaptation to different scenarios")
    print("   - Professional communication")
    print("   - Understanding of audit concepts")


if __name__ == "__main__":
    main()
