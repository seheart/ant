"""Ollama client for ANT."""

import json
from typing import Dict, List, Optional, Any

import requests
from rich.console import Console

from ant.cli.setup import get_config

console = Console()


class OllamaClient:
    """Client for interacting with Ollama models."""
    
    def __init__(self) -> None:
        self.config = get_config()
        self.base_url = self.config["ollama"]["base_url"]
        self.model = self.config["ollama"]["model"]
        self.completion_model = self.config["ollama"]["completion_model"]
    
    def chat(self, message: str, context: Optional[List[Dict[str, str]]] = None) -> str:
        """Send a chat message and get response."""
        try:
            # Prepare messages
            messages = []
            
            # Add context if provided
            if context:
                messages.extend(context[-10:])  # Last 10 messages for context
            
            # Add current message
            messages.append({"role": "user", "content": message})
            
            # Make request to Ollama
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                    }
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("message", {}).get("content", "No response received.")
            else:
                return f"Error: Received status code {response.status_code}"
                
        except requests.exceptions.ConnectionError:
            return "❌ Cannot connect to Ollama. Make sure it's running on http://localhost:11434"
        except requests.exceptions.Timeout:
            return "⏰ Request timed out. The model might be loading or overloaded."
        except Exception as e:
            return f"❌ Unexpected error: {str(e)}"
    
    def is_available(self) -> bool:
        """Check if Ollama is available."""
        try:
            response = requests.get(f"{self.base_url}/api/version", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model."""
        try:
            response = requests.get(f"{self.base_url}/api/show", 
                                    json={"name": self.model}, timeout=10)
            if response.status_code == 200:
                return response.json()
        except:
            pass
        
        return {
            "name": self.model,
            "status": "Unknown"
        }
    
    def list_models(self) -> List[Dict[str, Any]]:
        """List available models."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            if response.status_code == 200:
                return response.json().get("models", [])
        except:
            pass
        
        return []