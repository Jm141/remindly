"""
Test file demonstrating how the SOLID architecture improves testability.
This shows how easy it is to test individual components in isolation.
"""

import unittest
from unittest.mock import Mock, MagicMock
from datetime import datetime

# Import our SOLID components
from models.user import User
from models.task import Task, Subtask
from services.auth_service import AuthService
from services.task_service import TaskService
from repositories.database_interface import (
    UserRepositoryInterface, TaskRepositoryInterface, SubtaskRepositoryInterface
)

class MockUserRepository(UserRepositoryInterface):
    """Mock user repository for testing"""
    
    def __init__(self):
        self.users = {}
        self.next_id = 1
    
    def create_user(self, user: User) -> User:
        user.id = self.next_id
        self.users[user.username] = user
        self.next_id += 1
        return user
    
    def get_user_by_username(self, username: str):
        return self.users.get(username)
    
    def get_user_by_id(self, user_id: int):
        for user in self.users.values():
            if user.id == user_id:
                return user
        return None
    
    def user_exists(self, username: str) -> bool:
        return username in self.users

class MockTaskRepository(TaskRepositoryInterface):
    """Mock task repository for testing"""
    
    def __init__(self):
        self.tasks = {}
        self.next_id = 1
    
    def create_task(self, task: Task) -> Task:
        task.id = self.next_id
        self.tasks[task.id] = task
        self.next_id += 1
        return task
    
    def get_tasks_by_user(self, user_id: int, completed=None):
        tasks = [task for task in self.tasks.values() if task.user_id == user_id]
        if completed is not None:
            tasks = [task for task in tasks if task.completed == completed]
        return tasks
    
    def get_task_by_id(self, task_id: int, user_id: int):
        task = self.tasks.get(task_id)
        if task and task.user_id == user_id:
            return task
        return None
    
    def update_task(self, task_id: int, user_id: int, updates: dict) -> bool:
        task = self.get_task_by_id(task_id, user_id)
        if not task:
            return False
        
        for key, value in updates.items():
            if hasattr(task, key):
                setattr(task, key, value)
        return True
    
    def delete_task(self, task_id: int, user_id: int) -> bool:
        task = self.get_task_by_id(task_id, user_id)
        if task:
            del self.tasks[task_id]
            return True
        return False
    
    def get_tasks_due_soon(self, user_id: int, hours: int = 1):
        return []
    
    def get_overdue_tasks(self, user_id: int):
        return []

class MockSubtaskRepository(SubtaskRepositoryInterface):
    """Mock subtask repository for testing"""
    
    def __init__(self):
        self.subtasks = {}
        self.next_id = 1
    
    def create_subtask(self, subtask: Subtask) -> Subtask:
        subtask.id = self.next_id
        self.subtasks[subtask.id] = subtask
        self.next_id += 1
        return subtask
    
    def get_subtasks_by_task(self, task_id: int):
        return [st for st in self.subtasks.values() if st.task_id == task_id]
    
    def update_subtask(self, subtask_id: int, task_id: int, updates: dict) -> bool:
        subtask = self.subtasks.get(subtask_id)
        if subtask and subtask.task_id == task_id:
            for key, value in updates.items():
                if hasattr(subtask, key):
                    setattr(subtask, key, value)
            return True
        return False
    
    def delete_subtask(self, subtask_id: int, task_id: int) -> bool:
        subtask = self.subtasks.get(subtask_id)
        if subtask and subtask.task_id == task_id:
            del self.subtasks[subtask_id]
            return True
        return False

class TestAuthService(unittest.TestCase):
    """Test the AuthService in isolation"""
    
    def setUp(self):
        self.mock_user_repo = MockUserRepository()
        self.mock_bcrypt = Mock()
        self.auth_service = AuthService(self.mock_user_repo, self.mock_bcrypt)
    
    def test_register_user_success(self):
        """Test successful user registration"""
        self.mock_bcrypt.generate_password_hash.return_value = b'hashed_password'
        
        success, message = self.auth_service.register_user('testuser', 'password123')
        
        self.assertTrue(success)
        self.assertEqual(message, "User registered successfully")
        self.assertTrue(self.mock_user_repo.user_exists('testuser'))
    
    def test_register_user_duplicate(self):
        """Test registration with existing username"""
        # Create existing user
        existing_user = User(id=1, username='testuser', password='hashed')
        self.mock_user_repo.users['testuser'] = existing_user
        
        success, message = self.auth_service.register_user('testuser', 'password123')
        
        self.assertFalse(success)
        self.assertEqual(message, "Username already exists")
    
    def test_authenticate_user_success(self):
        """Test successful user authentication"""
        # Create user
        user = User(id=1, username='testuser', password='hashed_password')
        self.mock_user_repo.users['testuser'] = user
        self.mock_bcrypt.check_password_hash.return_value = True
        
        result_user, message = self.auth_service.authenticate_user('testuser', 'password123')
        
        self.assertEqual(result_user, user)
        self.assertEqual(message, "Authentication successful")
    
    def test_authenticate_user_invalid_credentials(self):
        """Test authentication with invalid credentials"""
        self.mock_bcrypt.check_password_hash.return_value = False
        
        result_user, message = self.auth_service.authenticate_user('testuser', 'wrongpassword')
        
        self.assertIsNone(result_user)
        self.assertEqual(message, "Invalid credentials")

class TestTaskService(unittest.TestCase):
    """Test the TaskService in isolation"""
    
    def setUp(self):
        self.mock_task_repo = MockTaskRepository()
        self.mock_subtask_repo = MockSubtaskRepository()
        self.task_service = TaskService(self.mock_task_repo, self.mock_subtask_repo)
    
    def test_create_task_success(self):
        """Test successful task creation"""
        task_data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'category': 'Work',
            'priority': 'High'
        }
        
        task, message = self.task_service.create_task(1, task_data)
        
        self.assertIsNotNone(task)
        self.assertEqual(message, "Task created successfully")
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.user_id, 1)
    
    def test_create_task_missing_title(self):
        """Test task creation without title"""
        task_data = {'description': 'Test Description'}
        
        task, message = self.task_service.create_task(1, task_data)
        
        self.assertIsNone(task)
        self.assertEqual(message, "Task title is required")
    
    def test_update_task_success(self):
        """Test successful task update"""
        # Create a task first
        task = Task(id=1, user_id=1, title='Original Title')
        self.mock_task_repo.tasks[1] = task
        
        updates = {'title': 'Updated Title', 'completed': True}
        success, message = self.task_service.update_task(1, 1, updates)
        
        self.assertTrue(success)
        self.assertEqual(message, "Task updated successfully")
        self.assertEqual(task.title, 'Updated Title')
        self.assertTrue(task.completed)
    
    def test_update_task_not_found(self):
        """Test updating non-existent task"""
        updates = {'title': 'Updated Title'}
        success, message = self.task_service.update_task(999, 1, updates)
        
        self.assertFalse(success)
        self.assertEqual(message, "Task not found or unauthorized")

class TestModels(unittest.TestCase):
    """Test the data models"""
    
    def test_user_to_dict(self):
        """Test User model to_dict method"""
        user = User(id=1, username='testuser', password='hashed_password')
        user_dict = user.to_dict()
        
        self.assertEqual(user_dict['id'], 1)
        self.assertEqual(user_dict['username'], 'testuser')
        self.assertNotIn('password', user_dict)  # Password should not be included
    
    def test_task_to_dict(self):
        """Test Task model to_dict method"""
        task = Task(
            id=1, 
            user_id=1, 
            title='Test Task',
            description='Test Description',
            completed=True
        )
        task_dict = task.to_dict()
        
        self.assertEqual(task_dict['id'], 1)
        self.assertEqual(task_dict['title'], 'Test Task')
        self.assertEqual(task_dict['completed'], True)
        self.assertEqual(task_dict['subtasks'], [])
    
    def test_task_is_overdue(self):
        """Test Task overdue detection"""
        # Create overdue task
        overdue_task = Task(
            id=1, 
            user_id=1, 
            title='Overdue Task',
            due_date='2023-01-01 12:00'  # Past date
        )
        
        self.assertTrue(overdue_task.is_overdue())
    
    def test_task_is_due_soon(self):
        """Test Task due soon detection"""
        # Create task due in 30 minutes
        from datetime import datetime, timedelta
        due_time = datetime.now() + timedelta(minutes=30)
        due_soon_task = Task(
            id=1, 
            user_id=1, 
            title='Due Soon Task',
            due_date=due_time.strftime('%Y-%m-%d %H:%M')
        )
        
        self.assertTrue(due_soon_task.is_due_soon(hours=1))

if __name__ == '__main__':
    print("🧪 Running SOLID Architecture Tests...")
    print("This demonstrates how the new architecture improves testability!")
    print("\n" + "="*50)
    
    unittest.main(verbosity=2) 