"""Personal learning tools for capturing insights about Seth."""

from typing import Dict, Any
from ant.learning.personal_memory import personal_memory


def record_personality_insight(category: str, trait_name: str, trait_value: str, 
                              confidence: float = 0.8, notes: str = None) -> Dict[str, Any]:
    """Record a personality insight about Seth.
    
    Args:
        category: Category like 'communication', 'working_style', 'values'
        trait_name: Specific trait name
        trait_value: The trait value or description
        confidence: Confidence level (0.0 to 1.0)
        notes: Additional notes about this trait
        
    Returns:
        Dict containing success status
    """
    try:
        personal_memory.record_personality_trait(
            category, trait_name, trait_value, confidence, notes
        )
        return {
            "success": True,
            "message": f"Recorded personality insight: {trait_name} = {trait_value}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to record insight: {str(e)}"
        }


def record_conversation_insight(insight_type: str, insight: str, 
                               context: str = None, confidence: float = 0.8) -> Dict[str, Any]:
    """Record an insight from our conversation.
    
    Args:
        insight_type: Type like 'preference', 'communication_style', 'goal'
        insight: The actual insight text
        context: Context where this was observed
        confidence: Confidence level (0.0 to 1.0)
        
    Returns:
        Dict containing success status
    """
    try:
        personal_memory.record_conversation_insight(
            insight_type, insight, context, confidence
        )
        return {
            "success": True,
            "message": f"Recorded conversation insight: {insight}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to record insight: {str(e)}"
        }


def record_personal_preference(category: str, preference_name: str, 
                              preference_value: str, reasoning: str = None,
                              confidence: float = 0.8) -> Dict[str, Any]:
    """Record a personal preference about Seth.
    
    Args:
        category: Category like 'communication', 'tools', 'workflow'
        preference_name: Specific preference name
        preference_value: The preference value
        reasoning: Why this preference exists
        confidence: Confidence level (0.0 to 1.0)
        
    Returns:
        Dict containing success status
    """
    try:
        personal_memory.record_personal_preference(
            category, preference_name, preference_value, reasoning, confidence
        )
        return {
            "success": True,
            "message": f"Recorded preference: {preference_name} = {preference_value}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to record preference: {str(e)}"
        }


def update_relationship_context(context_type: str, context_key: str,
                               context_value: str, importance: float = 0.8) -> Dict[str, Any]:
    """Update how we relate and communicate.
    
    Args:
        context_type: Type like 'communication', 'relationship', 'goals'
        context_key: Specific aspect
        context_value: How this works for us
        importance: How important this is (0.0 to 1.0)
        
    Returns:
        Dict containing success status
    """
    try:
        personal_memory.update_relationship_context(
            context_type, context_key, context_value, importance
        )
        return {
            "success": True,
            "message": f"Updated relationship context: {context_key}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to update context: {str(e)}"
        }


def get_personal_summary() -> Dict[str, Any]:
    """Get a summary of what I know about Seth.
    
    Returns:
        Dict containing personality profile and insights
    """
    try:
        profile = personal_memory.get_personality_profile()
        recent_insights = personal_memory.get_recent_insights(10)
        
        return {
            "success": True,
            "personality_profile": profile,
            "recent_insights": recent_insights,
            "conversation_context": personal_memory.get_conversation_context()
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to get personal summary: {str(e)}"
        }


# Tool registry for personal learning functions
PERSONAL_LEARNING_TOOLS = {
    "record_personality_insight": {
        "function": record_personality_insight,
        "description": "Record a personality insight about Seth (communication style, values, etc.)",
        "parameters": {
            "category": {"type": "string", "description": "Category like 'communication', 'working_style', 'values'"},
            "trait_name": {"type": "string", "description": "Specific trait name"},
            "trait_value": {"type": "string", "description": "The trait value or description"},
            "confidence": {"type": "number", "description": "Confidence level 0.0-1.0", "default": 0.8},
            "notes": {"type": "string", "description": "Additional notes", "default": None}
        }
    },
    "record_conversation_insight": {
        "function": record_conversation_insight,
        "description": "Record an insight from our conversation",
        "parameters": {
            "insight_type": {"type": "string", "description": "Type like 'preference', 'communication_style', 'goal'"},
            "insight": {"type": "string", "description": "The actual insight text"},
            "context": {"type": "string", "description": "Context where observed", "default": None},
            "confidence": {"type": "number", "description": "Confidence level 0.0-1.0", "default": 0.8}
        }
    },
    "record_personal_preference": {
        "function": record_personal_preference,
        "description": "Record a personal preference about Seth",
        "parameters": {
            "category": {"type": "string", "description": "Category like 'communication', 'tools', 'workflow'"},
            "preference_name": {"type": "string", "description": "Specific preference name"},
            "preference_value": {"type": "string", "description": "The preference value"},
            "reasoning": {"type": "string", "description": "Why this preference exists", "default": None},
            "confidence": {"type": "number", "description": "Confidence level 0.0-1.0", "default": 0.8}
        }
    },
    "get_personal_summary": {
        "function": get_personal_summary,
        "description": "Get a summary of what I know about Seth personally",
        "parameters": {}
    }
}