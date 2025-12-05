"""
Analyze chat costs to understand why they're high.

This script shows:
1. How many tokens are in Esther's system prompt
2. How much knowledge is loaded
3. What the cost breakdown is per message
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.agents.agent_factory import AgentFactory


def count_tokens(text: str, model: str = "gpt-4") -> int:
    """Count tokens in text using rough estimate."""
    # Rough estimate: 1 token ≈ 0.75 words (or 1 word ≈ 1.3 tokens)
    words = len(text.split())
    return int(words * 1.3)


def analyze_agent_costs(agent_name: str = "esther"):
    """Analyze the cost structure for an agent."""
    
    print("\n" + "=" * 80)
    print(f"ANALYZING CHAT COSTS FOR {agent_name.upper()}")
    print("=" * 80)
    print()
    
    # Create agent
    factory = AgentFactory("config/agent_models.yaml")
    team = factory.create_audit_team()
    agent = team.get(agent_name)
    
    if not agent:
        print(f"❌ Agent '{agent_name}' not found")
        return
    
    print(f"✓ Agent: {agent.name}")
    print(f"✓ Role: {agent.role}")
    print(f"✓ Model: {agent.llm.model}")
    print()
    
    # Get system prompt
    system_prompt = ""
    if agent.memory and agent.memory[0].get("role") == "system":
        system_prompt = agent.memory[0].get("content", "")
    
    # Count tokens
    system_tokens = count_tokens(system_prompt)
    
    print("=" * 80)
    print("TOKEN BREAKDOWN")
    print("=" * 80)
    print()
    
    # System prompt sections
    print("System Prompt Components:")
    print(f"  Total system prompt: {system_tokens:,} tokens")
    print()
    
    # Estimate breakdown
    lines = system_prompt.split('\n')
    
    # Find knowledge section
    knowledge_start = None
    for i, line in enumerate(lines):
        if "Knowledge Base" in line or "Loaded Procedures" in line:
            knowledge_start = i
            break
    
    before_tokens = 0
    knowledge_tokens = 0
    
    if knowledge_start:
        before_knowledge = '\n'.join(lines[:knowledge_start])
        knowledge_section = '\n'.join(lines[knowledge_start:])
        
        before_tokens = count_tokens(before_knowledge)
        knowledge_tokens = count_tokens(knowledge_section)
        
        print(f"  Core prompt (capabilities, tools, format): {before_tokens:,} tokens")
        print(f"  Knowledge base (procedures): {knowledge_tokens:,} tokens")
    else:
        # Estimate: knowledge is typically 60-70% of system prompt
        knowledge_tokens = int(system_tokens * 0.65)
        before_tokens = system_tokens - knowledge_tokens
        print(f"  Core prompt (estimated): {before_tokens:,} tokens")
        print(f"  Knowledge base (estimated): {knowledge_tokens:,} tokens")
    
    print()
    print("=" * 80)
    print("COST ANALYSIS")
    print("=" * 80)
    print()
    
    # Get pricing
    model = agent.llm.model
    pricing = agent.llm.PRICING.get(model, agent.llm.PRICING['gpt-4-turbo'])
    
    print(f"Model: {model}")
    print(f"Input pricing: ${pricing['input']:.4f} per 1K tokens")
    print(f"Output pricing: ${pricing['output']:.4f} per 1K tokens")
    print()
    
    # Simulate a chat exchange
    print("SIMULATED CHAT EXCHANGE:")
    print("-" * 80)
    
    # User message
    user_message = "Hello Esther, can you explain your role in the audit?"
    user_tokens = count_tokens(user_message)
    
    # Agent response (estimate)
    agent_response_tokens = 200  # Typical response
    
    # Total tokens per exchange
    input_tokens = system_tokens + user_tokens  # System prompt + user message
    output_tokens = agent_response_tokens
    total_tokens = input_tokens + output_tokens
    
    print(f"User message: '{user_message}'")
    print(f"  User message tokens: {user_tokens:,}")
    print()
    print(f"Input tokens (system + user): {input_tokens:,}")
    print(f"Output tokens (agent response): {output_tokens:,}")
    print(f"Total tokens: {total_tokens:,}")
    print()
    
    # Calculate cost
    input_cost = (input_tokens * pricing['input']) / 1000
    output_cost = (output_tokens * pricing['output']) / 1000
    total_cost = input_cost + output_cost
    
    print(f"Input cost: ${input_cost:.4f}")
    print(f"Output cost: ${output_cost:.4f}")
    print(f"Total cost per message: ${total_cost:.4f}")
    print()
    
    # Cost for 3 messages
    cost_3_messages = total_cost * 3
    print(f"Cost for 3 messages: ${cost_3_messages:.4f}")
    print()
    
    print("=" * 80)
    print("WHY IS IT EXPENSIVE?")
    print("=" * 80)
    print()
    print("The system prompt is sent with EVERY message!")
    print()
    print(f"System prompt size: {system_tokens:,} tokens")
    print(f"Cost per message just for system prompt: ${(system_tokens * pricing['input']) / 1000:.4f}")
    print()
    print("This includes:")
    print("  • Agent capabilities and instructions")
    print("  • Tool definitions (query_iam, create_workpaper, store_evidence)")
    print("  • Knowledge base (all audit procedures)")
    print("  • Response format instructions")
    print()
    
    print("=" * 80)
    print("COST REDUCTION OPTIONS")
    print("=" * 80)
    print()
    print("1. REDUCE KNOWLEDGE IN SYSTEM PROMPT")
    print("   • Only include relevant procedures for current task")
    print("   • Load knowledge on-demand instead of upfront")
    print(f"   • Potential savings: ~{knowledge_tokens:,} tokens per message")
    print(f"   • Cost reduction: ~${(knowledge_tokens * pricing['input']) / 1000:.4f} per message")
    print()
    print("2. USE CHEAPER MODEL FOR CHAT")
    print("   • Switch to gpt-4o (50% cheaper) or gpt-3.5-turbo (95% cheaper)")
    print("   • Keep gpt-4-turbo for complex audit tasks")
    print()
    print("3. OPTIMIZE SYSTEM PROMPT")
    print("   • Shorten capability descriptions")
    print("   • Simplify tool definitions")
    print("   • Remove redundant instructions")
    print()
    print("4. USE CONVERSATION CACHING (if available)")
    print("   • Some providers cache system prompts")
    print("   • Reduces cost for repeated system prompt")
    print()


def main():
    """Run the analysis."""
    
    # Check for API key
    if not os.environ.get('OPENAI_API_KEY'):
        print("\n⚠️  OPENAI_API_KEY not set")
        print("   This script doesn't make API calls, but needs the key to create agents")
        print()
        return
    
    analyze_agent_costs("esther")


if __name__ == "__main__":
    main()
