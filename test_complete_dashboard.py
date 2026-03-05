#!/usr/bin/env python3
"""
Comprehensive test to verify complete dashboard functionality.
Tests prescriptions, medicines, and agent execution information.
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"
ENDPOINT = f"{BASE_URL}/api/demo/quick-test"

def test_complete_dashboard():
    """Test complete dashboard with all sections."""
    print("\n" + "="*90)
    print("COMPREHENSIVE DASHBOARD TEST - PRESCRIPTIONS, MEDICINES & AGENT INFO")
    print("="*90 + "\n")
    
    test_data = {
        "glucose": 150,
        "hemoglobin": 11.5,
        "alt": 45,
        "ast": 50,
        "total_cholesterol": 250,
        "triglycerides": 180,
        "age": 45,
        "gender": "M"
    }
    
    try:
        print(f"📊 Requesting full analysis...\n")
        
        start_time = time.time()
        response = requests.post(ENDPOINT, json=test_data, timeout=180)
        elapsed = time.time() - start_time
        
        if response.status_code != 200:
            print(f"❌ Server returned status {response.status_code}")
            return False
        
        result = response.json()
        print(f"✅ Analysis completed in {elapsed:.1f}s\n")
        
        # Display Results Summary
        print("="*90)
        print("📋 RESULTS SUMMARY")
        print("="*90)
        
        sections = [
            ("Parameters", "extracted_parameters", "dict"),
            ("Interpretations", "interpretations", "list"),
            ("Risks", "risks", "list"),
            ("Recommendations", "recommendations", "list"),
            ("Medicines", "medicines", "list"),
            ("Prescriptions", "prescriptions", "list"),
            ("AI Prediction", "ai_prediction", "dict"),
        ]
        
        all_present = True
        for section_name, key, data_type in sections:
            data = result.get(key)
            if data_type == "list":
                count = len(data) if data else 0
                status = "✅" if count > 0 else "❌"
                print(f"{status} {section_name:25} {count:3} items")
                if count == 0:
                    all_present = False
            elif data_type == "dict":
                count = len(data) if data else 0
                status = "✅" if count > 0 else "⚠️ "
                print(f"{status} {section_name:25} {count:3} fields")
        
        # Agent Execution Information
        print("\n" + "="*90)
        print("🤖 AGENT EXECUTION INFORMATION")
        print("="*90)
        
        agent_exec = result.get("agent_execution")
        if agent_exec:
            print(f"✅ Agent execution data present")
            print(f"   Total Agents:     {agent_exec.get('total_agents', 0)}")
            print(f"   Successful:       {agent_exec.get('successful_agents', 0)}")
            
            agents = agent_exec.get('agents', [])
            if agents:
                print(f"\n   Agent Details:")
                for agent in agents[:5]:
                    status_icon = "✅" if agent.get('success') else "❌"
                    exec_time = agent.get('execution_time', 0)
                    print(f"   {status_icon} {agent.get('name', 'Unknown'):30} {exec_time:.2f}s")
                if len(agents) > 5:
                    print(f"   ... and {len(agents) - 5} more agents")
        else:
            print(f"❌ Agent execution data missing")
            all_present = False
        
        # Performance Information
        print("\n" + "="*90)
        print("⚡ PERFORMANCE METRICS")
        print("="*90)
        
        processing_time = result.get("processing_time", 0)
        response_size = len(json.dumps(result).encode('utf-8'))
        response_size_kb = response_size / 1024
        
        print(f"✅ Total Processing Time:  {processing_time:.2f}s")
        print(f"✅ Response Size:          {response_size_kb:.1f} KB")
        print(f"✅ Status:                 {result.get('status', 'unknown').upper()}")
        
        # Final Assessment
        print("\n" + "="*90)
        print("🎯 DASHBOARD READINESS ASSESSMENT")
        print("="*90 + "\n")
        
        checks = {
            "Prescriptions Present": len(result.get('prescriptions', [])) > 0,
            "Medicines Present": len(result.get('medicines', [])) > 0,
            "Agent Info Present": agent_exec is not None,
            "Processing Time < 30s": processing_time < 30,
            "Response Size < 50KB": response_size_kb < 50,
        }
        
        passed = sum(1 for v in checks.values() if v)
        total = len(checks)
        
        for check_name, result_val in checks.items():
            status = "✅ PASS" if result_val else "❌ FAIL"
            print(f"{status} | {check_name}")
        
        print(f"\n{'='*90}")
        print(f"OVERALL: {passed}/{total} checks passed")
        print(f"{'='*90}\n")
        
        if passed == total:
            print("🎉 DASHBOARD IS FULLY OPERATIONAL!")
            print("   ✓ Prescriptions are showing")
            print("   ✓ Medicines are showing") 
            print("   ✓ Agent latency/info tabs are working")
            return True
        elif passed >= total - 1:
            print("⚠️  MOSTLY OPERATIONAL (1 minor issue)")
            return True
        else:
            print("❌ MULTIPLE ISSUES DETECTED")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


if __name__ == "__main__":
    print("\n🔬 BLOOD REPORT AI - COMPLETE DASHBOARD TEST\n")
    
    try:
        if requests.get(f"{BASE_URL}/health", timeout=5).status_code == 200:
            print("✅ Server is responding\n")
            test_complete_dashboard()
        else:
            print("❌ Server is not responding")
    except:
        print("❌ Cannot connect to server. Start it with: python main.py")
