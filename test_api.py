#!/usr/bin/env python3
"""
Simple test script to verify the API endpoints are working
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_register():
    """Test user registration"""
    print("🔍 Testing user registration...")
    data = {
        "username": "testuser",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/api/register", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
    return response.status_code == 201

def test_login():
    """Test user login"""
    print("🔍 Testing user login...")
    data = {
        "username": "testuser",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/api/login", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
    
    if response.status_code == 200:
        return response.json().get('access_token')
    return None

def test_tasks(token):
    """Test tasks endpoint with authentication"""
    if not token:
        print("❌ No token available, skipping tasks test")
        return
    
    print("🔍 Testing tasks endpoint...")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test GET tasks
    response = requests.get(f"{BASE_URL}/api/tasks", headers=headers)
    print(f"GET Tasks Status: {response.status_code}")
    print(f"GET Tasks Response: {response.json()}")
    
    # Test POST task
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "category": "Test",
        "priority": "Medium"
    }
    response = requests.post(f"{BASE_URL}/api/tasks", json=task_data, headers=headers)
    print(f"POST Task Status: {response.status_code}")
    print(f"POST Task Response: {response.json()}")
    print()

def main():
    print("🚀 Testing Task Manager API (SOLID Architecture)")
    print("=" * 50)
    
    # Test health
    test_health()
    
    # Test registration
    if test_register():
        print("✅ Registration successful!")
    else:
        print("❌ Registration failed!")
        return
    
    # Test login
    token = test_login()
    if token:
        print("✅ Login successful!")
    else:
        print("❌ Login failed!")
        return
    
    # Test tasks
    test_tasks(token)
    
    print("🎉 All tests completed!")

if __name__ == "__main__":
    main() 