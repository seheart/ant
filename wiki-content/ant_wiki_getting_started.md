# Getting Started with ANT

This guide will help you install, set up, and start using ANT in minutes.

## Prerequisites

- **Python 3.9+** (Python 3.12 recommended)
- **Ollama** running locally with a compatible model
- **Git** (for cloning the repository)
- **Linux/macOS/WSL** environment

## Installation

### 1. Install Ollama

First, install Ollama if you haven't already:

```bash
# On Linux/macOS
curl -fsSL https://ollama.ai/install.sh | sh

# On Windows with WSL
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. Download a Model

ANT works best with coding-focused models:

```bash
# Recommended: Qwen2.5-Coder (good balance of performance and speed)
ollama pull qwen2.5-coder:14b

# Alternative: Smaller model for faster responses
ollama pull qwen2.5-coder:7b

# Or use any compatible model
ollama pull llama2:13b
```

### 3. Clone and Install ANT

```bash
# Clone the repository
git clone https://github.com/seheart/ant.git
cd ant

# Install in development mode
pip install -e .
```

### 4. Run Initial Setup

```bash
ant --setup
```

The setup wizard will guide you through:
- Model selection and configuration
- Personality preferences
- User profile setup
- Optional service authentication

## First Run

Start your first chat session:

```bash
ant
```

You'll see a welcome message and can start chatting immediately!

## Basic Usage

### Starting ANT
```bash
ant                    # Start interactive chat
ant chat               # Same as above
ant status             # Check system status
ant --help             # Show all commands
```

### In-Chat Commands
```
/help      - Show help
/status    - Session status
/clear     - Clear history
/wiki      - Open this wiki
/quit      - Exit ANT
```

### Quick Tips
- Just type naturally - ANT understands context
- Use `?` for quick help
- ANT remembers your conversation throughout the session
- Press Ctrl+C to exit anytime

## What's Next?

- Check out the **[Commands Reference](Commands-Reference)** for all available commands
- Set up **[Authentication](Authentication)** for GitHub and other services
- Customize your experience in **[Configuration](Configuration)**
- Having issues? See **[Troubleshooting](Troubleshooting)**

## Verification

Test that everything is working:

```bash
# Check ANT status
ant status

# Start a quick chat
ant
> Hello ANT!
```

You should see a personalized greeting and be able to chat with your AI assistant!

---
**Next: [Commands Reference](Commands-Reference) →**