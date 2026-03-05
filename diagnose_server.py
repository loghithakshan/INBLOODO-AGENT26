#!/usr/bin/env python
"""
Diagnostic script to identify why the server won't start or can't be reached
"""
import os
import sys
import subprocess
from pathlib import Path

def test(name, func):
    """Run a test and print result"""
    try:
        result = func()
        if result:
            print(f"✅ {name}")
            return True
        else:
            print(f"❌ {name}")
            return False
    except Exception as e:
        print(f"❌ {name}: {str(e)}")
        return False

def check_python_version():
    return sys.version_info >= (3, 8)

def check_venv():
    return os.getenv('VIRTUAL_ENV') is not None or Path("venv").exists()

def check_fastapi():
    try:
        import fastapi
        return True
    except ImportError:
        return False

def check_uvicorn():
    try:
        import uvicorn
        return True
    except ImportError:
        return False

def check_directories():
    dirs = ["data/uploads", "logs", "reports"]
    return all(Path(d).exists() or Path(d).mkdir(parents=True, exist_ok=True) for d in dirs)

def check_env_file():
    return Path(".env").exists() or Path(".env.example").exists()

def check_port_available():
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex(('localhost', 8000))
        s.close()
        return result != 0  # True if port is available (not in use)
    except:
        return True

def check_api_import():
    try:
        from src.api_optimized import app
        return True
    except ImportError as e:
        print(f"     Import error: {e}")
        return False
    except SyntaxError as e:
        print(f"     Syntax error: {e}")
        return False

print("\n" + "="*70)
print("BLOOD REPORT AI - DIAGNOSTIC CHECK")
print("="*70 + "\n")

print("🔍 ENVIRONMENT CHECK:")
test("Python 3.8+", check_python_version)
test("Virtual Environment", check_venv)

print("\n🔍 DEPENDENCIES CHECK:")
test("FastAPI installed", check_fastapi)
test("Uvicorn installed", check_uvicorn)

print("\n🔍 CONFIGURATION CHECK:")
test("Required directories exist", check_directories)
test(".env file exists", check_env_file)
test("Port 8000 available", check_port_available)

print("\n🔍 API MODULE CHECK:")
test("API module can be imported", check_api_import)

print("\n" + "="*70)

# Give recommendations
if not check_fastapi() or not check_uvicorn():
    print("\n⚠️  RECOMMENDATION: Install missing dependencies")
    print("   Run: pip install -r requirements.txt")

if not check_venv():
    print("\n⚠️  RECOMMENDATION: Create and activate virtual environment")
    print("   Run: python -m venv venv")
    print("        .\\venv\\Scripts\\activate")

if not check_port_available():
    print("\n⚠️  RECOMMENDATION: Port 8000 is already in use")
    print("   Option 1: Kill the process using port 8000")
    print("   Option 2: Use different port (set PORT=8001)")

print("\n" + "="*70)
print("\nTO START THE SERVER:")
print("   1. Run: python quick_start.py")
print("   2. Or double-click: START_SERVER.bat")
print("   3. Then open: http://localhost:8000/health")
print("\n" + "="*70 + "\n")
