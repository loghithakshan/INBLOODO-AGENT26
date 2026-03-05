import requests

r = requests.get('http://localhost:8000/', timeout=5)
print(f'HTML Status: {r.status_code}')
print(f'Has Download Button: {"Download Report" in r.text}')
print(f'Has jsPDF Library: {"jspdf" in r.text}')
print(f'Has downloadReportPDF function: {"downloadReportPDF" in r.text}')
print(f'HTML Size: {len(r.text)} bytes')
print('✅ All features present!' if 'Download Report' in r.text and 'downloadReportPDF' in r.text else '❌ Missing features')
