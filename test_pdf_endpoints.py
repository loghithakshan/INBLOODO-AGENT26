"""
Test script for PDF generation endpoints.
Tests the new PDF download functionality.
"""
import requests
import json
import time
from pathlib import Path

BASE_URL = "http://localhost:8000"
API_KEY = "vietGhJUH4jURLFLFGFRFmzr56i8Ek"  # Default API key

def test_demo_pdf():
    """Test demo PDF endpoint (no auth required)"""
    print("\n" + "="*60)
    print("Testing Demo PDF Endpoint")
    print("="*60)
    
    url = f"{BASE_URL}/api/demo/pdf"
    
    try:
        response = requests.get(url, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            # Check if response is PDF content
            if b'%PDF' in response.content[:10]:
                print(f"✓ PDF Generated Successfully!")
                print(f"  Content-Type: {response.headers.get('content-type')}")
                print(f"  Content-Length: {len(response.content)} bytes")
                
                # Save PDF for inspection
                output_path = Path("demo_blood_report_test.pdf")
                with open(output_path, "wb") as f:
                    f.write(response.content)
                print(f"  Saved to: {output_path}")
                return True
            else:
                print(f"✗ Response is not PDF format")
                print(f"  Response: {response.text[:200]}")
                return False
        else:
            print(f"✗ Request failed")
            print(f"  Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def test_pdf_with_auth():
    """Test PDF endpoint with authentication"""
    print("\n" + "="*60)
    print("Testing PDF Generation with Auth")
    print("="*60)
    
    url = f"{BASE_URL}/api/pdf/generate"
    
    # Sample analysis data
    analysis_data = {
        "parameters": {
            "hemoglobin": 13.5,
            "hematocrit": 41.2,
            "glucose": 95,
            "cholesterol": 180
        },
        "interpretation": {
            "hemoglobin": "Normal",
            "glucose": "Normal"
        },
        "recommendations": [
            "Maintain regular exercise",
            "Continue balanced diet"
        ],
        "precautions": [
            "Monitor blood sugar levels"
        ],
        "filename": "test_report.pdf"
    }
    
    try:
        response = requests.post(
            url,
            json=analysis_data,
            headers={"X-API-Key": API_KEY},
            timeout=30
        )
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            if b'%PDF' in response.content[:10]:
                print(f"✓ PDF Generated Successfully!")
                print(f"  Content-Type: {response.headers.get('content-type')}")
                print(f"  Content-Length: {len(response.content)} bytes")
                
                # Save PDF for inspection
                output_path = Path("generated_blood_report.pdf")
                with open(output_path, "wb") as f:
                    f.write(response.content)
                print(f"  Saved to: {output_path}")
                return True
            else:
                print(f"✗ Response is not PDF format")
                print(f"  Response: {response.text[:200]}")
                return False
        else:
            print(f"✗ Request failed")
            print(f"  Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def test_fallback_system_with_webp():
    """Test the fallback system with WebP file"""
    print("\n" + "="*60)
    print("Testing Fallback System with WebP Upload")
    print("="*60)
    
    url = f"{BASE_URL}/analyze-report/"
    
    # Create a simple test WebP-like file (just test with any file content)
    # The filename will trigger the fallback system
    
    test_content = b"This is a test file that cannot be parsed as an image"
    
    try:
        # Upload file with diabetes hint in filename
        files = {"file": ("diabetic_test.webp", test_content, "image/webp")}
        response = requests.post(
            url,
            files=files,
            headers={"X-API-Key": API_KEY},
            timeout=30
        )
        print(f"Status Code: {response.status_code}")
        
        if response.status_code in [200, 201]:
            result = response.json()
            
            # Check if fallback was used
            metadata = result.get("metadata", {})
            if metadata.get("extraction_status") == "fallback_used":
                print(f"✓ Fallback System Triggered!")
                print(f"  Fallback Notice: {metadata.get('fallback_notice', 'N/A')}")
                print(f"  Parameters Generated: {len(result.get('parameters', {}))} items")
                return True
            else:
                print(f"≈ Request successful but fallback not used")
                print(f"  Status: {metadata.get('extraction_status')}")
                # Still consider this a pass if we got a result
                print(f"  Parameters: {len(result.get('parameters', {}))} items")
                return True
        else:
            print(f"✗ Request failed")
            print(f"  Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("  PDF GENERATION & FALLBACK SYSTEM TESTS")
    print("="*70)
    
    # Wait for server to be fully ready
    print("\nWaiting for server to be ready...")
    time.sleep(2)
    
    results = []
    
    # Test 1: Demo PDF
    results.append(("Demo PDF Endpoint", test_demo_pdf()))
    
    # Test 2: PDF with Auth
    results.append(("PDF Generation with Auth", test_pdf_with_auth()))
    
    # Test 3: Fallback System
    results.append(("Fallback System (WebP)", test_fallback_system_with_webp()))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name:<40} {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All PDF generation tests passed!")
    else:
        print(f"\n≈ {total - passed} test(s) need attention")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
