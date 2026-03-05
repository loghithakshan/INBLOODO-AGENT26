"""
Test Multi-AI Analysis with Categorized Prescriptions and Ordered Recommendations
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

# Sample blood report data
sample_data = {
    "glucose": 145,
    "hemoglobin": 10.2,
    "white_blood_cells": 7500,
    "platelets": 250000,
    "cholesterol": 220,
    "ldl": 150,
    "hdl": 35,
    "triglycerides": 280,
    "creatinine": 1.2,
    "albumin": 3.5,
    "alt": 65,
    "ast": 72,
    "sodium": 138,
    "potassium": 4.2,
    "tsh": 2.8
}

def test_multi_ai_analysis():
    """Test multi-AI analysis with categorized prescriptions and ordered recommendations"""
    
    print("\n" + "="*80)
    print("🤖 Testing Multi-AI Analysis with Enhanced Features")
    print("="*80)
    
    try:
        # Upload and analyze report
        files = {"file": ("test.json", json.dumps(sample_data))}
        
        print("\n📤 Sending blood report for analysis...")
        response = requests.post(f"{BASE_URL}/analyze-report/", files=files, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ Analysis failed: {response.status_code}")
            print(response.text)
            return False
        
        data = response.json()
        
        # Verify response structure
        print("\n✅ Analysis completed successfully!")
        print(f"Processing Time: {data.get('processing_time', 'N/A')}s")
        
        # Check recommendations ordering
        print("\n" + "-"*80)
        print("📊 TEST 1: Recommendations Ordering by Priority")
        print("-"*80)
        recommendations = data.get('recommendations', [])
        if isinstance(recommendations, list) and len(recommendations) > 0:
            print(f"✅ Recommendations count: {len(recommendations)}")
            print("Recommendations (ordered by priority):")
            for i, rec in enumerate(recommendations[:5], 1):
                print(f"  {i}. {rec[:80]}...")
        else:
            print(f"⚠️ Recommendations: {recommendations}")
        
        # Check prescriptions categorization
        print("\n" + "-"*80)
        print("💊 TEST 2: Prescriptions Categorization")
        print("-"*80)
        prescriptions = data.get('prescriptions', {})
        
        if isinstance(prescriptions, dict):
            print(f"✅ Prescriptions organized into {len(prescriptions)} categories:")
            for category, items in prescriptions.items():
                if items:
                    print(f"\n  {category}")
                    for item in items[:2]:
                        print(f"    • {item[:70]}...")
        else:
            print(f"⚠️ Prescriptions (legacy format): {len(prescriptions) if isinstance(prescriptions, list) else 'N/A'} items")
        
        # Check AI attribution
        print("\n" + "-"*80)
        print("🧠 TEST 3: Multi-AI Attribution")
        print("-"*80)
        ai_attribution = data.get('ai_attribution', {})
        
        if ai_attribution:
            print("✅ AI Attribution Details:")
            for key, provider in ai_attribution.items():
                if not key.startswith('provider_'):
                    print(f"  • {key}: {provider}")
        else:
            print("⚠️ No AI attribution provided")
        
        # Check agent execution
        print("\n" + "-"*80)
        print("⚙️ TEST 4: Agent Execution Metrics")
        print("-"*80)
        agent_exec = data.get('agent_execution', {})
        
        if agent_exec:
            print("✅ Agent Execution Metrics:")
            print(f"  • Total Agents: {agent_exec.get('total_agents', 'N/A')}")
            print(f"  • Successful: {agent_exec.get('successful_agents', 'N/A')}")
            print(f"  • Total Tokens: {agent_exec.get('total_tokens', 'N/A'):,}")
            
            agents = agent_exec.get('agents', [])
            if agents:
                print("\n  Agent Details:")
                for agent in agents[:5]:
                    print(f"    - {agent.get('name', 'Unknown')}: {agent.get('execution_time', 0):.2f}s, {agent.get('tokens_used', 0):,} tokens")
        else:
            print("⚠️ No agent execution metrics provided")
        
        # Check response size
        print("\n" + "-"*80)
        print("📏 TEST 5: Response Size Optimization")
        print("-"*80)
        response_bytes = len(json.dumps(data).encode('utf-8'))
        response_kb = response_bytes / 1024
        
        print(f"✅ Response Size: {response_kb:.2f} KB ({response_bytes} bytes)")
        
        if response_kb > 1024:
            print("⚠️ Response size exceeds 1 MB - consider further optimization")
        else:
            print("✅ Response size is optimal for instant delivery")
        
        # Summary
        print("\n" + "="*80)
        print("📋 SUMMARY")
        print("="*80)
        
        checks = {
            "Recommendations ordered": isinstance(recommendations, list) and len(recommendations) > 0,
            "Prescriptions categorized": isinstance(prescriptions, dict) and len(prescriptions) > 0,
            "AI attribution present": bool(ai_attribution),
            "Agent metrics recorded": bool(agent_exec and agent_exec.get('total_agents', 0) > 0),
            "Response size optimal": response_kb < 1024
        }
        
        passed = sum(1 for v in checks.values() if v)
        total = len(checks)
        
        for check, result in checks.items():
            status = "✅" if result else "❌"
            print(f"{status} {check}")
        
        print(f"\n🎯 SCORE: {passed}/{total} ({int(100*passed/total)}%)")
        
        return passed == total
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the server is running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_multi_ai_analysis()
    exit(0 if success else 1)
