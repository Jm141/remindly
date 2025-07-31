#!/usr/bin/env python3
"""
Deployment Verification Script
Checks if the API is properly deployed and accessible
"""

import requests
import time
import sys

def check_deployment(url, max_attempts=10):
    """Check deployment with multiple attempts"""
    print(f"🔍 Checking deployment at: {url}")
    print("=" * 50)
    
    for attempt in range(1, max_attempts + 1):
        print(f"Attempt {attempt}/{max_attempts}...")
        
        try:
            # Test basic connectivity
            response = requests.get(url, timeout=15)
            
            if response.status_code == 200:
                print("✅ SUCCESS! API is responding!")
                print(f"Response: {response.text[:200]}...")
                return True
            else:
                print(f"❌ Status code: {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection refused - service may be starting up...")
        except requests.exceptions.Timeout:
            print("❌ Request timeout - service may be overloaded...")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        if attempt < max_attempts:
            print("⏳ Waiting 30 seconds before next attempt...")
            time.sleep(30)
        print()
    
    return False

def main():
    """Main verification function"""
    print("🚀 Remindly API Deployment Verification")
    print("=" * 60)
    
    # Test URLs
    urls = [
        "https://remindly-api.onrender.com",
        "https://remindly.onrender.com",
        "https://task-manager-api.onrender.com"
    ]
    
    success = False
    
    for url in urls:
        if check_deployment(url):
            print(f"\n🎉 DEPLOYMENT SUCCESSFUL!")
            print(f"Your API is live at: {url}")
            print("\n📋 Next steps:")
            print("1. Test the health endpoint: curl {url}/health")
            print("2. Test registration: curl -X POST {url}/api/register -H 'Content-Type: application/json' -d '{{\"username\":\"test\",\"email\":\"test@test.com\",\"password\":\"password123\"}}'")
            print("3. Check your Render dashboard for logs")
            success = True
            break
    
    if not success:
        print("\n❌ DEPLOYMENT NOT DETECTED")
        print("\n🔧 Troubleshooting steps:")
        print("1. Check your Render dashboard at https://render.com")
        print("2. Look for deployment logs and errors")
        print("3. Verify environment variables are set:")
        print("   - JWT_SECRET_KEY")
        print("   - SECRET_KEY")
        print("   - FLASK_ENV=production")
        print("4. Check if the service is marked as 'Live' in Render")
        print("5. Wait a few more minutes - deployments can take 5-10 minutes")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main() 