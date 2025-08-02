#!/usr/bin/env python3
"""
Test script for authentication APIs with different user
"""

import requests
import json
import time

BASE_URL = "https://remindly-api-gflf.onrender.com/api"

def test_register_new_user():
    """Test user registration with a new username"""
    print("🔐 Testing User Registration (New User)...")
    
    # Use timestamp to ensure unique username
    timestamp = int(time.time())
    username = f"testuser_{timestamp}"
    
    register_data = {
        "username": username,
        "password": "testpass123"
    }
    
    print(f"📝 Using username: {username}")
    
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
            return username
        else:
            print("❌ Registration failed!")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server.")
        return None
    except Exception as e:
        print(f"❌ Error during registration: {e}")
        return None

def test_login_user(username):
    """Test user login"""
    print(f"\n🔐 Testing User Login for {username}...")
    
    login_data = {
        "username": username,
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

def test_duplicate_registration():
    """Test registering with the same username (should fail)"""
    print("\n🔐 Testing Duplicate Registration...")
    
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
        
        if response.status_code == 400:
            print("✅ Duplicate registration correctly rejected!")
            return True
        else:
            print("❌ Duplicate registration should have been rejected!")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server.")
        return False
    except Exception as e:
        print(f"❌ Error during duplicate registration: {e}")
        return False

def test_invalid_login():
    """Test login with wrong password"""
    print("\n🔐 Testing Invalid Login (Wrong Password)...")
    
    login_data = {
        "username": "testuser",
        "password": "wrongpassword"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"📡 Status Code: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 401:
            print("✅ Invalid login correctly rejected!")
            return True
        else:
            print("❌ Invalid login should have been rejected!")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server.")
        return False
    except Exception as e:
        print(f"❌ Error during invalid login: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting Extended Authentication API Tests...")
    print("=" * 60)
    
    # Test registration with new user
    new_username = test_register_new_user()
    
    if new_username:
        # Test login with new user
        token = test_login_user(new_username)
        
        if token:
            print(f"✅ New user {new_username} can register and login successfully!")
    
    # Test duplicate registration
    test_duplicate_registration()
    
    # Test invalid login
    test_invalid_login()
    
    print("\n" + "=" * 60)
    print("🏁 Extended Authentication API Tests Completed!")

if __name__ == "__main__":
    main() 