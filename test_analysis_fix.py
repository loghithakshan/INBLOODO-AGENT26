import requests

print("=" * 70)
print("🔍 TESTING ANALYSIS ENDPOINT")
print("=" * 70)

csv_content = "parameter,value\nHemoglobin,14.5\nWBC,7.2\n"

with open('test_analysis.csv', 'w') as f:
    f.write(csv_content)

files = {'file': open('test_analysis.csv', 'rb')}
data = {'file_type': 'CSV'}

try:
    print("\n📤 Sending file to /analyze-report/ endpoint...")
    r = requests.post('http://localhost:8000/analyze-report/', files=files, data=data, timeout=30)
    
    print(f"\n✅ Status Code: {r.status_code}")
    
    if r.status_code == 200:
        result = r.json()
        print("\n✅ ANALYSIS RESPONSE RECEIVED:")
        print(f"   Risk Level: {result.get('overall_risk', 'N/A')}")
        print(f"   Medicines: {len(result.get('medicines', []))} items")
        print(f"   Recommendations: {len(result.get('recommendations', []))} items")
        print(f"   Parameters: {len(result.get('extracted_parameters', {})) if isinstance(result.get('extracted_parameters'), dict) else len(result.get('extracted_parameters', []))} items")
        print(f"   AI Provider: {result.get('ai_attribution', {}).get('primary_provider', 'N/A')}")
        print("\n✅ ANALYSIS IS WORKING CORRECTLY!")
    else:
        print(f"\n❌ Error Status: {r.status_code}")
        print(f"Response: {r.text[:300]}")
        
except requests.exceptions.ConnectionError as e:
    print(f"\n❌ CONNECTION ERROR: Cannot reach server at http://localhost:8000")
    print(f"   Make sure the server is running: python main.py")
    print(f"   Error: {str(e)[:100]}")
except Exception as e:
    print(f"\n❌ ERROR: {str(e)[:300]}")

print("\n" + "=" * 70)
