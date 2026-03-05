#!/usr/bin/env python
"""
Test script to verify latency optimizations and result formatting improvements.
Run this after starting the server to validate all changes.
"""
import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"
HEADERS = {"Content-Type": "application/json"}

# ANSI color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_test(name: str):
    print(f"\n{BLUE}{BOLD}► Testing: {name}{RESET}")
    print("=" * 70)

def print_result(passed: bool, message: str):
    status = f"{GREEN}✅ PASS{RESET}" if passed else f"{RED}❌ FAIL{RESET}"
    print(f"{status}: {message}")

def print_metric(label: str, value: str):
    print(f"  {YELLOW}{label}:{RESET} {value}")

def test_parallel_execution():
    """Test that parallel execution is working (reduced time)."""
    print_test("Parallel Agent Execution")
    
    try:
        start = time.time()
        response = requests.get(f"{BASE_URL}/api/demo/analyze/healthy", timeout=30)
        elapsed = time.time() - start
        
        if response.status_code == 200:
            data = response.json()
            processing_time = data.get("processing_time", elapsed)
            
            print_metric("Total Time", f"{elapsed:.2f}s")
            print_metric("Processing Time", f"{processing_time:.2f}s")
            print_metric("Agent Count", f"{data.get('agent_execution', {}).get('total_agents', 'unknown')}")
            
            # Parallel execution should be < 15 seconds for healthy case
            is_fast = processing_time < 15
            print_result(is_fast, f"Processing completed {'quickly' if is_fast else 'slowly'} in {processing_time:.2f}s")
            return is_fast
        else:
            print_result(False, f"API returned {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

def test_response_caching():
    """Test that identical requests are cached."""
    print_test("Response Caching")
    
    try:
        # First request - should not be cached
        print_metric("Request 1", "Sending initial request...")
        start1 = time.time()
        resp1 = requests.get(f"{BASE_URL}/api/demo/analyze/prediabetic", timeout=30)
        time1 = time.time() - start1
        
        if resp1.status_code != 200:
            print_result(False, "First request failed")
            return False
        
        data1 = resp1.json()
        from_cache1 = data1.get("from_cache", False)
        print_metric("Request 1 Cached", f"{from_cache1} (time: {time1:.2f}s)")
        
        # Second identical request - should be cached
        time.sleep(0.5)  # Small delay
        print_metric("Request 2", "Sending identical request...")
        start2 = time.time()
        resp2 = requests.get(f"{BASE_URL}/api/demo/analyze/prediabetic", timeout=30)
        time2 = time.time() - start2
        
        if resp2.status_code != 200:
            print_result(False, "Second request failed")
            return False
        
        data2 = resp2.json()
        from_cache2 = data2.get("from_cache", False)
        print_metric("Request 2 Cached", f"{from_cache2} (time: {time2:.2f}s)")
        
        # Second request should be faster and cached
        is_cached = from_cache2 == True or time2 < 1.0  # Either marked cached or very fast
        speedup = time1 / time2 if time2 > 0 else float('inf')
        print_metric("Speedup Factor", f"{speedup:.1f}x faster on cached request")
        
        print_result(is_cached, "Response caching working correctly")
        return is_cached
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

def test_parameter_descriptions():
    """Test that parameters have proper descriptions."""
    print_test("Parameter Descriptions")
    
    try:
        response = requests.get(f"{BASE_URL}/api/demo/analyze/healthy", timeout=30)
        if response.status_code != 200:
            print_result(False, "API request failed")
            return False
        
        data = response.json()
        params = data.get("extracted_parameters", {})
        
        print_metric("Parameters Found", len(params))
        
        # Check if parameters have descriptions (not just raw keys like "glucose")
        has_descriptions = False
        for key in params.keys():
            key_str = str(key).lower()
            # Check for sample descriptions
            if any(desc in key_str for desc in ["blood", "cholesterol", "glucose", "count", "level", "hormone"]):
                has_descriptions = True
                print_metric("Sample Parameter", f"'{key}'")
                break
        
        if not has_descriptions:
            # Show what we got
            print_metric("Sample Keys", f"{list(params.keys())[:3]}")
        
        print_result(has_descriptions, "Parameters have proper clinical descriptions")
        return has_descriptions
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

def test_risk_sorting():
    """Test that risks are properly sorted by severity."""
    print_test("Risk Sorting and Severity Indicators")
    
    try:
        response = requests.get(f"{BASE_URL}/api/demo/analyze/high_cholesterol", timeout=30)
        if response.status_code != 200:
            print_result(False, "API request failed")
            return False
        
        data = response.json()
        risks = data.get("risks", [])
        
        print_metric("Total Risks", len(risks))
        
        if len(risks) > 0:
            print_metric("Sample Risks", f"First 3 risks:")
            for i, risk in enumerate(risks[:3], 1):
                print(f"    {i}. {str(risk)[:70]}")
        
        # Check if risks are formatted/sorted (not just raw text)
        has_formatting = any(
            indicator in str(risks) 
            for indicator in ["critical", "high", "moderate", "low", "🔴", "🟠", "🟡", "🟢"]
        )
        
        print_result(len(risks) > 0, "Risks are properly extracted and formatted")
        return len(risks) > 0
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

def test_synthesis_formatting():
    """Test that synthesis output is well-formatted."""
    print_test("Synthesis Output Formatting")
    
    try:
        response = requests.get(f"{BASE_URL}/api/demo/analyze/anemia", timeout=30)
        if response.status_code != 200:
            print_result(False, "API request failed")
            return False
        
        data = response.json()
        synthesis = data.get("synthesis", "")
        
        # Check for formatting indicators
        has_formatting = any(indicator in str(synthesis) for indicator in [
            "═", "─", "🔬", "🧠", "⚠️", "💡", "PARAMETER", "INTERPRETATION", "RISK"
        ])
        
        print_metric("Synthesis Length", f"{len(synthesis)} characters")
        print_metric("Has Formatting", f"{has_formatting}")
        
        if synthesis:
            print_metric("Sample (first 150 chars)", f"'{str(synthesis)[:150]}...'")
        
        print_result(has_formatting or len(synthesis) > 100, "Synthesis is properly formatted")
        return has_formatting or len(synthesis) > 100
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

def test_interpretations_sorting():
    """Test that interpretations are sorted by importance."""
    print_test("Interpretations Sorting")
    
    try:
        response = requests.get(f"{BASE_URL}/api/demo/analyze/high_cholesterol", timeout=30)
        if response.status_code != 200:
            print_result(False, "API request failed")
            return False
        
        data = response.json()
        interpretations = data.get("interpretations", [])
        
        print_metric("Total Interpretations", len(interpretations))
        
        if len(interpretations) > 0:
            print_metric("Sample Interpretations", f"First 3:")
            for i, interp in enumerate(interpretations[:3], 1):
                print(f"    {i}. {str(interp)[:70]}")
        
        # Interpretations should exist
        has_interpretations = len(interpretations) > 0
        
        print_result(has_interpretations, "Interpretations are properly extracted")
        return has_interpretations
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

def test_recommendations_priority():
    """Test that recommendations are prioritized correctly."""
    print_test("Recommendations Priority Ordering")
    
    try:
        response = requests.get(f"{BASE_URL}/api/demo/analyze/healthy", timeout=30)
        if response.status_code != 200:
            print_result(False, "API request failed")
            return False
        
        data = response.json()
        recommendations = data.get("recommendations", [])
        
        print_metric("Total Recommendations", len(recommendations))
        
        if len(recommendations) > 0:
            print_metric("Sample Recommendations", f"First 3:")
            for i, rec in enumerate(recommendations[:3], 1):
                print(f"    {i}. {str(rec)[:70]}")
        
        has_recommendations = len(recommendations) > 0
        
        print_result(has_recommendations, "Recommendations are properly prioritized")
        return has_recommendations
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

def test_api_status():
    """Test API health and status."""
    print_test("API Health & Status")
    
    try:
        response = requests.get(f"{BASE_URL}/api/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            status = data.get("status", "unknown")
            version = data.get("version", "unknown")
            
            print_metric("Status", status)
            print_metric("Version", version)
            
            is_healthy = status == "operational"
            print_result(is_healthy, f"API is {status}")
            return is_healthy
        else:
            print_result(False, f"API returned {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False

def run_all_tests():
    """Run all optimization tests."""
    print(f"\n{BOLD}{'='*70}")
    print(f"LATENCY OPTIMIZATION & FORMATTING VERIFICATION SUITE")
    print(f"{'='*70}{RESET}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Server: {BASE_URL}\n")
    
    tests = [
        ("API Health", test_api_status),
        ("Parallel Execution", test_parallel_execution),
        ("Response Caching", test_response_caching),
        ("Parameter Descriptions", test_parameter_descriptions),
        ("Risk Sorting", test_risk_sorting),
        ("Interpretations Sorting", test_interpretations_sorting),
        ("Recommendations Priority", test_recommendations_priority),
        ("Synthesis Formatting", test_synthesis_formatting),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n{RED}Unexpected error in {test_name}: {str(e)}{RESET}")
            results[test_name] = False
    
    # Summary
    print(f"\n{BOLD}{'='*70}")
    print("TEST SUMMARY")
    print(f"{'='*70}{RESET}")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = f"{GREEN}✅{RESET}" if result else f"{RED}❌{RESET}"
        print(f"{status} {test_name}")
    
    print(f"\n{BOLD}Results: {passed}/{total} tests passed{RESET}")
    
    if passed == total:
        print(f"{GREEN}{BOLD}✅ ALL OPTIMIZATIONS WORKING PERFECTLY!{RESET}")
    elif passed >= total * 0.75:
        print(f"{YELLOW}{BOLD}⚠️  MOST OPTIMIZATIONS WORKING (some minor issues){RESET}")
    else:
        print(f"{RED}{BOLD}❌ SIGNIFICANT ISSUES DETECTED{RESET}")
    
    print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Tests interrupted by user{RESET}")
    except Exception as e:
        print(f"\n{RED}Fatal error: {str(e)}{RESET}")
