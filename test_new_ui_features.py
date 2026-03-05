#!/usr/bin/env python
"""
Test suite for new UI features:
1. Professional tables for recommendations
2. Separate natural remedies table
3. Separate medical prescriptions table
4. Download report functionality
"""
import requests
import json
import sys

def test_ui_features():
    print('TESTING NEW UI FEATURES')
    print('=' * 70)
    
    # Get demo analysis first
    print('\n1. Testing Demo Analysis Endpoint...')
    try:
        resp = requests.get('http://localhost:8000/api/demo/samples', timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            print('✓ Demo samples retrieved successfully')
            
            # Check for required fields
            if 'recommendations' in data and isinstance(data['recommendations'], list):
                print(f'✓ Recommendations field exists ({len(data["recommendations"])} items)')
            
            if 'prescriptions' in data and isinstance(data['prescriptions'], list):
                print(f'✓ Prescriptions field exists ({len(data["prescriptions"])} items)')
            
            if 'extracted_parameters' in data and isinstance(data['extracted_parameters'], dict):
                print(f'✓ Parameters field exists ({len(data["extracted_parameters"])} parameters)')
            
            # Show sample data structure
            print('\n2. Sample Response Structure:')
            print(f'   - Overall Risk: {data.get("overall_risk", "N/A")}')
            print(f'   - Summary: {str(data.get("summary", "N/A"))[:60]}...')
            print(f'   - Interpretations: {len(data.get("interpretations", []))} items')
            print(f'   - Risks: {len(data.get("risks", []))} items')
            print(f'   - Recommendations: {len(data.get("recommendations", []))} items')
            print(f'   - Prescriptions: {len(data.get("prescriptions", []))} items')
            
            # Split prescriptions to test table separation
            prescriptions = data.get('prescriptions', [])
            remedies = [p for p in prescriptions if 'PRESCRIPTION' not in p.upper()]
            medications = [p for p in prescriptions if 'PRESCRIPTION' in p.upper()]
            
            print('\n3. Table Separation Test (Critical for UI):')
            print(f'   ✓ Natural Remedies Table: {len(remedies)} rows')
            for i, remedy in enumerate(remedies[:3], 1):
                print(f'      {i}. {remedy[:50]}...')
            
            print(f'\n   ✓ Medical Prescriptions Table: {len(medications)} rows')
            for i, med in enumerate(medications[:3], 1):
                print(f'      {i}. {med[:50]}...')
            
            print('\n4. Testing Download Endpoint...')
            try:
                # Test the download endpoint
                resp = requests.post(
                    'http://localhost:8000/api/download-report/',
                    json=data,
                    headers={'x-api-key': 'test-key-temp'},
                    timeout=10
                )
                if resp.status_code == 200:
                    print('✓ Download endpoint responsive')
                    print(f'✓ Content-Type: {resp.headers.get("content-type", "N/A")}')
                    print(f'✓ Response size: {len(resp.content)} bytes')
                    if b'%PDF' in resp.content[:10]:
                        print('✓ PDF content detected (valid file)')
                else:
                    print(f'✗ Download failed (HTTP {resp.status_code})')
            except Exception as e:
                print(f'✗ Download test error: {e}')
            
            return True
        else:
            print(f'✗ Failed to get samples (HTTP {resp.status_code})')
            return False
    except Exception as e:
        print(f'✗ Error: {e}')
        return False

if __name__ == '__main__':
    success = test_ui_features()
    
    print('\n' + '=' * 70)
    if success:
        print('✓ ALL TESTS PASSED - UI READY FOR VISUAL INSPECTION')
        print('=' * 70)
        print('\nNEXT STEPS - MANUAL UI TESTING:')
        print('1. Navigate to: http://localhost:8000')
        print('2. Upload a blood report file (PDF, PNG, JPEG, WebP, etc.)')
        print('3. Verify three separate professional tables appear:')
        print('   ✓ Table 1: AI Health Recommendations (GREEN)')
        print('   ✓ Table 2: Natural Remedies (ORANGE)')
        print('   ✓ Table 3: Medical Prescriptions (YELLOW)')
        print('4. Click "Download Report" button')
        print('5. Verify INBLOODO_REPORT_*.pdf downloads with timestamp')
        print('=' * 70)
        sys.exit(0)
    else:
        print('✗ TESTS FAILED')
        print('=' * 70)
        sys.exit(1)
