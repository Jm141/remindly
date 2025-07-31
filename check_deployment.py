#!/usr/bin/env python3
"""
Deployment Status Checker for Remindly Flask API
Checks if the API is deployed and working correctly
"""

import requests
import json
import time
from datetime import datetime

def check_api_status(url):
    """Check if the API is responding"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"Status code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, str(e)

def test_health_endpoint(url):
    """Test the health check endpoint"""
    try:
        response = requests.get(f"{url}/health", timeout=10)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"Health check failed: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, str(e)

def test_register_endpoint(url):
    """Test user registration endpoint"""
    try:
        data = {
            "username": "testuser",
            "email": "test@example.com", 
            "password": "password123"
        }
        response = requests.post(
            f"{url}/api/register",
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        return True, response.json()
    except requests.exceptions.RequestException as e:
        return False, str(e)

def main():
    """Main function to check deployment status"""
    print("🔍 Remindly API Deployment Status Checker")
    print("=" * 60)
    
    # Potential deployment URLs
    urls = [
        "https://remindly-api.onrender.com",
        "https://remindly.onrender.com", 
        "https://task-manager-api.onrender.com"
    ]
    
    print("Checking deployment URLs...")
    print()
    
    for url in urls:
        print(f"🌐 Testing: {url}")
        print("-" * 40)
        
        # Check main API status
        print("1. Checking API status...")
        success, result = check_api_status(url)
        if success:
            print("✅ API is responding!")
            print(f"   Response: {json.dumps(result, indent=2)}")
            
            # Test health endpoint
            print("\n2. Testing health endpoint...")
            health_success, health_result = test_health_endpoint(url)
            if health_success:
                print("✅ Health check passed!")
                print(f"   Response: {json.dumps(health_result, indent=2)}")
            else:
                print(f"❌ Health check failed: {health_result}")
            
            # Test registration endpoint
            print("\n3. Testing registration endpoint...")
            reg_success, reg_result = test_register_endpoint(url)
            if reg_success:
                print("✅ Registration endpoint working!")
                print(f"   Response: {json.dumps(reg_result, indent=2)}")
            else:
                print(f"❌ Registration failed: {reg_result}")
            
            print(f"\n🎉 SUCCESS! Your API is deployed at: {url}")
            print("=" * 60)
            return url
            
        else:
            print(f"❌ API not responding: {result}")
            print()
    
    print("❌ No working deployment found.")
    print("Check your Render dashboard for deployment status.")
    print("=" * 60)

if __name__ == "__main__":
    main() 