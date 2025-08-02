#!/usr/bin/env python3
"""
Test script for authentication APIs
"""

import requests
import json
import time

BASE_URL = "https://remindly-api-gflf.onrender.com/api"

def test_register():
    """Test user registration"""
    print("🔐 Testing User Registration...")
    
    register_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/register",
            json=register_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"📡 Status Code: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code in [200, 201]:
            print("✅ Registration successful!")
            return True
        else:
            print("❌ Registration failed!")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the server is running.")
        return False
    except Exception as e:
        print(f"❌ Error during registration: {e}")
        return False

def test_login():
    """Test user login"""
    print("\n🔐 Testing User Login...")
    
    login_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"📡 Status Code: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Login successful!")
            # Try to parse the response to get the token
            try:
                data = response.json()
                if 'access_token' in data:
                    print(f"🎫 Access token received: {data['access_token'][:20]}...")
                    return data['access_token']
                else:
                    print("⚠️ No access token in response")
                    return None
            except json.JSONDecodeError:
                print("⚠️ Could not parse JSON response")
                return None
        else:
            print("❌ Login failed!")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server.")
        return None
    except Exception as e:
        print(f"❌ Error during login: {e}")
        return None

def test_protected_endpoint(token):
    """Test accessing a protected endpoint with the token"""
    if not token:
        print("❌ No token available, skipping protected endpoint test")
        return
    
    print("\n🔐 Testing Protected Endpoint...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            f"{BASE_URL}/tasks",
            headers=headers
        )
        
        print(f"📡 Status Code: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Protected endpoint access successful!")
        else:
            print("❌ Protected endpoint access failed!")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server.")
    except Exception as e:
        print(f"❌ Error accessing protected endpoint: {e}")

def test_api_status():
    """Test the API status endpoint"""
    print("🌐 Testing API Status...")
    
    try:
        response = requests.get("https://remindly-api-gflf.onrender.com/")
        
        print(f"📡 Status Code: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ API is running successfully!")
            return True
        else:
            print("❌ API status check failed!")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API.")
        return False
    except Exception as e:
        print(f"❌ Error checking API status: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting Authentication API Tests...")
    print("=" * 50)
    
    # Test API status first
    api_status = test_api_status()
    
    if not api_status:
        print("❌ API is not accessible. Exiting tests.")
        return
    
    print("\n" + "=" * 30)
    
    # Test registration
    register_success = test_register()
    
    # Wait a moment between tests
    time.sleep(1)
    
    # Test login
    token = test_login()
    
    # Test protected endpoint
    test_protected_endpoint(token)
    
    print("\n" + "=" * 50)
    print("🏁 Authentication API Tests Completed!")

if __name__ == "__main__":
    main() 