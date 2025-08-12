"""Web search utilities for ANT."""

import requests
import json
from typing import Dict, Any, List
from urllib.parse import quote_plus


def search_duckduckgo(query: str, max_results: int = 5) -> Dict[str, Any]:
    """Search DuckDuckGo for information.
    
    Args:
        query: Search query
        max_results: Maximum number of results to return
        
    Returns:
        Dict containing search results
    """
    try:
        # DuckDuckGo Instant Answer API
        url = "https://api.duckduckgo.com/"
        params = {
            "q": query,
            "format": "json",
            "no_html": "1",
            "skip_disambig": "1"
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            results = {
                "query": query,
                "abstract": data.get("Abstract", ""),
                "answer": data.get("Answer", ""),
                "definition": data.get("Definition", ""),
                "related_topics": [],
                "results": []
            }
            
            # Add related topics
            for topic in data.get("RelatedTopics", [])[:3]:
                if isinstance(topic, dict) and "Text" in topic:
                    results["related_topics"].append({
                        "text": topic["Text"],
                        "url": topic.get("FirstURL", "")
                    })
            
            # Add web results if available
            for result in data.get("Results", [])[:max_results]:
                if isinstance(result, dict):
                    results["results"].append({
                        "title": result.get("Text", ""),
                        "url": result.get("FirstURL", "")
                    })
            
            return results
        else:
            return {"error": f"Search failed with status {response.status_code}"}
            
    except Exception as e:
        return {"error": f"Search failed: {str(e)}"}


def search_web(query: str) -> str:
    """Get a concise summary from web search.
    
    Args:
        query: Search query
        
    Returns:
        Formatted search summary
    """
    search_results = search_duckduckgo(query)
    
    if "error" in search_results:
        return f"Web search failed: {search_results['error']}"
    
    summary_parts = []
    
    # Add direct answer if available
    if search_results.get("answer"):
        summary_parts.append(f"Answer: {search_results['answer']}")
    
    # Add abstract if available
    if search_results.get("abstract"):
        summary_parts.append(f"Summary: {search_results['abstract']}")
    
    # Add definition if available  
    if search_results.get("definition"):
        summary_parts.append(f"Definition: {search_results['definition']}")
    
    # Add related topics
    if search_results.get("related_topics"):
        topics = [topic["text"][:100] + "..." if len(topic["text"]) > 100 else topic["text"] 
                 for topic in search_results["related_topics"]]
        summary_parts.append(f"Related: {'; '.join(topics)}")
    
    if summary_parts:
        return "\n".join(summary_parts)
    else:
        return f"No specific information found for '{query}'. You may need to search more specifically."


def search_news(query: str) -> Dict[str, Any]:
    """Search for recent news about a topic.
    
    Args:
        query: News search query
        
    Returns:
        Dict containing news results
    """
    # For now, use general search with news-focused query
    news_query = f"{query} news latest"
    return search_duckduckgo(news_query, max_results=3)


# Tool registry for web search functions
WEB_TOOLS = {
    "search_web": {
        "function": search_web,
        "description": "Search the web for information about a topic",
        "parameters": {
            "query": {"type": "string", "description": "Search query"}
        }
    },
    "search_news": {
        "function": search_news, 
        "description": "Search for recent news about a topic",
        "parameters": {
            "query": {"type": "string", "description": "News search query"}
        }
    }
}