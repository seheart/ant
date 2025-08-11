#!/usr/bin/env python3
"""Test ANT's enhanced capabilities."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ant.models.ollama_client import OllamaClient

print("🧪 Testing ANT's enhanced capabilities...")

client = OllamaClient()

# Test connection
if not client.is_available():
    print("❌ Ollama not available. Make sure it's running.")
    sys.exit(1)

print("✅ Ollama connection successful!")

# Test time awareness
print("\n⏰ Testing time awareness...")
time_response = client.chat("What time is it right now?")
print(f"🐜 ANT: {time_response[:200]}...")

# Test web search capability  
print("\n🔍 Testing web search...")
search_response = client.chat("What is machine learning?")
print(f"🐜 ANT: {search_response[:300]}...")

# Test news search
print("\n📰 Testing news search...")
news_response = client.chat("Latest news about artificial intelligence")
print(f"🐜 ANT: {news_response[:300]}...")

print("\n🎉 Enhanced ANT testing complete!")