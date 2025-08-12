# Configuration

Customize ANT to match your preferences and workflow. All configuration is stored in `~/.ant/config.yaml`.

## Configuration File Location

```
~/.ant/
├── config.yaml         # Main configuration file
└── conversations.db    # Chat history database
```

## Configuration Structure

### Full Configuration Example

```yaml
# Ollama Model Settings
ollama:
  base_url: "http://localhost:11434"
  model: "qwen2.5-coder:14b"
  completion_model: "qwen2.5-coder:7b"

# Personality and Interaction Style
personality:
  style: "helpful_friend"        # helpful_friend, professional_assistant, casual_buddy
  verbosity: "balanced"          # concise, balanced, detailed
  formality: "casual"            # casual, formal

# Memory and Context Management
memory:
  max_context_messages: 20       # Messages to remember in conversations
  auto_save: true               # Automatically save chat history

# Feature Toggles
features:
  file_operations: true         # Enable file management tools
  git_integration: true         # Enable git-related features
  code_analysis: true          # Enable code analysis capabilities

# User Profile (auto-detected but customizable)
user:
  username: "seth"
  full_name: "Seth"
  nickname: "Seth"
  hostname: "Ubuntu"
  shell: "/bin/bash"
  timezone: "America/New_York"
  preferences:
    code_style: "auto"
    communication_style: "friendly"
    detail_level: "balanced"

# External Service Authentication
auth:
  tokens:
    github:
      type: "personal_access_token"
      token: "ghp_xxxxxxxxxxxx"
    google:
      type: "oauth"
      client_id: "your-client-id"
      client_secret: "your-client-secret"
  last_updated:
    github: "2025-08-12T10:30:00Z"
    google: "2025-08-12T10:30:00Z"
```

## Personality Customization

ANT offers three distinct personality modes:

### 1. Helpful Friend (Default)
```yaml
personality:
  style: "helpful_friend"
  verbosity: "balanced"
  formality: "casual"
```

**Characteristics:**
- Friendly and conversational tone
- Uses encouraging language
- Casual but professional responses
- Balanced level of detail

### 2. Professional Assistant
```yaml
personality:
  style: "professional_assistant"
  verbosity: "detailed"
  formality: "formal"
```

**Characteristics:**
- Formal, business-like tone
- Structured and detailed responses
- Professional language usage
- Comprehensive explanations

### 3. Casual Buddy
```yaml
personality:
  style: "casual_buddy"
  verbosity: "concise"
  formality: "casual"
```

**Characteristics:**
- Very informal and relaxed
- Uses slang and emojis freely
- Brief, to-the-point responses
- Playful interaction style

## Model Configuration

### Changing Models

```yaml
ollama:
  base_url: "http://localhost:11434"
  model: "llama2:13b"              # Main conversation model
  completion_model: "llama2:7b"    # Faster model for simple tasks
```

**Popular Model Options:**
- `qwen2.5-coder:14b` - Best for coding (recommended)
- `qwen2.5-coder:7b` - Faster coding model
- `llama2:13b` - General purpose, good reasoning
- `llama2:7b` - Faster general purpose
- `mistral:7b` - Efficient and capable
- `codellama:13b` - Specialized for code

### Remote Ollama Setup

```yaml
ollama:
  base_url: "http://remote-server:11434"  # Remote Ollama instance
  model: "qwen2.5-coder:14b"
  completion_model: "qwen2.5-coder:7b"
```

## Memory Settings

### Conversation Memory

```yaml
memory:
  max_context_messages: 20    # Number of messages to remember
  auto_save: true            # Save conversations automatically
  context_window: 4096       # Model context window size
```

**Guidelines:**
- **Small context (10-15)**: Faster responses, less memory usage
- **Medium context (20-30)**: Balanced performance (recommended)
- **Large context (40+)**: Better continuity, slower responses

## User Profile Customization

### Communication Preferences

```yaml
user:
  preferences:
    communication_style: "friendly"     # friendly, professional, technical
    detail_level: "balanced"           # brief, balanced, detailed
    code_style: "pythonic"            # pythonic, verbose, minimal
    help_style: "examples"            # examples, theory, both
```

### Personal Information

```yaml
user:
  nickname: "Seth"                     # How ANT addresses you
  full_name: "Seth Eheart"            # Full name for formal contexts
  timezone: "America/New_York"        # Your timezone
  preferred_language: "en"            # Interface language
```

## Feature Toggles

Control which ANT capabilities are enabled:

```yaml
features:
  file_operations: true      # File management and operations
  git_integration: true      # Git repository features
  code_analysis: true       # Code review and analysis
  web_search: true          # Real-time web search
  github_integration: true   # GitHub API features
  auto_tools: true          # Automatic tool usage
  learning_mode: false      # Personal learning (future)
```

## Environment Variables

Override config with environment variables:

```bash
# Configuration directory
export ANT_CONFIG_DIR="~/.config/ant"

# Ollama settings
export ANT_OLLAMA_URL="http://localhost:11434"
export ANT_MODEL="llama2:13b"

# Personality override
export ANT_PERSONALITY="professional_assistant"

# Debug mode
export ANT_DEBUG=true
```

## Advanced Configuration

### Logging Settings

```yaml
logging:
  level: "INFO"              # DEBUG, INFO, WARNING, ERROR
  file: "~/.ant/ant.log"     # Log file location
  max_size: "10MB"           # Maximum log file size
  backup_count: 3            # Number of backup logs
```

### Performance Tuning

```yaml
performance:
  response_timeout: 30       # Seconds to wait for model response
  retry_attempts: 3          # Number of retries on failure
  batch_size: 1             # Messages to process in batch
  cache_responses: true      # Cache similar responses
```

### Network Settings

```yaml
network:
  proxy:
    http: "http://proxy.company.com:8080"
    https: "https://proxy.company.com:8080"
  timeout: 30               # Network request timeout
  user_agent: "ANT/1.0"     # Custom user agent
```

## Configuration Management

### Reset Configuration

```bash
# Backup current config
cp ~/.ant/config.yaml ~/.ant/config.yaml.backup

# Reset to defaults
rm ~/.ant/config.yaml
ant --setup
```

### Validate Configuration

```bash
# Check current configuration
ant status

# Test model connectivity
ant
> Hello ANT!
```

### Import/Export Settings

```bash
# Export configuration
cp ~/.ant/config.yaml ~/ant-config-backup.yaml

# Import configuration
cp ~/ant-config-backup.yaml ~/.ant/config.yaml
```

## Troubleshooting Configuration

### Common Issues

**Problem**: ANT won't start after config changes
```bash
# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('~/.ant/config.yaml'))"

# Reset to defaults if corrupted
rm ~/.ant/config.yaml
ant --setup
```

**Problem**: Model not found
```bash
# Check available models
ollama list

# Update model name in config
# Edit ~/.ant/config.yaml
```

**Problem**: Permission errors
```bash
# Fix file permissions
chmod 600 ~/.ant/config.yaml
chown $USER ~/.ant/config.yaml
```

### Configuration Validation

ANT automatically validates configuration on startup:
- Checks YAML syntax
- Verifies model availability
- Tests Ollama connectivity
- Validates authentication tokens

---
**← [Authentication](Authentication) | [Troubleshooting](Troubleshooting) →**