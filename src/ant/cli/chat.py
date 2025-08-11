"""ANT chat session interface."""

from datetime import datetime
from typing import Optional

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.spinner import Spinner

from ant.memory.conversation import ConversationMemory
from ant.models.ollama_client import OllamaClient
from ant.personality.formatter import PersonalityFormatter

console = Console()


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
        
        # Show welcome message
        welcome = self.formatter.format_welcome()
        console.print(Panel(welcome, border_style="green", title="🐜 ANT"))
        
        # Main chat loop
        try:
            while True:
                # Get user input
                user_input = Prompt.ask("\n[bold blue]You[/bold blue]")
                
                if not user_input.strip():
                    continue
                
                # Handle special commands
                if user_input.lower() in ['/quit', '/exit', '/bye']:
                    break
                elif user_input.lower() == '/help':
                    self._show_help()
                    continue
                elif user_input.lower() == '/clear':
                    self.memory.clear_session()
                    console.clear()
                    console.print("🧹 Conversation cleared!", style="green")
                    continue
                elif user_input.lower() == '/status':
                    self._show_status()
                    continue
                
                # Save user message
                self.memory.add_message("user", user_input)
                
                # Get AI response
                response = self._get_ai_response(user_input)
                
                # Format and display response
                formatted_response = self.formatter.format_response(response)
                console.print(f"\n[bold green]🐜 ANT[/bold green]")
                console.print(Panel(Markdown(formatted_response), border_style="green"))
                
                # Save AI response
                self.memory.add_message("assistant", response)
                
        except KeyboardInterrupt:
            console.print("\n👋 Goodbye! Thanks for chatting with ANT!", style="yellow")
        except Exception as e:
            console.print(f"\n❌ Error: {e}", style="red")
        finally:
            # Save conversation
            self.memory.save_session()
    
    def _get_ai_response(self, user_input: str) -> str:
        """Get response from AI model."""
        with console.status("🤔 ANT is thinking...", spinner="dots"):
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
        help_text = """
**ANT Commands:**

• Just type naturally - I'm here to help!
• `/help` - Show this help message
• `/clear` - Clear conversation history  
• `/status` - Show system status
• `/quit` or `/exit` - End conversation

**Tips:**
• I remember our conversation throughout this session
• Ask me about code, files, or anything else
• I can help with development tasks and general questions
"""
        console.print(Panel(Markdown(help_text), title="❓ Help", border_style="blue"))
    
    def _show_status(self) -> None:
        """Show current session status."""
        stats = self.memory.get_session_stats()
        model_info = self.client.get_model_info()
        
        status_text = f"""
**Session Statistics:**
• Messages: {stats.get('message_count', 0)}
• Session started: {stats.get('start_time', 'Unknown')}
• Current model: {model_info.get('name', 'Unknown')}
• Model status: {'✅ Connected' if self.client.is_available() else '❌ Disconnected'}
"""
        console.print(Panel(Markdown(status_text), title="📊 Status", border_style="cyan"))


def start_chat_session() -> None:
    """Start a new chat session."""
    session = ChatSession()
    session.start()