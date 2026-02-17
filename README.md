# 🤖 Multi-Agent Content Studio (FREE VERSION)

A fully free AI-powered content creation system using multiple specialized agents. **Zero cost — no paid APIs required!**

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-red.svg)
![Groq](https://img.shields.io/badge/Groq-Free%20Tier-orange.svg)
![DuckDuckGo](https://img.shields.io/badge/Search-DuckDuckGo%20Free-green.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 💚 100% Free Tools Used

| Tool | Purpose | Cost |
|------|---------|------|
| **Groq API** | LLM for all 3 agents | ✅ FREE (no credit card) |
| **DuckDuckGo Search** | Internet research | ✅ FREE (no API key) |
| **Streamlit** | Web UI | ✅ FREE (open source) |
| **Docker** | Containerization | ✅ FREE (optional) |

## 🎯 Overview

Three specialized AI agents work in sequence:

1. **Researcher Agent** 🔍 — Searches the web using DuckDuckGo (no API key needed), extracts keywords and facts
2. **Writer Agent** ✍️ — Creates SEO-optimized content using Groq's free Llama 3.3 model
3. **Reviewer Agent** 📋 — Reviews, edits, and polishes the final content using Groq

## 🚀 Quick Start (3 Steps)

### Step 1: Get Your FREE Groq API Key
1. Go to **https://console.groq.com** (no credit card needed!)
2. Sign up for free
3. Navigate to **API Keys → Create API Key**
4. Copy the key

### Step 2: Configure
```bash
cd multi_agent_studio
cp .env.example .env
# Edit .env and add your Groq key:
# GROQ_API_KEY=gsk_your_key_here
```

### Step 3: Run
```bash
# Option A: Startup script (auto setup)
./start.sh          # Linux/Mac
start.bat           # Windows

# Option B: Manual
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py

# Option C: Docker
docker-compose up -d
```

Open browser: **http://localhost:8501**

## 🧠 Free Models Available (via Groq)

| Model | Speed | Quality | Best For |
|-------|-------|---------|----------|
| `llama-3.3-70b-versatile` | Fast | ⭐⭐⭐⭐⭐ | Best quality (default) |
| `llama-3.1-8b-instant` | Very Fast | ⭐⭐⭐ | Quick drafts |
| `mixtral-8x7b-32768` | Fast | ⭐⭐⭐⭐ | Long content |
| `gemma2-9b-it` | Fast | ⭐⭐⭐ | Lightweight |

All models are **100% free** on Groq's free tier!

## 📁 Project Structure

```
multi_agent_studio/
├── app.py                  # Main Streamlit UI & orchestration
├── requirements.txt        # Python dependencies (all free)
├── .env.example           # Environment template
│
├── agents/                # AI Agent classes
│   ├── researcher.py      # Groq + DuckDuckGo research agent
│   ├── writer.py          # Groq content writing agent
│   └── reviewer.py        # Groq review/edit agent
│
├── tools/                 # Agent tools
│   └── search_tool.py     # DuckDuckGo search (free, no key)
│
├── utils/                 # Utilities
│   └── logger.py          # Activity logging
│
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose
└── start.sh / start.bat   # Automated startup scripts
```

## ⚙️ Configuration

`.env` file:
```env
# REQUIRED: Free Groq API Key
GROQ_API_KEY=gsk_your_key_here

# OPTIONAL
DEFAULT_MODEL=llama-3.3-70b-versatile
MAX_SEARCH_RESULTS=5
DEBUG_MODE=False
```

## 🐳 Docker Deployment

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## 🔧 Troubleshooting

**API Key Error**
- Get free key at https://console.groq.com
- Ensure `.env` has: `GROQ_API_KEY=gsk_...`

**Search not working**
- Check internet connection (DuckDuckGo requires internet)

**Module not found**
- Activate venv and run `pip install -r requirements.txt`

**Port in use**
- Run: `streamlit run app.py --server.port=8502`

## 📊 Groq Free Tier Limits

- **Requests per minute:** 30 RPM
- **Tokens per minute:** 14,400 TPM (varies by model)
- **Daily limit:** Very generous for personal use
- **Credit card:** Not required

For full limits see: https://console.groq.com/docs/rate-limits

## 📄 License

MIT License — Free to use, modify, and distribute.

---

**Made with ❤️ using 100% free tools — Groq + DuckDuckGo + Streamlit**
