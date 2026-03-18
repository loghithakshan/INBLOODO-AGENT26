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
    print("[VERCEL] DEPLOYMENT VERIFICATION")
    print("="*70 + "\n")
    
    valid_entrypoints = [
        "app.py",
        "index.py",
        "server.py",
        "src/app.py",
        "src/index.py",
        "src/server.py",
        "app/app.py",
        "app/index.py",
        "app/server.py",
    ]

    checks = {
        "[OK] FastAPI entrypoint present": any(os.path.exists(p) for p in valid_entrypoints),
        "[OK] Root FastAPI entrypoint": os.path.exists("app.py"),
        "[OK] Requirements file": os.path.exists("requirements.txt"),
        "[OK] Main API module": os.path.exists("src/api_optimized.py"),
        "[OK] Vercel config (optional)": os.path.exists("vercel.json"),
        "[OK] Vercel ignore file (recommended)": os.path.exists(".vercelignore"),
        "[OK] pyproject.toml script config (optional)": os.path.exists("pyproject.toml"),
        "[OK] Environment file": os.path.exists(".env") or os.path.exists(".env.example"),
    }
    
    all_passed = True
    for check, result in checks.items():
        status = "[PASS]" if result else "[FAIL]"
        print(f"{check}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "="*70)
    print("[CONFIG] CONTENT VERIFICATION")
    print("="*70 + "\n")
    
    # Check vercel.json (optional)
    if os.path.exists("vercel.json"):
        try:
            with open("vercel.json", "r") as f:
                vercel_config = json.load(f)
            print(f"[OK] vercel.json is valid JSON")
            print(f"   Build Command: {vercel_config.get('buildCommand')}")
        except Exception as e:
            print(f"[ERROR] Error reading vercel.json: {e}")
            all_passed = False
    else:
        print("[INFO] vercel.json not found (zero-config deployment is supported)")
    
    # Check pyproject.toml (optional)
    if os.path.exists("pyproject.toml"):
        try:
            with open("pyproject.toml", "r") as f:
                content = f.read()
            if 'app = "app:app"' in content:
                print(f"[OK] pyproject.toml has app script mapping")
            else:
                print(f"[WARN] pyproject.toml exists but has no app script mapping")
        except Exception as e:
            print(f"[ERROR] Error reading pyproject.toml: {e}")
            all_passed = False
    else:
        print("[INFO] pyproject.toml not found (not required for standard entrypoints)")
    
    # Check app.py
    try:
        with open("app.py", "r") as f:
            content = f.read()
        if "from fastapi import" in content or "FastAPI" in content:
            print(f"[OK] app.py imports FastAPI")
        if "app = " in content:
            print(f"[OK] app.py exports 'app' variable")
        else:
            print(f"[WARN] app.py may not export 'app' variable")
    except Exception as e:
        print(f"[ERROR] Error reading app.py: {e}")
        all_passed = False
    
    # Check requirements.txt
    try:
        with open("requirements.txt", "r") as f:
            reqs = f.read()
        required_packages = ["fastapi", "uvicorn", "gunicorn"]
        missing = [p for p in required_packages if p not in reqs]
        if not missing:
            print(f"[OK] requirements.txt has all essential packages")
        else:
            print(f"[ERROR] requirements.txt missing: {missing}")
            all_passed = False
    except Exception as e:
        print(f"[ERROR] Error reading requirements.txt: {e}")
        all_passed = False
    
    print("\n" + "="*70)
    print("[DIRS] DIRECTORY STRUCTURE")
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
        icon = "[OK]" if exists else "[MISS]"
        print(f"{icon} {path}")
    
    print("\n" + "="*70)
    print("[STATUS] DEPLOYMENT STATUS")
    print("="*70 + "\n")
    
    if all_passed:
        print("[ALL-OK] ALL CHECKS PASSED - Ready for Vercel deployment!")
        print("\n[NEXT] Next Steps:")
        print("   1. Push code to main branch: git push origin main")
        print("   2. Vercel will automatically detect and deploy")
        print("   3. Monitor at: https://vercel.com/dashboard")
        print("   4. Your app will be available at: https://your-project.vercel.app")
    else:
        print("[WARN] Some checks failed - review errors above")
        print("   Fix issues before pushing to Vercel")
    
    print("\n" + "="*70 + "\n")
    
    return all_passed

if __name__ == "__main__":
    success = check_deployment_readiness()
    sys.exit(0 if success else 1)
