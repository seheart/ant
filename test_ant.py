#!/usr/bin/env python3
"""Test ANT connection to Ollama."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ant.models.ollama_client import OllamaClient

print("🧪 Testing ANT connection to Ollama...")

client = OllamaClient()

# Test connection
if client.is_available():
    print("✅ Ollama connection successful!")
    
    # Test model info
    model_info = client.get_model_info()
    print(f"📊 Model: {model_info.get('name', 'Unknown')}")
    
    # Test simple chat
    print("🤖 Testing chat response...")
    response = client.chat("Hello! Can you tell me what you are?")
    print(f"🐜 ANT: {response[:100]}...")
    
    print("\n🎉 ANT is ready to use!")
    print("To start chatting: PYTHONPATH=src python -m ant.cli.main")
    
else:
    print("❌ Cannot connect to Ollama")
    print("Make sure Ollama is running: ollama serve")