"""Response formatting with personality."""

from typing import Dict, Any
from rich.text import Text

from ant.cli.setup import get_config


class PersonalityFormatter:
    """Formats AI responses with personality."""
    
    def __init__(self) -> None:
        self.config = get_config()
        self.personality = self.config.get("personality", {})
    
    def format_welcome(self) -> str:
        """Format welcome message based on personality."""
        style = self.personality.get("style", "helpful_friend")
        
        welcomes = {
            "helpful_friend": """
Hey there! 👋 I'm ANT, your personal AI assistant.

I'm here to help with coding, answer questions, manage files, or just have a chat. The more we talk, the better I get at understanding what you need!

What would you like to work on today?
""",
            "professional_assistant": """
Good day! I am ANT, your personal AI assistant.

I am designed to assist with development tasks, code analysis, file management, and general inquiries. My capabilities improve through our interactions.

How may I assist you today?
""",
            "casual_buddy": """
Hey! 🐜 ANT here, ready to help out!

Whether you need help with code, want to chat about a project, or need me to handle some files - I'm your AI buddy. I learn as we go, so I'll get better at helping YOU specifically.

What's up?
"""
        }
        
        return welcomes.get(style, welcomes["helpful_friend"])
    
    def format_response(self, response: str) -> str:
        """Format AI response based on personality settings."""
        verbosity = self.personality.get("verbosity", "balanced")
        formality = self.personality.get("formality", "casual")
        
        # For now, return as-is, but this is where we'd add
        # post-processing based on personality settings
        return response
    
    def format_error(self, error_message: str) -> str:
        """Format error messages consistently."""
        style = self.personality.get("style", "helpful_friend")
        
        if style == "professional_assistant":
            return f"I apologize, but I encountered an issue: {error_message}"
        elif style == "casual_buddy":
            return f"Oops! Hit a snag: {error_message}"
        else:
            return f"Sorry about that! I ran into an issue: {error_message}"
    
    def format_thinking(self) -> str:
        """Get thinking message based on personality."""
        style = self.personality.get("style", "helpful_friend")
        
        thinking_msgs = {
            "helpful_friend": "🤔 Let me think about that...",
            "professional_assistant": "⏳ Processing your request...",
            "casual_buddy": "🧠 Thinking... give me a sec!"
        }
        
        return thinking_msgs.get(style, thinking_msgs["helpful_friend"])