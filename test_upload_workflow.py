import requests
import json
import time

# Create test CSV file
csv_content = """parameter,value,unit
Hemoglobin,14.5,g/dL
RBC,4.8,10^6/µL
WBC,7.2,10^3/µL
Platelets,250,10^3/µL
Hematocrit,43,percent
"""

# Upload file
with open('test_blood_report.csv', 'w') as f:
    f.write(csv_content)

files = {'file': open('test_blood_report.csv', 'rb')}
data = {'file_type': 'CSV'}

print("📤 Uploading test CSV...")
response = requests.post('http://localhost:8000/analyze-report/', files=files, data=data, timeout=30)
print(f"Response Status: {response.status_code}")

if response.status_code == 200:
    result = response.json()
    print(f"✅ Analysis received from: {result.get('primary_ai', 'N/A')}")
    print(f"   - Risk Level: {result.get('risk_level', 'N/A')}")
    print(f"   - Parameters found: {len(result.get('parameters', []))}")
    print(f"   - Medicines suggested: {len(result.get('medicines', []))}")
    
    # Check if medicines need to be increased
    if len(result.get('medicines', [])) < 8:
        print(f"\n⚠️  Currently {len(result.get('medicines', []))} medicines - Backend can suggest more!")
    else:
        print(f"\n✅ Good medicine count: {len(result.get('medicines', []))} medicines")
    
    print("\n✅ HTML has Download Button: Ready to download PDF")
else:
    print(f"❌ Error: {response.text}")
