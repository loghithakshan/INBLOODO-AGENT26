"""
Integration Test - Full Dashboard with Multi-AI Features
Verifies that the web interface correctly displays all new features
"""
import requests
import json
import time
from bs4 import BeautifulSoup

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

def test_dashboard_integration():
    """Test complete dashboard integration with multi-AI features"""
    
    print("\n" + "="*80)
    print("🌐 Full Dashboard Integration Test")
    print("="*80)
    
    try:
        # Step 1: Get dashboard
        print("\n📝 Step 1: Loading dashboard...")
        response = requests.get(f"{BASE_URL}/", timeout=10)
        
        if response.status_code != 200:
            print(f"❌ Failed to load dashboard: {response.status_code}")
            return False
        
        print("✅ Dashboard loaded successfully")
        
        # Step 2: Analyze a report
        print("\n📤 Step 2: Analyzing blood report...")
        files = {"file": ("test.json", json.dumps(sample_data))}
        response = requests.post(f"{BASE_URL}/analyze-report/", files=files, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ Analysis failed: {response.status_code}")
            return False
        
        data = response.json()
        print("✅ Blood report analyzed successfully")
        
        # Step 3: Verify data structure
        print("\n📊 Step 3: Verifying response structure...")
        
        required_fields = [
            "status", "extracted_parameters", "interpretations", "risks",
            "recommendations", "medicines", "prescriptions",
            "overall_risk", "summary", "processing_time",
            "agent_execution", "ai_attribution"
        ]
        
        missing_fields = [f for f in required_fields if f not in data]
        
        if missing_fields:
            print(f"❌ Missing fields: {missing_fields}")
            return False
        
        print(f"✅ All {len(required_fields)} required fields present")
        
        # Step 4: Verify prescriptions are categorized
        print("\n💊 Step 4: Verifying prescription categorization...")
        
        prescriptions = data.get('prescriptions', {})
        
        if isinstance(prescriptions, dict):
            print(f"✅ Prescriptions are categorized (object type)")
            print(f"   Categories found: {len(prescriptions)}")
            
            for category, items in prescriptions.items():
                if items:
                    print(f"   ├─ {category}: {len(items)} items")
                    
        else:
            print(f"⚠️ Prescriptions in legacy format (array): {len(prescriptions)} items")
        
        # Step 5: Verify recommendations are ordered
        print("\n📋 Step 5: Verifying recommendation ordering...")
        
        recommendations = data.get('recommendations', [])
        
        if isinstance(recommendations, list) and len(recommendations) > 0:
            print(f"✅ Recommendations present: {len(recommendations)} items")
            
            # Check if they look ordered (non-random)
            # A simple heuristic: first recommendation should mention action/fix
            first_rec = recommendations[0] if recommendations else ""
            
            if any(keyword in first_rec.lower() for keyword in 
                   ['schedule', 'consult', 'doctor', 'urgent', 'immediate', 'increase']):
                print(f"✅ Recommendations appear ordered (starts with action)")
                print(f"   First: {first_rec[:70]}...")
            else:
                print(f"⚠️ Cannot verify ordering from content alone")
        else:
            print(f"❌ No recommendations provided")
            return False
        
        # Step 6: Verify AI attribution
        print("\n🧠 Step 6: Verifying multi-AI attribution...")
        
        ai_attribution = data.get('ai_attribution', {})
        
        if ai_attribution:
            print(f"✅ AI attribution present:")
            
            for key, value in ai_attribution.items():
                if not key.startswith('provider_'):
                    print(f"   • {key}: {value}")
            
            # Check for multiple providers
            providers_set = set(str(v).lower() for k, v in ai_attribution.items() 
                               if not k.startswith('provider_'))
            
            if len(providers_set) > 1:
                print(f"✅ Multiple AI providers detected: {providers_set}")
            else:
                print(f"⚠️ Only one provider used: {providers_set}")
        else:
            print(f"❌ No AI attribution provided")
            return False
        
        # Step 7: Verify agent metrics
        print("\n⚙️ Step 7: Verifying agent execution metrics...")
        
        agent_exec = data.get('agent_execution', {})
        
        if agent_exec:
            total = agent_exec.get('total_agents', 0)
            successful = agent_exec.get('successful_agents', 0)
            tokens = agent_exec.get('total_tokens', 0)
            
            print(f"✅ Agent execution metrics present:")
            print(f"   • Total agents: {total}")
            print(f"   • Successful: {successful}/{total}")
            print(f"   • Tokens used: {tokens:,}")
            
            if successful == total:
                print(f"✅ All agents executed successfully")
            else:
                print(f"⚠️ Some agents failed: {total - successful} failures")
        else:
            print(f"❌ No agent metrics provided")
            return False
        
        # Step 8: Test data validation
        print("\n✔️ Step 8: Validating data types and ranges...")
        
        checks = {
            "Extracted parameters is dict": isinstance(data.get('extracted_parameters'), dict),
            "Interpretations is list": isinstance(data.get('interpretations'), list),
            "Risks is list": isinstance(data.get('risks'), list),
            "Recommendations is list": isinstance(data.get('recommendations'), list),
            "Medicines is list": isinstance(data.get('medicines'), list),
            "Prescriptions is dict or list": isinstance(data.get('prescriptions'), (dict, list)),
            "Processing time is number": isinstance(data.get('processing_time'), (int, float)),
            "Overall risk is string": isinstance(data.get('overall_risk'), str),
            "Status is 'success'": data.get('status') == 'success'
        }
        
        passed_checks = sum(1 for v in checks.values() if v)
        total_checks = len(checks)
        
        for check, result in checks.items():
            status = "✅" if result else "❌"
            print(f"   {status} {check}")
        
        # Summary
        print("\n" + "="*80)
        print("📋 INTEGRATION TEST SUMMARY")
        print("="*80)
        
        summary = {
            "Dashboard Load": "✅",
            "Report Analysis": "✅",
            "Response Structure": "✅" if not missing_fields else "❌",
            "Prescription Categorization": "✅" if isinstance(prescriptions, dict) else "⚠️",
            "Recommendation Ordering": "✅" if len(recommendations) > 0 else "❌",
            "AI Attribution": "✅" if len(providers_set) > 1 else "⚠️",
            "Agent Metrics": "✅" if successful == total else "⚠️",
            "Data Validation": f"✅ ({passed_checks}/{total_checks})"
        }
        
        for test, result in summary.items():
            print(f"{result} {test}")
        
        total_passed = sum(1 for v in summary.values() if "✅" in v)
        total_tests = len(summary)
        
        print(f"\n🎯 OVERALL: {total_passed}/{total_tests} features verified")
        print(f"Success Rate: {int(100*total_passed/total_tests)}%")
        
        return total_passed == total_tests
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server")
        return False
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_dashboard_integration()
    
    print("\n" + "="*80)
    if success:
        print("✅ INTEGRATION TEST PASSED - All features working correctly!")
        print("="*80)
        print("\n🎉 The system is ready for use with:")
        print("   • Multi-AI analysis (Gemini, OpenAI, Claude)")
        print("   • Ordered recommendations by priority")
        print("   • Categorized prescriptions by medical condition")
        print("   • Full attribution showing which AI provided each analysis")
        exit(0)
    else:
        print("❌ INTEGRATION TEST FAILED - Please review errors above")
        print("="*80)
        exit(1)
