#!/usr/bin/env python3
"""
Dashboard Switching Debug Test
Tests the complete flow: upload -> results -> dashboard switch
"""
import time
import requests
import json
from datetime import datetime

print(f"\n{'='*70}")
print(f"Dashboard Switching Debug Test - {datetime.now().strftime('%H:%M:%S')}")
print(f"{'='*70}\n")

# Test: Check server
print("Test 1: Verifying server is running...")
try:
    response = requests.get('http://localhost:8000/')
    if response.status_code == 200:
        print("✅ Server is online at http://localhost:8000/")
    else:
        print(f"⚠️ Server returned status {response.status_code}")
except requests.exceptions.ConnectionError:
    print("❌ Server is NOT running. Please start it first.")
    import sys
    sys.exit(1)

# Test: Upload file and get analysis data
print("\nTest 2: Uploading file for analysis...")
try:
    with open(r'c:\Users\rakes\Downloads\blood report ai\test_sample.csv', 'rb') as f:
        files = {'file': ('test_sample.csv', f, 'text/csv')}
        headers = {'x-api-key': 'test-key-12345'}
        
        response = requests.post(
            'http://localhost:8000/analyze-report/',
            files=files,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API returned analysis data (status 200)")
            print(f"   - Risk: {data.get('overall_risk', 'N/A')}")
            print(f"   - Medicines: {len(data.get('medicines', []))} items")
            print(f"   - Recommendations: {len(data.get('recommendations', []))} items")
        else:
            print(f"❌ API returned status {response.status_code}")
            
except Exception as e:
    print(f"❌ Upload test failed: {e}")

# Test: Verify HTML structure
print("\nTest 3: Checking HTML structure for view switching...")
try:
    with open(r'c:\Users\rakes\Downloads\blood report ai\templates\index.html', 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    
    checks = {
        'resultsSection element': 'id="resultsSection"' in html,
        'dashboardSection element': 'id="dashboardSection"' in html,
        'navAnalysis button': 'id="navAnalysis"' in html,
        'navDashboard button': 'id="navDashboard"' in html,
        'showView() function': 'function showView(view)' in html,
        'populateDashboard() function': 'function populateDashboard(data)' in html,
        'CSS for .results-section': '.results-section {' in html,
        'CSS for .dashboard-grid': '.dashboard-grid {' in html,
        'CSS for .dashboard-grid.active': '.dashboard-grid.active {' in html,
    }
    
    for check_name, result in checks.items():
        print(f"   {'✅' if result else '❌'} {check_name}")
        
    # Check for orphaned CSS
    if '        }\\n            display: grid;' in html or 'animation: fadeIn 0.5s ease;\\n        }' in html:
        print("\n   ⚠️  WARNING: Orphaned CSS detected (may cause issues)")
    else:
        print("\n   ✅ No orphaned CSS found")
        
    # Check debug logging
    logging_checks = {
        'uploadFile logging': 'console.log' in html and '🚀 uploadFile()' in html,
        'showResults logging': '✅ showResults()' in html,
        'showView logging': '📋 showView called' in html,
        'populateDashboard logging': '📊 populateDashboard()' in html,
    }
    
    print("\n   Debug Logging Status:")
    for check_name, result in logging_checks.items():
        print(f"   {'✅' if result else '❌'} {check_name}")
        
except Exception as e:
    print(f"❌ HTML check failed: {e}")

# Summary
print("\n" + "="*70)
print("MANUAL TESTING INSTRUCTIONS:")
print("="*70)

print("""
1. Hard Refresh Browser:
   - Press Ctrl+F5 to clear cache
   
2. Open Developer Console:
   - Press F12 → Console tab
   - Clear previous messages
   
3. Upload a Blood Report File:
   - Watch for console logs in this order:
   
   🚀 uploadFile() started. File: [filename]
   📤 Uploading to /analyze-report/...
   📩 Response status: 200
   ✅ Successfully received analysis data
   ✨ Results HTML set with show class
   🎯 Element visibility: 1
   ✅ showResults() completed successfully!
   📋 showView called with: analysis
   ✅ showView() completed
   
4. CLICK DASHBOARD BUTTON:
   - Watch for console logs:
   
   📋 showView called with: dashboard
   📊 populateDashboard() called with data: [...]
   ✨ Dashboard HTML rendered
   ✅ showView() completed
   
5. VERIFY DISPLAY:
   - Dashboard should appear with stat cards
   - Risk level, parameters, recommendations should show
   - Click back to Analysis button
   - Analysis results should reappear
   
✅ SUCCESS: If you see all these logs and can switch between views!
❌ PROBLEM: If dashboard doesn't appear or logs don't show, report the error
""")

print("="*70)
print("Test Complete!")
print("="*70 + "\n")
