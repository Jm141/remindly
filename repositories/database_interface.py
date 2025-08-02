from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from models.user import User
from models.task import Task, Subtask

class DatabaseInterface(ABC):
    """Abstract database interface following Interface Segregation Principle"""
    
    @abstractmethod
    def connect(self):
        """Establish database connection"""
        pass
    
    @abstractmethod
    def close(self):
        """Close database connection"""
        pass
    
    @abstractmethod
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute a query and return results"""
        pass
    
    @abstractmethod
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute an update query and return affected rows"""
        pass

class UserRepositoryInterface(ABC):
    """User repository interface following Interface Segregation Principle"""
    
    @abstractmethod
    def create_user(self, user: User) -> User:
        """Create a new user"""
        pass
    
    @abstractmethod
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        pass
    
    @abstractmethod
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        pass
    
    @abstractmethod
    def user_exists(self, username: str) -> bool:
        """Check if user exists"""
        pass

class TaskRepositoryInterface(ABC):
    """Task repository interface following Interface Segregation Principle"""
    
    @abstractmethod
    def create_task(self, task: Task) -> Task:
        """Create a new task"""
        pass
    
    @abstractmethod
    def get_tasks_by_user(self, user_id: str, completed: Optional[bool] = None) -> List[Task]:
        """Get tasks for a user"""
        pass
    
    @abstractmethod
    def get_task_by_id(self, task_id: str, user_id: str) -> Optional[Task]:
        """Get task by ID for a specific user"""
        pass
    
    @abstractmethod
    def get_task_by_id_only(self, task_id: str) -> Optional[Task]:
        """Get task by ID without user restriction (for task sharing)"""
        pass
    
    @abstractmethod
    def update_task(self, task_id: str, user_id: str, updates: Dict[str, Any]) -> bool:
        """Update a task"""
        pass
    
    @abstractmethod
    def delete_task(self, task_id: str, user_id: str) -> bool:
        """Delete a task"""
        pass
    
    @abstractmethod
    def get_tasks_due_soon(self, user_id: str, hours: int = 1) -> List[Task]:
        """Get tasks due within specified hours"""
        pass
    
    @abstractmethod
    def get_overdue_tasks(self, user_id: str) -> List[Task]:
        """Get overdue tasks for a user"""
        pass

class SubtaskRepositoryInterface(ABC):
    """Subtask repository interface following Interface Segregation Principle"""
    
    @abstractmethod
    def create_subtask(self, subtask: Subtask) -> Subtask:
        """Create a new subtask"""
        pass
    
    @abstractmethod
    def get_subtasks_by_task(self, task_id: str) -> List[Subtask]:
        """Get subtasks for a task"""
        pass
    
    @abstractmethod
    def get_subtask_by_id(self, subtask_id: str, task_id: str) -> Optional[Subtask]:
        """Get subtask by ID for a specific task"""
        pass
    
    @abstractmethod
    def update_subtask(self, subtask_id: str, task_id: str, updates: Dict[str, Any]) -> bool:
        """Update a subtask"""
        pass
    
    @abstractmethod
    def delete_subtask(self, subtask_id: str, task_id: str) -> bool:
        """Delete a subtask"""
        pass
    
    @abstractmethod
    def get_completed_subtasks_count(self, task_id: str) -> int:
        """Get count of completed subtasks for a task"""
        pass
    
    @abstractmethod
    def get_total_subtasks_count(self, task_id: str) -> int:
        """Get total count of subtasks for a task"""
        pass 