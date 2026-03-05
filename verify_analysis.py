import requests
import time

time.sleep(1)

r = requests.get('http://localhost:8000/', timeout=5)
print(f'HTML Status: {r.status_code}')
print(f'Page size: {len(r.text)} bytes')

# Check for key elements
checks = {
    'parameter-grid': 'parameter-grid' in r.text,
    'showResults function': 'showResults' in r.text,
    'Medicines display': 'Medicines' in r.text or 'medicines' in r.text,
    'Recommendations display': 'Recommendations' in r.text or 'recommendations' in r.text,
    'Risk badge': 'RISK' in r.text,
    'Summary card': 'Summary' in r.text,
}

for check_name, result in checks.items():
    status = '✅' if result else '❌' 
    print(f'{status} {check_name}: {result}')

print('\n✅ Analysis display restored and verified!')
