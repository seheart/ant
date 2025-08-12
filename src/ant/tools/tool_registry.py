"""Tool registry for ANT function calling."""

from typing import Dict, Any, Callable
from .datetime_tools import DATETIME_TOOLS
from .web_tools import WEB_TOOLS
from .github_tools import GITHUB_TOOLS


class ToolRegistry:
    """Registry for all available tools/functions."""
    
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Register default tools."""
        self.tools.update(DATETIME_TOOLS)
        self.tools.update(WEB_TOOLS)
        self.tools.update(GITHUB_TOOLS)
    
    def register_tool(self, name: str, function: Callable, description: str, parameters: Dict[str, Any] = None):
        """Register a new tool.
        
        Args:
            name: Tool name
            function: Function to call
            description: Tool description
            parameters: Parameter schema
        """
        self.tools[name] = {
            "function": function,
            "description": description,
            "parameters": parameters or {}
        }
    
    def get_tool(self, name: str) -> Dict[str, Any]:
        """Get a tool by name.
        
        Args:
            name: Tool name
            
        Returns:
            Tool definition or None if not found
        """
        return self.tools.get(name)
    
    def list_tools(self) -> Dict[str, str]:
        """List all available tools.
        
        Returns:
            Dict mapping tool names to descriptions
        """
        return {name: tool["description"] for name, tool in self.tools.items()}
    
    def call_tool(self, name: str, **kwargs) -> Any:
        """Call a tool by name.
        
        Args:
            name: Tool name
            **kwargs: Tool parameters
            
        Returns:
            Tool result
            
        Raises:
            ValueError: If tool not found
        """
        tool = self.get_tool(name)
        if not tool:
            raise ValueError(f"Tool '{name}' not found")
        
        return tool["function"](**kwargs)


# Global tool registry instance
tool_registry = ToolRegistry()