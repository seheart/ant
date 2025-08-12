# 🐜 ANT User Guide

> Your personal AI assistant that learns and grows with you

## Quick Start

```bash
# Install ANT
cd /path/to/ant
pip install -e .

# First-time setup
ant --setup

# Start chatting
ant
```

## Commands Overview

### Basic Commands
```bash
ant                    # Start interactive chat session
ant chat               # Same as above
ant ask "question"     # Quick question (coming soon)
ant status             # Show system status
ant --setup            # Run setup wizard
ant --version          # Show version
```

### Authentication
```bash
ant auth               # Show authentication manager
ant auth github        # Set up GitHub integration
ant auth google        # Set up Google integration  
ant auth status        # Show detailed auth status
ant auth revoke <service>  # Remove service authentication
```

## Chat Session Commands

Once you're in a chat session with ANT, you can use these special commands:

```
/help      - Show help information
/clear     - Clear conversation history
/status    - Show current session status
/quit      - End conversation (or Ctrl+C)
/exit      - Same as quit
/bye       - Same as quit
```

## Configuration

ANT stores its configuration in `~/.ant/`:

```
~/.ant/
├── config.yaml         # Main configuration
└── conversations.db    # Chat history database
```

### Configuration File Structure

```yaml
# Ollama Model Settings
ollama:
  base_url: "http://localhost:11434"
  model: "qwen2.5-coder:14b"
  completion_model: "qwen2.5-coder:7b"

# Personality Settings
personality:
  style: "helpful_friend"        # helpful_friend, professional_assistant, casual_buddy
  verbosity: "balanced"          # concise, balanced, detailed
  formality: "casual"            # casual, formal

# Memory Settings
memory:
  max_context_messages: 20
  auto_save: true

# Feature Toggles
features:
  file_operations: true
  git_integration: true
  code_analysis: true

# User Profile (auto-detected)
user:
  username: "seth"
  full_name: "Seth"
  nickname: "Seth"
  # ... other system info

# Authentication (managed via 'ant auth' commands)
auth:
  tokens: {}
  last_updated: {}
```

## GitHub Integration

ANT can integrate with your GitHub account for repository management and issue tracking.

### Setup GitHub Authentication

```bash
ant auth github
```

Choose between:
1. **Personal Access Token** (recommended for simplicity)
   - Go to https://github.com/settings/tokens
   - Create token with `repo`, `user`, `gist` scopes
   - Enter token when prompted

2. **OAuth Flow** (coming soon)

### GitHub Capabilities

Once authenticated, ANT can:
- Show your GitHub profile info
- List your repositories
- Get repository details and issues
- Access repository information in conversations

Example conversations:
```
You: "Show me my recent repositories"
ANT: [Lists your GitHub repos with details]

You: "What issues are open in my ant project?"
ANT: [Shows open issues from your ant repository]
```

## Google Integration

Basic Google OAuth setup is available for future features.

```bash
ant auth google
```

Currently requires Google Cloud Console setup with OAuth credentials.

## Personality Customization

ANT has three personality modes:

### 1. Helpful Friend (default)
- Friendly and conversational
- Uses casual language
- Encouraging and supportive

### 2. Professional Assistant  
- More formal tone
- Business-like interactions
- Structured responses

### 3. Casual Buddy
- Very informal and relaxed
- Uses slang and emojis
- Playful interactions

Change personality during setup:
```bash
ant --setup
```

## Memory and Context

ANT remembers:
- **Conversation history** - Your chat sessions are saved
- **User preferences** - Communication style, settings
- **System context** - Your username, hostname, shell
- **Authentication** - Connected services and tokens

Memory is stored locally in SQLite database at `~/.ant/conversations.db`.

## Available Tools

ANT has built-in tools that work automatically in conversations:

### DateTime Tools
- Current time and date
- Timezone information
- Time-based responses

### Web Search Tools  
- DuckDuckGo search integration
- News search capabilities
- Real-time information lookup

### GitHub Tools (when authenticated)
- User profile information
- Repository listing and details
- Issue tracking and management

## Tips and Best Practices

### Getting Better Results
1. **Be specific** - ANT works better with clear requests
2. **Use context** - Reference previous conversations
3. **Try different phrasings** - ANT learns from variety
4. **Use tools** - Ask for current information, GitHub data, etc.

### Privacy and Security
- **Local-first** - All conversations stored locally
- **No data sharing** - Your data never leaves your machine
- **Token security** - External service tokens stored securely
- **User control** - You control all authentication and data

### Troubleshooting

#### ANT won't start
```bash
# Check if Ollama is running
curl http://localhost:11434/api/version

# Check if model is available
ollama list

# Reinstall ANT
pip install -e . --force-reinstall
```

#### Authentication issues
```bash
# Check auth status
ant auth status

# Re-authenticate
ant auth revoke github
ant auth github
```

#### Memory issues
```bash
# Clear conversation history
ant
> /clear
```

#### Configuration problems
```bash
# Reset configuration
rm -rf ~/.ant/
ant --setup
```

## Advanced Usage

### Custom Model Configuration

Edit `~/.ant/config.yaml` to use different models:

```yaml
ollama:
  base_url: "http://localhost:11434"
  model: "llama2:13b"           # Change main model
  completion_model: "llama2:7b" # Change completion model
```

### Environment Variables

ANT respects these environment variables:
- `ANT_CONFIG_DIR` - Override config directory (default: `~/.ant`)
- `ANT_OLLAMA_URL` - Override Ollama URL
- `ANT_MODEL` - Override default model

## Development and Learning

ANT is designed to learn and improve with use:

### Current Capabilities (Phase 1)
- ✅ Conversation memory and context
- ✅ User profile and personalization  
- ✅ External service integration
- ✅ Web search and real-time data
- ✅ GitHub repository management

### Planned Features
- **Phase 2**: File operations, Git integration, Code analysis
- **Phase 3**: Learning pipeline, User feedback collection
- **Phase 4**: Personal model fine-tuning
- **Phase 5**: Advanced reasoning, Multi-modal support

## Getting Help

### In-Chat Help
```
ant
> /help
```

### Command Help
```bash
ant --help
ant auth --help
```

### Community and Support
- **Issues**: Report bugs and feature requests
- **Documentation**: This guide and inline help
- **Code**: Explore the source code for deeper understanding

## FAQ

**Q: Does ANT work offline?**
A: Mostly yes. Chat works offline with local Ollama models. Web search and GitHub features require internet.

**Q: Can I use different AI models?**  
A: Yes! ANT works with any Ollama-compatible model. Configure in settings.

**Q: Is my data private?**
A: Completely. Everything runs locally. External services only accessed with your explicit authentication.

**Q: How do I reset ANT?**
A: Delete `~/.ant/` directory and run `ant --setup` to start fresh.

**Q: Can I backup my conversations?**
A: Yes, backup `~/.ant/conversations.db` to preserve chat history.

**Q: Why qwen2.5-coder as default?**
A: It's optimized for development tasks and works well on most systems. You can change it anytime.

---

**Built with ❤️ for developers who want AI that truly understands them.**