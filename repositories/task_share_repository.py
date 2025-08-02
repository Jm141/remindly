from abc import ABC, abstractmethod
from typing import List, Optional
from models.task_share import TaskShare
from repositories.database_interface import DatabaseInterface

class TaskShareRepositoryInterface(ABC):
    """Abstract interface for task share repository"""
    
    @abstractmethod
    def create_share(self, task_share: TaskShare) -> TaskShare:
        """Create a new task share"""
        pass
    
    @abstractmethod
    def get_shares_by_task(self, task_id: int) -> List[TaskShare]:
        """Get all shares for a specific task"""
        pass
    
    @abstractmethod
    def get_shares_by_user(self, user_id: int) -> List[TaskShare]:
        """Get all tasks shared with a user"""
        pass
    
    @abstractmethod
    def get_shared_tasks_for_user(self, user_id: int) -> List[int]:
        """Get list of task IDs shared with a user"""
        pass
    
    @abstractmethod
    def get_share_permission(self, task_id: int, user_id: int) -> Optional[str]:
        """Get permission level for a user on a specific task"""
        pass
    
    @abstractmethod
    def update_share_permission(self, task_id: int, shared_with_id: int, permission_level: str) -> bool:
        """Update permission level for a task share"""
        pass
    
    @abstractmethod
    def delete_share(self, task_id: int, shared_with_id: int) -> bool:
        """Delete a task share"""
        pass
    
    @abstractmethod
    def delete_all_shares_for_task(self, task_id: int) -> bool:
        """Delete all shares for a specific task"""
        pass

class SQLiteTaskShareRepository(TaskShareRepositoryInterface):
    """SQLite implementation of task share repository"""
    
    def __init__(self, database: DatabaseInterface):
        self.db = database
        self._init_table()
    
    def _init_table(self):
        """Initialize task shares table"""
        self.db.execute_update('''CREATE TABLE IF NOT EXISTS task_shares (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER NOT NULL,
            owner_id INTEGER NOT NULL,
            shared_with_id INTEGER NOT NULL,
            permission_level TEXT DEFAULT 'view',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (task_id) REFERENCES tasks (id) ON DELETE CASCADE,
            FOREIGN KEY (owner_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (shared_with_id) REFERENCES users (id) ON DELETE CASCADE,
            UNIQUE(task_id, shared_with_id)
        )''')
    
    def create_share(self, task_share: TaskShare) -> TaskShare:
        """Create a new task share"""
        query = '''INSERT INTO task_shares (task_id, owner_id, shared_with_id, permission_level)
                   VALUES (?, ?, ?, ?)'''
        self.db.execute_update(query, (
            task_share.task_id, task_share.owner_id, 
            task_share.shared_with_id, task_share.permission_level
        ))
        
        # Get the created share with ID
        created_share = self._get_share_by_task_and_user(task_share.task_id, task_share.shared_with_id)
        return created_share
    
    def get_shares_by_task(self, task_id: int) -> List[TaskShare]:
        """Get all shares for a specific task"""
        query = 'SELECT * FROM task_shares WHERE task_id = ?'
        results = self.db.execute_query(query, (task_id,))
        return [self._row_to_task_share(row) for row in results]
    
    def get_shares_by_user(self, user_id: int) -> List[TaskShare]:
        """Get all tasks shared with a user"""
        query = 'SELECT * FROM task_shares WHERE shared_with_id = ?'
        results = self.db.execute_query(query, (user_id,))
        return [self._row_to_task_share(row) for row in results]
    
    def get_shared_tasks_for_user(self, user_id: int) -> List[int]:
        """Get list of task IDs shared with a user"""
        query = 'SELECT task_id FROM task_shares WHERE shared_with_id = ?'
        results = self.db.execute_query(query, (user_id,))
        return [row[0] for row in results]
    
    def get_share_permission(self, task_id: int, user_id: int) -> Optional[str]:
        """Get permission level for a user on a specific task"""
        query = 'SELECT permission_level FROM task_shares WHERE task_id = ? AND shared_with_id = ?'
        result = self.db.execute_query(query, (task_id, user_id))
        if result:
            return result[0][0]
        return None
    
    def update_share_permission(self, task_id: int, shared_with_id: int, permission_level: str) -> bool:
        """Update permission level for a task share"""
        query = '''UPDATE task_shares 
                   SET permission_level = ?, updated_at = CURRENT_TIMESTAMP
                   WHERE task_id = ? AND shared_with_id = ?'''
        self.db.execute_update(query, (permission_level, task_id, shared_with_id))
        return True
    
    def delete_share(self, task_id: int, shared_with_id: int) -> bool:
        """Delete a task share"""
        query = 'DELETE FROM task_shares WHERE task_id = ? AND shared_with_id = ?'
        self.db.execute_update(query, (task_id, shared_with_id))
        return True
    
    def delete_all_shares_for_task(self, task_id: int) -> bool:
        """Delete all shares for a specific task"""
        query = 'DELETE FROM task_shares WHERE task_id = ?'
        self.db.execute_update(query, (task_id,))
        return True
    
    def _get_share_by_task_and_user(self, task_id: int, shared_with_id: int) -> TaskShare:
        """Get share by task ID and shared user ID"""
        query = 'SELECT * FROM task_shares WHERE task_id = ? AND shared_with_id = ?'
        result = self.db.execute_query(query, (task_id, shared_with_id))
        if result:
            return self._row_to_task_share(result[0])
        return None
    
    def _row_to_task_share(self, row) -> TaskShare:
        """Convert database row to TaskShare object"""
        return TaskShare(
            id=row[0],
            task_id=row[1],
            owner_id=row[2],
            shared_with_id=row[3],
            permission_level=row[4],
            created_at=row[5],
            updated_at=row[6]
        ) 