"""User profile management for ANT."""

import os
import pwd
import socket
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from ant.cli.setup import get_config, save_config


class UserProfile:
    """Manages user profile and preferences."""
    
    def __init__(self) -> None:
        self.config = get_config()
        self._init_profile()
    
    def _init_profile(self) -> None:
        """Initialize user profile from system info."""
        if "user" not in self.config:
            self.config["user"] = {}
        
        # Auto-detect user info if not set
        user_info = self._get_system_user_info()
        
        # Update config with system info (but don't overwrite existing preferences)
        for key, value in user_info.items():
            if key not in self.config["user"]:
                self.config["user"][key] = value
        
        # Set defaults for user preferences
        defaults = {
            "nickname": user_info["username"],
            "timezone": self._get_timezone(),
            "first_setup": datetime.now().isoformat(),
            "preferences": {
                "code_style": "auto",
                "communication_style": "friendly",
                "detail_level": "balanced"
            }
        }
        
        for key, value in defaults.items():
            if key not in self.config["user"]:
                self.config["user"][key] = value
    
    def _get_system_user_info(self) -> Dict[str, str]:
        """Get user information from the Linux system."""
        try:
            # Get current user info
            username = os.getuser()
            uid = os.getuid()
            
            # Get more detailed user info from passwd
            user_info = pwd.getpwuid(uid)
            
            # Parse GECOS field (usually contains full name)
            full_name = user_info.pw_gecos.split(',')[0] if user_info.pw_gecos else username
            
            return {
                "username": username,
                "full_name": full_name or username,
                "home_dir": str(Path.home()),
                "shell": user_info.pw_shell,
                "uid": str(uid),
                "hostname": self._format_hostname(socket.gethostname())
            }
        except Exception:
            # Fallback if system calls fail
            return {
                "username": os.environ.get("USER", "user"),
                "full_name": os.environ.get("USER", "user"),
                "home_dir": str(Path.home()),
                "shell": "/bin/bash",
                "uid": "1000",
                "hostname": self._format_hostname("localhost")
            }
    
    def _format_hostname(self, hostname: str) -> str:
        """Format hostname to camel case (e.g., ubuntu -> Ubuntu)."""
        if not hostname:
            return hostname
        
        # Handle common cases
        if hostname.lower() == "ubuntu":
            return "Ubuntu"
        elif hostname.lower() == "localhost":
            return "LocalHost"
        else:
            # General camel case: first letter uppercase, rest lowercase
            return hostname.capitalize()
    
    def _get_timezone(self) -> str:
        """Get user's timezone."""
        try:
            # Try to get timezone from system
            if Path("/etc/timezone").exists():
                with open("/etc/timezone", "r") as f:
                    return f.read().strip()
            
            # Fallback to TZ environment variable
            return os.environ.get("TZ", "UTC")
        except Exception:
            return "UTC"
    
    def get_user_name(self) -> str:
        """Get the user's preferred name."""
        name = self.config["user"].get("nickname", 
                                      self.config["user"].get("full_name", 
                                                             self.config["user"].get("username", "User")))
        # Capitalize the name for display (seth -> Seth)
        return name.capitalize() if isinstance(name, str) else name
    
    def get_user_info(self) -> Dict[str, Any]:
        """Get complete user profile information."""
        return self.config["user"].copy()
    
    def update_preference(self, key: str, value: Any) -> None:
        """Update a user preference."""
        if "preferences" not in self.config["user"]:
            self.config["user"]["preferences"] = {}
        
        self.config["user"]["preferences"][key] = value
        save_config(self.config)
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get a user preference."""
        return self.config["user"].get("preferences", {}).get(key, default)
    
    def set_nickname(self, nickname: str) -> None:
        """Set user's nickname."""
        self.config["user"]["nickname"] = nickname
        save_config(self.config)
    
    def get_greeting_context(self) -> Dict[str, Any]:
        """Get context for personalized greetings."""
        now = datetime.now()
        hour = now.hour
        
        if 5 <= hour < 12:
            time_of_day = "morning"
        elif 12 <= hour < 17:
            time_of_day = "afternoon"
        elif 17 <= hour < 21:
            time_of_day = "evening"
        else:
            time_of_day = "night"
        
        return {
            "name": self.get_user_name(),
            "time_of_day": time_of_day,
            "username": self.config["user"].get("username"),
            "hostname": self.config["user"].get("hostname"),
            "communication_style": self.get_preference("communication_style", "friendly")
        }
    
    def is_first_time_user(self) -> bool:
        """Check if this is the user's first time running ANT."""
        return "first_setup" not in self.config["user"]
    
    def mark_setup_complete(self) -> None:
        """Mark initial setup as complete."""
        self.config["user"]["setup_completed"] = datetime.now().isoformat()
        save_config(self.config)


# Global user profile instance
user_profile = UserProfile()