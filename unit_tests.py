#!/usr/bin/env python3
"""Unit Tests for Task Scheduler Backend Components"""

import unittest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
from dependency_injection import container
from services.auth_service import AuthService
from services.task_service import TaskService
from services.task_share_service import TaskShareService
from models.user import User
from models.task import Task, Subtask
from models.task_share import TaskShare
from utils.user_code_generator import UserCodeGenerator
from flask_bcrypt import Bcrypt

class TestUserCodeGenerator(unittest.TestCase):
    """Test UserCodeGenerator utility"""
    
    def test_generate_user_code(self):
        """Test user code generation"""
        code = UserCodeGenerator.generate_user_code()
        self.assertEqual(len(code), 8)
        self.assertTrue(UserCodeGenerator.is_valid_user_code(code))
    
    def test_is_valid_user_code(self):
        """Test user code validation"""
        # Valid codes (8 characters, no similar characters)
        self.assertTrue(UserCodeGenerator.is_valid_user_code("ABCD2345"))
        self.assertTrue(UserCodeGenerator.is_valid_user_code("XYZ98765"))
        
        # Invalid codes
        self.assertFalse(UserCodeGenerator.is_valid_user_code("ABCD234"))  # Too short
        self.assertFalse(UserCodeGenerator.is_valid_user_code("ABCD23456"))  # Too long
        self.assertFalse(UserCodeGenerator.is_valid_user_code("ABCD234O"))  # Contains O
        self.assertFalse(UserCodeGenerator.is_valid_user_code("ABCD2340"))  # Contains 0
        self.assertFalse(UserCodeGenerator.is_valid_user_code("ABCD234I"))  # Contains I
        self.assertFalse(UserCodeGenerator.is_valid_user_code("ABCD234L"))  # Contains L
        self.assertFalse(UserCodeGenerator.is_valid_user_code("ABCD2341"))  # Contains 1

class TestUserModel(unittest.TestCase):
    """Test User model"""
    
    def test_user_creation(self):
        """Test user object creation"""
        user = User(
            id=1,
            user_code="ABC12345",
            username="testuser",
            password_hash="hashed_password",
            email="test@example.com"
        )
        
        self.assertEqual(user.id, 1)
        self.assertEqual(user.user_code, "ABC12345")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.password_hash, "hashed_password")
        self.assertEqual(user.email, "test@example.com")
    
    def test_user_to_dict(self):
        """Test user to_dict method"""
        user = User(
            id=1,
            user_code="ABC12345",
            username="testuser",
            password_hash="hashed_password",
            email="test@example.com"
        )
        
        user_dict = user.to_dict()
        self.assertEqual(user_dict['id'], 1)
        self.assertEqual(user_dict['user_code'], "ABC12345")
        self.assertEqual(user_dict['username'], "testuser")
        self.assertEqual(user_dict['email'], "test@example.com")
        self.assertNotIn('password_hash', user_dict)  # Password should not be included
    
    def test_user_from_dict(self):
        """Test user from_dict method"""
        user_dict = {
            'id': 1,
            'user_code': 'ABC12345',
            'username': 'testuser',
            'password_hash': 'hashed_password',
            'email': 'test@example.com',
            'created_at': '2023-01-01T00:00:00',
            'updated_at': '2023-01-01T00:00:00'
        }
        
        user = User.from_dict(user_dict)
        self.assertEqual(user.id, 1)
        self.assertEqual(user.user_code, "ABC12345")
        self.assertEqual(user.username, "testuser")

class TestTaskModel(unittest.TestCase):
    """Test Task model"""
    
    def test_task_creation(self):
        """Test task object creation"""
        task = Task(
            id=1,
            user_id=1,
            title="Test Task",
            description="Test Description",
            due_date=datetime.now(),
            priority="high",
            completed=False,
            category="work"
        )
        
        self.assertEqual(task.id, 1)
        self.assertEqual(task.user_id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test Description")
        self.assertEqual(task.priority, "high")
        self.assertFalse(task.completed)
        self.assertEqual(task.category, "work")
    
    def test_task_to_dict(self):
        """Test task to_dict method"""
        due_date = datetime.now()
        task = Task(
            id=1,
            user_id=1,
            title="Test Task",
            description="Test Description",
            due_date=due_date,
            priority="high",
            completed=False,
            category="work"
        )
        
        task_dict = task.to_dict()
        self.assertEqual(task_dict['id'], 1)
        self.assertEqual(task_dict['title'], "Test Task")
        self.assertEqual(task_dict['priority'], "high")
        self.assertFalse(task_dict['completed'])

class TestSubtaskModel(unittest.TestCase):
    """Test Subtask model"""
    
    def test_subtask_creation(self):
        """Test subtask object creation"""
        subtask = Subtask(
            id=1,
            task_id=1,
            title="Test Subtask",
            description="Test Description",
            completed=False
        )
        
        self.assertEqual(subtask.id, 1)
        self.assertEqual(subtask.task_id, 1)
        self.assertEqual(subtask.title, "Test Subtask")
        self.assertEqual(subtask.description, "Test Description")
        self.assertFalse(subtask.completed)
    
    def test_subtask_to_dict(self):
        """Test subtask to_dict method"""
        subtask = Subtask(
            id=1,
            task_id=1,
            title="Test Subtask",
            description="Test Description",
            completed=False
        )
        
        subtask_dict = subtask.to_dict()
        self.assertEqual(subtask_dict['id'], 1)
        self.assertEqual(subtask_dict['title'], "Test Subtask")
        self.assertFalse(subtask_dict['completed'])

class TestTaskShareModel(unittest.TestCase):
    """Test TaskShare model"""
    
    def test_task_share_creation(self):
        """Test task share object creation"""
        task_share = TaskShare(
            id=1,
            task_id=1,
            owner_code="ABC12345",
            shared_with_code="XYZ98765",
            permission_level="view"
        )
        
        self.assertEqual(task_share.id, 1)
        self.assertEqual(task_share.task_id, 1)
        self.assertEqual(task_share.owner_code, "ABC12345")
        self.assertEqual(task_share.shared_with_code, "XYZ98765")
        self.assertEqual(task_share.permission_level, "view")
    
    def test_task_share_to_dict(self):
        """Test task share to_dict method"""
        task_share = TaskShare(
            id=1,
            task_id=1,
            owner_code="ABC12345",
            shared_with_code="XYZ98765",
            permission_level="view"
        )
        
        share_dict = task_share.to_dict()
        self.assertEqual(share_dict['id'], 1)
        self.assertEqual(share_dict['task_id'], 1)
        self.assertEqual(share_dict['owner_code'], "ABC12345")
        self.assertEqual(share_dict['shared_with_code'], "XYZ98765")
        self.assertEqual(share_dict['permission_level'], "view")

class TestAuthService(unittest.TestCase):
    """Test AuthService"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_user_repo = Mock()
        self.bcrypt = Bcrypt()
        self.auth_service = AuthService(self.mock_user_repo, self.bcrypt)
    
    def test_register_user_success(self):
        """Test successful user registration"""
        # Mock user repository
        self.mock_user_repo.user_exists.return_value = False
        self.mock_user_repo.user_exists_case_insensitive.return_value = False
        self.mock_user_repo.create_user.return_value = User(
            id=1, user_code="ABC12345", username="testuser", password_hash="hashed"
        )
        
        # Mock UserCodeGenerator
        with patch('services.auth_service.UserCodeGenerator.generate_unique_user_code') as mock_gen:
            mock_gen.return_value = "ABC12345"
            
            success, message = self.auth_service.register_user("testuser", "password123")
            
            self.assertTrue(success)
            self.assertIn("ABC12345", message)
    
    def test_register_user_duplicate_username(self):
        """Test registration with duplicate username"""
        self.mock_user_repo.user_exists.return_value = True
        
        success, message = self.auth_service.register_user("testuser", "password123")
        
        self.assertFalse(success)
        self.assertIn("already exists", message)
    
    def test_register_user_short_password(self):
        """Test registration with short password"""
        success, message = self.auth_service.register_user("testuser", "123")
        
        self.assertFalse(success)
        self.assertIn("at least", message)
    
    def test_authenticate_user_success(self):
        """Test successful authentication"""
        hashed_password = self.bcrypt.generate_password_hash("password123").decode('utf-8')
        mock_user = User(
            id=1, user_code="ABC12345", username="testuser", password_hash=hashed_password
        )
        
        self.mock_user_repo.get_user_by_username.return_value = mock_user
        
        user, message = self.auth_service.authenticate_user("testuser", "password123")
        
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(message, "Authentication successful")
    
    def test_authenticate_user_case_insensitive(self):
        """Test case-insensitive authentication"""
        hashed_password = self.bcrypt.generate_password_hash("password123").decode('utf-8')
        mock_user = User(
            id=1, user_code="ABC12345", username="testuser", password_hash=hashed_password
        )
        
        self.mock_user_repo.get_user_by_username.return_value = None
        self.mock_user_repo.get_user_by_username_case_insensitive.return_value = mock_user
        
        user, message = self.auth_service.authenticate_user("TESTUSER", "password123")
        
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "testuser")
    
    def test_authenticate_user_invalid_password(self):
        """Test authentication with invalid password"""
        hashed_password = self.bcrypt.generate_password_hash("password123").decode('utf-8')
        mock_user = User(
            id=1, user_code="ABC12345", username="testuser", password_hash=hashed_password
        )
        
        self.mock_user_repo.get_user_by_username.return_value = mock_user
        
        user, message = self.auth_service.authenticate_user("testuser", "wrongpassword")
        
        self.assertIsNone(user)
        self.assertEqual(message, "Invalid credentials")

class TestTaskShareService(unittest.TestCase):
    """Test TaskShareService"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_task_share_repo = Mock()
        self.mock_task_repo = Mock()
        self.mock_user_repo = Mock()
        self.task_share_service = TaskShareService(
            self.mock_task_share_repo,
            self.mock_task_repo,
            self.mock_user_repo
        )
    
    def test_share_task_success(self):
        """Test successful task sharing"""
        # Mock task
        mock_task = Task(id=1, user_id=1, title="Test Task")
        self.mock_task_repo.get_task_by_id_only.return_value = mock_task
        
        # Mock owner user
        mock_owner = User(id=1, user_code="ABC12345", username="owner", password_hash="hashed")
        self.mock_user_repo.get_user_by_username.return_value = mock_owner
        
        # Mock recipient user (need to set up both username lookups)
        mock_recipient = User(id=2, user_code="XYZ98765", username="recipient", password_hash="hashed")
        
        # Set up the mock to return recipient for the second call (recipient lookup)
        self.mock_user_repo.get_user_by_username.side_effect = [mock_owner, mock_recipient]
        
        # Mock no existing share
        self.mock_task_share_repo.get_share_permission.return_value = None
        
        success, message = self.task_share_service.share_task(
            "1", "owner", "recipient", "view"
        )
        
        self.assertTrue(success)
        self.assertIn("shared successfully", message)
    
    def test_share_task_not_owner(self):
        """Test sharing task that user doesn't own"""
        # Mock task owned by different user
        mock_task = Task(id=1, user_id=2, title="Test Task")
        self.mock_task_repo.get_task_by_id_only.return_value = mock_task
        
        # Mock owner user
        mock_owner = User(id=1, user_code="ABC12345", username="owner", password_hash="hashed")
        self.mock_user_repo.get_user_by_username.return_value = mock_owner
        
        success, message = self.task_share_service.share_task(
            "1", "owner", "recipient", "view"
        )
        
        self.assertFalse(success)
        self.assertIn("only share tasks you own", message)
    
    def test_share_task_recipient_not_found(self):
        """Test sharing with non-existent recipient"""
        # Mock task
        mock_task = Task(id=1, user_id=1, title="Test Task")
        self.mock_task_repo.get_task_by_id_only.return_value = mock_task
        
        # Mock owner user
        mock_owner = User(id=1, user_code="ABC12345", username="owner", password_hash="hashed")
        self.mock_user_repo.get_user_by_username.return_value = mock_owner
        
        # Mock recipient not found
        self.mock_user_repo.get_user_by_username.return_value = None
        self.mock_user_repo.get_user_by_username_case_insensitive.return_value = None
        
        success, message = self.task_share_service.share_task(
            "1", "owner", "nonexistent", "view"
        )
        
        self.assertFalse(success)
        self.assertIn("not found", message)

def run_unit_tests():
    """Run all unit tests"""
    print("🧪 Running Unit Tests...")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestUserCodeGenerator,
        TestUserModel,
        TestTaskModel,
        TestSubtaskModel,
        TestTaskShareModel,
        TestAuthService,
        TestTaskShareService
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 UNIT TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print("\n❌ ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    if not result.failures and not result.errors:
        print("\n✅ All unit tests passed!")
    
    return len(result.failures) == 0 and len(result.errors) == 0

if __name__ == "__main__":
    run_unit_tests() 