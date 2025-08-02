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
    def get_shares_by_user(self, user_id: int) -> List[TaskShare]:
        pass
    
    @abstractmethod
    def get_shared_tasks_for_user(self, user_id: int) -> List[int]:
        pass
    
    @abstractmethod
    def get_share_permission(self, task_id: int, user_id: int) -> Optional[str]:
        pass
    
    @abstractmethod
    def update_share_permission(self, task_id: int, shared_with_id: int, permission_level: str) -> bool:
        pass
    
    @abstractmethod
    def delete_share(self, task_id: int, shared_with_id: int) -> bool:
        pass
    
    @abstractmethod
    def delete_all_shares_for_task(self, task_id: int) -> bool:
        pass

class SQLiteTaskShareRepository(TaskShareRepositoryInterface):
    """SQLite implementation of task share repository"""
    
    def __init__(self, database: sqlite3.Connection):
        self.db = database
        self._init_table()
    
    def _init_table(self):
        """Initialize task shares table"""
        cursor = self.db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS task_shares (
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
        self.db.commit()
    
    def create_share(self, task_share: TaskShare) -> TaskShare:
        """Create a new task share"""
        try:
            cursor = self.db.cursor()
            cursor.execute('''INSERT INTO task_shares (task_id, owner_id, shared_with_id, permission_level)
                             VALUES (?, ?, ?, ?)''', (
                task_share.task_id, task_share.owner_id, 
                task_share.shared_with_id, task_share.permission_level
            ))
            
            task_share.id = cursor.lastrowid
            self.db.commit()
            
            # Get the created share with full data
            created_share = self._get_share_by_task_and_user(task_share.task_id, task_share.shared_with_id)
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
    
    def get_shares_by_user(self, user_id: int) -> List[TaskShare]:
        """Get all tasks shared with a user"""
        try:
            cursor = self.db.cursor()
            cursor.execute('SELECT * FROM task_shares WHERE shared_with_id = ?', (user_id,))
            results = cursor.fetchall()
            return [self._row_to_task_share(row) for row in results]
        except Exception as e:
            raise e
    
    def get_shared_tasks_for_user(self, user_id: int) -> List[int]:
        """Get list of task IDs shared with a user"""
        try:
            cursor = self.db.cursor()
            cursor.execute('SELECT task_id FROM task_shares WHERE shared_with_id = ?', (user_id,))
            results = cursor.fetchall()
            return [row['task_id'] for row in results]
        except Exception as e:
            raise e
    
    def get_share_permission(self, task_id: int, user_id: int) -> Optional[str]:
        """Get permission level for a user on a specific task"""
        try:
            cursor = self.db.cursor()
            cursor.execute('SELECT permission_level FROM task_shares WHERE task_id = ? AND shared_with_id = ?', (task_id, user_id))
            result = cursor.fetchone()
            if result:
                return result['permission_level']
            return None
        except Exception as e:
            raise e
    
    def update_share_permission(self, task_id: int, shared_with_id: int, permission_level: str) -> bool:
        """Update permission level for a task share"""
        try:
            cursor = self.db.cursor()
            cursor.execute('''UPDATE task_shares 
                             SET permission_level = ?, updated_at = CURRENT_TIMESTAMP
                             WHERE task_id = ? AND shared_with_id = ?''', (permission_level, task_id, shared_with_id))
            self.db.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.db.rollback()
            raise e
    
    def delete_share(self, task_id: int, shared_with_id: int) -> bool:
        """Delete a task share"""
        try:
            cursor = self.db.cursor()
            cursor.execute('DELETE FROM task_shares WHERE task_id = ? AND shared_with_id = ?', (task_id, shared_with_id))
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
    
    def _get_share_by_task_and_user(self, task_id: int, shared_with_id: int) -> TaskShare:
        """Get share by task ID and shared user ID"""
        try:
            cursor = self.db.cursor()
            cursor.execute('SELECT * FROM task_shares WHERE task_id = ? AND shared_with_id = ?', (task_id, shared_with_id))
            result = cursor.fetchone()
            if result:
                return self._row_to_task_share(result)
            return None
        except Exception as e:
            raise e
    
    def _row_to_task_share(self, row) -> TaskShare:
        """Convert database row to TaskShare object"""
        return TaskShare(
            id=row['id'],
            task_id=row['task_id'],
            owner_id=row['owner_id'],
            shared_with_id=row['shared_with_id'],
            permission_level=row['permission_level'],
            created_at=row['created_at'],
            id=row[0],
            task_id=row[1],
            owner_id=row[2],
            shared_with_id=row[3],
            permission_level=row[4],
            created_at=row[5],
            updated_at=row[6]
        ) 