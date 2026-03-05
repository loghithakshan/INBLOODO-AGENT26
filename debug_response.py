import requests
import json

csv_content = """parameter,value,unit
Hemoglobin,14.5,g/dL
RBC,4.8,10^6/µL
WBC,7.2,10^3/µL
Platelets,250,10^3/µL
Hematocrit,43,percent
"""

with open('test_blood_report.csv', 'w') as f:
    f.write(csv_content)

files = {'file': open('test_blood_report.csv', 'rb')}
data = {'file_type': 'CSV'}

print("📤 Uploading test CSV...")
response = requests.post('http://localhost:8000/analyze-report/', files=files, data=data, timeout=30)
print(f"Status: {response.status_code}\n")
print("Response data:")
result = response.json()
for key, value in result.items():
    if isinstance(value, list):
        print(f"  {key}: {len(value)} items")
        if value and isinstance(value[0], dict):
            print(f"    → First item: {list(value[0].keys())}")
    elif isinstance(value, dict):
        print(f"  {key}: {list(value.keys())}")
    else:
        print(f"  {key}: {value}")
