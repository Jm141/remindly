import sqlite3
from typing import List, Optional, Dict, Any
from models.task import Subtask
from repositories.database_interface import SubtaskRepositoryInterface

class SubtaskRepository(SubtaskRepositoryInterface):
    """Subtask repository implementation following Single Responsibility Principle"""
    
    def __init__(self, database: sqlite3.Connection):
        self.database = database
    
    def create_subtask(self, subtask: Subtask) -> Subtask:
        """Create a new subtask"""
        try:
            cursor = self.database.cursor()
            cursor.execute('''
                INSERT INTO subtasks (id, task_id, title, description, completed)
                VALUES (?, ?, ?, ?, ?)
            ''', (subtask.id, subtask.task_id, subtask.title, subtask.description, subtask.completed))
            
            self.database.commit()
            return subtask
        except Exception as e:
            self.database.rollback()
            raise e
    
    def get_subtasks_by_task(self, task_id: str) -> List[Subtask]:
        """Get subtasks for a task"""
        try:
            cursor = self.database.cursor()
            cursor.execute('''
                SELECT id, task_id, title, description, completed, created_at, updated_at
                FROM subtasks WHERE task_id = ?
                ORDER BY created_at ASC
            ''', (task_id,))
            
            rows = cursor.fetchall()
            subtasks = []
            for row in rows:
                subtasks.append(Subtask(
                    id=row['id'],
                    task_id=row['task_id'],
                    title=row['title'],
                    description=row['description'],
                    completed=bool(row['completed']),
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                ))
            return subtasks
        except Exception as e:
            raise e
    
    def get_subtask_by_id(self, subtask_id: str, task_id: str) -> Optional[Subtask]:
        """Get subtask by ID for a specific task"""
        try:
            cursor = self.database.cursor()
            cursor.execute('''
                SELECT id, task_id, title, description, completed, created_at, updated_at
                FROM subtasks WHERE id = ? AND task_id = ?
            ''', (subtask_id, task_id))
            
            row = cursor.fetchone()
            if row:
                return Subtask(
                    id=row['id'],
                    task_id=row['task_id'],
                    title=row['title'],
                    description=row['description'],
                    completed=bool(row['completed']),
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
            return None
        except Exception as e:
            raise e
    
    def update_subtask(self, subtask_id: str, task_id: str, updates: Dict[str, Any]) -> bool:
        """Update a subtask"""
        try:
            cursor = self.database.cursor()
            
            # Build update query dynamically
            set_clauses = []
            params = []
            
            for key, value in updates.items():
                if key in ['title', 'description', 'completed']:
                    set_clauses.append(f"{key} = ?")
                    params.append(value)
            
            if not set_clauses:
                return False
            
            set_clauses.append("updated_at = CURRENT_TIMESTAMP")
            params.extend([subtask_id, task_id])
            
            query = f"UPDATE subtasks SET {', '.join(set_clauses)} WHERE id = ? AND task_id = ?"
            cursor.execute(query, params)
            
            self.database.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.database.rollback()
            raise e
    
    def delete_subtask(self, subtask_id: str, task_id: str) -> bool:
        """Delete a subtask"""
        try:
            cursor = self.database.cursor()
            cursor.execute('DELETE FROM subtasks WHERE id = ? AND task_id = ?', (subtask_id, task_id))
            self.database.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.database.rollback()
            raise e
    
    def get_completed_subtasks_count(self, task_id: str) -> int:
        """Get count of completed subtasks for a task"""
        try:
            cursor = self.database.cursor()
            cursor.execute('SELECT COUNT(*) as count FROM subtasks WHERE task_id = ? AND completed = 1', (task_id,))
            row = cursor.fetchone()
            return row['count']
        except Exception as e:
            raise e
    
    def get_total_subtasks_count(self, task_id: str) -> int:
        """Get total count of subtasks for a task"""
        try:
            cursor = self.database.cursor()
            cursor.execute('SELECT COUNT(*) as count FROM subtasks WHERE task_id = ?', (task_id,))
            row = cursor.fetchone()
            return row['count']
        except Exception as e:
            raise e 