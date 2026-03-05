#!/usr/bin/env python3
"""
Test enhanced dashboard with AI attribution and tokens.
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"
ENDPOINT = f"{BASE_URL}/api/demo/quick-test"

def test_enhanced_dashboard():
    """Test dashboard with AI attribution and tokens."""
    print("\n" + "="*90)
    print("ENHANCED DASHBOARD TEST - AI ATTRIBUTION & TOKENS")
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
        print(f"📊 Requesting analysis with AI attribution...\n")
        
        start_time = time.time()
        response = requests.post(ENDPOINT, json=test_data, timeout=180)
        elapsed = time.time() - start_time
        
        if response.status_code != 200:
            print(f"❌ Server returned status {response.status_code}")
            return False
        
        result = response.json()
        print(f"✅ Analysis completed in {elapsed:.1f}s\n")
        
        # Display AI Attribution Info
        print("="*90)
        print("🤖 AI ATTRIBUTION INFORMATION")
        print("="*90)
        
        ai_attr = result.get("ai_attribution", {})
        if ai_attr:
            print(f"✅ Primary Provider:        {ai_attr.get('primary_provider', 'N/A')}")
            print(f"✅ Recommendations By:      {ai_attr.get('recommendations_by', 'N/A')}")
            print(f"✅ Medicines By:            {ai_attr.get('medicines_by', 'N/A')}")
            print(f"✅ Prescriptions By:        {ai_attr.get('prescriptions_by', 'N/A')}")
            print(f"✅ Synthesis By:            {ai_attr.get('synthesis_by', 'N/A')}")
        else:
            print(f"❌ AI attribution data missing")
        
        # Display Agent Information with Tokens
        print("\n" + "="*90)
        print("⚡ AGENT EXECUTION & TOKENS")
        print("="*90)
        
        agent_exec = result.get("agent_execution", {})
        if agent_exec:
            print(f"✅ Total Agents:            {agent_exec.get('total_agents', 0)}")
            print(f"✅ Successful:              {agent_exec.get('successful_agents', 0)}")
            print(f"✅ Total Tokens Used:       {agent_exec.get('total_tokens', 0)}")
            
            agents = agent_exec.get('agents', [])
            if agents:
                print(f"\n   Agent Execution Details:")
                for agent in agents[:6]:
                    status = "✅" if agent.get('success') else "❌"
                    name = agent.get('name', 'Unknown')
                    exec_time = agent.get('execution_time', 0)
                    tokens = agent.get('tokens_used', 0)
                    print(f"   {status} {name:35} {exec_time:6.2f}s  {tokens:8} tokens")
        else:
            print(f"❌ Agent execution data missing")
        
        # Verify Data Structure
        print("\n" + "="*90)
        print("📋 DATA STRUCTURE VERIFICATION")
        print("="*90)
        
        checks = [
            ("AI Attribution Present", ai_attr is not None and len(ai_attr) > 0),
            ("Primary Provider Set", bool(ai_attr.get('primary_provider'))),
            ("Agent Execution Present", agent_exec is not None),
            ("Tokens Recorded", agent_exec.get('total_tokens', 0) > 0),
            ("Prescriptions", len(result.get('prescriptions', [])) > 0),
            ("Medicines", len(result.get('medicines', [])) > 0),
            ("Recommendations", len(result.get('recommendations', [])) > 0),
        ]
        
        passed = sum(1 for _, check in checks if check)
        total = len(checks)
        
        for check_name, check_result in checks:
            status = "✅ PASS" if check_result else "❌ FAIL"
            print(f"{status} | {check_name}")
        
        # Summary
        print("\n" + "="*90)
        if passed == total:
            print(f"🎉 ALL FEATURES WORKING! ({passed}/{total} checks passed)")
            print("\nDashboard now displays:")
            print("  ✓ Tokens used by each agent")
            print("  ✓ AI provider attribution for recommendations")
            print("  ✓ AI provider attribution for medicines")
            print("  ✓ AI provider attribution for prescriptions")
            print("  ✓ Summary shows which AI analyzed the report")
        else:
            print(f"⚠️  {passed}/{total} checks passed")
        print("="*90 + "\n")
        
        return passed == total
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n🔬 BLOOD REPORT AI - ENHANCED DASHBOARD TEST\n")
    
    try:
        if requests.get(f"{BASE_URL}/health", timeout=5).status_code == 200:
            print("✅ Server is responding\n")
            test_enhanced_dashboard()
        else:
            print("❌ Server is not responding")
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
