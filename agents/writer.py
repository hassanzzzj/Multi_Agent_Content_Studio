"""
Writer Agent (Powered by Groq - FREE)
Responsible for creating high-quality content drafts based on research findings
Uses: Groq API (free tier)
"""

from groq import Groq
from typing import Dict
import os
from utils.logger import agent_logger


class WriterAgent:
    """
    Expert Content Writer Agent
    Powered by Groq Free API
    """

    def __init__(self, model: str = None):
        self.name = "Content Writer"
        self.model = model or os.getenv("DEFAULT_MODEL", "llama-3.3-70b-versatile")
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        self.system_prompt = """You are an expert Content Writer and SEO Specialist.

Your responsibilities:
1. Create engaging, well-structured content based on research findings
2. Incorporate SEO keywords naturally throughout the content
3. Write in a clear, professional, and engaging tone
4. Structure content with proper headings and sections
5. Ensure content is informative and valuable to readers

Content Guidelines:
- Use H1, H2, H3 headings with # ## ### markdown
- Write compelling introductions and conclusions
- Include relevant keywords naturally (avoid keyword stuffing)
- Use short paragraphs for readability
- Add bullet points or numbered lists where appropriate
- Aim for 800-1000 words

Always create content that is valuable, original, and SEO-optimized."""

    def write(self, topic: str, research_findings: str) -> Dict[str, any]:
        """
        Create a content draft based on research findings

        Args:
            topic: The main topic for the content
            research_findings: Research data from the Researcher agent

        Returns:
            Dictionary containing the written draft
        """
        agent_logger.log_agent_start(self.name, f"Writing content for: {topic}")

        try:
            prompt = f"""Based on the following research findings, write a comprehensive, SEO-optimized article about "{topic}".

RESEARCH FINDINGS:
{research_findings}

Write a complete article that:
1. Has a compelling H1 title (# Title)
2. Includes an engaging introduction
3. Covers all key points from the research
4. Uses relevant keywords naturally
5. Has clear H2 section headings (## Section)
6. Ends with a strong conclusion
7. Is approximately 800-1000 words

Write the complete article now in Markdown format:"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=3000,
                temperature=0.7
            )

            draft = response.choices[0].message.content
            agent_logger.log_agent_complete(self.name, draft[:100])

            return {
                "agent": self.name,
                "draft": draft,
                "status": "success"
            }

        except Exception as e:
            agent_logger.log_agent_error(self.name, str(e))
            return {
                "agent": self.name,
                "draft": f"Writing error: {str(e)}",
                "status": "error"
            }
