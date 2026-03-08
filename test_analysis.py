import requests
import json

# Test with sample blood report data
payload = {
    'hemoglobin': 11.5,
    'glucose': 180,
    'cholesterol': 240,
    'blood_pressure': 140,
    'wbc': 7500,
    'platelets': 250000,
    'creatinine': 0.9,
    'alt': 45,
    'ast': 50,
    'ldl': 160,
    'hdl': 35
}

print('Testing Analysis Endpoint...')
print('=' * 60)
response = requests.post('http://localhost:8000/analyze-report/', json=payload)
result = response.json()

print(f'Status Code: {response.status_code}')
print(f'Status: {result.get("status")}')
print(f'Extracted Parameters: {len(result.get("extracted_parameters", {}))} parameters found')
print(f'Risk Assessment: {len(result.get("risks", []))} risks identified')
print(f'Recommendations: {len(result.get("recommendations", []))} recommendations')
print()
if result.get('recommendations'):
    print('Sample Recommendation:', result['recommendations'][0])
print('=' * 60)
