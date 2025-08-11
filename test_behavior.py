#!/usr/bin/env python3
"""Test ANT's improved behavior without AI disclaimers."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ant.models.ollama_client import OllamaClient

print("🧪 Testing ANT's confident behavior...")

client = OllamaClient()

# Test connection
if not client.is_available():
    print("❌ Ollama not available. Make sure it's running.")
    sys.exit(1)

print("✅ Ollama connection successful!")

# Test confident responses without AI disclaimers
print("\n💪 Testing confident responses...")

test_questions = [
    "What time is it?",
    "What is quantum computing?", 
    "Should I invest in Bitcoin?",
    "How do I become a better programmer?"
]

for question in test_questions:
    print(f"\n❓ Question: {question}")
    response = client.chat(question)
    print(f"🐜 ANT: {response[:200]}...")
    
    # Check for AI disclaimers
    disclaimers = ["i am only an ai", "as an ai", "i'm just an ai", "being an ai"]
    has_disclaimer = any(disclaimer in response.lower() for disclaimer in disclaimers)
    
    if has_disclaimer:
        print("⚠️  Contains AI disclaimer")
    else:
        print("✅ Confident response")

print("\n🎉 Behavior testing complete!")