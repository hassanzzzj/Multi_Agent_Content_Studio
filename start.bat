@echo off
REM Multi-Agent Content Studio Startup Script for Windows
REM This script checks prerequisites and starts the application

echo.
echo 🤖 Multi-Agent Content Studio - Startup Script
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed
    echo Please install Python 3.11 or higher from python.org
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist .env (
    echo ⚠️  Warning: .env file not found
    if exist .env.example (
        echo Creating .env from .env.example...
        copy .env.example .env
        echo ✅ Created .env file
        echo ⚠️  Please edit .env and add your ANTHROPIC_API_KEY
        echo.
        pause
    ) else (
        echo ❌ Error: .env.example not found
        pause
        exit /b 1
    )
)

REM Check if virtual environment exists
if not exist venv (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
if not exist venv\installed.txt (
    echo 📥 Installing dependencies...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    echo. > venv\installed.txt
    echo ✅ Dependencies installed
) else (
    echo ✅ Dependencies already installed
)

echo.
echo 🚀 Starting Multi-Agent Content Studio...
echo ================================================
echo.
echo The application will open in your default browser.
echo Press Ctrl+C to stop the server.
echo.

REM Start Streamlit
streamlit run app.py

REM Deactivate virtual environment
call venv\Scripts\deactivate.bat
