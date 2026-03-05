#!/usr/bin/env python3
"""
Blood Report AI - Complete Google Cloud Run Deployment Automation
This script fully automates deployment to Google Cloud Run
"""

import subprocess
import sys
import os
import json
from pathlib import Path

def run_command(cmd, description=""):
    """Run a command and return success status"""
    try:
        if description:
            print(f"⏳ {description}...")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=Path(__file__).parent)
        if result.returncode == 0:
            if description:
                print(f"✅ {description}")
            return True, result.stdout
        else:
            print(f"❌ {description}")
            print(f"   Error: {result.stderr}")
            return False, result.stderr
    except Exception as e:
        print(f"❌ Error: {e}")
        return False, str(e)

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def print_step(num, text):
    print(f"\n📍 STEP {num}: {text}")

def print_success(text):
    print(f"✅ {text}")

def print_error(text):
    print(f"❌ {text}")

def main():
    """Main deployment automation"""
    
    print_header("BLOOD REPORT AI - GOOGLE CLOUD RUN DEPLOYMENT")
    print("""
    This script will automatically deploy your app to Google Cloud Run.
    
    Prerequisites:
    ✅ Google Cloud account (create at https://cloud.google.com)
    ✅ gcloud CLI installed (https://cloud.google.com/sdk/docs/install)
    ✅ Authenticated: gcloud auth login
    
    This script will:
    ✅ Create Cloud Run service
    ✅ Configure from Dockerfile
    ✅ Set environment variables
    ✅ Deploy automatically
    ✅ Provide live URL
    """)
    
    # Step 1: Check gcloud is installed
    print_step(1, "Checking gcloud CLI")
    success, output = run_command("gcloud --version", "Checking gcloud CLI installation")
    if not success:
        print_error("gcloud CLI not installed!")
        print("Install from: https://cloud.google.com/sdk/docs/install")
        return False
    
    # Step 2: Check authentication
    print_step(2, "Checking Google Cloud authentication")
    success, output = run_command("gcloud auth list", "Checking authentication")
    if not success or "ACTIVE" not in output:
        print("You need to authenticate with Google Cloud:")
        run_command("gcloud auth login", "Authenticating with Google Cloud")
    print_success("Google Cloud authenticated")
    
    # Step 3: Get or create project
    print_step(3, "Setting up Google Cloud project")
    success, output = run_command("gcloud config get-value project", "Getting current project")
    
    if not success or not output.strip():
        print("No project set. Please create a new project:")
        print("1. Go to: https://console.cloud.google.com/projectcreate")
        print("2. Create project: blood-report-ai")
        print("3. Copy the PROJECT_ID")
        
        project_id = input("\nEnter your Google Cloud PROJECT_ID: ").strip()
        if not project_id:
            print_error("Project ID required")
            return False
        
        run_command(f"gcloud config set project {project_id}", f"Setting project to {project_id}")
    else:
        project_id = output.strip()
        print_success(f"Using project: {project_id}")
    
    # Step 4: Enable Cloud Run API
    print_step(4, "Enabling Cloud Run API")
    run_command(f"gcloud services enable run.googleapis.com --project={project_id}", "Enabling Cloud Run API")
    run_command(f"gcloud services enable artifactregistry.googleapis.com --project={project_id}", "Enabling Artifact Registry")
    run_command(f"gcloud services enable cloudbuild.googleapis.com --project={project_id}", "Enabling Cloud Build")
    
    # Step 5: Configure environment variables
    print_step(5, "Setting up environment variables")
    
    env_vars = {
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY", ""),
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
        "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY", ""),
        "GROK_API_KEY": os.getenv("GROK_API_KEY", ""),
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "DEBUG": "false"
    }
    
    # Ask for API keys if not set
    for key in ["GEMINI_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GROK_API_KEY"]:
        if not env_vars[key]:
            value = input(f"\nEnter {key} (or press ENTER to skip): ").strip()
            if value:
                env_vars[key] = value
    
    # Build environment variable string
    env_string = ",".join([f"{k}={v}" for k, v in env_vars.items() if v])
    print_success(f"Environment variables configured: {len(env_vars.items())} variables")
    
    # Step 6: Deploy to Cloud Run
    print_step(6, "Deploying to Google Cloud Run")
    
    service_name = "blood-report-ai"
    region = "us-central1"
    
    deploy_cmd = f"""
    gcloud run deploy {service_name} \
      --source . \
      --platform managed \
      --region {region} \
      --allow-unauthenticated \
      --memory 512Mi \
      --cpu 1 \
      --timeout 3600 \
      --set-env-vars={env_string} \
      --project={project_id}
    """
    
    print(f"Deploying service: {service_name}")
    print(f"Region: {region}")
    print(f"Memory: 512Mi")
    print(f"CPU: 1")
    
    success, output = run_command(deploy_cmd, "Deploying to Cloud Run")
    
    if not success:
        print_error("Deployment failed!")
        print(output)
        return False
    
    print_success("Deployment completed!")
    
    # Step 7: Get service URL
    print_step(7, "Retrieving service URL")
    
    url_cmd = f"gcloud run services describe {service_name} --platform managed --region {region} --format='value(status.url)' --project={project_id}"
    success, url = run_command(url_cmd, "Getting service URL")
    
    if success and url:
        url = url.strip()
        print_success(f"Your app is live at: {url}")
        
        # Print final summary
        print_header("DEPLOYMENT COMPLETE! ✅")
        print(f"""
        🎉 Your Blood Report AI is now running on Google Cloud Run!
        
        📌 SERVICE DETAILS:
        Service Name: {service_name}
        Region: {region}
        Project: {project_id}
        
        🌐 LIVE URLs:
        Main App:    {url}/
        API Docs:    {url}/docs
        Health:      {url}/health
        
        ✨ FEATURES:
        ✅ 24/7 Uptime
        ✅ Auto-scaling (0 to 1000+ instances)
        ✅ HTTPS/SSL included
        ✅ Global distribution
        ✅ Integrated monitoring
        
        💰 PRICING:
        Free Tier: 2 million requests/month
        Additional: $0.40 per million requests
        24/7 average: $10-20/month
        
        📊 NEXT STEPS:
        1. Test your app: {url}
        2. Upload a blood report image
        3. Check logs: gcloud run logs read {service_name} --region {region}
        4. Monitor: https://console.cloud.google.com/run
        
        🔗 USEFUL COMMANDS:
        View logs:        gcloud run logs read {service_name} --region {region}
        View metrics:     gcloud run services describe {service_name} --region {region}
        Update service:   gcloud run deploy {service_name} --source .
        Delete service:   gcloud run services delete {service_name} --region {region}
        
        📚 DOCUMENTATION:
        Cloud Run: https://cloud.google.com/run/docs
        FastAPI: https://fastapi.tiangolo.com
        Your Repo: https://github.com/loghithakshan/INBLOODO-AGENT26
        
        Enjoy your live Blood Report AI! 🚀
        """)
        
        return True
    else:
        print_error("Could not retrieve service URL")
        print("Try checking: https://console.cloud.google.com/run")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nDeployment cancelled.")
        sys.exit(1)
