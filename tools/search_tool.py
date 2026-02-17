"""
Search Tool for Internet Research
Uses DuckDuckGo Search API (completely FREE - no API key needed)
Compatible with duckduckgo-search v6+
"""

from duckduckgo_search import DDGS
from typing import List, Dict
import os


class SearchTool:
    """Free internet search using DuckDuckGo — no API key required"""

    def __init__(self, max_results: int = 5):
        self.max_results = int(os.getenv("MAX_SEARCH_RESULTS", max_results))

    def search(self, query: str) -> List[Dict[str, str]]:
        """
        Search the internet for a given query

        Args:
            query: Search query string

        Returns:
            List of dicts with title, link, snippet
        """
        try:
            results = []
            with DDGS() as ddgs:
                for r in ddgs.text(query, max_results=self.max_results):
                    results.append({
                        "title":   r.get("title", ""),
                        "link":    r.get("href", ""),
                        "snippet": r.get("body", "")
                    })
            return results if results else [{"error": "No results found"}]
        except Exception as e:
            return [{"error": f"Search failed: {str(e)}"}]


# Tool description (kept for compatibility)
SEARCH_TOOL_DESCRIPTION = {
    "name": "search_internet",
    "description": "Search the internet for information on a given topic.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query"
            }
        },
        "required": ["query"]
    }
}
