"""ANT CLI main entry point."""

import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import ROUNDED

from ant.__about__ import __version__
from ant.cli.chat import start_chat_session
from ant.cli.setup import run_setup
from ant.user.auth import auth_manager
from ant.user.profile import user_profile

console = Console(width=None, legacy_windows=False)


def show_banner() -> None:
    """Display ANT banner."""
    # Create a boxed banner with the ant emoji and title
    banner_content = "🐜 ANT - Your personal AI assistant that learns with you"
    banner_panel = Panel(
        banner_content,
        box=ROUNDED,
        padding=(0, 1)
    )
    
    console.print()
    console.print(banner_panel)
    console.print()


@click.group(invoke_without_command=True)
@click.option("--setup", is_flag=True, help="Run initial setup")
@click.option("--version", is_flag=True, help="Show version")
@click.pass_context
def main(ctx: click.Context, setup: bool, version: bool) -> None:
    """ANT - Your personal AI assistant that learns and grows with you."""
    
    if version:
        console.print(f"ANT version {__version__}")
        return
    
    if setup:
        run_setup()
        return
    
    # If no subcommand, start chat session
    if ctx.invoked_subcommand is None:
        show_banner()
        start_chat_session()


@main.command()
def chat() -> None:
    """Start a chat session with ANT."""
    show_banner()
    start_chat_session()


@main.command()
@click.argument("message", nargs=-1)
def ask(message: tuple[str, ...]) -> None:
    """Ask ANT a quick question."""
    if not message:
        console.print("❌ Please provide a message to ask", style="red")
        return
    
    question = " ".join(message)
    # TODO: Implement quick ask functionality
    console.print(f"🤔 You asked: {question}")
    console.print("🚧 Quick ask feature coming soon!", style="yellow")


@main.command()
def status() -> None:
    """Show ANT system status."""
    console.print("📊 ANT Status", style="bold blue")
    
    # User info
    user_name = user_profile.get_user_name()
    user_info = user_profile.get_user_info()
    console.print(f"User: {user_name} ({user_info.get('username', 'unknown')})")
    console.print(f"System: {user_info.get('hostname', 'unknown')}")
    
    # Auth status
    services = auth_manager.list_authenticated_services()
    if services:
        console.print(f"Authenticated services: {', '.join(services)}")
    else:
        console.print("No external services authenticated")


@main.command()
@click.argument("service", required=False)
@click.argument("action", required=False)
def auth(service: Optional[str], action: Optional[str]) -> None:
    """Manage authentication for external services."""
    if not service:
        console.print("🔐 ANT Authentication Manager", style="bold blue")
        console.print()
        
        # Show current status
        services = auth_manager.list_authenticated_services()
        if services:
            console.print("✅ Authenticated services:")
            for svc in services:
                console.print(f"  • {svc}")
            console.print()
        
        console.print("Usage:")
        console.print("  ant auth github   - Set up GitHub authentication")
        console.print("  ant auth google   - Set up Google authentication") 
        console.print("  ant auth status   - Show detailed auth status")
        console.print("  ant auth revoke <service> - Revoke service authentication")
        return
    
    if service == "status":
        # Show detailed status
        console.print("🔐 Authentication Status", style="bold blue")
        services = auth_manager.list_authenticated_services()
        
        if not services:
            console.print("No services authenticated")
            return
        
        for svc in services:
            token = auth_manager.get_token(svc)
            console.print(f"\n{svc}:")
            console.print(f"  Status: ✅ Authenticated")
            console.print(f"  Type: {token.get('type', 'unknown')}")
            if 'last_updated' in auth_manager.config.get('auth', {}).get('last_updated', {}):
                console.print(f"  Updated: {auth_manager.config['auth']['last_updated'][svc]}")
        
    elif service == "revoke" and action:
        auth_manager.revoke_service_auth(action)
        
    elif service == "github":
        auth_manager.setup_github_auth()
        
    elif service == "google":
        auth_manager.setup_google_auth()
        
    else:
        console.print(f"❌ Unknown service or command: {service}", style="red")
        console.print("Run 'ant auth' for help")


if __name__ == "__main__":
    main()