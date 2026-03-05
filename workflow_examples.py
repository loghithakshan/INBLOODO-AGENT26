#!/usr/bin/env python
"""Complete workflow example - upload and analyze blood report."""
import requests
import json
import io
import sys

def print_section(title):
    """Print formatted section header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def example_1_demo_endpoint():
    """Example 1: Use demo endpoint for instant analysis."""
    print_section("EXAMPLE 1: Demo Endpoint (Fastest Way to Test)")
    
    print("URL: http://localhost:8000/api/demo/analyze/healthy")
    print("Method: GET")
    print("No authentication needed!\n")
    
    try:
        resp = requests.get('http://localhost:8000/api/demo/analyze/healthy', timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            print("✓ Response received successfully!\n")
            print(f"Processing Time: {data.get('processing_time', 'N/A'):.2f}s")
            print(f"Parameters Found: {len(data.get('extracted_parameters', {}))}")
            print(f"Immediate Test Recommendations: {len(data.get('recommendations', []))}")
            
            if data.get('recommendations'):
                print(f"\nKey Recommendations:")
                for i, rec in enumerate(data['recommendations'][:3], 1):
                    if isinstance(rec, dict):
                        print(f"  {i}. {rec.get('recommendation', str(rec))[:70]}...")
                    else:
                        print(f"  {i}. {str(rec)[:70]}...")
            return True
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    return False

def example_2_json_upload():
    """Example 2: Upload JSON parameters."""
    print_section("EXAMPLE 2: JSON Parameter Upload")
    
    # Sample prediabetic blood report
    blood_data = {
        "hemoglobin": 12.8,
        "glucose": 115,
        "cholesterol": 210,
        "hdl": 42,
        "ldl": 135,
        "triglycerides": 180,
        "creatinine": 0.95,
        "urea": 32,
        "bilirubin_total": 0.8,
        "ast": 32,
        "alt": 38,
    }
    
    print("Using prediabetic sample data:")
    print(json.dumps(blood_data, indent=2))
    
    print("\nURL: http://localhost:8000/analyze-json/")
    print("Method: POST")
    print("Headers: X-API-Key: your-api-key")
    print("         Content-Type: application/json")
    
    try:
        # Test users from the system
        headers = {
            "X-API-Key": "test-key",  # The system accepts test-key
            "Content-Type": "application/json"
        }
        
        resp = requests.post(
            'http://localhost:8000/analyze-json/',
            json=blood_data,
            headers=headers,
            timeout=60
        )
        
        if resp.status_code == 200:
            data = resp.json()
            print("\n✓ Analysis completed!\n")
            print(f"Processing Time: {data.get('processing_time', 'N/A'):.2f}s")
            print(f"Parameters Validated: {len(data.get('extracted_parameters', {}))}")
            print(f"Risk Factors Identified: {len(data.get('risks', []))}")
            print(f"Recommendations Generated: {len(data.get('recommendations', []))}")
            
            # Show identified risks
            risks = data.get('risks', [])
            if risks:
                print(f"\nIdentified Health Risks:")
                for i, risk in enumerate(risks[:3], 1):
                    if isinstance(risk, dict):
                        print(f"  {i}. {risk.get('category', 'Unknown')}: {risk.get('description', '')[:60]}...")
                    else:
                        print(f"  {i}. {str(risk)[:60]}...")
            
            return True
        else:
            print(f"\n✗ Status: {resp.status_code}")
            print(f"Response: {resp.text[:200]}")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    return False

def example_3_csv_upload():
    """Example 3: Upload CSV file."""
    print_section("EXAMPLE 3: CSV File Upload")
    
    # Create sample CSV content
    csv_content = """parameter,value
hemoglobin,13.5
glucose,95
cholesterol,180
hdl,55
ldl,100
triglycerides,120
creatinine,0.9
urea,30"""
    
    print("CSV Content:")
    print(csv_content)
    
    print("\nURL: http://localhost:8000/analyze-report/")
    print("Method: POST (multipart/form-data)")
    print("Headers: X-API-Key: your-api-key")
    
    try:
        files = {'file': ('blood_report.csv', io.BytesIO(csv_content.encode()), 'text/csv')}
        headers = {"X-API-Key": "test-key"}
        
        resp = requests.post(
            'http://localhost:8000/analyze-report/',
            files=files,
            headers=headers,
            timeout=60
        )
        
        if resp.status_code == 200:
            data = resp.json()
            print("\n✓ CSV analyzed successfully!\n")
            print(f"Processing Time: {data.get('processing_time', 'N/A'):.2f}s")
            print(f"Parameters Extracted: {len(data.get('extracted_parameters', {}))}")
            
            # Show parameter keys
            params = data.get('extracted_parameters', {})
            if params:
                print(f"\nExtracted Parameters:")
                for key, value in list(params.items())[:8]:
                    print(f"  - {key}: {value}")
            
            return True
        else:
            print(f"\n✗ Status: {resp.status_code}")
            print(f"Response: {resp.text[:200]}")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    return False

def example_4_all_samples():
    """Example 4: Try all sample types."""
    print_section("EXAMPLE 4: All Available Samples")
    
    samples = ['healthy', 'prediabetic', 'high_cholesterol', 'anemia']
    
    print("Available sample types:\n")
    
    for sample_type in samples:
        try:
            resp = requests.get(
                f'http://localhost:8000/api/demo/analyze/{sample_type}',
                timeout=60
            )
            
            if resp.status_code == 200:
                data = resp.json()
                recs = len(data.get('recommendations', []))
                risks = len(data.get('risks', []))
                print(f"  ✓ {sample_type:20} | Recommendations: {recs:2} | Risks: {risks}")
            else:
                print(f"  ✗ {sample_type:20} | Status: {resp.status_code}")
        except Exception as e:
            print(f"  ✗ {sample_type:20} | Error")
    
    return True

def main():
    """Run all examples."""
    print("\n" + "="*70)
    print("         BLOOD REPORT AI - COMPLETE WORKFLOW EXAMPLES")
    print("="*70)
    
    examples = [
        (1, "Demo Endpoint (Fastest)", example_1_demo_endpoint, True),
        (2, "JSON Parameter Upload", example_2_json_upload, True),
        (3, "CSV File Upload", example_3_csv_upload, True),
        (4, "All Sample Types", example_4_all_samples, True),
    ]
    
    results = []
    
    for ex_num, title, func, enabled in examples:
        if enabled:
            try:
                success = func()
                results.append((title, success))
            except Exception as e:
                print(f"\n✗ Error in {title}: {str(e)}")
                results.append((title, False))
        else:
            print(f"\n⊘ Skipped: {title}")
    
    # Print summary
    print_section("SUMMARY")
    successful = sum(1 for _, s in results if s)
    total = len(results)
    
    for title, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"  {status:8} - {title}")
    
    print(f"\n  {'='*50}")
    print(f"  Result: {successful}/{total} examples successful")
    print(f"  {'='*50}\n")
    
    return successful == total

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nFatal error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
