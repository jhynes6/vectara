"""
Google Search tool for Vertex AI agents
Provides web search capability using Google Custom Search API
"""

import os
import logging
from typing import List, Dict, Any
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared import config

logger = logging.getLogger(__name__)


class GoogleSearchTool:
    """Tool for performing Google web searches"""
    
    def __init__(self, api_key: str = None, search_engine_id: str = None):
        """
        Initialize Google Search tool
        
        Args:
            api_key: Google API key (defaults to config)
            search_engine_id: Custom Search Engine ID (defaults to config)
        """
        self.api_key = api_key or config.GOOGLE_SEARCH_API_KEY
        self.search_engine_id = search_engine_id or config.GOOGLE_SEARCH_ENGINE_ID
        
        if not self.api_key or not self.search_engine_id:
            raise ValueError(
                "Google Search API key and Search Engine ID must be configured in .env file"
            )
        
        self.service = build("customsearch", "v1", developerKey=self.api_key)
    
    def search(
        self,
        query: str,
        num_results: int = 10,
        date_restrict: str = None
    ) -> List[Dict[str, Any]]:
        """
        Perform a Google search
        
        Args:
            query: Search query
            num_results: Number of results to return (max 10 per request)
            date_restrict: Date restriction (e.g., 'd7' for past week, 'm1' for past month)
            
        Returns:
            List of search results with title, link, snippet
        """
        try:
            logger.info(f"🔍 Searching Google for: {query}")
            
            search_kwargs = {
                'q': query,
                'cx': self.search_engine_id,
                'num': min(num_results, 10)  # API limit
            }
            
            if date_restrict:
                search_kwargs['dateRestrict'] = date_restrict
            
            result = self.service.cse().list(**search_kwargs).execute()
            
            items = result.get('items', [])
            
            results = []
            for item in items:
                results.append({
                    'title': item.get('title', ''),
                    'link': item.get('link', ''),
                    'snippet': item.get('snippet', ''),
                    'displayLink': item.get('displayLink', '')
                })
            
            logger.info(f"✅ Found {len(results)} results")
            return results
            
        except HttpError as e:
            logger.error(f"❌ Google Search API error: {e}")
            return []
        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
            return []
    
    def search_recent(
        self,
        query: str,
        num_results: int = 10,
        months: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Search for recent content (within specified months)
        
        Args:
            query: Search query
            num_results: Number of results
            months: How many months back to search
            
        Returns:
            List of search results
        """
        date_restrict = f"m{months}"
        return self.search(query, num_results, date_restrict)
    
    def format_results_for_llm(self, results: List[Dict[str, Any]]) -> str:
        """
        Format search results for LLM consumption
        
        Args:
            results: List of search results
            
        Returns:
            Formatted string for LLM
        """
        if not results:
            return "No search results found."
        
        formatted = "# Web Search Results\n\n"
        
        for i, result in enumerate(results, 1):
            formatted += f"## Result {i}: {result['title']}\n"
            formatted += f"**URL**: {result['link']}\n"
            formatted += f"**Source**: {result['displayLink']}\n"
            formatted += f"**Summary**: {result['snippet']}\n\n"
        
        return formatted


# For ADK integration
def create_google_search_function():
    """Create a function that can be used as an ADK tool"""
    
    search_tool = GoogleSearchTool()
    
    def search_web(query: str, recent_only: bool = False) -> str:
        """
        Search the web for information
        
        Args:
            query: Search query string
            recent_only: If True, only search content from past 3 months
            
        Returns:
            Formatted search results as a string
        """
        if recent_only:
            results = search_tool.search_recent(query, num_results=5)
        else:
            results = search_tool.search(query, num_results=5)
        
        return search_tool.format_results_for_llm(results)
    
    return search_web
