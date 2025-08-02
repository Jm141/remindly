#!/usr/bin/env python3
"""
Test script for logout functionality
"""

import requests
import json

BASE_URL = "https://remindly-api-gflf.onrender.com/api"

def test_logout():
    """Test user logout"""
    print("🔐 Testing User Logout...")
    
    # First, login to get a token
    login_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    try:
        # Login first
        print("🔐 Logging in to get token...")
        login_response = requests.post(
            f"{BASE_URL}/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if login_response.status_code != 200:
            print("❌ Login failed, cannot test logout")
            return False
        
        login_data = login_response.json()
        access_token = login_data['access_token']
        print(f"🎫 Got access token: {access_token[:20]}...")
        
        # Now test logout
        print("🔐 Testing logout...")
        logout_headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        logout_response = requests.post(
            f"{BASE_URL}/logout",
            headers=logout_headers
        )
        
        print(f"📡 Logout Status Code: {logout_response.status_code}")
        print(f"📄 Logout Response: {logout_response.text}")
        
        if logout_response.status_code == 200:
            print("✅ Logout successful!")
            
            # Test that the token is now invalid by trying to access a protected endpoint
            print("🔐 Testing that token is now invalid...")
            test_response = requests.get(
                f"{BASE_URL}/tasks",
                headers=logout_headers
            )
            
            print(f"📡 Test Status Code: {test_response.status_code}")
            print(f"📄 Test Response: {test_response.text}")
            
            if test_response.status_code == 401:
                print("✅ Token correctly invalidated after logout!")
                return True
            else:
                print("❌ Token should have been invalidated after logout!")
                return False
        else:
            print("❌ Logout failed!")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server.")
        return False
    except Exception as e:
        print(f"❌ Error during logout test: {e}")
        return False

def test_logout_without_token():
    """Test logout without providing a token"""
    print("\n🔐 Testing Logout Without Token...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/logout",
            headers={"Content-Type": "application/json"}
        )
        
        print(f"📡 Status Code: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 401:
            print("✅ Logout without token correctly rejected!")
            return True
        else:
            print("❌ Logout without token should have been rejected!")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server.")
        return False
    except Exception as e:
        print(f"❌ Error during logout without token test: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting Logout API Tests...")
    print("=" * 50)
    
    # Test logout with valid token
    logout_success = test_logout()
    
    # Test logout without token
    test_logout_without_token()
    
    print("\n" + "=" * 50)
    print("🏁 Logout API Tests Completed!")

if __name__ == "__main__":
    main() 
 