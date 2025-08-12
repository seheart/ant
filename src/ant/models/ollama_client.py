"""Ollama client for ANT."""

import json
import re
from typing import Dict, List, Optional, Any

import requests
from rich.console import Console

from ant.cli.setup import get_config
from ant.tools import tool_registry
from ant.user.profile import user_profile

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
        
        return f"""You are ANT (Adaptive Neural Terminal), {user_name}'s knowledgeable and capable personal assistant.

USER CONTEXT:
- User's name: {user_name}
- Username: {user_info.get('username', 'user')}
- Communication style preference: {comm_style}
- System: {user_info.get('hostname', 'local')} ({user_info.get('shell', '/bin/bash')})

You have access to real-time information through these tools:
{tool_list}

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

You have real-time access to current information. Use these capabilities confidently to help {user_name}."""

    def _enhance_with_tools(self, message: str) -> str:
        """Enhance message with tool results if needed."""
        enhanced = message
        
        # Check for time-related queries
        time_keywords = ["time", "date", "today", "now", "current", "what day"]
        if any(keyword in message.lower() for keyword in time_keywords):
            try:
                time_info = tool_registry.call_tool("get_current_time")
                enhanced = f"{message}\n\nCurrent time: {time_info['current_time']} on {time_info['current_date']}"
            except Exception as e:
                console.print(f"[yellow]Warning: Could not get time info: {e}[/yellow]")
        
        # Check for web search needs
        search_indicators = ["search", "look up", "find information about", "what is", "who is", "latest news", "current events"]
        knowledge_questions = ["what is", "who is", "how does", "explain", "define"]
        
        if any(indicator in message.lower() for indicator in search_indicators):
            try:
                # Extract search query from message
                search_query = self._extract_search_query(message)
                if search_query:
                    search_results = tool_registry.call_tool("search_web", query=search_query)
                    enhanced = f"{message}\n\nWeb search results: {search_results}"
            except Exception as e:
                console.print(f"[yellow]Warning: Web search failed: {e}[/yellow]")
        
        # Check for news-specific queries
        if "news" in message.lower() or "latest" in message.lower():
            try:
                search_query = self._extract_search_query(message)
                if search_query:
                    news_results = tool_registry.call_tool("search_news", query=search_query)
                    enhanced = f"{message}\n\nLatest news: {news_results}"
            except Exception as e:
                console.print(f"[yellow]Warning: News search failed: {e}[/yellow]")
            
        return enhanced
    
    def _extract_search_query(self, message: str) -> Optional[str]:
        """Extract search query from user message."""
        message_lower = message.lower()
        
        # Common patterns to extract search terms
        patterns = [
            r"search for (.+)",
            r"look up (.+)", 
            r"find information about (.+)",
            r"what is (.+)",
            r"who is (.+)",
            r"explain (.+)",
            r"define (.+)",
            r"latest news about (.+)",
            r"news about (.+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message_lower)
            if match:
                return match.group(1).strip()
        
        # If no pattern matches, use the whole message but clean it up
        # Remove common question words
        stop_words = ["what", "who", "how", "when", "where", "why", "is", "are", "the", "a", "an"]
        words = message.split()
        filtered_words = [word for word in words if word.lower() not in stop_words]
        
        if len(filtered_words) >= 2:  # Need at least 2 meaningful words
            return " ".join(filtered_words[:5])  # Limit to 5 words
        
        return None
    
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