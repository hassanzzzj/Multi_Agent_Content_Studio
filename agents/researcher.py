"""
Researcher Agent (Powered by Groq - FREE)
Responsible for internet research, keyword extraction, and fact-finding
Uses: Groq API (free) + DuckDuckGo Search (free, no key needed)
"""

from groq import Groq
from typing import Dict
import os
from tools.search_tool import SearchTool
from utils.logger import agent_logger


class ResearcherAgent:
    """
    Expert SEO Researcher Agent
    Powered by Groq (Free) + DuckDuckGo (Free)
    """

    def __init__(self, model: str = None):
        self.name = "SEO Researcher"
        self.model = model or os.getenv("DEFAULT_MODEL", "llama-3.3-70b-versatile")
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.search_tool = SearchTool()

        self.system_prompt = """You are an expert SEO Researcher and Content Strategist.

Your responsibilities:
1. Research the given topic thoroughly using the provided search results
2. Extract relevant keywords and trending terms
3. Find factual information and statistics
4. Identify content gaps and opportunities
5. Provide structured research findings

Always provide your findings in a structured format with:
- Top Keywords (10-15 relevant terms)
- Key Facts and Statistics
- Content Opportunities
- Trending Topics
- Recommended Focus Areas

Be thorough, accurate, and data-driven in your research."""

    def _search_and_compile(self, topic: str) -> str:
        """Search multiple angles and compile results"""
        queries = [
            topic,
            f"{topic} latest trends 2024 2025",
            f"{topic} statistics facts benefits",
        ]

        all_results = []
        for query in queries:
            agent_logger.log_tool_use("DuckDuckGo Search (Free)", query)
            results = self.search_tool.search(query)
            if results and "error" not in results[0]:
                all_results.append(f"\n=== Search: '{query}' ===")
                for i, r in enumerate(results[:3], 1):
                    all_results.append(
                        f"{i}. {r.get('title', '')}\n"
                        f"   {r.get('snippet', '')}\n"
                        f"   Source: {r.get('link', '')}"
                    )

        return "\n".join(all_results) if all_results else "No search results found."

    def research(self, topic: str) -> Dict[str, any]:
        """
        Conduct comprehensive research on the given topic

        Args:
            topic: The topic to research

        Returns:
            Dictionary containing research findings
        """
        agent_logger.log_agent_start(self.name, f"Researching: {topic}")

        try:
            # Step 1: Gather free search results via DuckDuckGo
            search_data = self._search_and_compile(topic)

            # Step 2: Ask Groq (free) to analyze and structure findings
            prompt = f"""Based on the following internet search results about "{topic}", provide comprehensive research findings.

SEARCH RESULTS:
{search_data}

Please analyze and provide:

## 🔑 Top Keywords (10-15)
List the most relevant SEO keywords

## 📊 Key Facts & Statistics
List important facts and numbers found

## 🎯 Content Opportunities
What angles/topics should we cover?

## 📈 Trending Topics
What's currently trending about this topic?

## ✅ Recommended Focus Areas
What are the most important points to address?

Be specific and use the actual search data provided."""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.3
            )

            findings = response.choices[0].message.content
            agent_logger.log_agent_complete(self.name, findings[:100])

            return {
                "agent": self.name,
                "findings": findings,
                "raw_search_data": search_data,
                "status": "success"
            }

        except Exception as e:
            agent_logger.log_agent_error(self.name, str(e))
            return {
                "agent": self.name,
                "findings": f"Research error: {str(e)}",
                "status": "error"
            }
