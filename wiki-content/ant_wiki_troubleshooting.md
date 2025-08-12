# Troubleshooting

Common issues and solutions for ANT. Most problems can be resolved with these steps.

## Quick Diagnosis

Run these commands to check ANT's status:

```bash
# Check ANT status
ant status

# Check Ollama connectivity  
curl http://localhost:11434/api/version

# Check available models
ollama list

# Check configuration
cat ~/.ant/config.yaml
```

## Installation Issues

### ANT Command Not Found

**Symptoms**: `bash: ant: command not found`

**Solutions**:
```bash
# Reinstall ANT
cd /path/to/ant
pip install -e . --force-reinstall

# Check if it's in PATH
which ant
echo $PATH

# Manual PATH addition (if needed)
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

### Python/Pip Issues

**Symptoms**: Import errors, package conflicts

**Solutions**:
```bash
# Check Python version (need 3.9+)
python --version

# Use virtual environment
python -m venv ant-env
source ant-env/bin/activate
pip install -e .

# Clear pip cache
pip cache purge
```

## Ollama Connection Issues

### Ollama Not Running

**Symptoms**: Connection refused, timeout errors

**Solutions**:
```bash
# Start Ollama service
ollama serve

# Check if Ollama is running
ps aux | grep ollama

# Test connectivity
curl http://localhost:11434/api/version

# Check port availability
lsof -i :11434
```

### Model Not Available

**Symptoms**: "Model not found" errors

**Solutions**:
```bash
# List available models
ollama list

# Pull required model
ollama pull qwen2.5-coder:14b

# Update ANT config to use available model
ant --setup
# Or edit ~/.ant/config.yaml directly
```

### Slow Model Response

**Symptoms**: Long delays, timeouts

**Solutions**:
```bash
# Use smaller model
ollama pull qwen2.5-coder:7b

# Check system resources
htop
nvidia-smi  # If using GPU

# Increase timeout in config
# Edit ~/.ant/config.yaml:
# performance:
#   response_timeout: 60
```

## Authentication Problems

### GitHub Authentication Fails

**Symptoms**: "Not authenticated" or "401 Unauthorized"

**Solutions**:
```bash
# Check current auth status
ant auth status

# Revoke and re-authenticate
ant auth revoke github
ant auth github

# Verify token permissions
# Go to https://github.com/settings/tokens
# Ensure token has 'repo' and 'user' scopes
```

### Token Expired

**Symptoms**: Authentication worked before but fails now

**Solutions**:
```bash
# Check token expiration on GitHub
# Go to https://github.com/settings/tokens

# Generate new token
# Copy new token
ant auth revoke github
ant auth github
# Paste new token
```

## Configuration Issues

### Corrupted Configuration

**Symptoms**: YAML parsing errors, ANT won't start

**Solutions**:
```bash
# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('/home/$USER/.ant/config.yaml'))"

# Backup and reset
cp ~/.ant/config.yaml ~/.ant/config.yaml.backup
rm ~/.ant/config.yaml
ant --setup
```

### Permission Denied

**Symptoms**: Can't read/write config files

**Solutions**:
```bash
# Fix file permissions
chmod 600 ~/.ant/config.yaml
chown $USER ~/.ant/config.yaml

# Fix directory permissions
chmod 755 ~/.ant/
chown $USER ~/.ant/
```

## Chat Session Issues

### Memory/Context Problems

**Symptoms**: ANT doesn't remember conversation, repetitive responses

**Solutions**:
```bash
# Clear conversation history
ant
> /clear

# Check memory settings in config
cat ~/.ant/config.yaml | grep -A5 memory:

# Reduce context window if using large model
# Edit ~/.ant/config.yaml:
# memory:
#   max_context_messages: 10
```

### Response Quality Issues

**Symptoms**: Poor responses, nonsensical output

**Solutions**:
```bash
# Try different model
ollama pull llama2:13b
ant --setup  # Select new model

# Check model is fully downloaded
ollama list

# Clear conversation and restart
ant
> /clear
```

### Unicode/Display Issues

**Symptoms**: Garbled text, missing emojis, formatting problems

**Solutions**:
```bash
# Check terminal UTF-8 support
locale

# Set UTF-8 locale
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

# Try different terminal
# Use modern terminal with Unicode support
```

## Performance Issues

### High Memory Usage

**Symptoms**: System slowdown, out of memory errors

**Solutions**:
```bash
# Monitor resource usage
htop
nvidia-smi  # GPU memory

# Use smaller model
ollama pull qwen2.5-coder:7b

# Reduce context window
# Edit ~/.ant/config.yaml:
# memory:
#   max_context_messages: 10
```

### Slow Startup

**Symptoms**: ANT takes long time to start

**Solutions**:
```bash
# Check model loading time
time ollama run qwen2.5-coder:14b "test"

# Pre-load model
ollama run qwen2.5-coder:14b ""

# Use faster model for quick tasks
# Edit ~/.ant/config.yaml:
# ollama:
#   completion_model: "qwen2.5-coder:7b"
```

## Network Issues

### Web Search Fails

**Symptoms**: "No search results", timeout errors

**Solutions**:
```bash
# Test internet connectivity
ping google.com

# Check firewall/proxy settings
curl https://duckduckgo.com

# Configure proxy if needed
# Edit ~/.ant/config.yaml:
# network:
#   proxy:
#     http: "http://proxy.company.com:8080"
```

### GitHub API Rate Limiting

**Symptoms**: "Rate limit exceeded" errors

**Solutions**:
```bash
# Check rate limit status
curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/rate_limit

# Wait for reset (shown in response)
# Or use OAuth instead of personal token

# Reduce GitHub API usage
# ANT automatically handles rate limiting
```

## Data Recovery

### Lost Configuration

**Symptoms**: ANT reverted to defaults

**Solutions**:
```bash
# Check for backup files
ls ~/.ant/*.backup
ls ~/.ant/*.bak

# Restore from backup
cp ~/.ant/config.yaml.backup ~/.ant/config.yaml

# Recreate configuration
ant --setup
```

### Lost Conversation History

**Symptoms**: Chat history disappeared

**Solutions**:
```bash
# Check database file
ls -la ~/.ant/conversations.db

# Database might be corrupted
# Backup and reset
cp ~/.ant/conversations.db ~/.ant/conversations.db.backup
rm ~/.ant/conversations.db

# ANT will create new database on next run
```

## Advanced Troubleshooting

### Debug Mode

Enable verbose logging:

```bash
# Set debug environment
export ANT_DEBUG=true
ant

# Check logs
tail -f ~/.ant/ant.log

# Or add to config:
# logging:
#   level: "DEBUG"
```

### System Information

Gather diagnostic info:

```bash
# System info
uname -a
python --version
pip --version

# ANT info
ant --version
ant status

# Ollama info
ollama version
ollama list
```

### Clean Reinstall

Nuclear option - complete reset:

```bash
# Stop any running processes
pkill -f ant
pkill -f ollama

# Remove ANT data
rm -rf ~/.ant/

# Reinstall ANT
cd /path/to/ant
pip uninstall ant -y
pip install -e .

# Restart Ollama
ollama serve &

# Setup from scratch
ant --setup
```

## Getting Help

If you're still having issues:

1. **Check the logs**: `~/.ant/ant.log`
2. **Search existing issues**: [GitHub Issues](https://github.com/seheart/ant/issues)
3. **Create new issue**: Include:
   - ANT version (`ant --version`)
   - System info (`uname -a`, `python --version`)
   - Error messages and logs
   - Steps to reproduce

## Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `ConnectionError: ('Connection aborted.', RemoteDisconnected(...))` | Ollama not running | Start Ollama: `ollama serve` |
| `Model 'qwen2.5-coder:14b' not found` | Model not downloaded | Pull model: `ollama pull qwen2.5-coder:14b` |
| `FileNotFoundError: [Errno 2] No such file or directory: '/home/user/.ant/config.yaml'` | Config not initialized | Run setup: `ant --setup` |
| `yaml.scanner.ScannerError: while scanning for the next token` | Invalid YAML in config | Reset config: `rm ~/.ant/config.yaml && ant --setup` |
| `requests.exceptions.HTTPError: 401 Client Error: Unauthorized` | Invalid GitHub token | Re-authenticate: `ant auth revoke github && ant auth github` |

---
**← [Configuration](Configuration) | [Home](Home) →**