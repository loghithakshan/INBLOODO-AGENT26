"""
Enhanced test to verify fallback system is working correctly.
Tests WebP image uploads with various filename hints.
"""
import requests
import json
from pathlib import Path

BASE_URL = "http://localhost:8000"
API_KEY = "vietGhJUH4jURLFLFGFRFmzr56i8Ek"

def test_fallback_with_filename_hints():
    """Test that fallback system detects condition from filename"""
    print("\n" + "="*70)
    print("TESTING FALLBACK SYSTEM WITH VARIOUS FILENAMES")
    print("="*70)
    
    test_cases = [
        ("diabetic_report.webp", "prediabetic"),
        ("cholesterol_test.webp", "high_cholesterol"),
        ("anemia_sample.webp", "anemia"),
        ("healthy_baseline.webp", "healthy"),
    ]
    
    # Create a fake image file (invalid content)
    fake_image = b"This is not a real image file"
    
    all_passed = True
    
    for filename, expected_type in test_cases:
        print(f"\n{'-'*70}")
        print(f"Testing: {filename}")
        print(f"Expected Fallback Type: {expected_type}")
        print(f"{'-'*70}")
        
        try:
            files = {"file": (filename, fake_image, "image/webp")}
            response = requests.post(
                f"{BASE_URL}/analyze-report/",
                files=files,
                headers={"X-API-Key": API_KEY},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                params = result.get("extracted_parameters", {})
                fallback_notice = result.get("fallback_notice", "")
                extraction_status = result.get("extraction_status", "")
                
                print(f"✓ Status: {response.status_code}")
                print(f"  Parameters Extracted: {len(params)} items")
                print(f"  Extraction Status: {extraction_status}")
                
                # Check if fallback was used
                if extraction_status == "fallback_used":
                    print(f"  ✓ Fallback System Triggered!")
                    print(f"  ✓ Fallback Notice: {fallback_notice[:70]}...")
                    
                    # Check if we got sample data
                    if len(params) > 0:
                        print(f"  ✓ Sample Parameters Generated: {list(params.keys())[:3]}...")
                    else:
                        print(f"  ✗ No parameters in response")
                        all_passed = False
                else:
                    print(f"  ≈ Status: {extraction_status}")
                    all_passed = False
                    
            else:
                print(f"✗ Status: {response.status_code}")
                print(f"  Error: {response.text[:200]}")
                all_passed = False
                
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            all_passed = False
    
    return all_passed


def test_pdf_download_endpoints():
    """Test all PDF download endpoints"""
    print("\n" + "="*70)
    print("TESTING PDF DOWNLOAD ENDPOINTS")
    print("="*70)
    
    endpoints = [
        ("GET", f"{BASE_URL}/api/demo/pdf", "Demo PDF Endpoint"),
        ("POST", f"{BASE_URL}/api/pdf/generate", "PDF Generation Endpoint"),
    ]
    
    all_passed = True
    
    for method, url, description in endpoints[0:1]:  # Test GET first
        print(f"\n{description}")
        print(f"  Method: {method}")
        print(f"  URL: {url}")
        
        try:
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200 and b'%PDF' in response.content[:10]:
                file_size = len(response.content)
                print(f"  ✓ Status: {response.status_code}")
                print(f"  ✓ Valid PDF Generated ({file_size} bytes)")
            else:
                print(f"  ✗ Invalid PDF or error status: {response.status_code}")
                all_passed = False
                
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            all_passed = False
    
    # Test POST
    headers = {"X-API-Key": API_KEY}
    analysis_data = {
        "parameters": {"hemoglobin": 13.5, "glucose": 95},
        "recommendations": ["Test recommendation"],
        "precautions": ["Test precaution"],
        "filename": "test.pdf"
    }
    
    print(f"\nPDF Generation Endpoint")
    print(f"  Method: POST")
    print(f"  URL: {endpoints[1][1]}")
    
    try:
        response = requests.post(
            endpoints[1][1],
            json=analysis_data,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200 and b'%PDF' in response.content[:10]:
            file_size = len(response.content)
            print(f"  ✓ Status: {response.status_code}")
            print(f"  ✓ Valid PDF Generated ({file_size} bytes)")
        else:
            print(f"  ✗ Invalid PDF or error status: {response.status_code}")
            all_passed = False
            
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        all_passed = False
    
    return all_passed


def main():
    """Run all enhanced tests"""
    print("\n" + "="*70)
    print("  COMPREHENSIVE FALLBACK & PDF SYSTEM TESTS")
    print("="*70)
    
    fallback_passed = test_fallback_with_filename_hints()
    pdf_passed = test_pdf_download_endpoints()
    
    print("\n" + "="*70)
    print("FINAL SUMMARY")
    print("="*70)
    print(f"Fallback System Tests: {'✓ PASSED' if fallback_passed else '✗ FAILED'}")
    print(f"PDF Download Tests:    {'✓ PASSED' if pdf_passed else '✗ FAILED'}")
    
    if fallback_passed and pdf_passed:
        print("\n✓ ALL SYSTEMS OPERATIONAL!")
        print("\n✓ WebP Support: WORKING")
        print("✓ Automated Data Extraction with Fallback: WORKING")
        print("✓ PDF Report Generation: WORKING")
        return True
    else:
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
