from pyngrok import ngrok
import time

print("\n" + "="*60)
print("🌐 NGROK TUNNEL SETUP")
print("="*60 + "\n")

try:
    # Connect ngrok (free tier) - authtoken already configured
    public_url = ngrok.connect(8000, "http")
    print(f"✅ Public URL: {public_url}")
    print(f"✅ Share this link with anyone!")
    print(f"\n🩺 INBLOODO Agent is now PUBLIC!")
    print(f"   Local:     http://localhost:8000")
    print(f"   Public:    {public_url}")
    print(f"\n📊 API Docs: {public_url}/docs")
    print(f"📊 Health:   {public_url}/health")
    print("="*60)
    print("\n✨ Your app is LIVE and accessible from anywhere!")
    print("Press Ctrl+C to stop the tunnel\n")
    print("="*60 + "\n")
    
    # Keep tunnel open
    ngrok_process = ngrok.get_ngrok_process()
    ngrok_process.proc.wait()
    
except Exception as e:
    print(f"⚠️  Error: {e}")
    print("If authtoken issue, logout and login again")
