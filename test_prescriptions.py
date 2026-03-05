#!/usr/bin/env python3
"""
Test script to verify prescriptions and medicines are properly returned.
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"
DEMO_ENDPOINT = f"{BASE_URL}/api/demo/quick-test"

def test_json_analysis():
    """Test JSON-based analysis to verify prescriptions are returned."""
    print("\n" + "="*80)
    print("TESTING PRESCRIPTIONS & MEDICINES IN JSON ANALYSIS")
    print("="*80 + "\n")
    
    # Sample medical data
    test_data = {
        "glucose": 150,
        "hemoglobin": 11.5,
        "alt": 45,
        "ast": 50,
        "total_cholesterol": 250,
        "triglycerides": 180,
        "age": 45,
        "gender": "M"
    }
    
    try:
        print(f"📤 Sending test data to {DEMO_ENDPOINT}")
        print(f"   Parameters: {json.dumps(test_data, indent=2)}\n")
        
        start_time = time.time()
        response = requests.post(
            DEMO_ENDPOINT,
            json=test_data,
            timeout=180
        )
        elapsed = time.time() - start_time
        
        if response.status_code != 200:
            print(f"❌ Server returned status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        result = response.json()
        
        # Check critical fields
        print(f"✅ Analysis completed in {elapsed:.1f}s\n")
        print("📊 RESULTS CHECK:\n")
        
        # Check prescriptions
        prescriptions = result.get('prescriptions', [])
        if prescriptions:
            print(f"✅ PRESCRIPTIONS: {len(prescriptions)} items found")
            for i, rx in enumerate(prescriptions[:3], 1):
                print(f"   {i}. {rx[:120]}...")
            if len(prescriptions) > 3:
                print(f"   ... and {len(prescriptions) - 3} more")
        else:
            print(f"❌ PRESCRIPTIONS: EMPTY OR MISSING")
        
        # Check medicines
        medicines = result.get('medicines', [])
        if medicines:
            print(f"\n✅ MEDICINES: {len(medicines)} items found")
            for i, med in enumerate(medicines[:3], 1):
                print(f"   {i}. {med[:120]}...")
            if len(medicines) > 3:
                print(f"   ... and {len(medicines) - 3} more")
        else:
            print(f"\n❌ MEDICINES: EMPTY OR MISSING")
        
        # Check other fields
        print(f"\n✅ Interpretations: {len(result.get('interpretations', []))} items")
        print(f"✅ Risks: {len(result.get('risks', []))} items")
        print(f"✅ Recommendations: {len(result.get('recommendations', []))} items")
        print(f"✅ Parameters: {len(result.get('extracted_parameters', {}))} fields")
        
        # Overall assessment
        print("\n" + "="*80)
        if prescriptions and medicines:
            print("🎉 SUCCESS: Prescriptions and medicines are being returned!")
        elif prescriptions:
            print("⚠️  PARTIAL: Prescriptions found, but medicines missing")
        elif medicines:
            print("⚠️  PARTIAL: Medicines found, but prescriptions missing")
        else:
            print("❌ FAILURE: Both prescriptions and medicines are missing!")
        print("="*80 + "\n")
        
        return bool(prescriptions and medicines)
        
    except requests.exceptions.Timeout:
        print(f"❌ Request timed out after 180 seconds")
        return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to server at {BASE_URL}")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_health():
    """Quick health check."""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False


if __name__ == "__main__":
    print("\n🔍 BLOOD REPORT AI - PRESCRIPTIONS TEST SUITE\n")
    
    # Health check
    if not test_health():
        print("❌ Server is not responding. Start it with: python main.py")
        exit(1)
    
    print("✅ Server is responding\n")
    
    # Run test
    success = test_json_analysis()
    
    if success:
        print("✨ All checks passed! Prescriptions and medicines are working.")
    else:
        print("⚠️  Some fields are missing. Check server logs for details.")
