"""Ollama client for ANT."""

import json
import re
from typing import Dict, List, Optional, Any

import requests
from rich.console import Console

from ant.cli.setup import get_config
from ant.tools import tool_registry
from ant.user.profile import user_profile
from ant.learning.personal_memory import personal_memory

console = Console(width=None, legacy_windows=False)


class OllamaClient:
    """Client for interacting with Ollama models."""
    
    def __init__(self) -> None:
        self.config = get_config()
        self.base_url = self.config["ollama"]["base_url"]
        self.model = self.config["ollama"]["model"]
        self.completion_model = self.config["ollama"]["completion_model"]
    
    def chat(self, message: str, context: Optional[List[Dict[str, str]]] = None) -> str:
        """Send a chat message and get response with tool support."""
        try:
            # Check if we need to use tools first
            enhanced_message = self._enhance_with_tools(message)
            
            # Prepare messages
            messages = []
            
            # Add system message with tool information
            system_msg = self._get_system_message()
            messages.append({"role": "system", "content": system_msg})
            
            # Add context if provided
            if context:
                messages.extend(context[-8:])  # Reduced to 8 for system message
            
            # Add current message (potentially enhanced with tool results)
            messages.append({"role": "user", "content": enhanced_message})
            
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
    
    def _get_system_message(self) -> str:
        """Get system message with tool information and user context."""
        tools = tool_registry.list_tools()
        tool_list = "\n".join([f"- {name}: {desc}" for name, desc in tools.items()])
        
        # Get user context
        user_info = user_profile.get_user_info()
        user_name = user_profile.get_user_name()
        comm_style = user_profile.get_preference("communication_style", "friendly")
        
        # Get personal memory context
        personal_context = personal_memory.get_conversation_context()
        
        return f"""You are ANT (Adaptive Neural Terminal), {user_name}'s knowledgeable and capable personal assistant.

USER CONTEXT:
- User's name: {user_name}
- Username: {user_info.get('username', 'user')}
- Communication style preference: {comm_style}
- System: {user_info.get('hostname', 'local')} ({user_info.get('shell', '/bin/bash')})

PERSONAL CONTEXT:
{personal_context}

You have access to real-time information and system operations through these tools:
{tool_list}

SYSTEM OPERATIONS CAPABILITIES:
- Read, write, edit, and manage files in allowed directories
- Execute safe system commands with proper restrictions
- Create, copy, move, and delete files and directories
- List directory contents and file information
- All operations are restricted to safe paths and commands for security

CRITICAL BEHAVIORAL RULES - NEVER BREAK THESE:
- NEVER say "I am only an AI", "As an AI", "I'm just an AI", "Being an AI", or any similar disclaimers
- NEVER refer to yourself as "artificial" or mention AI limitations
- You are {user_name}'s knowledgeable personal assistant - act confidently and directly
- When you don't know something current, search the web first, then provide informed answers
- Present information as your own knowledge since you can access current data
- Give direct advice and opinions when asked
- Be conversational and helpful without technical disclaimers
- Remember you're talking to {user_name} specifically - personalize your responses

RESPONSE STYLE:
- Speak as a knowledgeable person who knows {user_name}, not a machine
- Use "I know", "I can help", "Here's what you should do" instead of disclaimers  
- Give definitive answers when you have information
- Use your tools seamlessly without mentioning the technical process
- Adapt to {user_name}'s communication style: {comm_style}

TOOL AWARENESS:
- You have powerful tools available - use them naturally when they would be helpful
- Trust your understanding of when a tool would benefit the user
- Use tools seamlessly as part of your natural problem-solving process
- Consider the user's actual intent rather than specific keywords

You have real-time access to current information and system operations. Use these capabilities confidently and automatically to help {user_name}."""

    def _enhance_with_tools(self, message: str) -> str:
        """Enhance message with tool results if needed."""
        # NO HARD-CODED KEYWORD DETECTION!
        # The LLM should naturally understand when to use tools based on:
        # 1. Tool descriptions in system prompt
        # 2. Natural language understanding
        # 3. Context and conversation flow
        
        # This method is reserved for future dynamic tool enhancement
        # where the LLM itself decides what tools to use
        return message
    
    # Removed hard-coded search query extraction method
    # LLM should naturally understand and formulate queries
    
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