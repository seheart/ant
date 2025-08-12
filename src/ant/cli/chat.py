"""ANT chat session interface."""

import webbrowser
from datetime import datetime
from typing import Optional

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.spinner import Spinner
from rich.text import Text
from rich.box import ROUNDED

from ant.memory.conversation import ConversationMemory
from ant.models.ollama_client import OllamaClient
from ant.personality.formatter import PersonalityFormatter

console = Console(width=None, legacy_windows=False)


class ChatSession:
    """Main chat session handler."""
    
    def __init__(self) -> None:
        self.memory = ConversationMemory()
        self.client = OllamaClient()
        self.formatter = PersonalityFormatter()
        self.session_id = datetime.now().isoformat()
    
    def start(self) -> None:
        """Start the interactive chat session."""
        console.print("💬 Starting chat session...", style="dim")
        
        # Load conversation history
        self.memory.load_session(self.session_id)
        
        # Show welcome message with integrated model info
        model_info = self.client.get_model_info()
        model_name = model_info.get('name', self.client.model)
        welcome = self.formatter.format_welcome(model_name)
        
        console.print(welcome.strip())
        console.print()
        
        # Main chat loop
        try:
            while True:
                # Show clean input prompt like Claude Code
                console.print()
                
                # Simple prompt like Claude Code 
                console.print("> ", end="")
                user_input = input()
                
                if not user_input.strip():
                    console.print("[dim]? for help[/dim]")
                    continue
                
                # Don't duplicate user input - they already see what they typed
                
                # Handle special commands
                if user_input.lower() in ['/quit', '/exit', '/bye']:
                    break
                elif user_input.lower() in ['/help', '?']:
                    self._show_help()
                    continue
                elif user_input.lower() == '/clear':
                    self.memory.clear_session()
                    console.clear()
                    console.print("[dim]Conversation cleared[/dim]")
                    continue
                elif user_input.lower() in ['/cls', '/clear-terminal']:
                    import os
                    os.system('clear' if os.name == 'posix' else 'cls')
                    # Show banner again after clearing
                    from ant.cli.main import show_banner
                    show_banner()
                    console.print("💬 Starting chat session...")
                    continue
                elif user_input.lower() == '/status':
                    self._show_status()
                    continue
                elif user_input.lower() == '/wiki':
                    self._open_wiki()
                    continue
                
                # Save user message
                self.memory.add_message("user", user_input)
                
                # Get AI response
                response = self._get_ai_response(user_input)
                
                # Format and display response with dot like Claude Code
                formatted_response = self.formatter.format_response(response)
                console.print(f"\n[dim]●[/dim] ", end="")
                console.print(Markdown(formatted_response))
                
                # Save AI response
                self.memory.add_message("assistant", response)
                
        except KeyboardInterrupt:
            console.print("\nGoodbye!", style="dim")
        except Exception as e:
            console.print(f"\nError: {e}", style="red")
        finally:
            # Save conversation
            self.memory.save_session()
    
    def _get_ai_response(self, user_input: str) -> str:
        """Get response from AI model."""
        with console.status("[dim]Thinking...[/dim]", spinner="dots"):
            try:
                # Get conversation context
                context = self.memory.get_context_messages()
                
                # Get response from model
                response = self.client.chat(user_input, context)
                return response
                
            except Exception as e:
                return f"Sorry, I encountered an error: {e}. Please try again!"
    
    def _show_help(self) -> None:
        """Show help information."""
        help_text = """**ANT Commands:**

• Just type naturally - I'm here to help!
• `?` or `/help` - Show this help message
• `/clear` - Clear conversation history  
• `/cls` or `/clear-terminal` - Clear screen and restart fresh
• `/status` - Show system status
• `/quit` or `/exit` - End conversation
• `/wiki` - Open full documentation in web browser

**Tips:**
• I remember our conversation throughout this session
• Ask me about code, files, or anything else
• I can help with development tasks and general questions
"""
        console.print()
        console.print(Markdown(help_text))
    
    def _show_status(self) -> None:
        """Show current session status."""
        stats = self.memory.get_session_stats()
        model_info = self.client.get_model_info()
        
        status_text = f"""**Session Statistics:**
• Messages: {stats.get('message_count', 0)}
• Session started: {stats.get('start_time', 'Unknown')}
• Current model: {model_info.get('name', 'Unknown')}
• Model status: {'Connected' if self.client.is_available() else 'Disconnected'}
"""
        console.print()
        console.print(Markdown(status_text))
    
    def _open_wiki(self) -> None:
        """Open ANT documentation wiki in web browser."""
        wiki_url = "https://github.com/seheart/ant/wiki"
        console.print()
        console.print(f"[dim]Opening ANT documentation at {wiki_url}...[/dim]")
        try:
            webbrowser.open(wiki_url)
            console.print("[dim]Documentation opened in your default browser[/dim]")
        except Exception as e:
            console.print(f"[red]Could not open browser: {e}[/red]")
            console.print(f"[dim]Please visit manually: {wiki_url}[/dim]")


def start_chat_session() -> None:
    """Start a new chat session."""
    session = ChatSession()
    session.start()