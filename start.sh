#!/bin/bash
echo "🤖 Multi-Agent Content Studio (FREE VERSION)"
echo "============================================="
echo "💚 Powered by Groq (Free) + DuckDuckGo (Free)"
echo ""

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Install from python.org"
    exit 1
fi

if [ ! -f .env ]; then
    cp .env.example .env 2>/dev/null
    echo "⚠️  Created .env — please add your FREE Groq API key"
    echo "   Get it free at: https://console.groq.com"
    echo ""
    read -p "Press Enter once you've added your GROQ_API_KEY to .env..."
fi

if [ ! -d venv ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

if [ ! -f venv/installed.txt ]; then
    echo "📥 Installing free dependencies..."
    pip install --upgrade pip -q
    pip install -r requirements.txt -q
    touch venv/installed.txt
    echo "✅ All dependencies installed!"
fi

echo ""
echo "🚀 Starting application..."
echo "   Open browser at: http://localhost:8501"
echo "   Press Ctrl+C to stop"
echo ""
streamlit run app.py
