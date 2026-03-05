#!/usr/bin/env python
"""
Quick Start Server - Handles setup and starts the Blood Report AI server
"""
import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def check_python():
    """Verify Python version"""
    print_header("Checking Python")
    version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"✓ Python {version}")
    if sys.version_info < (3, 8):
        print("❌ ERROR: Python 3.8+ required")
        sys.exit(1)

def check_venv():
    """Check if virtual environment is activated"""
    print_header("Checking Virtual Environment")
    venv = os.getenv('VIRTUAL_ENV')
    if venv:
        print(f"✓ Virtual environment active: {venv}")
    else:
        print("⚠️  WARNING: Virtual environment not detected")
        print("   Run: python -m venv venv")
        print("   Then: venv\\Scripts\\activate")

def check_dependencies():
    """Check if key dependencies are installed"""
    print_header("Checking Dependencies")
    
    required = [
        ('fastapi', 'FastAPI'),
        ('uvicorn', 'Uvicorn'),
        ('sqlalchemy', 'SQLAlchemy'),
        ('dotenv', 'Python-dotenv'),
    ]
    
    missing = []
    for package, name in required:
        try:
            __import__(package)
            print(f"✓ {name}")
        except ImportError:
            print(f"❌ {name} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("\nInstalling missing packages...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=False)
        return False
    return True

def check_directories():
    """Create necessary directories"""
    print_header("Checking Directories")
    
    dirs = [
        "data/uploads",
        "logs",
        "reports",
        "templates",
        "src",
    ]
    
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
        print(f"✓ {d}")

def check_env_file():
    """Check for .env file"""
    print_header("Checking Configuration")
    
    if Path(".env").exists():
        print("✓ .env file found")
    else:
        print("⚠️  .env file not found, using defaults")
        print("   Default: HOST=0.0.0.0, PORT=8000")

def start_server():
    """Start the server"""
    print_header("Starting Server")
    
    try:
        import uvicorn
        from main import app
        
        host = os.getenv("HOST", "0.0.0.0")
        port = int(os.getenv("PORT", "8000"))
        
        print(f"\n✓ Server starting on http://localhost:{port}")
        print(f"✓ API Docs:  http://localhost:{port}/docs")
        print(f"✓ Health:    http://localhost:{port}/health")
        print("\n📌 Press CTRL+C to stop the server\n")
        
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=False,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ ERROR starting server: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    try:
        check_python()
        check_venv()
        check_directories()
        check_env_file()
        check_dependencies()
        start_server()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        sys.exit(1)
