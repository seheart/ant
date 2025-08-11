"""Date and time utilities for ANT."""

import datetime
from typing import Dict, Any


def get_current_time() -> Dict[str, Any]:
    """Get the current time and date information.
    
    Returns:
        Dict containing current time information
    """
    now = datetime.datetime.now()
    
    return {
        "current_time": now.strftime("%I:%M:%S %p"),
        "current_date": now.strftime("%A, %B %d, %Y"),
        "iso_datetime": now.isoformat(),
        "timezone": str(now.astimezone().tzinfo),
        "unix_timestamp": int(now.timestamp()),
        "day_of_week": now.strftime("%A"),
        "month": now.strftime("%B"),
        "year": now.year,
        "hour_24": now.hour,
        "minute": now.minute,
        "second": now.second
    }


def get_time_only() -> str:
    """Get just the current time as a formatted string.
    
    Returns:
        Current time in 12-hour format
    """
    return datetime.datetime.now().strftime("%I:%M:%S %p")


def get_date_only() -> str:
    """Get just the current date as a formatted string.
    
    Returns:
        Current date in readable format
    """
    return datetime.datetime.now().strftime("%A, %B %d, %Y")


def get_iso_datetime() -> str:
    """Get current datetime in ISO format.
    
    Returns:
        ISO formatted datetime string
    """
    return datetime.datetime.now().isoformat()


# Tool registry for function calling
DATETIME_TOOLS = {
    "get_current_time": {
        "function": get_current_time,
        "description": "Get comprehensive current time and date information",
        "parameters": {}
    },
    "get_time_only": {
        "function": get_time_only,
        "description": "Get only the current time in 12-hour format",
        "parameters": {}
    },
    "get_date_only": {
        "function": get_date_only,
        "description": "Get only the current date in readable format",
        "parameters": {}
    },
    "get_iso_datetime": {
        "function": get_iso_datetime,
        "description": "Get current datetime in ISO format",
        "parameters": {}
    }
}