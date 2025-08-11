"""ANT CLI main entry point."""

import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from ant.__about__ import __version__
from ant.cli.chat import start_chat_session
from ant.cli.setup import run_setup

console = Console()


def show_banner() -> None:
    """Display ANT banner."""
    banner = Text("🐜 ANT - Adaptive Neural Terminal", style="bold magenta")
    subtitle = Text("Your personal AI assistant that learns with you", style="dim")
    
    panel = Panel.fit(
        Text.assemble(banner, "\n", subtitle),
        border_style="magenta",
        padding=(1, 2)
    )
    console.print(panel)


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
    # TODO: Implement status check
    console.print("📊 ANT Status", style="bold blue")
    console.print("🚧 Status check coming soon!", style="yellow")


if __name__ == "__main__":
    main()