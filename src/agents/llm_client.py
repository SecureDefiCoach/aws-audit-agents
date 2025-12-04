"""
LLM Client - Unified interface for multiple LLM providers.

Supports:
- OpenAI GPT-4 (production)
- Ollama (local development)
- Anthropic Claude (alternative)

Includes rate limiting and cost tracking.
"""

import os
import time
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class LLMResponse:
    """Response from LLM"""
    content: str
    model: str
    tokens_used: int
    cost: float
    timestamp: datetime


class RateLimiter:
    """Rate limiter to control API call frequency"""
    
    def __init__(self, max_calls_per_minute: int = 10):
        self.max_calls = max_calls_per_minute
        self.calls: List[float] = []
    
    def wait_if_needed(self):
        """Pause execution if rate limit reached"""
        now = time.time()
        
        # Remove calls older than 1 minute
        self.calls = [c for c in self.calls if now - c < 60]
        
        if len(self.calls) >= self.max_calls:
            wait_time = 60 - (now - self.calls[0])
            print(f"⏸️  Rate limit reached. Pausing for {wait_time:.0f}s...")
            time.sleep(wait_time)
        
        self.calls.append(now)


class CostTracker:
    """Track LLM API costs"""
    
    def __init__(self):
        self.total_cost = 0.0
        self.total_tokens = 0
        self.call_count = 0
        self.calls: List[Dict] = []
    
    def record_call(self, model: str, tokens: int, cost: float):
        """Record an API call"""
        self.total_cost += cost
        self.total_tokens += tokens
        self.call_count += 1
        
        self.calls.append({
            'timestamp': datetime.now(),
            'model': model,
            'tokens': tokens,
            'cost': cost
        })
    
    def get_summary(self) -> Dict:
        """Get cost summary"""
        return {
            'total_calls': self.call_count,
            'total_tokens': self.total_tokens,
            'total_cost': self.total_cost,
            'avg_cost_per_call': self.total_cost / self.call_count if self.call_count > 0 else 0
        }
    
    def print_summary(self):
        """Print cost summary"""
        summary = self.get_summary()
        print("\n" + "=" * 60)
        print("LLM Cost Summary")
        print("=" * 60)
        print(f"Total API calls: {summary['total_calls']}")
        print(f"Total tokens: {summary['total_tokens']:,}")
        print(f"Total cost: ${summary['total_cost']:.4f}")
        print(f"Avg cost per call: ${summary['avg_cost_per_call']:.4f}")
        print("=" * 60 + "\n")


class LLMClient:
    """Unified LLM client supporting multiple providers"""
    
    # Pricing per 1K tokens (as of 2025)
    PRICING = {
        'gpt-5': {'input': 0.015, 'output': 0.045},  # Estimated pricing
        'gpt-4-turbo': {'input': 0.01, 'output': 0.03},
        'gpt-4o': {'input': 0.005, 'output': 0.015},
        'gpt-3.5-turbo': {'input': 0.0005, 'output': 0.0015},
        'claude-3-haiku': {'input': 0.00025, 'output': 0.00125},
        'ollama': {'input': 0.0, 'output': 0.0}  # Free
    }
    
    def __init__(
        self,
        provider: str = 'openai',
        model: str = 'gpt-5',
        rate_limit: int = 10,
        temperature: float = 0.7
    ):
        """
        Initialize LLM client.
        
        Args:
            provider: 'openai', 'anthropic', or 'ollama'
            model: Model name (e.g., 'gpt-5', 'gpt-4-turbo', 'claude-3-haiku', 'llama3')
            rate_limit: Max API calls per minute
            temperature: Sampling temperature (0.0-1.0)
        """
        self.provider = provider
        self.model = model
        self.temperature = temperature
        
        self.rate_limiter = RateLimiter(rate_limit)
        self.cost_tracker = CostTracker()
        
        # Initialize provider client
        self._init_provider()
    
    def _init_provider(self):
        """Initialize the LLM provider client"""
        if self.provider == 'openai':
            from openai import OpenAI
            api_key = os.environ.get('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable not set")
            self.client = OpenAI(api_key=api_key)
        
        elif self.provider == 'anthropic':
            import anthropic
            api_key = os.environ.get('ANTHROPIC_API_KEY')
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY environment variable not set")
            self.client = anthropic.Anthropic(api_key=api_key)
        
        elif self.provider == 'ollama':
            import ollama
            self.client = ollama.Client()
        
        else:
            raise ValueError(f"Unknown provider: {self.provider}")
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 1000
    ) -> LLMResponse:
        """
        Send chat messages to LLM and get response.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            max_tokens: Maximum tokens in response
        
        Returns:
            LLMResponse with content, model, tokens, and cost
        """
        # Apply rate limiting
        self.rate_limiter.wait_if_needed()
        
        # Call appropriate provider
        if self.provider == 'openai':
            return self._chat_openai(messages, max_tokens)
        elif self.provider == 'anthropic':
            return self._chat_anthropic(messages, max_tokens)
        elif self.provider == 'ollama':
            return self._chat_ollama(messages, max_tokens)
    
    def _chat_openai(self, messages: List[Dict], max_tokens: int) -> LLMResponse:
        """Chat with OpenAI GPT models"""
        # GPT-5 uses max_completion_tokens and doesn't support custom temperature
        if self.model.startswith('gpt-5'):
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_completion_tokens=max_tokens
                # GPT-5 only supports temperature=1 (default)
            )
        else:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=self.temperature
            )
        
        # Extract response
        content = response.choices[0].message.content
        tokens = response.usage.total_tokens
        
        # Calculate cost
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        
        pricing = self.PRICING.get(self.model, self.PRICING['gpt-5'])
        cost = (input_tokens * pricing['input'] / 1000) + \
               (output_tokens * pricing['output'] / 1000)
        
        # Track cost
        self.cost_tracker.record_call(self.model, tokens, cost)
        
        return LLMResponse(
            content=content,
            model=response.model,
            tokens_used=tokens,
            cost=cost,
            timestamp=datetime.now()
        )
    
    def _chat_anthropic(self, messages: List[Dict], max_tokens: int) -> LLMResponse:
        """Chat with Anthropic Claude models"""
        # Convert messages format (Claude uses different format)
        system_msg = None
        claude_messages = []
        
        for msg in messages:
            if msg['role'] == 'system':
                system_msg = msg['content']
            else:
                claude_messages.append({
                    'role': msg['role'],
                    'content': msg['content']
                })
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=self.temperature,
            system=system_msg,
            messages=claude_messages
        )
        
        # Extract response
        content = response.content[0].text
        tokens = response.usage.input_tokens + response.usage.output_tokens
        
        # Calculate cost
        pricing = self.PRICING.get(self.model, self.PRICING['claude-3-haiku'])
        cost = (response.usage.input_tokens * pricing['input'] / 1000) + \
               (response.usage.output_tokens * pricing['output'] / 1000)
        
        # Track cost
        self.cost_tracker.record_call(self.model, tokens, cost)
        
        return LLMResponse(
            content=content,
            model=self.model,
            tokens_used=tokens,
            cost=cost,
            timestamp=datetime.now()
        )
    
    def _chat_ollama(self, messages: List[Dict], max_tokens: int) -> LLMResponse:
        """Chat with Ollama local models"""
        response = self.client.chat(
            model=self.model,
            messages=messages
        )
        
        content = response['message']['content']
        
        # Ollama doesn't provide token counts, estimate
        tokens = len(content.split()) * 1.3  # Rough estimate
        
        return LLMResponse(
            content=content,
            model=self.model,
            tokens_used=int(tokens),
            cost=0.0,  # Free
            timestamp=datetime.now()
        )
    
    def get_cost_summary(self) -> Dict:
        """Get cost tracking summary"""
        return self.cost_tracker.get_summary()
    
    def print_cost_summary(self):
        """Print cost summary"""
        self.cost_tracker.print_summary()
