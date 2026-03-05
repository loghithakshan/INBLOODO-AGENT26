import requests
import sys

# Create a simple test CSV file
csv_data = """Parameter,Value
Glucose,95
Hemoglobin,13.5
Hematocrit,40.5
WBC,7.2
Platelets,250"""

with open('test_report.csv', 'w') as f:
    f.write(csv_data)

# Upload the test file
with open('test_report.csv', 'rb') as f:
    files = {'file': f}
    r = requests.post('http://localhost:8000/analyze-report/', files=files, headers={'x-api-key': 'test'})
    print(f'Upload Status: {r.status_code}')
    if r.status_code == 200:
        print('✅ File upload working!')
        print(f'Response has medicines: {"medicines" in r.text}')
        print(f'Response has recommendations: {"recommendations" in r.text}')
        print(f'Response length: {len(r.text)} bytes')
    else:
        print(f'❌ Error: {r.status_code}')
        print(f'Message: {r.text[:300]}')
        sys.exit(1)
