"""ANT setup and configuration."""

from pathlib import Path
from typing import Any, Dict

import yaml
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt

console = Console()

CONFIG_DIR = Path.home() / ".ant"
CONFIG_FILE = CONFIG_DIR / "config.yaml"
DEFAULT_CONFIG = {
    "ollama": {
        "base_url": "http://localhost:11434",
        "model": "qwen2.5-coder:14b",
        "completion_model": "qwen2.5-coder:7b",
    },
    "personality": {
        "style": "helpful_friend",
        "verbosity": "balanced",
        "formality": "casual",
    },
    "memory": {
        "max_context_messages": 20,
        "auto_save": True,
    },
    "features": {
        "file_operations": True,
        "git_integration": True,
        "code_analysis": True,
    }
}


def run_setup() -> None:
    """Run ANT initial setup."""
    console.print("🚀 Welcome to ANT Setup!", style="bold magenta")
    console.print()
    
    # Create config directory
    CONFIG_DIR.mkdir(exist_ok=True)
    
    # Load existing config or start fresh
    config = load_config() if CONFIG_FILE.exists() else DEFAULT_CONFIG.copy()
    
    # Setup sections
    _setup_ollama(config)
    _setup_personality(config)
    _setup_features(config)
    
    # Save configuration
    save_config(config)
    
    console.print()
    console.print("✅ ANT setup complete!", style="bold green")
    console.print("You can now run 'ant' to start chatting!")


def _setup_ollama(config: Dict[str, Any]) -> None:
    """Setup Ollama configuration."""
    console.print("🤖 Ollama Model Configuration", style="bold blue")
    
    current_url = config["ollama"]["base_url"]
    new_url = Prompt.ask(
        f"Ollama server URL", 
        default=current_url
    )
    config["ollama"]["base_url"] = new_url
    
    current_model = config["ollama"]["model"]
    new_model = Prompt.ask(
        f"Main model for conversations", 
        default=current_model
    )
    config["ollama"]["model"] = new_model
    
    current_completion = config["ollama"]["completion_model"]
    new_completion = Prompt.ask(
        f"Completion model (faster for inline help)", 
        default=current_completion
    )
    config["ollama"]["completion_model"] = new_completion
    
    console.print()


def _setup_personality(config: Dict[str, Any]) -> None:
    """Setup personality preferences."""
    console.print("🎭 Personality Configuration", style="bold blue")
    
    style_options = ["helpful_friend", "professional_assistant", "casual_buddy"]
    current_style = config["personality"]["style"]
    
    console.print("Available personality styles:")
    for i, style in enumerate(style_options, 1):
        marker = "→" if style == current_style else " "
        console.print(f"  {marker} {i}. {style.replace('_', ' ').title()}")
    
    choice = Prompt.ask(
        "Choose personality style (1-3)",
        choices=["1", "2", "3"],
        default="1" if current_style == style_options[0] else 
               ("2" if current_style == style_options[1] else "3")
    )
    config["personality"]["style"] = style_options[int(choice) - 1]
    
    verbosity_options = ["concise", "balanced", "detailed"]
    current_verbosity = config["personality"]["verbosity"]
    
    verbosity_choice = Prompt.ask(
        "Response length preference",
        choices=verbosity_options,
        default=current_verbosity
    )
    config["personality"]["verbosity"] = verbosity_choice
    
    console.print()


def _setup_features(config: Dict[str, Any]) -> None:
    """Setup feature preferences."""
    console.print("🔧 Feature Configuration", style="bold blue")
    
    features = [
        ("file_operations", "File reading and writing"),
        ("git_integration", "Git repository integration"),
        ("code_analysis", "Code analysis and suggestions"),
    ]
    
    for key, description in features:
        current = config["features"].get(key, True)
        enabled = Confirm.ask(f"Enable {description}?", default=current)
        config["features"][key] = enabled
    
    console.print()


def load_config() -> Dict[str, Any]:
    """Load configuration from file."""
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = yaml.safe_load(f)
            
        # Merge with defaults to ensure all keys exist
        merged = DEFAULT_CONFIG.copy()
        merged.update(config)
        return merged
        
    except Exception as e:
        console.print(f"⚠️  Warning: Could not load config: {e}", style="yellow")
        return DEFAULT_CONFIG.copy()


def save_config(config: Dict[str, Any]) -> None:
    """Save configuration to file."""
    try:
        with open(CONFIG_FILE, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, indent=2)
        
        console.print(f"💾 Configuration saved to {CONFIG_FILE}", style="green")
        
    except Exception as e:
        console.print(f"❌ Error saving config: {e}", style="red")


def get_config() -> Dict[str, Any]:
    """Get current configuration."""
    if CONFIG_FILE.exists():
        return load_config()
    return DEFAULT_CONFIG.copy()