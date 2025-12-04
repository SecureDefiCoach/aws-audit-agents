#!/usr/bin/env python3
"""Test different prompt formats to get GPT-5 working."""

import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

print("Testing different GPT-5 prompt formats...\n")

# Test 1: Simple direct question
print("=" * 80)
print("Test 1: Simple direct question")
print("=" * 80)
try:
    response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "user", "content": "List 3 IAM risks in AWS."}
        ],
        max_completion_tokens=1000
    )
    print(f"Response: {response.choices[0].message.content}")
    print(f"Tokens: {response.usage.total_tokens}")
except Exception as e:
    print(f"Error: {e}")

# Test 2: Structured format
print("\n" + "=" * 80)
print("Test 2: Structured format with explicit instructions")
print("=" * 80)
try:
    response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "user", "content": """Task: Identify IAM security risks

Instructions:
1. List exactly 3 risks
2. Be specific
3. Use bullet points

Begin:"""}
        ],
        max_completion_tokens=1000
    )
    print(f"Response: {response.choices[0].message.content}")
    print(f"Tokens: {response.usage.total_tokens}")
except Exception as e:
    print(f"Error: {e}")

# Test 3: Role-based with clear output format
print("\n" + "=" * 80)
print("Test 3: Role-based with output format")
print("=" * 80)
try:
    response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "user", "content": """You are a senior AWS auditor.

Question: What are the top 3 IAM security risks?

Format your response as:
Risk 1: [description]
Risk 2: [description]
Risk 3: [description]"""}
        ],
        max_completion_tokens=1000
    )
    print(f"Response: {response.choices[0].message.content}")
    print(f"Tokens: {response.usage.total_tokens}")
except Exception as e:
    print(f"Error: {e}")

# Test 4: Conversational
print("\n" + "=" * 80)
print("Test 4: Conversational style")
print("=" * 80)
try:
    response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "user", "content": "Hi! I need help with AWS IAM security."},
            {"role": "assistant", "content": "I'd be happy to help with AWS IAM security. What would you like to know?"},
            {"role": "user", "content": "What are the 3 most critical risks I should look for?"}
        ],
        max_completion_tokens=1000
    )
    print(f"Response: {response.choices[0].message.content}")
    print(f"Tokens: {response.usage.total_tokens}")
except Exception as e:
    print(f"Error: {e}")

# Test 5: JSON format request
print("\n" + "=" * 80)
print("Test 5: JSON format request")
print("=" * 80)
try:
    response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "user", "content": """Provide 3 IAM risks in JSON format:
{
  "risks": [
    {"name": "...", "description": "..."},
    {"name": "...", "description": "..."},
    {"name": "...", "description": "..."}
  ]
}"""}
        ],
        max_completion_tokens=1000
    )
    print(f"Response: {response.choices[0].message.content}")
    print(f"Tokens: {response.usage.total_tokens}")
except Exception as e:
    print(f"Error: {e}")

# Test 6: Very short response
print("\n" + "=" * 80)
print("Test 6: Request very short response")
print("=" * 80)
try:
    response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "user", "content": "Name 1 IAM risk. One sentence only."}
        ],
        max_completion_tokens=50
    )
    print(f"Response: {response.choices[0].message.content}")
    print(f"Tokens: {response.usage.total_tokens}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 80)
print("Testing complete!")
print("=" * 80)
