"""ANT tools and functions."""

from .tool_registry import tool_registry
from .datetime_tools import get_current_time, get_time_only, get_date_only, get_iso_datetime
from .web_tools import search_web, search_news
from .github_tools import get_github_user, list_github_repos, get_repository_info
from .system_tools import (
    read_file, write_file, list_directory, create_directory, 
    delete_file_or_directory, execute_command, copy_file_or_directory, 
    move_file_or_directory
)
from .system_analysis import analyze_linux_system
from .personal_learning import (
    record_personality_insight, record_conversation_insight, 
    record_personal_preference, get_personal_summary
)

# Auto-register all tools
tool_registry.register_tool("get_current_time", get_current_time, "Get current date and time")
tool_registry.register_tool("get_time_only", get_time_only, "Get current time only")
tool_registry.register_tool("get_date_only", get_date_only, "Get current date only")
tool_registry.register_tool("get_iso_datetime", get_iso_datetime, "Get ISO format datetime")
tool_registry.register_tool("search_web", search_web, "Search the web for current information")
tool_registry.register_tool("search_news", search_news, "Search for recent news articles")
tool_registry.register_tool("get_github_user", get_github_user, "Get GitHub user information")
tool_registry.register_tool("list_github_repos", list_github_repos, "List user's GitHub repositories")
tool_registry.register_tool("get_repository_info", get_repository_info, "Get detailed repository information")

# System operations tools
tool_registry.register_tool("read_file", read_file, "Read contents of a file")
tool_registry.register_tool("write_file", write_file, "Write content to a file")
tool_registry.register_tool("list_directory", list_directory, "List contents of a directory")
tool_registry.register_tool("create_directory", create_directory, "Create a new directory")
tool_registry.register_tool("delete_file_or_directory", delete_file_or_directory, "Delete a file or directory")
tool_registry.register_tool("execute_command", execute_command, "Execute a system command safely")
tool_registry.register_tool("copy_file_or_directory", copy_file_or_directory, "Copy a file or directory")
tool_registry.register_tool("move_file_or_directory", move_file_or_directory, "Move or rename a file or directory")
tool_registry.register_tool("analyze_linux_system", analyze_linux_system, "Perform comprehensive Linux system analysis and generate detailed report")

# Personal learning tools
tool_registry.register_tool("record_personality_insight", record_personality_insight, "Record a personality insight about Seth (communication style, values, etc.)")
tool_registry.register_tool("record_conversation_insight", record_conversation_insight, "Record an insight from our conversation")
tool_registry.register_tool("record_personal_preference", record_personal_preference, "Record a personal preference about Seth") 
tool_registry.register_tool("get_personal_summary", get_personal_summary, "Get a summary of what I know about Seth personally")

__all__ = [
    "tool_registry",
    "get_current_time", 
    "get_time_only", 
    "get_date_only", 
    "get_iso_datetime",
    "search_web",
    "search_news",
    "get_github_user",
    "list_github_repos", 
    "get_repository_info",
    "read_file",
    "write_file",
    "list_directory",
    "create_directory",
    "delete_file_or_directory",
    "execute_command",
    "copy_file_or_directory",
    "move_file_or_directory",
    "analyze_linux_system",
    "record_personality_insight",
    "record_conversation_insight", 
    "record_personal_preference",
    "get_personal_summary"
]