"""
Multi-Agent Content Studio (FREE VERSION)
Powered by Groq (Free API) + DuckDuckGo (Free Search)
"""

import streamlit as st
import os
from dotenv import load_dotenv
from agents import ResearcherAgent, WriterAgent, ReviewerAgent
from utils.logger import agent_logger

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Multi-Agent Content Studio (Free)",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.8rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #6366f1, #8b5cf6, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        text-align: center;
        color: #888;
        margin-bottom: 0.5rem;
    }
    .free-badge {
        text-align: center;
        margin-bottom: 2rem;
    }
    .agent-card {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border: 1px solid #4f46e5;
        color: white;
    }
    .free-info {
        background: linear-gradient(135deg, #064e3b 0%, #065f46 100%);
        padding: 1rem 1.5rem;
        border-radius: 10px;
        border: 1px solid #10b981;
        color: #a7f3d0;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    if 'logs' not in st.session_state:
        st.session_state.logs = []


def check_api_key():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key_here":
        st.error("⚠️ Please set your GROQ_API_KEY in the .env file")

        st.markdown("""
        ### 🔑 How to get your FREE Groq API Key:
        1. Go to **https://console.groq.com**
        2. Sign up for **free** (no credit card needed!)
        3. Navigate to **API Keys**
        4. Click **Create API Key**
        5. Copy the key and paste it in your `.env` file:
        ```
        GROQ_API_KEY=gsk_your_key_here
        ```
        """)
        st.stop()
    return True


def run_multi_agent_pipeline(topic: str, model: str):
    """Orchestrate the multi-agent pipeline"""

    progress_bar = st.progress(0)
    status_text = st.empty()

    # ── Phase 1: Research ──────────────────────────────────────
    status_text.text("🔍 Phase 1/3: Researching topic (DuckDuckGo - Free)...")
    progress_bar.progress(10)

    with st.spinner("🔍 Researcher Agent is searching the internet..."):
        researcher = ResearcherAgent(model=model)
        research_results = researcher.research(topic)
        progress_bar.progress(33)

    if research_results.get("status") != "success":
        st.error(f"❌ Research failed: {research_results.get('findings')}")
        return

    with st.expander("📊 Research Findings", expanded=False):
        st.markdown(research_results.get("findings", ""))

    # ── Phase 2: Writing ───────────────────────────────────────
    status_text.text("✍️ Phase 2/3: Writing content (Groq LLM - Free)...")
    progress_bar.progress(40)

    with st.spinner("✍️ Writer Agent is crafting content..."):
        writer = WriterAgent(model=model)
        writing_results = writer.write(
            topic=topic,
            research_findings=research_results.get("findings", "")
        )
        progress_bar.progress(66)

    if writing_results.get("status") != "success":
        st.error(f"❌ Writing failed: {writing_results.get('draft')}")
        return

    with st.expander("📝 Content Draft", expanded=False):
        st.markdown(writing_results.get("draft", ""))

    # ── Phase 3: Review ────────────────────────────────────────
    status_text.text("📋 Phase 3/3: Reviewing and polishing (Groq LLM - Free)...")
    progress_bar.progress(75)

    with st.spinner("📋 Reviewer Agent is polishing the content..."):
        reviewer = ReviewerAgent(model=model)
        review_results = reviewer.review(
            topic=topic,
            draft=writing_results.get("draft", "")
        )
        progress_bar.progress(100)

    status_text.text("✅ All phases completed successfully!")

    # ── Final Output ───────────────────────────────────────────
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: #6366f1;'>🎉 Final Content Ready!</h2>",
                unsafe_allow_html=True)

    if review_results.get("status") == "success":
        with st.expander("📋 Review Report", expanded=False):
            st.markdown(review_results.get("review_report", ""))

        st.markdown("### ✨ Final Polished Content:")
        st.markdown("---")
        final_content = review_results.get("final_content", "")
        st.markdown(final_content)

        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📥 Download as Markdown",
                data=final_content,
                file_name=f"{topic.replace(' ', '_')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        with col2:
            st.download_button(
                label="📄 Download as Text",
                data=final_content,
                file_name=f"{topic.replace(' ', '_')}.txt",
                mime="text/plain",
                use_container_width=True
            )
    else:
        st.error("❌ Review phase failed. Please try again.")

    agent_logger.display_logs()


def main():
    initialize_session_state()
    check_api_key()

    # ── Header ─────────────────────────────────────────────────
    st.markdown("<h1 class='main-header'>🤖 Multi-Agent Content Studio</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>AI-Powered Content Creation — Research → Write → Review</p>",
                unsafe_allow_html=True)
    st.markdown("""
    <div class='free-badge'>
        <span style='background:#10b981;color:white;padding:4px 14px;border-radius:20px;font-size:0.85rem;font-weight:600;'>
            ✅ 100% FREE — No Paid APIs Required
        </span>
        &nbsp;
        <span style='background:#6366f1;color:white;padding:4px 14px;border-radius:20px;font-size:0.85rem;font-weight:600;'>
            ⚡ Powered by Groq + DuckDuckGo
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ── Sidebar ────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")

        model_option = st.selectbox(
            "🧠 Select Free Model (Groq)",
            [
                "llama-3.3-70b-versatile",
                "llama-3.1-8b-instant",
                "mixtral-8x7b-32768",
                "gemma2-9b-it",
            ],
            index=0,
            help="All models are FREE on Groq!"
        )

        st.markdown("---")
        st.markdown("""
        <div class='free-info'>
        <strong>💚 All FREE Tools Used:</strong><br><br>
        🔍 <strong>DuckDuckGo Search</strong><br>
        &nbsp;&nbsp;&nbsp;No API key needed<br><br>
        🤖 <strong>Groq LLM API</strong><br>
        &nbsp;&nbsp;&nbsp;Free tier available<br>
        &nbsp;&nbsp;&nbsp;<a href='https://console.groq.com' style='color:#6ee7b7'>Get key →</a><br><br>
        🖥️ <strong>Streamlit UI</strong><br>
        &nbsp;&nbsp;&nbsp;Open source & free
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("## 🤖 Agent Pipeline")
        st.markdown("""
**1. 🔍 Researcher**
- Searches web (DuckDuckGo)
- Extracts keywords & facts

**2. ✍️ Writer**
- Creates SEO content
- Structures the article

**3. 📋 Reviewer**
- Fixes errors
- Polishes final output
        """)

        st.markdown("---")
        # API Status
        if os.getenv("GROQ_API_KEY") and os.getenv("GROQ_API_KEY") != "your_groq_api_key_here":
            st.success("✅ Groq API Key Set")
        else:
            st.error("❌ Groq API Key Missing")
            st.markdown("[Get free key →](https://console.groq.com)")

    # ── Main Input Area ────────────────────────────────────────
    col1, col2 = st.columns([4, 1])

    with col1:
        topic = st.text_input(
            "📝 Enter your content topic:",
            placeholder="e.g., Benefits of AI in Healthcare, SEO Best Practices 2025...",
            help="Enter any topic — agents will research, write, and review automatically!"
        )

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        run_button = st.button("🚀 Generate", type="primary", use_container_width=True)

    # ── Info Cards ─────────────────────────────────────────────
    if not run_button:
        st.markdown("---")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div class='agent-card'>
                <h3>🔍 Researcher Agent</h3>
                <p>Searches DuckDuckGo (free) for trends, keywords, and facts about your topic.</p>
                <small style='color:#a5b4fc'>Tool: DuckDuckGo • No API Key</small>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class='agent-card'>
                <h3>✍️ Writer Agent</h3>
                <p>Creates a full SEO-optimized article using Groq's free Llama 3.3 model.</p>
                <small style='color:#a5b4fc'>Model: Llama 3.3 70B • Groq Free</small>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class='agent-card'>
                <h3>📋 Reviewer Agent</h3>
                <p>Reviews and polishes the content, fixes errors, and ensures quality.</p>
                <small style='color:#a5b4fc'>Model: Llama 3.3 70B • Groq Free</small>
            </div>
            """, unsafe_allow_html=True)

        # Example topics
        st.markdown("---")
        st.markdown("### 💡 Try these example topics:")
        ecols = st.columns(4)
        examples = [
            "AI in Healthcare",
            "SEO Best Practices 2025",
            "Remote Work Productivity",
            "Climate Change Solutions"
        ]
        for i, ex in enumerate(examples):
            with ecols[i]:
                if st.button(ex, use_container_width=True):
                    topic = ex

    # ── Run Pipeline ───────────────────────────────────────────
    if run_button:
        if not topic or not topic.strip():
            st.warning("⚠️ Please enter a topic first!")
        else:
            st.markdown("---")
            run_multi_agent_pipeline(topic.strip(), model_option)


if __name__ == "__main__":
    main()
