"""Authentication and OAuth management for external services."""

import json
import secrets
import webbrowser
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional
from urllib.parse import urlencode

import requests
from rich.console import Console
from rich.prompt import Confirm, Prompt

from ant.cli.setup import get_config, save_config

console = Console(width=None, legacy_windows=False)

# OAuth configurations
GITHUB_CONFIG = {
    "client_id": "your_github_client_id",  # You'll need to register an app
    "scope": "repo,user,gist",
    "auth_url": "https://github.com/login/oauth/authorize",
    "token_url": "https://github.com/login/oauth/access_token"
}

GOOGLE_CONFIG = {
    "client_id": "your_google_client_id",  # You'll need to register an app
    "scope": "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/drive.readonly",
    "auth_url": "https://accounts.google.com/o/oauth2/v2/auth",
    "token_url": "https://oauth2.googleapis.com/token"
}


class AuthManager:
    """Manages authentication for external services."""
    
    def __init__(self) -> None:
        self.config = get_config()
        self._init_auth_config()
    
    def _init_auth_config(self) -> None:
        """Initialize auth configuration."""
        if "auth" not in self.config:
            self.config["auth"] = {
                "tokens": {},
                "last_updated": {}
            }
    
    def store_token(self, service: str, token_data: Dict[str, Any]) -> None:
        """Store an authentication token for a service."""
        self.config["auth"]["tokens"][service] = token_data
        self.config["auth"]["last_updated"][service] = datetime.now().isoformat()
        save_config(self.config)
        console.print(f"✅ {service} authentication saved!", style="green")
    
    def get_token(self, service: str) -> Optional[Dict[str, Any]]:
        """Get authentication token for a service."""
        return self.config["auth"]["tokens"].get(service)
    
    def is_authenticated(self, service: str) -> bool:
        """Check if user is authenticated with a service."""
        token = self.get_token(service)
        if not token:
            return False
        
        # Check if token is expired (if expiry info available)
        if "expires_at" in token:
            expires_at = datetime.fromisoformat(token["expires_at"])
            if datetime.now() > expires_at:
                return False
        
        return True
    
    def setup_github_auth(self) -> bool:
        """Set up GitHub authentication."""
        console.print("🔐 GitHub Authentication Setup", style="bold blue")
        console.print()
        
        if self.is_authenticated("github"):
            if not Confirm.ask("You're already authenticated with GitHub. Re-authenticate?"):
                return True
        
        console.print("Setting up GitHub authentication...")
        console.print("You can either:")
        console.print("1. Use a Personal Access Token (simpler)")
        console.print("2. Use OAuth flow (more secure)")
        
        choice = Prompt.ask("Choose method", choices=["1", "2"], default="1")
        
        if choice == "1":
            return self._setup_github_token()
        else:
            return self._setup_github_oauth()
    
    def _setup_github_token(self) -> bool:
        """Set up GitHub using Personal Access Token."""
        console.print()
        console.print("📋 To create a Personal Access Token:")
        console.print("1. Go to: https://github.com/settings/tokens")
        console.print("2. Click 'Generate new token (classic)'")
        console.print("3. Select scopes: repo, user, gist")
        console.print("4. Copy the generated token")
        console.print()
        
        if Confirm.ask("Open GitHub token page in browser?"):
            webbrowser.open("https://github.com/settings/tokens")
        
        token = Prompt.ask("Enter your GitHub token", password=True)
        
        if not token:
            console.print("❌ No token provided", style="red")
            return False
        
        # Test the token
        if self._test_github_token(token):
            self.store_token("github", {
                "access_token": token,
                "type": "personal_access_token",
                "scopes": ["repo", "user", "gist"]
            })
            return True
        else:
            console.print("❌ Invalid token", style="red")
            return False
    
    def _test_github_token(self, token: str) -> bool:
        """Test if GitHub token is valid."""
        try:
            headers = {"Authorization": f"token {token}"}
            response = requests.get("https://api.github.com/user", headers=headers)
            return response.status_code == 200
        except Exception:
            return False
    
    def _setup_github_oauth(self) -> bool:
        """Set up GitHub using OAuth (requires app registration)."""
        console.print("❌ OAuth setup requires GitHub app registration", style="yellow")
        console.print("For now, please use Personal Access Token method.")
        return False
    
    def setup_google_auth(self) -> bool:
        """Set up Google authentication."""
        console.print("🔐 Google Authentication Setup", style="bold blue")
        console.print()
        
        if self.is_authenticated("google"):
            if not Confirm.ask("You're already authenticated with Google. Re-authenticate?"):
                return True
        
        console.print("📋 Google OAuth setup requires:")
        console.print("1. Create a project at: https://console.cloud.google.com/")
        console.print("2. Enable APIs you want to use")
        console.print("3. Create OAuth 2.0 credentials")
        console.print("4. Add redirect URI: http://localhost:8080/callback")
        console.print()
        
        if not Confirm.ask("Have you completed Google Cloud Console setup?"):
            console.print("Please complete the setup first, then run this again.")
            return False
        
        client_id = Prompt.ask("Enter your Google Client ID")
        client_secret = Prompt.ask("Enter your Google Client Secret", password=True)
        
        if not client_id or not client_secret:
            console.print("❌ Client ID and Secret are required", style="red")
            return False
        
        # For now, store the credentials (a full OAuth flow would be more complex)
        console.print("⚠️  Full OAuth flow not implemented yet", style="yellow")
        console.print("Storing credentials for future OAuth implementation...")
        
        self.store_token("google", {
            "client_id": client_id,
            "client_secret": client_secret,
            "type": "oauth_credentials"
        })
        return True
    
    def github_api_call(self, endpoint: str, method: str = "GET", **kwargs) -> Optional[Dict[str, Any]]:
        """Make an authenticated GitHub API call."""
        token = self.get_token("github")
        if not token:
            console.print("❌ Not authenticated with GitHub. Run setup first.", style="red")
            return None
        
        headers = {
            "Authorization": f"token {token['access_token']}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        url = f"https://api.github.com/{endpoint.lstrip('/')}"
        
        try:
            response = requests.request(method, url, headers=headers, **kwargs)
            if response.status_code == 200:
                return response.json()
            else:
                console.print(f"GitHub API error: {response.status_code}", style="red")
                return None
        except Exception as e:
            console.print(f"GitHub API call failed: {e}", style="red")
            return None
    
    def get_github_user_info(self) -> Optional[Dict[str, Any]]:
        """Get authenticated GitHub user information."""
        return self.github_api_call("user")
    
    def list_github_repos(self, limit: int = 10) -> Optional[list]:
        """List user's GitHub repositories."""
        data = self.github_api_call("user/repos", params={"per_page": limit, "sort": "updated"})
        return data if data else []
    
    def revoke_service_auth(self, service: str) -> None:
        """Revoke authentication for a service."""
        if service in self.config["auth"]["tokens"]:
            del self.config["auth"]["tokens"][service]
            del self.config["auth"]["last_updated"][service]
            save_config(self.config)
            console.print(f"✅ {service} authentication revoked", style="green")
        else:
            console.print(f"❌ Not authenticated with {service}", style="yellow")
    
    def list_authenticated_services(self) -> list:
        """List all authenticated services."""
        return list(self.config["auth"]["tokens"].keys())


# Global auth manager instance
auth_manager = AuthManager()