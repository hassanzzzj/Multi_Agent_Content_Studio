"""
Reviewer Agent (Powered by Groq - FREE)
Responsible for reviewing content, fixing errors, and ensuring quality
Uses: Groq API (free tier)
"""

from groq import Groq
from typing import Dict
import os
from utils.logger import agent_logger


class ReviewerAgent:
    """
    Expert Content Reviewer and Editor Agent
    Powered by Groq Free API
    """

    def __init__(self, model: str = None):
        self.name = "Content Reviewer"
        self.model = model or os.getenv("DEFAULT_MODEL", "llama-3.3-70b-versatile")
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        self.system_prompt = """You are an expert Content Reviewer, Editor, and Quality Assurance Specialist.

Your responsibilities:
1. Review content for grammar, spelling, and punctuation errors
2. Check logical flow and structure
3. Ensure SEO optimization is properly implemented
4. Improve clarity and engagement
5. Fix any inconsistencies or errors

Review Checklist:
✓ Grammar and spelling
✓ Sentence structure and flow
✓ Heading hierarchy
✓ Keyword placement and density
✓ Content accuracy and completeness
✓ Tone consistency
✓ Readability

Always provide:
1. A brief review report with identified issues
2. The final polished version of the content"""

    def review(self, topic: str, draft: str) -> Dict[str, any]:
        """
        Review and improve the content draft

        Args:
            topic: The original topic
            draft: The draft content from the Writer agent

        Returns:
            Dictionary containing review feedback and final content
        """
        agent_logger.log_agent_start(self.name, f"Reviewing content for: {topic}")

        try:
            prompt = f"""Review and improve the following content draft about "{topic}".

DRAFT CONTENT:
{draft}

Provide your response in EXACTLY this format:

### REVIEW REPORT
[List the issues found: grammar, structure, SEO improvements, etc. Be specific but concise.]

### FINAL CONTENT
[The fully polished, corrected, and improved version of the article in Markdown format]"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=3500,
                temperature=0.3
            )

            review_output = response.choices[0].message.content

            # Parse review report and final content
            review_report = "Review completed."
            final_content = review_output

            if "### FINAL CONTENT" in review_output:
                parts = review_output.split("### FINAL CONTENT")
                if len(parts) == 2:
                    review_report = parts[0].replace("### REVIEW REPORT", "").strip()
                    final_content = parts[1].strip()

            agent_logger.log_agent_complete(self.name, final_content[:100])

            return {
                "agent": self.name,
                "review_report": review_report,
                "final_content": final_content,
                "status": "success"
            }

        except Exception as e:
            agent_logger.log_agent_error(self.name, str(e))
            return {
                "agent": self.name,
                "review_report": f"Review error: {str(e)}",
                "final_content": draft,
                "status": "error"
            }
