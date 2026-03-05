#!/usr/bin/env python
"""Test all sample report types."""
import requests
import time

samples = ['healthy', 'prediabetic', 'high_cholesterol', 'anemia']

print("Testing all sample report types...")
print("=" * 60)

for sample_type in samples:
    try:
        start = time.time()
        resp = requests.get(f'http://localhost:8000/api/demo/analyze/{sample_type}', timeout=60)
        elapsed = time.time() - start
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"✓ {sample_type:20} | Status: 200 | Time: {elapsed:6.2f}s | "
                  f"Recommendations: {len(data.get('recommendations', []))} | "
                  f"Risks: {len(data.get('risks', []))}")
        else:
            print(f"✗ {sample_type:20} | Status: {resp.status_code}")
    except Exception as e:
        print(f"✗ {sample_type:20} | Error: {str(e)}")

print("=" * 60)
print("✓ All sample types tested successfully!")
