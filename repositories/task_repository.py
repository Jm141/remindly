import sqlite3
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from models.task import Task
from repositories.database_interface import TaskRepositoryInterface, SubtaskRepositoryInterface
from abc import abstractmethod

class TaskRepository(TaskRepositoryInterface):
    """Task repository implementation following Single Responsibility Principle"""
    
    def __init__(self, database: sqlite3.Connection, subtask_repository: Optional[SubtaskRepositoryInterface] = None):
        self.database = database
        self.subtask_repository = subtask_repository
    
    def create_task(self, task: Task) -> Task:
        """Create a new task"""
        try:
            cursor = self.database.cursor()
            cursor.execute('''
                INSERT INTO tasks (user_id, title, description, due_date, priority, status, completed)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                task.user_id, task.title, task.description, task.due_date,
                task.priority, task.status, task.completed
            ))
            
            task.id = cursor.lastrowid
            self.database.commit()
            return task
        except Exception as e:
            self.database.rollback()
            raise e
    
    def get_tasks_by_user(self, user_id: int, completed: Optional[bool] = None) -> List[Task]:
        """Get tasks for a user"""
        try:
            cursor = self.database.cursor()
            
            if completed is not None:
                cursor.execute('''
                    SELECT id, user_id, title, description, due_date, priority, status, completed, created_at, updated_at
                    FROM tasks WHERE user_id = ? AND completed = ?
                    ORDER BY created_at DESC
                ''', (user_id, completed))
            else:
                cursor.execute('''
                    SELECT id, user_id, title, description, due_date, priority, status, completed, created_at, updated_at
                    FROM tasks WHERE user_id = ?
                    ORDER BY created_at DESC
                ''', (user_id,))
            
            rows = cursor.fetchall()
            tasks = []
            for row in rows:
                task = Task(
                    id=row['id'],
                    user_id=row['user_id'],
                    title=row['title'],
                    description=row['description'],
                    due_date=row['due_date'],
                    priority=row['priority'],
                    status=row['status'],
                    completed=bool(row['completed']),
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
                
                # Load subtasks for this task if subtask repository is available
                if self.subtask_repository:
                    try:
                        subtasks = self.subtask_repository.get_subtasks_by_task(task.id)
                        task.subtasks = subtasks
                        print(f"Loaded {len(subtasks)} subtasks for task {task.id}")
                    except Exception as e:
                        print(f"Error loading subtasks for task {task.id}: {e}")
                        task.subtasks = []
                else:
                    print(f"No subtask repository available, subtasks will be empty for task {task.id}")
                
                tasks.append(task)
            return tasks
        except Exception as e:
            raise e
    
    def get_task_by_id(self, task_id: int, user_id: int) -> Optional[Task]:
        """Get task by ID for a specific user"""
        try:
            cursor = self.database.cursor()
            cursor.execute('''
                SELECT id, user_id, title, description, due_date, priority, status, completed, created_at, updated_at
                FROM tasks WHERE id = ? AND user_id = ?
            ''', (task_id, user_id))
            
            row = cursor.fetchone()
            if row:
                return Task(
                    id=row['id'],
                    user_id=row['user_id'],
                    title=row['title'],
                    description=row['description'],
                    due_date=row['due_date'],
                    priority=row['priority'],
                    status=row['status'],
                    completed=bool(row['completed']),
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
            return None
        except Exception as e:
            raise e
    
    def get_task_by_id_only(self, task_id: int) -> Optional[Task]:
        """Get task by ID without user restriction (for task sharing)"""
        try:
            cursor = self.database.cursor()
            cursor.execute('''
                SELECT id, user_id, title, description, due_date, priority, status, completed, created_at, updated_at
                FROM tasks WHERE id = ?
            ''', (task_id,))
            
            row = cursor.fetchone()
            if row:
                return Task(
                    id=row['id'],
                    user_id=row['user_id'],
                    title=row['title'],
                    description=row['description'],
                    due_date=row['due_date'],
                    priority=row['priority'],
                    status=row['status'],
                    completed=bool(row['completed']),
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
            return None
        except Exception as e:
            raise e
    
    def update_task(self, task_id: int, user_id: int, updates: Dict[str, Any]) -> bool:
        """Update a task"""
        try:
            cursor = self.database.cursor()
            
            # Build update query dynamically
            set_clauses = []
            params = []
            
            for key, value in updates.items():
                if key in ['title', 'description', 'due_date', 'priority', 'status', 'completed']:
                    set_clauses.append(f"{key} = ?")
                    params.append(value)
            
            if not set_clauses:
                return False
            
            set_clauses.append("updated_at = CURRENT_TIMESTAMP")
            params.extend([task_id, user_id])
            
            query = f"UPDATE tasks SET {', '.join(set_clauses)} WHERE id = ? AND user_id = ?"
            cursor.execute(query, params)
            
            self.database.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.database.rollback()
            raise e
    
    def delete_task(self, task_id: int, user_id: int) -> bool:
        """Delete a task"""
        try:
            cursor = self.database.cursor()
            cursor.execute('DELETE FROM tasks WHERE id = ? AND user_id = ?', (task_id, user_id))
            self.database.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.database.rollback()
            raise e
    
    def get_tasks_due_soon(self, user_id: int, hours: int = 1) -> List[Task]:
        """Get tasks due within specified hours"""
        try:
            cursor = self.database.cursor()
            due_time = datetime.now() + timedelta(hours=hours)
            
            cursor.execute('''
                SELECT id, user_id, title, description, due_date, priority, status, completed, created_at, updated_at
                FROM tasks 
                WHERE user_id = ? AND due_date <= ? AND completed = 0
                ORDER BY due_date ASC
            ''', (user_id, due_time.strftime('%Y-%m-%d %H:%M')))
            
            rows = cursor.fetchall()
            tasks = []
            for row in rows:
                tasks.append(Task(
                    id=row['id'],
                    user_id=row['user_id'],
                    title=row['title'],
                    description=row['description'],
                    due_date=row['due_date'],
                    priority=row['priority'],
                    status=row['status'],
                    completed=bool(row['completed']),
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                ))
            return tasks
        except Exception as e:
            raise e
    
    def get_overdue_tasks(self, user_id: int) -> List[Task]:
        """Get overdue tasks for a user"""
        try:
            cursor = self.database.cursor()
            now = datetime.now()
            
            cursor.execute('''
                SELECT id, user_id, title, description, due_date, priority, status, completed, created_at, updated_at
                FROM tasks 
                WHERE user_id = ? AND due_date < ? AND completed = 0
                ORDER BY due_date ASC
            ''', (user_id, now.strftime('%Y-%m-%d %H:%M')))
            
            rows = cursor.fetchall()
            tasks = []
            for row in rows:
                tasks.append(Task(
                    id=row['id'],
                    user_id=row['user_id'],
                    title=row['title'],
                    description=row['description'],
                    due_date=row['due_date'],
                    priority=row['priority'],
                    status=row['status'],
                    completed=bool(row['completed']),
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                ))
            return tasks
        except Exception as e:
            raise e 