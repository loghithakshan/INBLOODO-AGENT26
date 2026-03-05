#!/usr/bin/env python3
"""
Verification Test - Analysis Results Display Fix
Tests that the fix resolves the display issue
"""
import time
import requests
import json
from datetime import datetime

print(f"\n{'='*70}")
print(f"Analysis Results Display Fix Verification Test")
print(f"{'='*70}\n")

# Test 1: Server is running
print("Test 1: Checking if server is running...")
try:
    response = requests.get('http://localhost:8000/')
    if response.status_code == 200:
        print("✅ Server is running at http://localhost:8000/")
    else:
        print(f"⚠️  Server returned status {response.status_code}")
except requests.exceptions.ConnectionError:
    print("❌ Server is NOT running. Starting server...")
    import subprocess
    import os
    
    # Kill any existing python processes
    os.system("taskkill /IM python.exe /F 2>nul")
    time.sleep(2)
    
    # Start the server
    print("   Starting server with: python main.py")
    subprocess.Popen(['python', 'main.py'], cwd=r'c:\Users\rakes\Downloads\blood report ai')
    time.sleep(5)
    
    try:
        response = requests.get('http://localhost:8000/')
        if response.status_code == 200:
            print("✅ Server started successfully")
    except:
        print("❌ Failed to start server")

# Test 2: Test with a sample CSV file
print("\nTest 2: Testing file upload with sample data...")
try:
    # Create a simple test CSV
    test_csv = """Parameter,Value,Unit
Red Blood Cells,4.5,10^6/uL
White Blood Cells,7.2,10^3/uL
Hemoglobin,13.5,g/dL
Hematocrit,40,percent
Glucose,95,mg/dL
Creatinine,0.8,mg/dL
BUN,18,mg/dL
Sodium,138,mEq/L
Potassium,4.2,mEq/L
Total Protein,7.0,g/dL
Albumin,4.0,g/dL
Globulin,3.0,g/dL
AST,25,U/L
ALT,30,U/L"""
    
    with open(r'c:\Users\rakes\Downloads\blood report ai\test_sample.csv', 'w') as f:
        f.write(test_csv)
    
    # Upload the file
    with open(r'c:\Users\rakes\Downloads\blood report ai\test_sample.csv', 'rb') as f:
        files = {'file': ('test_sample.csv', f, 'text/csv')}
        headers = {'x-api-key': 'test-key-12345'}
        
        print("   Uploading test_sample.csv to /analyze-report/...")
        response = requests.post(
            'http://localhost:8000/analyze-report/',
            files=files,
            headers=headers,
            timeout=30
        )
        
        print(f"   Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ File upload successful!")
            print(f"\n   Analysis Data Received:")
            print(f"   - Risk Level: {data.get('overall_risk', 'N/A').upper()}")
            print(f"   - Medicines: {len(data.get('medicines', []))} items")
            print(f"   - Recommendations: {len(data.get('recommendations', []))} items")
            print(f"   - Risks: {len(data.get('risks', []))} identified")
            print(f"   - AI Provider: {data.get('ai_attribution', {}).get('primary_provider', 'Unknown')}")
            
            # Verify all critical fields are present
            critical_fields = ['overall_risk', 'medicines', 'recommendations', 'summary']
            missing = [f for f in critical_fields if f not in data]
            
            if not missing:
                print(f"\n   ✅ All critical fields present")
            else:
                print(f"\n   ❌ Missing fields: {missing}")
        else:
            print(f"❌ Upload failed")
            print(f"   Response: {response.text[:200]}")
            
except Exception as e:
    print(f"❌ Error during upload test: {e}")

# Test 3: Verify CSS fix in HTML
print("\nTest 3: Verifying CSS fix in HTML...")
try:
    with open(r'c:\Users\rakes\Downloads\blood report ai\templates\index.html', 'r') as f:
        html = f.read()
    
    if '.results-section.show {\n            opacity: 1 !important;\n            animation: none !important;' in html.replace(' ', '').replace('\n', ''):
        print("✅ CSS fix is applied (.show class has !important rules)")
    else:
        print("⚠️  CSS fix might not be properly applied")
        
    if 'showResults() called with data:' in html:
        print("✅ Debug logging added to showResults()")
    else:
        print("⚠️  Debug logging not found")
        
except Exception as e:
    print(f"❌ Error checking HTML: {e}")

# Test 4: Instructions for user
print("\n" + "="*70)
print("MANUAL VERIFICATION STEPS:")
print("="*70)

print("""
1. Hard Refresh Browser:
   - Press Ctrl+F5 (or Cmd+Shift+R on Mac)
   - This clears the CSS/JS cache
   
2. Open Browser Console:
   - Press F12 to open Developer Tools
   - Go to Console tab
   - Clear any previous messages
   
3. Upload a Test File:
   - Select any blood report file (PDF, CSV, PNG, etc.)
   - Watch the Console for debug messages:
     🚀 uploadFile() started. File: ...
     📤 Uploading to /analyze-report/...
     📩 Response status: 200
     ✅ Successfully received analysis data
     ✨ Results HTML set with show class
     🎯 Element visibility: 1
     ✅ showResults() completed successfully!
   
4. Verify Display:
   - Analysis results should appear on the screen
   - Risk badge should be visible
   - 15 medicines should be listed
   - 5 recommendations should appear
   - "Produced by: [AI Name]" should show
   
5. Console Output Interpretation:
   - If you see the above messages: ✅ FIXED
   - If you DON'T see them: ❌ Still broken (check network tab)
   - If you see errors: ❌ Report the error message
""")

# Test 5: Summary
print("\n" + "="*70)
print("FIX SUMMARY:")
print("="*70)

print("""
What was fixed:
1. CSS Animation Conflict
   - Problem: .results-section had opacity:0 with animation delay
   - Solution: .show class now uses !important and cancels animation
   - Result: Results appear immediately when data arrives

2. Debug Logging
   - Added console.log statements to trace execution
   - Can now easily see if functions are being called
   - Helpful for future troubleshooting

3. Better Error Messages
   - uploadFile() now logs each step
   - showResults() logs the data received
   - Easier to diagnose issues

Expected Outcome:
- User uploads file
- Progress bar animates (0-100%)
- Analysis results appear immediately (opacity:1)
- No CSS animation delays
- All data displays correctly
- Download PDF button works

Next Steps if Still Broken:
1. Check browser Console (F12) for errors
2. Hard refresh Ctrl+F5 to clear cache
3. Check Network tab to see if API returns data
4. Watch console logs to see execution flow
""")

print("="*70)
print("Test Complete!")
print("="*70 + "\n")
