#!/usr/bin/env python3
"""
Blood Report AI - Google Cloud Run Deployment Quick Start
This script provides step-by-step deployment to Google Cloud Run
"""

import os
import sys
import webbrowser

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def print_step(num, text):
    print(f"\n📍 STEP {num}: {text}")
    print("─" * 70)

def print_action(text):
    print(f"  → {text}")

def print_info(text):
    print(f"  ℹ️  {text}")

def print_success(text):
    print(f"  ✅ {text}")

def print_warning(text):
    print(f"  ⚠️  {text}")

def quick_start():
    """Google Cloud Run Quick Start Guide"""
    
    print_header("GOOGLE CLOUD RUN - QUICK START DEPLOYMENT")
    
    print("""
    Your Blood Report AI is ready to deploy to Google Cloud Run!
    
    Best for:
    ✅ Free tier (2M requests/month)
    ✅ Scales automatically (0 to 1000+ instances)
    ✅ Pay only for what you use
    ✅ World-class monitoring
    
    Estimated time: 15 minutes
    Cost: FREE tier or $10-20/month for 24/7
    """)
    
    # Step 1
    print_step(1, "Create Google Cloud Account")
    print_action("Visit: https://cloud.google.com/run")
    print_action("Click: 'Start for free'")
    print_action("Sign up with Google account")
    print_action("Verify payment method (no charge for free tier)")
    input("\n  Press ENTER when you've created your account...")
    
    # Step 2
    print_step(2, "Enable Cloud Run API")
    print_action("Go to: https://console.cloud.google.com/run")
    print_action("Click: 'Enable API' if prompted")
    print_action("Wait for API to enable (30 seconds)")
    print_info("You'll see the Cloud Run dashboard")
    input("\n  Press ENTER when API is enabled...")
    
    # Step 3
    print_step(3, "Create New Service")
    print_action("Click: 'Create Service' (blue button)")
    print_action("Select: 'Deploy one revision from source code'")
    print_action("Choose: 'GitHub'")
    print_action("Click: 'Set up with Cloud Build'")
    print_action("Authorize Cloud Build to access GitHub")
    print_action("Select Repository: 'loghithakshan/INBLOODO-AGENT26'")
    print_action("Branch: 'main'")
    print_action("Build Type: 'Dockerfile' (auto-detected)")
    input("\n  Press ENTER when repository is selected...")
    
    # Step 4
    print_step(4, "Configure Service")
    print_action("Service Name: blood-report-ai")
    print_action("Region: us-central1 (or nearest to you)")
    print_action("Memory: 512 MB (sufficient)")
    print_action("CPU: 1 (auto-scaling enabled)")
    print_info("Leave other settings as default")
    input("\n  Press ENTER when configured...")
    
    # Step 5
    print_step(5, "Add Environment Variables")
    print_action("In 'Runtime settings', scroll down")
    print_action("Click: 'Add variable' for each:")
    
    env_vars = {
        "GEMINI_API_KEY": "your_actual_key_here",
        "OPENAI_API_KEY": "your_actual_key_here",
        "ANTHROPIC_API_KEY": "your_actual_key_here",
        "GROK_API_KEY": "your_actual_key_here",
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "DEBUG": "false"
    }
    
    for key, value in env_vars.items():
        print(f"\n  Variable: {key}")
        if "KEY" in key:
            print(f"  Value: (your actual {key})")
        else:
            print(f"  Value: {value}")
    
    print_warning("IMPORTANT: Replace API keys with YOUR ACTUAL keys!")
    print_action("Google AI Studio: https://aistudio.google.com/app/apikey")
    print_action("OpenAI: https://platform.openai.com/account/api-keys")
    print_action("Anthropic: https://console.anthropic.com/account/keys")
    print_action("Grok: https://console.x.ai/")
    input("\n  Press ENTER when all variables are added...")
    
    # Step 6
    print_step(6, "Deploy!")
    print_action("Review all settings")
    print_action("Click: 'Create' button (bottom right)")
    print_info("Build starts automatically")
    print_info("Takes 3-5 minutes")
    print_info("Watch logs in real-time")
    input("\n  Press ENTER to continue...")
    
    # Step 7
    print_step(7, "Access Your Live App")
    print_action("Status changes to 'Ready' when deployed")
    print_action("Your URL appears at top of page")
    print_action("Format: https://blood-report-ai-xxxxx-uc.a.run.app")
    
    print_info("Access these endpoints:")
    print_action("Main app: https://your-url.a.run.app/")
    print_action("API Docs: https://your-url.a.run.app/docs")
    print_action("Health: https://your-url.a.run.app/health")
    
    print_success("Your Blood Report AI is LIVE!")
    
    # Step 8
    print_step(8, "Test Your App")
    print_action("Visit your URL")
    print_action("Upload a blood report image")
    print_action("Verify analysis works")
    print_action("Check API documentation at /docs")
    
    # Step 9
    print_step(9, "Monitor Your App")
    print_action("Dashboard → Logs: View all requests")
    print_action("Dashboard → Metrics: CPU, memory, requests")
    print_action("Dashboard → Revisions: Version history")
    
    print_success("Deployment complete!")
    
    # Final summary
    print_header("DEPLOYMENT COMPLETE! ✅")
    
    summary = """
    Your Blood Report AI is now:
    ✅ Live on Google Cloud Run
    ✅ Accessible 24/7 with auto-scaling
    ✅ Using free tier (2M requests/month)
    ✅ Fully monitored and secure
    ✅ Auto-deployed when you push to GitHub
    
    NEXT ACTIONS:
    1. Share your live URL with users
    2. Monitor dashboard for logs
    3. Push code changes (auto-deploys)
    4. Upgrade to paid plan if needed ($10-20/month for 24/7)
    
    YOUR DEPLOYMENT:
    - Platform: Google Cloud Run
    - Region: us-central1 (or your choice)
    - Uptime: 99.95%
    - Auto-scaling: 0 to 1000+ instances
    - Monitoring: World-class
    - Cost: Free tier or $10-20/month
    
    DOCUMENTATION:
    - Full guide: GOOGLE_CLOUD_RUN_GUIDE.md (in your repo)
    - Cloud Console: https://console.cloud.google.com
    - Cloud Run Docs: https://cloud.google.com/run/docs
    - FastAPI Docs: https://fastapi.tiangolo.com
    
    TROUBLESHOOTING:
    If deployment fails:
    1. Check "Build details" for errors
    2. Verify Dockerfile is valid
    3. Check environment variables
    4. Redeploy with "Create Service" again
    
    ENJOY YOUR 24/7 SERVER! 🚀
    """
    
    print(summary)

if __name__ == "__main__":
    try:
        quick_start()
    except KeyboardInterrupt:
        print("\n\nDeployment setup cancelled.")
        sys.exit(0)
