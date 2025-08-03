import sqlite3
from abc import ABC, abstractmethod
from typing import List, Optional
from models.task_share import TaskShare

class TaskShareRepositoryInterface(ABC):
    """Task share repository interface following Interface Segregation Principle"""
    
    @abstractmethod
    def create_share(self, task_share: TaskShare) -> TaskShare:
        pass
    
    @abstractmethod
    def get_shares_by_task(self, task_id: int) -> List[TaskShare]:
        pass
    
    @abstractmethod
    def get_shares_by_user_code(self, user_code: str) -> List[TaskShare]:
        pass
    
    @abstractmethod
    def get_shared_tasks_for_user(self, user_code: str) -> List[int]:
        pass
    
    @abstractmethod
    def get_share_permission(self, task_id: int, user_code: str) -> Optional[str]:
        pass
    
    @abstractmethod
    def update_share_permission(self, task_id: int, shared_with_code: str, permission_level: str) -> bool:
        pass
    
    @abstractmethod
    def delete_share(self, task_id: int, shared_with_code: str) -> bool:
        pass
    
    @abstractmethod
    def delete_all_shares_for_task(self, task_id: int) -> bool:
        pass

class SQLiteTaskShareRepository(TaskShareRepositoryInterface):
    """SQLite implementation of task share repository using user codes"""
    
    def __init__(self, database: sqlite3.Connection):
        self.db = database
        # Table is created in dependency_injection.py, no need to create here
    
    def create_share(self, task_share: TaskShare) -> TaskShare:
        """Create a new task share"""
        try:
            cursor = self.db.cursor()
            cursor.execute('''INSERT INTO task_shares (task_id, owner_code, shared_with_code, permission_level)
                             VALUES (?, ?, ?, ?)''', (
                task_share.task_id, task_share.owner_code, 
                task_share.shared_with_code, task_share.permission_level
            ))
            
            task_share.id = cursor.lastrowid
            self.db.commit()
            
            # Get the created share with full data
            created_share = self._get_share_by_task_and_user(task_share.task_id, task_share.shared_with_code)
            return created_share
        except sqlite3.IntegrityError:
            raise ValueError("Task share already exists")
        except Exception as e:
            self.db.rollback()
            raise e
    
    def get_shares_by_task(self, task_id: int) -> List[TaskShare]:
        """Get all shares for a specific task"""
        try:
            cursor = self.db.cursor()
            cursor.execute('SELECT * FROM task_shares WHERE task_id = ?', (task_id,))
            results = cursor.fetchall()
            return [self._row_to_task_share(row) for row in results]
        except Exception as e:
            raise e
    
    def get_shares_by_user_code(self, user_code: str) -> List[TaskShare]:
        """Get all tasks shared with a user by user code"""
        try:
            cursor = self.db.cursor()
            cursor.execute('SELECT * FROM task_shares WHERE shared_with_code = ?', (user_code,))
            results = cursor.fetchall()
            return [self._row_to_task_share(row) for row in results]
        except Exception as e:
            raise e
    
    def get_shared_tasks_for_user(self, user_code: str) -> List[int]:
        """Get all task IDs shared with a user by user code"""
        try:
            cursor = self.db.cursor()
            cursor.execute('SELECT task_id FROM task_shares WHERE shared_with_code = ?', (user_code,))
            results = cursor.fetchall()
            return [row['task_id'] for row in results]
        except Exception as e:
            raise e
    
    def get_share_permission(self, task_id: int, user_code: str) -> Optional[str]:
        """Get permission level for a specific task and user code"""
        try:
            cursor = self.db.cursor()
            cursor.execute('SELECT permission_level FROM task_shares WHERE task_id = ? AND shared_with_code = ?', 
                         (task_id, user_code))
            result = cursor.fetchone()
            return result['permission_level'] if result else None
        except Exception as e:
            raise e
    
    def update_share_permission(self, task_id: int, shared_with_code: str, permission_level: str) -> bool:
        """Update permission level for a shared task"""
        try:
            cursor = self.db.cursor()
            cursor.execute('''UPDATE task_shares 
                             SET permission_level = ?, updated_at = CURRENT_TIMESTAMP
                             WHERE task_id = ? AND shared_with_code = ?''', 
                         (permission_level, task_id, shared_with_code))
            self.db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.db.rollback()
            raise e
    
    def delete_share(self, task_id: int, shared_with_code: str) -> bool:
        """Delete a specific task share"""
        try:
            cursor = self.db.cursor()
            cursor.execute('DELETE FROM task_shares WHERE task_id = ? AND shared_with_code = ?', 
                         (task_id, shared_with_code))
            self.db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.db.rollback()
            raise e
    
    def delete_all_shares_for_task(self, task_id: int) -> bool:
        """Delete all shares for a specific task"""
        try:
            cursor = self.db.cursor()
            cursor.execute('DELETE FROM task_shares WHERE task_id = ?', (task_id,))
            self.db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.db.rollback()
            raise e
    
    def _get_share_by_task_and_user(self, task_id: int, shared_with_code: str) -> TaskShare:
        """Get a specific share by task ID and user code"""
        try:
            cursor = self.db.cursor()
            cursor.execute('SELECT * FROM task_shares WHERE task_id = ? AND shared_with_code = ?', 
                         (task_id, shared_with_code))
            row = cursor.fetchone()
            return self._row_to_task_share(row) if row else None
        except Exception as e:
            raise e
    
    def _row_to_task_share(self, row) -> TaskShare:
        """Convert database row to TaskShare object"""
        return TaskShare(
            id=row['id'],
            task_id=row['task_id'],
            owner_code=row['owner_code'],
            shared_with_code=row['shared_with_code'],
            permission_level=row['permission_level'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        ) 