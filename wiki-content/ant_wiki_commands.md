# Commands Reference

Complete reference for all ANT commands and features.

## Command Line Interface

### Basic Commands

| Command | Description | Example |
|---------|-------------|---------|
| `ant` | Start interactive chat session | `ant` |
| `ant chat` | Same as above | `ant chat` |
| `ant ask "question"` | Quick question mode *(coming soon)* | `ant ask "What time is it?"` |
| `ant status` | Show system and user status | `ant status` |
| `ant --setup` | Run setup wizard | `ant --setup` |
| `ant --version` | Show ANT version | `ant --version` |
| `ant --help` | Show help message | `ant --help` |

### Authentication Commands

| Command | Description | Example |
|---------|-------------|---------|
| `ant auth` | Show authentication manager | `ant auth` |
| `ant auth github` | Set up GitHub integration | `ant auth github` |
| `ant auth google` | Set up Google integration | `ant auth google` |
| `ant auth status` | Show detailed auth status | `ant auth status` |
| `ant auth revoke <service>` | Remove service authentication | `ant auth revoke github` |

## Chat Session Commands

When you're in an interactive chat with ANT, use these commands:

### Help and Information

| Command | Shortcut | Description |
|---------|----------|-------------|
| `/help` | `?` | Show help information |
| `/status` | - | Show current session statistics |
| `/wiki` | - | Open ANT wiki in browser |

### Session Management

| Command | Description |
|---------|-------------|
| `/clear` | Clear conversation history |
| `/quit` | Exit ANT chat session |
| `/exit` | Same as `/quit` |
| `/bye` | Same as `/quit` |

### Special Features

- **Empty input + Enter**: Shows help hint (`? for help`)
- **Ctrl+C**: Quick exit from chat session
- **Natural language**: Just type normally, ANT understands context

## Built-in Tools

ANT automatically uses these tools when relevant:

### DateTime Tools
- Current time and date queries
- Timezone information
- Time-based responses and greetings

### Web Search Tools
- Real-time web search via DuckDuckGo
- News and current information lookup
- Automatic fact checking

### GitHub Tools *(requires authentication)*
- Repository listing and information
- User profile data
- Issue tracking and management

## Command Examples

### Getting Started
```bash
# First time setup
ant --setup

# Check everything is working
ant status

# Start chatting
ant
> Hello ANT!
> What's the current time?
> Can you search for Python tutorials?
```

### Authentication Flow
```bash
# Set up GitHub integration
ant auth github
# Follow prompts to enter token or complete OAuth

# Verify authentication
ant auth status

# Use in chat
ant
> Show me my GitHub repositories
> What issues are open in my ant project?
```

### Daily Usage
```bash
# Quick status check
ant status

# Start productive session
ant
> Let's work on my Python project
> Can you help me debug this code?
> What's the best practice for error handling?
```

## Configuration Commands

While ANT doesn't have dedicated config commands, you can:

1. **Re-run setup**: `ant --setup` to change preferences
2. **Edit config file**: `~/.ant/config.yaml` for advanced settings
3. **Reset completely**: Delete `~/.ant/` folder and run setup again

## Error Handling

If commands fail:

1. **Check Ollama**: `ollama list` to verify models
2. **Check status**: `ant status` for system info
3. **Reset auth**: `ant auth revoke <service>` then re-authenticate
4. **Clear data**: Delete `~/.ant/` and run `ant --setup`

## Environment Variables

Override defaults with environment variables:

```bash
export ANT_CONFIG_DIR="~/.config/ant"  # Change config location
export ANT_OLLAMA_URL="http://localhost:11434"  # Ollama URL
export ANT_MODEL="llama2:13b"  # Default model
```

## Integration with Other Tools

### Shell Integration
```bash
# Add to your shell profile for quick access
alias a="ant"
alias chat="ant chat"
alias askant="ant ask"
```

### IDE Integration
ANT works great alongside your favorite editor:
- Use ANT for research and problem-solving
- Get code explanations and examples
- Debug issues in real-time

---
**← [Getting Started](Getting-Started) | [Authentication](Authentication) →**