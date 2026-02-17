"""
Logger utility for multi-agent system
Provides structured logging for agents and tools
"""

import sys
from loguru import logger
from datetime import datetime
import streamlit as st


class AgentLogger:
    """Custom logger for agent activities"""
    
    def __init__(self):
        # Configure loguru
        logger.remove()  # Remove default handler
        logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
            level="INFO"
        )
    
    def log_agent_start(self, agent_name: str, task: str):
        """Log when an agent starts working"""
        logger.info(f"🤖 {agent_name} started: {task}")
        if 'logs' not in st.session_state:
            st.session_state.logs = []
        st.session_state.logs.append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "agent": agent_name,
            "message": f"Started: {task}",
            "type": "start"
        })
    
    def log_agent_complete(self, agent_name: str, result_preview: str = ""):
        """Log when an agent completes its task"""
        logger.success(f"✅ {agent_name} completed")
        if 'logs' not in st.session_state:
            st.session_state.logs = []
        st.session_state.logs.append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "agent": agent_name,
            "message": f"Completed: {result_preview[:50]}...",
            "type": "complete"
        })
    
    def log_agent_error(self, agent_name: str, error: str):
        """Log when an agent encounters an error"""
        logger.error(f"❌ {agent_name} error: {error}")
        if 'logs' not in st.session_state:
            st.session_state.logs = []
        st.session_state.logs.append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "agent": agent_name,
            "message": f"Error: {error}",
            "type": "error"
        })
    
    def log_tool_use(self, tool_name: str, query: str):
        """Log when a tool is used"""
        logger.debug(f"🔧 Tool used: {tool_name} - Query: {query}")
    
    def display_logs(self):
        """Display logs in Streamlit UI"""
        if 'logs' in st.session_state and st.session_state.logs:
            with st.expander("📋 Agent Activity Logs", expanded=False):
                for log in st.session_state.logs:
                    icon = "🟢" if log["type"] == "start" else "✅" if log["type"] == "complete" else "🔴"
                    st.text(f"{icon} [{log['time']}] {log['agent']}: {log['message']}")


# Global logger instance
agent_logger = AgentLogger()
