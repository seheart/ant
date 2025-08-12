# Authentication & Service Integration

ANT can integrate with external services to enhance your experience. All authentication is handled securely with tokens stored locally.

## Overview

ANT supports authentication with:
- **GitHub** - Repository management, issue tracking, user info
- **Google** - OAuth setup for future features *(basic setup)*

All tokens and credentials are stored locally in `~/.ant/config.yaml` and never leave your machine.

## GitHub Authentication

GitHub integration allows ANT to access your repositories, issues, and profile information during conversations.

### Setup Methods

#### Method 1: Personal Access Token (Recommended)

1. **Create a GitHub Token**:
   - Go to [GitHub Settings > Personal Access Tokens](https://github.com/settings/tokens)
   - Click "Generate new token (classic)"
   - Add a note like "ANT AI Assistant"
   - Select scopes:
     - `repo` - Full repository access
     - `user` - User profile information
     - `gist` - Gist management

2. **Add to ANT**:
   ```bash
   ant auth github
   # Select "Personal Access Token"
   # Paste your token when prompted
   ```

#### Method 2: OAuth Flow *(Coming Soon)*

Full OAuth integration is planned for future releases.

### GitHub Capabilities

Once authenticated, you can:

**In conversations:**
```
You: "Show me my recent repositories"
ANT: [Lists your GitHub repos with details]

You: "What issues are open in my ant project?"  
ANT: [Shows open issues from ant repository]

You: "Tell me about my GitHub profile"
ANT: [Displays profile information and statistics]
```

**Available data:**
- Repository listing and details
- Issue tracking and management  
- User profile and statistics
- Organization information
- Collaboration data

### Managing GitHub Auth

```bash
# Check authentication status
ant auth status

# View detailed GitHub info
ant auth github status

# Remove GitHub authentication
ant auth revoke github

# Re-authenticate
ant auth github
```

## Google Authentication

Basic Google OAuth setup is available for future feature development.

### Setup Process

```bash
ant auth google
```

**Note**: Currently requires manual Google Cloud Console setup:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable APIs you want to use
4. Create OAuth 2.0 credentials
5. Add credentials to ANT when prompted

### Planned Google Features

Future integrations may include:
- Google Drive file access
- Gmail integration
- Calendar management
- Google Search API

## Security & Privacy

### Token Storage

- All tokens stored in `~/.ant/config.yaml`
- File permissions set to user-only (`600`)
- No tokens sent to external services except target APIs
- Local encryption planned for future releases

### Best Practices

1. **Use specific scopes** - Only grant necessary permissions
2. **Rotate tokens regularly** - Update tokens every few months  
3. **Revoke unused services** - Clean up old authentications
4. **Monitor access** - Check GitHub/Google access logs periodically

### Revoking Access

#### From ANT:
```bash
ant auth revoke github  # Remove from ANT
ant auth revoke google   # Remove from ANT
```

#### From Services:
- **GitHub**: Settings > Applications > Personal access tokens
- **Google**: Account settings > Security > Third-party app access

## Authentication Commands Reference

| Command | Description |
|---------|-------------|
| `ant auth` | Show authentication manager overview |
| `ant auth status` | Detailed status of all services |
| `ant auth github` | Set up GitHub integration |
| `ant auth google` | Set up Google integration |
| `ant auth revoke <service>` | Remove service authentication |

## Troubleshooting Authentication

### GitHub Issues

**Problem**: "Not authenticated" errors
```bash
# Check current status
ant auth status

# Verify token is valid
ant auth github status

# Re-authenticate if needed
ant auth revoke github
ant auth github
```

**Problem**: "Permission denied" errors
- Check token scopes include `repo` and `user`
- Verify token hasn't expired
- Ensure repository access permissions

**Problem**: Rate limiting
- GitHub API has rate limits (5000/hour for authenticated users)
- ANT automatically handles rate limiting with delays
- Consider using OAuth instead of PAT for higher limits

### Google Issues

**Problem**: OAuth setup difficulties
- Ensure Google Cloud project is properly configured
- Verify OAuth consent screen is set up
- Check redirect URIs match ANT's expectations

### General Auth Issues

**Problem**: Config file corruption
```bash
# Backup current config
cp ~/.ant/config.yaml ~/.ant/config.yaml.backup

# Reset authentication section
ant auth revoke github
ant auth revoke google

# Re-authenticate services
ant auth github
```

**Problem**: Permission errors on config file
```bash
# Fix file permissions
chmod 600 ~/.ant/config.yaml
chown $USER ~/.ant/config.yaml
```

## Advanced Configuration

### Custom API Endpoints

Edit `~/.ant/config.yaml` for custom endpoints:

```yaml
auth:
  github:
    api_url: "https://api.github.com"  # GitHub Enterprise
  google:
    oauth_url: "https://accounts.google.com/o/oauth2/v2/auth"
```

### Proxy Settings

For corporate networks:

```yaml
auth:
  proxy:
    http: "http://proxy.company.com:8080"
    https: "https://proxy.company.com:8080"
```

---
**← [Commands Reference](Commands-Reference) | [Configuration](Configuration) →**