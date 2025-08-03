#!/usr/bin/env python3
"""
Simple API test script to fetch all users via HTTP requests
This demonstrates how to test the API endpoints
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:5000"  # Change this to your Render URL when deployed
API_PREFIX = "/api"

def test_get_all_users():
    """Test fetching all users via API endpoint"""
    try:
        print("🌐 Testing API endpoint to fetch all users...")
        print(f"📡 Making request to: {BASE_URL}{API_PREFIX}/users")
        
        # Make the request
        response = requests.get(f"{BASE_URL}{API_PREFIX}/users", timeout=10)
        
        print(f"📊 Response Status: {response.status_code}")
        print(f"📋 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            users = response.json()
            print(f"✅ Successfully fetched {len(users)} users:")
            
            for i, user in enumerate(users, 1):
                print(f"\n👤 User #{i}:")
                print(f"   ID: {user.get('id', 'N/A')}")
                print(f"   Username: {user.get('username', 'N/A')}")
                print(f"   Email: {user.get('email', 'Not provided')}")
                print(f"   Created: {user.get('created_at', 'N/A')}")
                print("-" * 40)
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Could not connect to the server")
        print("💡 Make sure your Flask app is running on localhost:5000")
        print("💡 Or update BASE_URL to point to your deployed Render URL")
    except requests.exceptions.Timeout:
        print("❌ Timeout Error: Request took too long")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")

def test_api_health():
    """Test the health check endpoint"""
    try:
        print("\n🏥 Testing API health check...")
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        
        print(f"📊 Health Status: {response.status_code}")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ API is healthy: {health_data}")
        else:
            print(f"❌ API health check failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")

def test_api_root():
    """Test the API root endpoint"""
    try:
        print("\n🏠 Testing API root endpoint...")
        response = requests.get(f"{BASE_URL}/", timeout=5)
        
        print(f"📊 Root Status: {response.status_code}")
        if response.status_code == 200:
            root_data = response.json()
            print(f"✅ API root response: {json.dumps(root_data, indent=2)}")
        else:
            print(f"❌ API root failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Root endpoint error: {str(e)}")

def test_user_registration():
    """Test user registration (for creating test data)"""
    try:
        print("\n📝 Testing user registration...")
        
        # Create a unique username
        timestamp = int(time.time())
        test_user_data = {
            "username": f"testuser_{timestamp}",
            "password": "testpassword123",
            "email": f"testuser_{timestamp}@example.com"
        }
        
        print(f"📋 Registering user: {test_user_data['username']}")
        
        response = requests.post(
            f"{BASE_URL}{API_PREFIX}/register",
            json=test_user_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"📊 Registration Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ User registered successfully!")
            print(f"   User ID: {result.get('user', {}).get('id', 'N/A')}")
            print(f"   Username: {result.get('user', {}).get('username', 'N/A')}")
        elif response.status_code == 400:
            print(f"⚠️ Registration failed (expected for duplicate user): {response.text}")
        else:
            print(f"❌ Registration failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Registration error: {str(e)}")

def main():
    """Main test function"""
    print("🚀 Starting API User Tests")
    print("=" * 60)
    
    # Test 1: Health check
    test_api_health()
    
    # Test 2: API root
    test_api_root()
    
    # Test 3: User registration (to create test data)
    test_user_registration()
    
    # Test 4: Fetch all users
    test_get_all_users()
    
    print("\n" + "=" * 60)
    print("🏁 All API tests completed!")
    print("\n💡 Tips:")
    print("   - If you get connection errors, make sure your Flask app is running")
    print("   - Update BASE_URL to your Render URL when testing the deployed version")
    print("   - The unique ID system will generate IDs like 'user_abc12345'")

if __name__ == "__main__":
    main() 