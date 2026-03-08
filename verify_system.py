#!/usr/bin/env python3
"""
INBLOODO Agent - Comprehensive System Verification
Tests all critical components and endpoints
"""

import requests
import json
import sys
from datetime import datetime

BASE_URL = "http://localhost:8000"
PUBLIC_URL = "https://impalpable-perspectively-andria.ngrok-free.dev"

print("\n" + "="*70)
print("🩺 INBLOODO AGENT - SYSTEM VERIFICATION")
print("="*70)
print(f"Timestamp: {datetime.now().isoformat()}\n")

# Test results tracking
tests_passed = 0
tests_failed = 0

def test_endpoint(method, endpoint, name, data=None, is_public=False):
    """Test an API endpoint"""
    global tests_passed, tests_failed
    
    url = (PUBLIC_URL if is_public else BASE_URL) + endpoint
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=30)
        
        if response.status_code == 200:
            print(f"✅ {name}")
            print(f"   Status: {response.status_code}")
            tests_passed += 1
            return True
        else:
            print(f"⚠️  {name}")
            print(f"   Status: {response.status_code}")
            tests_failed += 1
            return False
    except Exception as e:
        print(f"❌ {name}")
        print(f"   Error: {str(e)}")
        tests_failed += 1
        return False

# ============================================================================
# BASIC CONNECTIVITY TESTS
# ============================================================================
print("1️⃣  CONNECTIVITY TESTS")
print("-" * 70)

test_endpoint("GET", "/health", "Local Health Check")
test_endpoint("GET", "/health", "Public Health Check (ngrok)", is_public=True)

# ============================================================================
# API ENDPOINT TESTS
# ============================================================================
print("\n2️⃣  API ENDPOINT TESTS")
print("-" * 70)

test_endpoint("GET", "/", "Home Page")

# Test analysis endpoint
sample_data = {
    "hemoglobin": 11.5,
    "glucose": 180,
    "cholesterol": 240,
    "blood_pressure": 140,
    "wbc": 7500,
    "platelets": 250000,
    "creatinine": 0.9,
    "alt": 45,
    "ast": 50,
    "ldl": 160,
    "hdl": 35
}
test_endpoint("POST", "/analyze-report/", "Blood Report Analysis", data=sample_data)

# ============================================================================
# DOCUMENTATION TESTS
# ============================================================================
print("\n3️⃣  DOCUMENTATION TESTS")
print("-" * 70)

test_endpoint("GET", "/docs", "API Documentation (Swagger)")
test_endpoint("GET", "/redoc", "API Documentation (ReDoc)")

# ============================================================================
# PERFORMANCE CHECK
# ============================================================================
print("\n4️⃣  PERFORMANCE CHECK")
print("-" * 70)

try:
    response = requests.get(f"{BASE_URL}/health", timeout=10)
    if response.status_code == 200:
        data = response.json()
        perf = data.get('performance', {})
        ops = perf.get('operations', {})
        
        print("✅ Performance Metrics Available")
        for op_name, op_data in ops.items():
            if isinstance(op_data, dict):
                avg_time = op_data.get('avg_ms', 0)
                print(f"   • {op_name}: {avg_time:.2f}ms avg")
        tests_passed += 1
    else:
        tests_failed += 1
except:
    tests_failed += 1

# ============================================================================
# DATABASE TESTS
# ============================================================================
print("\n5️⃣  DATABASE TESTS")
print("-" * 70)

try:
    response = requests.get(f"{BASE_URL}/health", timeout=10)
    data = response.json()
    if data.get('status') == 'healthy':
        print("✅ Database Connection")
        print(f"   Status: {data['status']}")
        print(f"   Service: {data.get('service', 'Unknown')}")
        print(f"   Version: {data.get('version', 'Unknown')}")
        tests_passed += 1
    else:
        tests_failed += 1
except:
    tests_failed += 1

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*70)
print("📊 TEST SUMMARY")
print("="*70)

total_tests = tests_passed + tests_failed
success_rate = (tests_passed / total_tests * 100) if total_tests > 0 else 0

print(f"\n✅ Tests Passed:  {tests_passed}")
print(f"❌ Tests Failed:  {tests_failed}")
print(f"📊 Success Rate:  {success_rate:.1f}%")

print("\n" + "="*70)
print("ACCESS INFORMATION")
print("="*70)

print(f"""
🌍 PUBLIC ACCESS (Worldwide):
   https://impalpable-perspectively-andria.ngrok-free.dev

🏠 LOCAL ACCESS (This Machine):
   http://localhost:8000

📡 NETWORK ACCESS (Same WiFi):
   http://10.100.55.69:8000

📊 API DOCUMENTATION:
   http://localhost:8000/docs (Local)
   https://impalpable-perspectively-andria.ngrok-free.dev/docs (Public)

❤️  HEALTH CHECK:
   curl http://localhost:8000/health
""")

print("="*70)
if success_rate >= 80:
    print("🟢 SYSTEM STATUS: OPERATIONAL ✅")
else:
    print("🟡 SYSTEM STATUS: WARNINGS ⚠️")
print("="*70 + "\n")

sys.exit(0 if success_rate >= 80 else 1)
