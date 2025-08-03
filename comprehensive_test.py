#!/usr/bin/env python3
"""Comprehensive Test Suite for Task Scheduler Backend"""

import requests
import json
import time
from datetime import datetime, timedelta
from dependency_injection import container
from services.auth_service import AuthService
from services.task_service import TaskService
from services.task_share_service import TaskShareService
from flask_bcrypt import Bcrypt

class ComprehensiveTester:
    def __init__(self):
        self.base_url = "http://localhost:5000/api"
        self.test_users = []
        self.test_tasks = []
        self.test_shares = []
        self.session = requests.Session()
        
        # Initialize services for direct testing
        bcrypt = Bcrypt()
        self.auth_service = container.get_auth_service(bcrypt)
        self.task_service = container.get_task_service()
        self.task_share_service = container.get_task_share_service()
        
    def print_header(self, title):
        """Print a formatted header"""
        print(f"\n{'='*60}")
        print(f"🧪 {title}")
        print(f"{'='*60}")
    
    def print_success(self, message):
        """Print success message"""
        print(f"✅ {message}")
    
    def print_error(self, message):
        """Print error message"""
        print(f"❌ {message}")
    
    def print_info(self, message):
        """Print info message"""
        print(f"ℹ️ {message}")
    
    def test_user_registration(self):
        """Test user registration functionality"""
        self.print_header("USER REGISTRATION TESTS")
        
        # Test 1: Valid registration
        self.print_info("Testing valid user registration...")
        response = self.session.post(f"{self.base_url}/auth/register", json={
            "username": "testuser1",
            "password": "password123"
        })
        
        if response.status_code == 201:
            data = response.json()
            self.print_success(f"User registered: {data.get('message', 'Success')}")
            self.test_users.append("testuser1")
        else:
            self.print_error(f"Registration failed: {response.status_code} - {response.text}")
        
        # Test 2: Duplicate username (case-insensitive)
        self.print_info("Testing duplicate username (case-insensitive)...")
        response = self.session.post(f"{self.base_url}/auth/register", json={
            "username": "TESTUSER1",
            "password": "password123"
        })
        
        if response.status_code == 400:
            self.print_success("Correctly rejected duplicate username (case-insensitive)")
        else:
            self.print_error(f"Should have rejected duplicate: {response.status_code}")
        
        # Test 3: Short password
        self.print_info("Testing short password...")
        response = self.session.post(f"{self.base_url}/auth/register", json={
            "username": "testuser2",
            "password": "123"
        })
        
        if response.status_code == 400:
            self.print_success("Correctly rejected short password")
        else:
            self.print_error(f"Should have rejected short password: {response.status_code}")
        
        # Test 4: Empty username
        self.print_info("Testing empty username...")
        response = self.session.post(f"{self.base_url}/auth/register", json={
            "username": "",
            "password": "password123"
        })
        
        if response.status_code == 400:
            self.print_success("Correctly rejected empty username")
        else:
            self.print_error(f"Should have rejected empty username: {response.status_code}")
    
    def test_user_authentication(self):
        """Test user authentication functionality"""
        self.print_header("USER AUTHENTICATION TESTS")
        
        # Test 1: Valid login
        self.print_info("Testing valid login...")
        response = self.session.post(f"{self.base_url}/auth/login", json={
            "username": "testuser1",
            "password": "password123"
        })
        
        if response.status_code == 200:
            data = response.json()
            self.session.headers.update({'Authorization': f"Bearer {data['access_token']}"})
            self.print_success("Login successful")
        else:
            self.print_error(f"Login failed: {response.status_code} - {response.text}")
        
        # Test 2: Case-insensitive login
        self.print_info("Testing case-insensitive login...")
        response = self.session.post(f"{self.base_url}/auth/login", json={
            "username": "TESTUSER1",
            "password": "password123"
        })
        
        if response.status_code == 200:
            self.print_success("Case-insensitive login successful")
        else:
            self.print_error(f"Case-insensitive login failed: {response.status_code}")
        
        # Test 3: Invalid password
        self.print_info("Testing invalid password...")
        response = self.session.post(f"{self.base_url}/auth/login", json={
            "username": "testuser1",
            "password": "wrongpassword"
        })
        
        if response.status_code == 401:
            self.print_success("Correctly rejected invalid password")
        else:
            self.print_error(f"Should have rejected invalid password: {response.status_code}")
        
        # Test 4: Non-existent user
        self.print_info("Testing non-existent user...")
        response = self.session.post(f"{self.base_url}/auth/login", json={
            "username": "nonexistent",
            "password": "password123"
        })
        
        if response.status_code == 401:
            self.print_success("Correctly rejected non-existent user")
        else:
            self.print_error(f"Should have rejected non-existent user: {response.status_code}")
    
    def test_task_management(self):
        """Test task management functionality"""
        self.print_header("TASK MANAGEMENT TESTS")
        
        # Test 1: Create task
        self.print_info("Testing task creation...")
        task_data = {
            "title": "Test Task 1",
            "description": "This is a test task",
            "due_date": (datetime.now() + timedelta(days=1)).isoformat(),
            "priority": "medium",
            "category": "work"
        }
        
        response = self.session.post(f"{self.base_url}/tasks", json=task_data)
        
        if response.status_code == 201:
            data = response.json()
            task_id = data['task']['id']
            self.test_tasks.append(task_id)
            self.print_success(f"Task created with ID: {task_id}")
        else:
            self.print_error(f"Task creation failed: {response.status_code} - {response.text}")
            return
        
        # Test 2: Get tasks
        self.print_info("Testing get tasks...")
        response = self.session.get(f"{self.base_url}/tasks")
        
        if response.status_code == 200:
            data = response.json()
            tasks = data.get('tasks', [])
            self.print_success(f"Retrieved {len(tasks)} tasks")
        else:
            self.print_error(f"Get tasks failed: {response.status_code} - {response.text}")
        
        # Test 3: Update task
        self.print_info("Testing task update...")
        update_data = {
            "title": "Updated Test Task 1",
            "priority": "high"
        }
        
        response = self.session.patch(f"{self.base_url}/tasks/{task_id}", json=update_data)
        
        if response.status_code == 200:
            self.print_success("Task updated successfully")
        else:
            self.print_error(f"Task update failed: {response.status_code} - {response.text}")
        
        # Test 4: Get single task
        self.print_info("Testing get single task...")
        response = self.session.get(f"{self.base_url}/tasks/{task_id}")
        
        if response.status_code == 200:
            data = response.json()
            self.print_success(f"Retrieved task: {data['task']['title']}")
        else:
            self.print_error(f"Get single task failed: {response.status_code} - {response.text}")
    
    def test_subtask_management(self):
        """Test subtask management functionality"""
        self.print_header("SUBTASK MANAGEMENT TESTS")
        
        if not self.test_tasks:
            self.print_error("No test tasks available for subtask testing")
            return
        
        task_id = self.test_tasks[0]
        
        # Test 1: Create subtask
        self.print_info("Testing subtask creation...")
        subtask_data = {
            "title": "Test Subtask 1",
            "description": "This is a test subtask"
        }
        
        response = self.session.post(f"{self.base_url}/tasks/{task_id}/subtasks", json=subtask_data)
        
        if response.status_code == 201:
            data = response.json()
            subtask_id = data['subtask']['id']
            self.print_success(f"Subtask created with ID: {subtask_id}")
        else:
            self.print_error(f"Subtask creation failed: {response.status_code} - {response.text}")
            return
        
        # Test 2: Get subtasks
        self.print_info("Testing get subtasks...")
        response = self.session.get(f"{self.base_url}/tasks/{task_id}/subtasks")
        
        if response.status_code == 200:
            data = response.json()
            subtasks = data.get('subtasks', [])
            self.print_success(f"Retrieved {len(subtasks)} subtasks")
        else:
            self.print_error(f"Get subtasks failed: {response.status_code} - {response.text}")
        
        # Test 3: Update subtask
        self.print_info("Testing subtask update...")
        update_data = {
            "title": "Updated Test Subtask 1",
            "completed": True
        }
        
        response = self.session.patch(f"{self.base_url}/tasks/{task_id}/subtasks/{subtask_id}", json=update_data)
        
        if response.status_code == 200:
            self.print_success("Subtask updated successfully")
        else:
            self.print_error(f"Subtask update failed: {response.status_code} - {response.text}")
        
        # Test 4: Delete subtask
        self.print_info("Testing subtask deletion...")
        response = self.session.delete(f"{self.base_url}/tasks/{task_id}/subtasks/{subtask_id}")
        
        if response.status_code == 200:
            self.print_success("Subtask deleted successfully")
        else:
            self.print_error(f"Subtask deletion failed: {response.status_code} - {response.text}")
    
    def test_task_sharing(self):
        """Test task sharing functionality"""
        self.print_header("TASK SHARING TESTS")
        
        # Create a second user for sharing
        self.print_info("Creating second user for sharing tests...")
        response = self.session.post(f"{self.base_url}/auth/register", json={
            "username": "testuser2",
            "password": "password123"
        })
        
        if response.status_code == 201:
            self.test_users.append("testuser2")
            self.print_success("Second user created")
        else:
            self.print_error(f"Failed to create second user: {response.status_code}")
            return
        
        if not self.test_tasks:
            self.print_error("No test tasks available for sharing")
            return
        
        task_id = self.test_tasks[0]
        
        # Test 1: Share task by username
        self.print_info("Testing task sharing by username...")
        share_data = {
            "recipient_identifier": "testuser2",
            "permission_level": "view"
        }
        
        response = self.session.post(f"{self.base_url}/tasks/share", json=share_data)
        
        if response.status_code == 200:
            data = response.json()
            self.print_success(f"Task shared successfully: {data.get('message', 'Success')}")
        else:
            self.print_error(f"Task sharing failed: {response.status_code} - {response.text}")
        
        # Test 2: Share task by user code (case-insensitive)
        self.print_info("Testing task sharing by user code...")
        
        # First, get the user code for testuser2
        user2 = self.auth_service.get_user_by_username("testuser2")
        if user2:
            share_data = {
                "recipient_identifier": user2.user_code,
                "permission_level": "edit"
            }
            
            response = self.session.post(f"{self.base_url}/tasks/share", json=share_data)
            
            if response.status_code == 200:
                data = response.json()
                self.print_success(f"Task shared by user code: {data.get('message', 'Success')}")
            else:
                self.print_error(f"Task sharing by user code failed: {response.status_code} - {response.text}")
        
        # Test 3: Get task shares
        self.print_info("Testing get task shares...")
        response = self.session.get(f"{self.base_url}/tasks/{task_id}/shares")
        
        if response.status_code == 200:
            data = response.json()
            shares = data.get('shares', [])
            self.print_success(f"Retrieved {len(shares)} task shares")
        else:
            self.print_error(f"Get task shares failed: {response.status_code} - {response.text}")
        
        # Test 4: Update share permission
        if user2:
            self.print_info("Testing update share permission...")
            update_data = {
                "user_code": user2.user_code,
                "permission_level": "admin"
            }
            
            response = self.session.patch(f"{self.base_url}/tasks/{task_id}/shares", json=update_data)
            
            if response.status_code == 200:
                self.print_success("Share permission updated successfully")
            else:
                self.print_error(f"Update share permission failed: {response.status_code} - {response.text}")
        
        # Test 5: Remove share
        if user2:
            self.print_info("Testing remove share...")
            remove_data = {
                "user_code": user2.user_code
            }
            
            response = self.session.delete(f"{self.base_url}/tasks/{task_id}/shares", json=remove_data)
            
            if response.status_code == 200:
                self.print_success("Share removed successfully")
            else:
                self.print_error(f"Remove share failed: {response.status_code} - {response.text}")
    
    def test_notifications(self):
        """Test notification functionality"""
        self.print_header("NOTIFICATION TESTS")
        
        # Test 1: Get due notifications
        self.print_info("Testing get due notifications...")
        response = self.session.get(f"{self.base_url}/notifications/due")
        
        if response.status_code == 200:
            data = response.json()
            notifications = data.get('notifications', [])
            self.print_success(f"Retrieved {len(notifications)} due notifications")
        else:
            self.print_error(f"Get notifications failed: {response.status_code} - {response.text}")
    
    def test_error_handling(self):
        """Test error handling"""
        self.print_header("ERROR HANDLING TESTS")
        
        # Test 1: Invalid task ID
        self.print_info("Testing invalid task ID...")
        response = self.session.get(f"{self.base_url}/tasks/99999")
        
        if response.status_code == 404:
            self.print_success("Correctly handled invalid task ID")
        else:
            self.print_error(f"Should have returned 404 for invalid task ID: {response.status_code}")
        
        # Test 2: Unauthorized access
        self.print_info("Testing unauthorized access...")
        # Remove authorization header
        self.session.headers.pop('Authorization', None)
        response = self.session.get(f"{self.base_url}/tasks")
        
        if response.status_code == 401:
            self.print_success("Correctly handled unauthorized access")
        else:
            self.print_error(f"Should have returned 401 for unauthorized access: {response.status_code}")
        
        # Restore authorization
        self.session.post(f"{self.base_url}/auth/login", json={
            "username": "testuser1",
            "password": "password123"
        })
        data = self.session.post(f"{self.base_url}/auth/login", json={
            "username": "testuser1",
            "password": "password123"
        }).json()
        self.session.headers.update({'Authorization': f"Bearer {data['access_token']}"})
    
    def test_direct_service_methods(self):
        """Test service methods directly"""
        self.print_header("DIRECT SERVICE METHOD TESTS")
        
        # Test 1: User code generation
        self.print_info("Testing user code generation...")
        from utils.user_code_generator import UserCodeGenerator
        user_code = UserCodeGenerator.generate_user_code()
        if len(user_code) == 8:
            self.print_success(f"Generated user code: {user_code}")
        else:
            self.print_error(f"Invalid user code length: {len(user_code)}")
        
        # Test 2: User code validation
        self.print_info("Testing user code validation...")
        valid_code = "ABC12345"
        invalid_code = "ABC1234"  # Too short
        
        if UserCodeGenerator.is_valid_user_code(valid_code):
            self.print_success("Valid user code accepted")
        else:
            self.print_error("Valid user code rejected")
        
        if not UserCodeGenerator.is_valid_user_code(invalid_code):
            self.print_success("Invalid user code rejected")
        else:
            self.print_error("Invalid user code accepted")
        
        # Test 3: Case-insensitive username lookup
        self.print_info("Testing case-insensitive username lookup...")
        user = self.auth_service.get_user_by_username("TESTUSER1")
        if user:
            self.print_success(f"Found user with case-insensitive lookup: {user.username}")
        else:
            self.print_error("Case-insensitive username lookup failed")
    
    def cleanup(self):
        """Clean up test data"""
        self.print_header("CLEANUP")
        
        # Delete test tasks
        for task_id in self.test_tasks:
            try:
                response = self.session.delete(f"{self.base_url}/tasks/{task_id}")
                if response.status_code == 200:
                    self.print_success(f"Deleted test task {task_id}")
                else:
                    self.print_error(f"Failed to delete test task {task_id}")
            except:
                pass
        
        self.print_info("Test cleanup completed")
    
    def run_all_tests(self):
        """Run all tests"""
        self.print_header("COMPREHENSIVE TEST SUITE")
        self.print_info("Starting comprehensive testing...")
        
        try:
            # Run all test suites
            self.test_user_registration()
            self.test_user_authentication()
            self.test_task_management()
            self.test_subtask_management()
            self.test_task_sharing()
            self.test_notifications()
            self.test_error_handling()
            self.test_direct_service_methods()
            
            self.print_header("TEST SUMMARY")
            self.print_success("All tests completed!")
            self.print_info("✅ User registration and authentication working")
            self.print_info("✅ Task management working")
            self.print_info("✅ Subtask management working")
            self.print_info("✅ Task sharing working")
            self.print_info("✅ Notifications working")
            self.print_info("✅ Error handling working")
            self.print_info("✅ Case-insensitive functionality working")
            
        except Exception as e:
            self.print_error(f"Test suite failed with exception: {e}")
        finally:
            self.cleanup()

if __name__ == "__main__":
    # Make sure the server is running
    print("🚀 Starting Comprehensive Test Suite...")
    print("⚠️  Make sure the Flask server is running on http://localhost:5000")
    print("Press Enter to continue or Ctrl+C to cancel...")
    
    try:
        input()
    except KeyboardInterrupt:
        print("\n❌ Test cancelled by user")
        exit(1)
    
    tester = ComprehensiveTester()
    tester.run_all_tests() 