#!/usr/bin/env python3
"""Quick setup script for ANT."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ant.cli.setup import save_config, DEFAULT_CONFIG

# Configure for your system
config = DEFAULT_CONFIG.copy()
config["ollama"]["model"] = "qwen2.5-coder:14b"
config["ollama"]["completion_model"] = "qwen2.5-coder:7b"
config["personality"]["style"] = "helpful_friend"

# Save configuration
save_config(config)

print("✅ ANT configured successfully!")
print("🚀 Ready to start chatting!")
print("\nRun: PYTHONPATH=src python -m ant.cli.main")