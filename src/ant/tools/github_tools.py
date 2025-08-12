"""GitHub integration tools for ANT."""

from typing import Dict, Any, List, Optional

from ant.user.auth import auth_manager


def get_github_user() -> Dict[str, Any]:
    """Get the authenticated GitHub user information.
    
    Returns:
        Dict containing GitHub user info or error message
    """
    if not auth_manager.is_authenticated("github"):
        return {"error": "Not authenticated with GitHub. Run 'ant auth github' first."}
    
    user_info = auth_manager.get_github_user_info()
    if not user_info:
        return {"error": "Failed to fetch GitHub user information"}
    
    return {
        "username": user_info.get("login"),
        "name": user_info.get("name"),
        "email": user_info.get("email"),
        "bio": user_info.get("bio"),
        "location": user_info.get("location"),
        "public_repos": user_info.get("public_repos", 0),
        "followers": user_info.get("followers", 0),
        "following": user_info.get("following", 0),
        "created_at": user_info.get("created_at"),
        "updated_at": user_info.get("updated_at")
    }


def list_github_repos(limit: int = 10) -> Dict[str, Any]:
    """List the user's GitHub repositories.
    
    Args:
        limit: Maximum number of repositories to return
        
    Returns:
        Dict containing repository list or error message
    """
    if not auth_manager.is_authenticated("github"):
        return {"error": "Not authenticated with GitHub. Run 'ant auth github' first."}
    
    repos = auth_manager.list_github_repos(limit)
    if not repos:
        return {"error": "Failed to fetch repositories or no repositories found"}
    
    repo_list = []
    for repo in repos:
        repo_info = {
            "name": repo.get("name"),
            "full_name": repo.get("full_name"),
            "description": repo.get("description"),
            "private": repo.get("private", False),
            "language": repo.get("language"),
            "stars": repo.get("stargazers_count", 0),
            "forks": repo.get("forks_count", 0),
            "updated_at": repo.get("updated_at"),
            "url": repo.get("html_url")
        }
        repo_list.append(repo_info)
    
    return {
        "repositories": repo_list,
        "count": len(repo_list)
    }


def get_github_repo_info(repo_name: str) -> Dict[str, Any]:
    """Get detailed information about a specific repository.
    
    Args:
        repo_name: Repository name in format "owner/repo" or just "repo" for user's repo
        
    Returns:
        Dict containing repository information or error message
    """
    if not auth_manager.is_authenticated("github"):
        return {"error": "Not authenticated with GitHub. Run 'ant auth github' first."}
    
    # If just repo name provided, assume it's user's repo
    if "/" not in repo_name:
        user_info = auth_manager.get_github_user_info()
        if not user_info:
            return {"error": "Cannot determine user for repository lookup"}
        repo_name = f"{user_info['login']}/{repo_name}"
    
    repo_info = auth_manager.github_api_call(f"repos/{repo_name}")
    if not repo_info:
        return {"error": f"Repository '{repo_name}' not found or access denied"}
    
    return {
        "name": repo_info.get("name"),
        "full_name": repo_info.get("full_name"),
        "description": repo_info.get("description"),
        "private": repo_info.get("private", False),
        "language": repo_info.get("language"),
        "size": repo_info.get("size", 0),
        "stars": repo_info.get("stargazers_count", 0),
        "watchers": repo_info.get("watchers_count", 0),
        "forks": repo_info.get("forks_count", 0),
        "open_issues": repo_info.get("open_issues_count", 0),
        "default_branch": repo_info.get("default_branch"),
        "created_at": repo_info.get("created_at"),
        "updated_at": repo_info.get("updated_at"),
        "pushed_at": repo_info.get("pushed_at"),
        "clone_url": repo_info.get("clone_url"),
        "ssh_url": repo_info.get("ssh_url"),
        "url": repo_info.get("html_url"),
        "topics": repo_info.get("topics", [])
    }


def get_github_repo_issues(repo_name: str, limit: int = 10) -> Dict[str, Any]:
    """Get issues for a GitHub repository.
    
    Args:
        repo_name: Repository name in format "owner/repo" or just "repo" for user's repo
        limit: Maximum number of issues to return
        
    Returns:
        Dict containing issues list or error message
    """
    if not auth_manager.is_authenticated("github"):
        return {"error": "Not authenticated with GitHub. Run 'ant auth github' first."}
    
    # If just repo name provided, assume it's user's repo
    if "/" not in repo_name:
        user_info = auth_manager.get_github_user_info()
        if not user_info:
            return {"error": "Cannot determine user for repository lookup"}
        repo_name = f"{user_info['login']}/{repo_name}"
    
    issues = auth_manager.github_api_call(f"repos/{repo_name}/issues", 
                                         params={"per_page": limit, "state": "open"})
    if not issues:
        return {"error": f"Failed to fetch issues for '{repo_name}'"}
    
    issue_list = []
    for issue in issues:
        # Skip pull requests (they appear as issues in GitHub API)
        if "pull_request" in issue:
            continue
            
        issue_info = {
            "number": issue.get("number"),
            "title": issue.get("title"),
            "body": issue.get("body", "")[:200] + ("..." if len(issue.get("body", "")) > 200 else ""),
            "state": issue.get("state"),
            "labels": [label["name"] for label in issue.get("labels", [])],
            "assignees": [assignee["login"] for assignee in issue.get("assignees", [])],
            "created_at": issue.get("created_at"),
            "updated_at": issue.get("updated_at"),
            "url": issue.get("html_url"),
            "author": issue.get("user", {}).get("login")
        }
        issue_list.append(issue_info)
    
    return {
        "issues": issue_list,
        "count": len(issue_list),
        "repository": repo_name
    }


# Tool registry for GitHub functions
GITHUB_TOOLS = {
    "get_github_user": {
        "function": get_github_user,
        "description": "Get authenticated GitHub user information",
        "parameters": {}
    },
    "list_github_repos": {
        "function": list_github_repos,
        "description": "List user's GitHub repositories",
        "parameters": {
            "limit": {"type": "integer", "description": "Maximum number of repos to return", "default": 10}
        }
    },
    "get_github_repo_info": {
        "function": get_github_repo_info,
        "description": "Get detailed information about a GitHub repository",
        "parameters": {
            "repo_name": {"type": "string", "description": "Repository name (owner/repo or just repo for user's repo)"}
        }
    },
    "get_github_repo_issues": {
        "function": get_github_repo_issues,
        "description": "Get issues for a GitHub repository",
        "parameters": {
            "repo_name": {"type": "string", "description": "Repository name (owner/repo or just repo for user's repo)"},
            "limit": {"type": "integer", "description": "Maximum number of issues to return", "default": 10}
        }
    }
}

# Aliases for backward compatibility
get_repository_info = get_github_repo_info