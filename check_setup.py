#!/usr/bin/env python3
"""
Configuration and Environment Checker for FREE version
Validates Groq API key and all free dependencies
"""

import sys
import os
from pathlib import Path


def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def check_python_version():
    print("🐍 Checking Python version...")
    version = sys.version_info
    ok = version.major == 3 and version.minor >= 11
    status = f"Python {version.major}.{version.minor}.{version.micro}"
    print(f"   {'✅' if ok else '⚠️ '} {status} {'(OK)' if ok else '(3.11+ recommended)'}")
    return ok


def check_dependencies():
    print("\n📦 Checking free dependencies...")
    packages = {
        'streamlit': 'Streamlit UI',
        'groq': 'Groq LLM (Free API)',
        'dotenv': 'python-dotenv',
        'duckduckgo_search': 'DuckDuckGo Search (Free)',
        'requests': 'Requests',
        'loguru': 'Loguru Logger',
        'pydantic': 'Pydantic',
    }

    all_ok = True
    for pkg, label in packages.items():
        try:
            __import__(pkg)
            print(f"   ✅ {label}")
        except ImportError:
            print(f"   ❌ {label} — run: pip install -r requirements.txt")
            all_ok = False
    return all_ok


def check_env_file():
    print("\n🔐 Checking environment configuration...")
    env_path = Path('.env')

    if not env_path.exists():
        if Path('.env.example').exists():
            import shutil
            shutil.copy('.env.example', '.env')
            print("   ✅ Created .env from .env.example")
        print("   ⚠️  Please add your FREE Groq API key to .env")
        print("   Get key at: https://console.groq.com (no credit card!)")
        return False

    content = env_path.read_text()
    if 'GROQ_API_KEY=' not in content:
        print("   ❌ GROQ_API_KEY not found in .env")
        return False
    if 'your_groq_api_key_here' in content:
        print("   ⚠️  GROQ_API_KEY not set — add your key from https://console.groq.com")
        return False

    print("   ✅ GROQ_API_KEY configured")
    return True


def check_project_structure():
    print("\n📁 Checking project structure...")
    required = [
        'app.py', 'requirements.txt', '.env.example',
        'agents/__init__.py', 'agents/researcher.py',
        'agents/writer.py', 'agents/reviewer.py',
        'tools/__init__.py', 'tools/search_tool.py',
        'utils/__init__.py', 'utils/logger.py',
        'Dockerfile',
    ]
    all_ok = True
    for item in required:
        exists = Path(item).exists()
        print(f"   {'✅' if exists else '❌'} {item}")
        if not exists:
            all_ok = False
    return all_ok


def check_docker():
    print("\n🐳 Checking Docker (optional)...")
    try:
        import subprocess
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"   ✅ {result.stdout.strip()}")
            return True
    except Exception:
        pass
    print("   ⚠️  Docker not found (optional for deployment)")
    return False


def main():
    print_header("Multi-Agent Content Studio (FREE) — Environment Check")

    results = {
        'Python Version': check_python_version(),
        'Free Dependencies': check_dependencies(),
        'Environment (Groq Key)': check_env_file(),
        'Project Structure': check_project_structure(),
        'Docker (optional)': check_docker(),
    }

    print_header("Summary")
    for check, passed in results.items():
        print(f"{check:.<45} {'✅ PASS' if passed else '⚠️  ATTENTION'}")

    critical_ok = all([results['Python Version'], results['Free Dependencies'],
                       results['Environment (Groq Key)'], results['Project Structure']])

    print("\n" + "="*60)
    if critical_ok:
        print("🎉 All checks passed! Run: streamlit run app.py")
        print("\n💚 Using 100% free tools:")
        print("   • Groq API (free tier)")
        print("   • DuckDuckGo Search (no key needed)")
    else:
        print("⚠️  Fix the issues above, then run: streamlit run app.py")
        print("\n🔑 Get your FREE Groq API key at:")
        print("   https://console.groq.com (no credit card!)")
    print("="*60 + "\n")

    return 0 if critical_ok else 1


if __name__ == "__main__":
    sys.exit(main())
