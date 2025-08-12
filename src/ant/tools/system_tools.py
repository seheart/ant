"""System operations tools for ANT - File and command execution capabilities."""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
import stat
import pwd
import grp

from ant.cli.setup import get_config


class SystemOperations:
    """Secure system operations handler for ANT."""
    
    def __init__(self):
        self.config = get_config()
        self.safe_mode = self.config.get("system", {}).get("safe_mode", True)
        self.allowed_paths = self._get_allowed_paths()
        self.restricted_commands = [
            "rm -rf /", "sudo rm", "mkfs", "fdisk", "parted", 
            "dd if=", "chmod 777 /", "chown root", "passwd",
            "userdel", "usermod", "groupdel", "shutdown", "reboot"
        ]
    
    def _get_allowed_paths(self) -> List[str]:
        """Get list of allowed paths for operations."""
        user_home = str(Path.home())
        default_paths = [
            user_home,
            f"{user_home}/Documents",
            f"{user_home}/Desktop",
            f"{user_home}/Downloads", 
            f"{user_home}/Development",
            "/tmp",
            "/var/tmp"
        ]
        
        # Add custom allowed paths from config
        custom_paths = self.config.get("system", {}).get("allowed_paths", [])
        return default_paths + custom_paths
    
    def _is_path_allowed(self, path: str) -> bool:
        """Check if path is within allowed directories."""
        abs_path = os.path.abspath(path)
        return any(abs_path.startswith(allowed) for allowed in self.allowed_paths)
    
    def _is_command_safe(self, command: str) -> bool:
        """Check if command is safe to execute."""
        command_lower = command.lower()
        return not any(restricted in command_lower for restricted in self.restricted_commands)


def read_file(file_path: str, encoding: str = "utf-8") -> Dict[str, Any]:
    """Read contents of a file.
    
    Args:
        file_path: Path to the file to read
        encoding: File encoding (default: utf-8)
        
    Returns:
        Dict with file contents or error message
    """
    sys_ops = SystemOperations()
    
    try:
        abs_path = os.path.abspath(file_path)
        
        if not sys_ops._is_path_allowed(abs_path):
            return {"error": f"Access denied: {file_path} is outside allowed directories"}
        
        if not os.path.exists(abs_path):
            return {"error": f"File not found: {file_path}"}
        
        if not os.path.isfile(abs_path):
            return {"error": f"Path is not a file: {file_path}"}
        
        with open(abs_path, 'r', encoding=encoding) as f:
            content = f.read()
        
        file_stats = os.stat(abs_path)
        return {
            "success": True,
            "content": content,
            "path": abs_path,
            "size": file_stats.st_size,
            "modified": file_stats.st_mtime,
            "encoding": encoding
        }
        
    except PermissionError:
        return {"error": f"Permission denied: {file_path}"}
    except UnicodeDecodeError:
        return {"error": f"Cannot decode file with {encoding} encoding: {file_path}"}
    except Exception as e:
        return {"error": f"Error reading file: {str(e)}"}


def write_file(file_path: str, content: str, encoding: str = "utf-8", 
               backup: bool = True) -> Dict[str, Any]:
    """Write content to a file.
    
    Args:
        file_path: Path to the file to write
        content: Content to write
        encoding: File encoding (default: utf-8)
        backup: Create backup if file exists (default: True)
        
    Returns:
        Dict with operation result
    """
    sys_ops = SystemOperations()
    
    try:
        abs_path = os.path.abspath(file_path)
        
        if not sys_ops._is_path_allowed(abs_path):
            return {"error": f"Access denied: {file_path} is outside allowed directories"}
        
        # Create backup if file exists and backup is requested
        backup_path = None
        if backup and os.path.exists(abs_path):
            backup_path = f"{abs_path}.backup"
            shutil.copy2(abs_path, backup_path)
        
        # Ensure parent directory exists
        parent_dir = os.path.dirname(abs_path)
        os.makedirs(parent_dir, exist_ok=True)
        
        with open(abs_path, 'w', encoding=encoding) as f:
            f.write(content)
        
        file_stats = os.stat(abs_path)
        return {
            "success": True,
            "path": abs_path,
            "size": file_stats.st_size,
            "backup_created": backup_path if backup_path else False,
            "encoding": encoding
        }
        
    except PermissionError:
        return {"error": f"Permission denied: {file_path}"}
    except Exception as e:
        return {"error": f"Error writing file: {str(e)}"}


def list_directory(dir_path: str, show_hidden: bool = False) -> Dict[str, Any]:
    """List contents of a directory.
    
    Args:
        dir_path: Path to directory
        show_hidden: Include hidden files (default: False)
        
    Returns:
        Dict with directory contents
    """
    sys_ops = SystemOperations()
    
    try:
        abs_path = os.path.abspath(dir_path)
        
        if not sys_ops._is_path_allowed(abs_path):
            return {"error": f"Access denied: {dir_path} is outside allowed directories"}
        
        if not os.path.exists(abs_path):
            return {"error": f"Directory not found: {dir_path}"}
        
        if not os.path.isdir(abs_path):
            return {"error": f"Path is not a directory: {dir_path}"}
        
        items = []
        for item in os.listdir(abs_path):
            if not show_hidden and item.startswith('.'):
                continue
                
            item_path = os.path.join(abs_path, item)
            stats = os.stat(item_path)
            
            items.append({
                "name": item,
                "path": item_path,
                "type": "directory" if os.path.isdir(item_path) else "file",
                "size": stats.st_size,
                "modified": stats.st_mtime,
                "permissions": oct(stats.st_mode)[-3:]
            })
        
        return {
            "success": True,
            "path": abs_path,
            "items": sorted(items, key=lambda x: (x["type"] == "file", x["name"]))
        }
        
    except PermissionError:
        return {"error": f"Permission denied: {dir_path}"}
    except Exception as e:
        return {"error": f"Error listing directory: {str(e)}"}


def create_directory(dir_path: str, parents: bool = True) -> Dict[str, Any]:
    """Create a directory.
    
    Args:
        dir_path: Path to directory to create
        parents: Create parent directories if needed (default: True)
        
    Returns:
        Dict with operation result
    """
    sys_ops = SystemOperations()
    
    try:
        abs_path = os.path.abspath(dir_path)
        
        if not sys_ops._is_path_allowed(abs_path):
            return {"error": f"Access denied: {dir_path} is outside allowed directories"}
        
        if os.path.exists(abs_path):
            return {"error": f"Path already exists: {dir_path}"}
        
        os.makedirs(abs_path, exist_ok=not parents)
        
        return {
            "success": True,
            "path": abs_path,
            "created": True
        }
        
    except PermissionError:
        return {"error": f"Permission denied: {dir_path}"}
    except Exception as e:
        return {"error": f"Error creating directory: {str(e)}"}


def delete_file_or_directory(path: str, force: bool = False) -> Dict[str, Any]:
    """Delete a file or directory.
    
    Args:
        path: Path to delete
        force: Force deletion of non-empty directories (default: False)
        
    Returns:
        Dict with operation result
    """
    sys_ops = SystemOperations()
    
    try:
        abs_path = os.path.abspath(path)
        
        if not sys_ops._is_path_allowed(abs_path):
            return {"error": f"Access denied: {path} is outside allowed directories"}
        
        if not os.path.exists(abs_path):
            return {"error": f"Path not found: {path}"}
        
        # Extra safety check
        if abs_path in ["/", "/home", "/usr", "/etc", "/var", "/bin", "/sbin"]:
            return {"error": f"Refusing to delete system directory: {path}"}
        
        if os.path.isfile(abs_path):
            os.remove(abs_path)
            return {"success": True, "path": abs_path, "type": "file"}
        elif os.path.isdir(abs_path):
            if force:
                shutil.rmtree(abs_path)
            else:
                os.rmdir(abs_path)  # Only works if empty
            return {"success": True, "path": abs_path, "type": "directory"}
        
    except PermissionError:
        return {"error": f"Permission denied: {path}"}
    except OSError as e:
        if "not empty" in str(e):
            return {"error": f"Directory not empty (use force=True): {path}"}
        return {"error": f"Error deleting: {str(e)}"}
    except Exception as e:
        return {"error": f"Error deleting: {str(e)}"}


def execute_command(command: str, cwd: Optional[str] = None, timeout: int = 30) -> Dict[str, Any]:
    """Execute a system command safely.
    
    Args:
        command: Command to execute
        cwd: Working directory (default: current directory)
        timeout: Timeout in seconds (default: 30)
        
    Returns:
        Dict with command result
    """
    sys_ops = SystemOperations()
    
    try:
        if not sys_ops._is_command_safe(command):
            return {"error": f"Command blocked for safety: {command}"}
        
        if cwd and not sys_ops._is_path_allowed(cwd):
            return {"error": f"Working directory not allowed: {cwd}"}
        
        # Run command with timeout
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        return {
            "success": True,
            "command": command,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "cwd": cwd or os.getcwd()
        }
        
    except subprocess.TimeoutExpired:
        return {"error": f"Command timed out after {timeout} seconds: {command}"}
    except Exception as e:
        return {"error": f"Error executing command: {str(e)}"}


def copy_file_or_directory(src: str, dst: str, follow_symlinks: bool = True) -> Dict[str, Any]:
    """Copy a file or directory.
    
    Args:
        src: Source path
        dst: Destination path
        follow_symlinks: Follow symbolic links (default: True)
        
    Returns:
        Dict with operation result
    """
    sys_ops = SystemOperations()
    
    try:
        abs_src = os.path.abspath(src)
        abs_dst = os.path.abspath(dst)
        
        if not sys_ops._is_path_allowed(abs_src):
            return {"error": f"Source access denied: {src}"}
        
        if not sys_ops._is_path_allowed(abs_dst):
            return {"error": f"Destination access denied: {dst}"}
        
        if not os.path.exists(abs_src):
            return {"error": f"Source not found: {src}"}
        
        if os.path.isfile(abs_src):
            shutil.copy2(abs_src, abs_dst)
            return {"success": True, "src": abs_src, "dst": abs_dst, "type": "file"}
        elif os.path.isdir(abs_src):
            shutil.copytree(abs_src, abs_dst, symlinks=not follow_symlinks)
            return {"success": True, "src": abs_src, "dst": abs_dst, "type": "directory"}
        
    except PermissionError:
        return {"error": f"Permission denied copying from {src} to {dst}"}
    except Exception as e:
        return {"error": f"Error copying: {str(e)}"}


def move_file_or_directory(src: str, dst: str) -> Dict[str, Any]:
    """Move (rename) a file or directory.
    
    Args:
        src: Source path
        dst: Destination path
        
    Returns:
        Dict with operation result
    """
    sys_ops = SystemOperations()
    
    try:
        abs_src = os.path.abspath(src)
        abs_dst = os.path.abspath(dst)
        
        if not sys_ops._is_path_allowed(abs_src):
            return {"error": f"Source access denied: {src}"}
        
        if not sys_ops._is_path_allowed(abs_dst):
            return {"error": f"Destination access denied: {dst}"}
        
        if not os.path.exists(abs_src):
            return {"error": f"Source not found: {src}"}
        
        shutil.move(abs_src, abs_dst)
        
        return {
            "success": True,
            "src": abs_src,
            "dst": abs_dst,
            "type": "directory" if os.path.isdir(abs_dst) else "file"
        }
        
    except PermissionError:
        return {"error": f"Permission denied moving from {src} to {dst}"}
    except Exception as e:
        return {"error": f"Error moving: {str(e)}"}