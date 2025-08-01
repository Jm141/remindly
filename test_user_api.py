import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_user_management():
    """Test user management endpoints"""
    
    print("🧪 Testing User Management API Endpoints")
    print("=" * 50)
    
    # Test 1: Register a new user
    print("\n1. Testing User Registration...")
    register_data = {
        "username": "testuser",
        "password": "password123",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/register", json=register_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 201:
            print("✅ User registration successful!")
        else:
            print("❌ User registration failed!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Login
    print("\n2. Testing User Login...")
    login_data = {
        "username": "testuser",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/login", json=login_data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            login_response = response.json()
            access_token = login_response.get('access_token')
            print("✅ Login successful!")
            print(f"Access Token: {access_token[:20]}...")
        else:
            print("❌ Login failed!")
            print(f"Response: {response.json()}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Test 3: Get current user
    print("\n3. Testing Get Current User...")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/user", headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            user_data = response.json()
            print("✅ Get current user successful!")
            print(f"User: {user_data}")
        else:
            print("❌ Get current user failed!")
            print(f"Response: {response.json()}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Update user information
    print("\n4. Testing Update User Information...")
    update_data = {
        "email": "updated@example.com",
        "first_name": "Updated",
        "last_name": "Name"
    }
    
    try:
        response = requests.put(f"{BASE_URL}/user", json=update_data, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Update user successful!")
            print(f"Response: {response.json()}")
        else:
            print("❌ Update user failed!")
            print(f"Response: {response.json()}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 5: Update password
    print("\n5. Testing Update Password...")
    password_data = {
        "current_password": "password123",
        "new_password": "newpassword123"
    }
    
    try:
        response = requests.put(f"{BASE_URL}/user/password", json=password_data, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Update password successful!")
            print(f"Response: {response.json()}")
        else:
            print("❌ Update password failed!")
            print(f"Response: {response.json()}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 6: Update username
    print("\n6. Testing Update Username...")
    username_data = {
        "new_username": "newtestuser"
    }
    
    try:
        response = requests.put(f"{BASE_URL}/user/username", json=username_data, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Update username successful!")
            print(f"Response: {response.json()}")
        else:
            print("❌ Update username failed!")
            print(f"Response: {response.json()}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 7: Get all users (admin function)
    print("\n7. Testing Get All Users...")
    
    try:
        response = requests.get(f"{BASE_URL}/users", headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            users_data = response.json()
            print("✅ Get all users successful!")
            print(f"Users: {users_data}")
        else:
            print("❌ Get all users failed!")
            print(f"Response: {response.json()}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 User Management API Testing Complete!")

if __name__ == "__main__":
    test_user_management() 