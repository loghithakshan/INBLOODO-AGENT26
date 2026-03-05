"""
Debug test to see exact response structure for fallback system.
"""
import requests
import json

BASE_URL = "http://localhost:8000"
API_KEY = "vietGhJUH4jURLFLFGFRFmzr56i8Ek"

def test_with_detail():
    """Test with detailed output"""
    filename = "diabetic_report.webp"
    fake_image = b"Not a real image"
    
    print(f"Uploading {filename}...")
    files = {"file": (filename, fake_image, "image/webp")}
    response = requests.post(
        f"{BASE_URL}/analyze-report/",
        files=files,
        headers={"X-API-Key": API_KEY},
        timeout=30
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"\nFull Response:")
    print(json.dumps(response.json(), indent=2))
    
    result = response.json()
    
    # Check all levels
    print(f"\n\nResponse Keys: {result.keys()}")
    print(f"'parameters' in response: {'parameters' in result}")
    print(f"'metadata' in response: {'metadata' in result}")
    
    if 'metadata' in result:
        metadata = result['metadata']
        print(f"\nMetadata Keys: {metadata.keys()}")
        print(f"'fallback_notice' in metadata: {'fallback_notice' in metadata}")

if __name__ == "__main__":
    test_with_detail()
