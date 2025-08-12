"""Response formatting with personality."""

from typing import Dict, Any
from rich.text import Text

from ant.cli.setup import get_config
from ant.user.profile import user_profile


class PersonalityFormatter:
    """Formats AI responses with personality."""
    
    def __init__(self) -> None:
        self.config = get_config()
        self.personality = self.config.get("personality", {})
    
    def format_welcome(self, model_name: str = None) -> str:
        """Format welcome message based on personality."""
        style = self.personality.get("style", "helpful_friend")
        context = user_profile.get_greeting_context()
        
        name = context["name"]
        time_of_day = context["time_of_day"]
        
        # Creative time-based greetings
        greeting_variants = {
            "morning": [
                f"Rise and shine, {name}! ☀️",
                f"Good morning, {name}! ⭐",
                f"Morning, {name}! Ready to crush the day? 💪",
                f"Hey {name}! Hope you've got your coffee ready ☕",
                f"Good morning, {name}! Time to make some magic happen ✨"
            ],
            "afternoon": [
                f"Good afternoon, {name}! 🌤️",
                f"Hey there, {name}! Afternoon productivity time! 📈",
                f"Good afternoon, {name}! How's your day going? 😊",
                f"Afternoon, {name}! Ready to tackle some challenges? 🚀",
                f"Hey {name}! Perfect time for getting things done 🎯"
            ],
            "evening": [
                f"Good evening, {name}! 🌅",
                f"Evening, {name}! Winding down or powering through? 🌙",
                f"Hey {name}! Hope you're having a great evening 🌆",
                f"Good evening, {name}! Time for some focused work? 💻",
                f"Evening, {name}! Let's make the most of these quiet hours 🌃"
            ],
            "night": [
                f"Burning the midnight oil, {name}? 🌙",
                f"Late night coding session, {name}? 👨‍💻",
                f"Hey {name}! Night owl mode activated 🦉",
                f"Working late tonight, {name}? I'm here to help! 🌌",
                f"Hey {name}! Ready for some late-night productivity? 🌃"
            ]
        }
        
        import random
        creative_greeting = random.choice(greeting_variants.get(time_of_day, greeting_variants["morning"]))
        
        # Create model description
        model_desc = ""
        if model_name:
            clean_model = model_name.replace("qwen2.5-coder:", "Qwen2.5-Coder ").replace(":14b", " 14B").replace(":7b", " 7B")
            model_desc = f" powered by {clean_model}"
        
        # Core technologies
        tech_stack = "Ollama • SQLite • Rich CLI"
        
        welcomes = {
            "helpful_friend": f"""
{creative_greeting} I'm ANT, your personal AI assistant{model_desc}.

I'm here to help with coding, answer questions, manage files, or just have a chat. I run locally on your machine using {tech_stack}, so everything stays private. The more we talk, the better I get at understanding what you need!

What would you like to work on today?
""",
            "professional_assistant": f"""
{creative_greeting} I am ANT, your personal AI assistant{model_desc}.

I am designed to assist with development tasks, code analysis, file management, and general inquiries. Built with {tech_stack} for local, private operation. My capabilities improve through our interactions.

How may I assist you today?
""",
            "casual_buddy": f"""
{creative_greeting} ANT here, ready to help out!

Whether you need help with code, want to chat about a project, or need me to handle some files - I'm your AI buddy{model_desc}. Running locally with {tech_stack} to keep things private. I learn as we go, so I'll get better at helping YOU specifically.

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