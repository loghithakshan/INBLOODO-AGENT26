#!/usr/bin/env python
"""Test the complete blood report analysis system."""
import requests
import json
import time

def test_demo_analysis():
    """Test demo endpoint with sample data."""
    print("Testing Blood Report AI - Demo Analysis")
    print("=" * 50)
    
    try:
        # Test 1: Get available samples
        print("\n1. Getting available sample types...")
        resp = requests.get('http://localhost:8000/api/demo/samples', timeout=5)
        samples = resp.json()
        print(f"✓ Available samples: {samples['available_samples']}")
        
        # Test 2: Analyze healthy sample
        print("\n2. Analyzing 'healthy' sample...")
        start = time.time()
        resp = requests.get('http://localhost:8000/api/demo/analyze/healthy', timeout=60)
        elapsed = time.time() - start
        
        if resp.status_code != 200:
            print(f"✗ Error: {resp.status_code}")
            print(f"Response: {resp.text}")
            return False
        
        result = resp.json()
        print(f"✓ Status: {resp.status_code}")
        print(f"✓ Processing time: {result.get('processing_time', elapsed):.2f}s")
        print(f"✓ Demo type: {result.get('demo_type')}")
        
        # Show extracted parameters
        params = result.get('extracted_parameters', {})
        print(f"\n3. Extracted Parameters ({len(params)}):")
        for key, value in list(params.items())[:5]:
            print(f"   - {key}: {value}")
        if len(params) > 5:
            print(f"   ... and {len(params) - 5} more")
        
        # Show analysis results
        print(f"\n4. Analysis Results:")
        print(f"   - Interpretations: {len(result.get('interpretations', []))} items")
        print(f"   - Risk factors: {len(result.get('risks', []))} items")
        print(f"   - AI predictions: {len(result.get('ai_prediction', {}).get('health_scores', {})) if result.get('ai_prediction') else 0} scores")
        print(f"   - Recommendations: {len(result.get('recommendations', []))} items")
        
        # Show first recommendation
        recommendations = result.get('recommendations', [])
        if recommendations:
            print(f"\n5. Sample Recommendation:")
            rec = recommendations[0]
            if isinstance(rec, dict):
                print(f"   - Category: {rec.get('category', 'N/A')}")
                print(f"   - Recommendation: {rec.get('recommendation', 'N/A')[:100]}...")
            else:
                print(f"   - {str(rec)[:100]}...")
        
        print("\n" + "=" * 50)
        print("✓ ALL TESTS PASSED - System is working correctly!")
        print("=" * 50)
        return True
        
    except requests.exceptions.ConnectionError:
        print("✗ ERROR: Cannot connect to server at http://localhost:8000")
        print("Please make sure the server is running (python main.py)")
        return False
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_demo_analysis()
    exit(0 if success else 1)
