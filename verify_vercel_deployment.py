#!/usr/bin/env python3
"""
Vercel Deployment Verification Script
Checks if all required files and configurations are in place for Vercel deployment
"""

import os
import sys
import json
from pathlib import Path

def check_deployment_readiness():
    """Verify Vercel deployment configuration"""
    
    print("\n" + "="*70)
    print("🚀 VERCEL DEPLOYMENT VERIFICATION")
    print("="*70 + "\n")
    
    checks = {
        "✅ Root FastAPI entrypoint": os.path.exists("app.py"),
        "✅ Alternative API entrypoint": os.path.exists("api/index.py"),
        "✅ Project configuration": os.path.exists("pyproject.toml"),
        "✅ Vercel config": os.path.exists("vercel.json"),
        "✅ Vercel ignore file": os.path.exists(".vercelignore"),
        "✅ Requirements file": os.path.exists("requirements.txt"),
        "✅ Main API module": os.path.exists("src/api_optimized.py"),
        "✅ Environment file": os.path.exists(".env") or os.path.exists(".env.example"),
    }
    
    all_passed = True
    for check, result in checks.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "="*70)
    print("📋 CONFIGURATION CONTENT VERIFICATION")
    print("="*70 + "\n")
    
    # Check vercel.json
    try:
        with open("vercel.json", "r") as f:
            vercel_config = json.load(f)
        print(f"✅ vercel.json is valid JSON")
        print(f"   Framework: {vercel_config.get('framework')}")
        print(f"   Build Command: {vercel_config.get('buildCommand')}")
        print(f"   Python Runtime: {vercel_config.get('env', {}).get('PYTHON_VERSION')}")
    except Exception as e:
        print(f"❌ Error reading vercel.json: {e}")
        all_passed = False
    
    # Check pyproject.toml
    try:
        with open("pyproject.toml", "r") as f:
            content = f.read()
        if "fastapi" in content and 'app = "app:app"' in content:
            print(f"✅ pyproject.toml has FastAPI and correct app reference")
        else:
            print(f"⚠️  pyproject.toml may be missing FastAPI or app reference")
    except Exception as e:
        print(f"❌ Error reading pyproject.toml: {e}")
        all_passed = False
    
    # Check app.py
    try:
        with open("app.py", "r") as f:
            content = f.read()
        if "from fastapi import" in content or "FastAPI" in content:
            print(f"✅ app.py imports FastAPI")
        if "app = " in content:
            print(f"✅ app.py exports 'app' variable")
        else:
            print(f"⚠️  app.py may not export 'app' variable")
    except Exception as e:
        print(f"❌ Error reading app.py: {e}")
        all_passed = False
    
    # Check requirements.txt
    try:
        with open("requirements.txt", "r") as f:
            reqs = f.read()
        required_packages = ["fastapi", "uvicorn", "gunicorn"]
        missing = [p for p in required_packages if p not in reqs]
        if not missing:
            print(f"✅ requirements.txt has all essential packages")
        else:
            print(f"❌ requirements.txt missing: {missing}")
            all_passed = False
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        all_passed = False
    
    print("\n" + "="*70)
    print("📁 DIRECTORY STRUCTURE")
    print("="*70 + "\n")
    
    key_dirs = [
        "src",
        "src/api_optimized.py",
        "templates",
        "data",
        "logs",
    ]
    
    for path in key_dirs:
        exists = os.path.exists(path)
        icon = "✅" if exists else "⚠️"
        print(f"{icon} {path}")
    
    print("\n" + "="*70)
    print("🔍 DEPLOYMENT STATUS")
    print("="*70 + "\n")
    
    if all_passed:
        print("✅ ALL CHECKS PASSED - Ready for Vercel deployment!")
        print("\n📍 Next Steps:")
        print("   1. Push code to main branch: git push origin main")
        print("   2. Vercel will automatically detect and deploy")
        print("   3. Monitor at: https://vercel.com/dashboard")
        print("   4. Your app will be available at: https://your-project.vercel.app")
    else:
        print("⚠️  Some checks failed - review errors above")
        print("   Fix issues before pushing to Vercel")
    
    print("\n" + "="*70 + "\n")
    
    return all_passed

if __name__ == "__main__":
    success = check_deployment_readiness()
    sys.exit(0 if success else 1)
