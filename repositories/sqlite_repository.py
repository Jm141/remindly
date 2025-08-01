import sqlite3
import os
import threading
from typing import List, Optional, Dict, Any
from models.user import User
from models.task import Task, Subtask
from repositories.database_interface import (
    DatabaseInterface, UserRepositoryInterface, 
    TaskRepositoryInterface, SubtaskRepositoryInterface
)
from config import Config

class SQLiteDatabase(DatabaseInterface):
    """SQLite database implementation following Liskov Substitution Principle"""
    
    def __init__(self, db_path: str = Config.DATABASE_PATH):
        self.db_path = db_path
        self._local = threading.local()
    
    def _get_connection(self):
        """Get thread-local database connection"""
        if not hasattr(self._local, 'connection'):
            if not os.path.exists(os.path.dirname(self.db_path)):
                os.makedirs(os.path.dirname(self.db_path))
            self._local.connection = sqlite3.connect(self.db_path)
            self._local.connection.row_factory = sqlite3.Row
        return self._local.connection
    
    def connect(self):
        """Establish database connection (for compatibility)"""
        self._get_connection()
    
    def close(self):
        """Close database connection"""
        if hasattr(self._local, 'connection'):
            self._local.connection.close()
            delattr(self._local, 'connection')
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute a query and return results"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute an update query and return affected rows"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount

class SQLiteUserRepository(UserRepositoryInterface):
    """SQLite user repository implementation following Liskov Substitution Principle"""
    
    def __init__(self, database: DatabaseInterface):
        self.db = database
        self._init_table()
    
    def _init_table(self):
        """Initialize users table"""
        self.db.execute_update('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            first_name TEXT,
            last_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    def create_user(self, user: User) -> User:
        """Create a new user"""
        query = '''INSERT INTO users (username, password, email, first_name, last_name, created_at) 
                   VALUES (?, ?, ?, ?, ?, ?)'''
        self.db.execute_update(query, (user.username, user.password, user.email, user.first_name, user.last_name, user.created_at))
        
        # Get the created user with ID
        created_user = self.get_user_by_username(user.username)
        return created_user
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        query = '''SELECT id, username, password, email, first_name, last_name, created_at 
                   FROM users WHERE username = ?'''
        result = self.db.execute_query(query, (username,))
        if result:
            row = result[0]
            return User(
                id=row['id'], 
                username=row['username'], 
                password=row['password'],
                email=row.get('email', ''),
                first_name=row.get('first_name', ''),
                last_name=row.get('last_name', ''),
                created_at=row.get('created_at')
            )
        return None
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        query = '''SELECT id, username, password, email, first_name, last_name, created_at 
                   FROM users WHERE id = ?'''
        result = self.db.execute_query(query, (user_id,))
        if result:
            row = result[0]
            return User(
                id=row['id'], 
                username=row['username'], 
                password=row['password'],
                email=row.get('email', ''),
                first_name=row.get('first_name', ''),
                last_name=row.get('last_name', ''),
                created_at=row.get('created_at')
            )
        return None
    
    def user_exists(self, username: str) -> bool:
        """Check if user exists"""
        return self.get_user_by_username(username) is not None
    
    def update_user(self, user: User) -> User:
        """Update user information"""
        query = '''UPDATE users 
                   SET username = ?, email = ?, first_name = ?, last_name = ?
                   WHERE id = ?'''
        self.db.execute_update(query, (user.username, user.email, user.first_name, user.last_name, user.id))
        return user
    
    def get_all_users(self) -> List[User]:
        """Get all users"""
        query = '''SELECT id, username, password, email, first_name, last_name, created_at 
                   FROM users'''
        result = self.db.execute_query(query)
        users = []
        for row in result:
            users.append(User(
                id=row['id'], 
                username=row['username'], 
                password=row['password'],
                email=row.get('email', ''),
                first_name=row.get('first_name', ''),
                last_name=row.get('last_name', ''),
                created_at=row.get('created_at')
            ))
        return users
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user by ID"""
        query = 'DELETE FROM users WHERE id = ?'
        affected_rows = self.db.execute_update(query, (user_id,))
        return affected_rows > 0

class SQLiteTaskRepository(TaskRepositoryInterface):
    """SQLite task repository implementation following Liskov Substitution Principle"""
    
    def __init__(self, database: DatabaseInterface, subtask_repo: SubtaskRepositoryInterface):
        self.db = database
        self.subtask_repo = subtask_repo
        self._init_table()
    
    def _init_table(self):
        """Initialize tasks table"""
        self.db.execute_update('''CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            description TEXT,
            category TEXT,
            recurrence TEXT,
            priority TEXT,
            due_date TEXT,
            completed BOOLEAN DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id))''')
    
    def create_task(self, task: Task) -> Task:
        """Create a new task"""
        query = '''INSERT INTO tasks (user_id, title, description, category, recurrence, priority, due_date)
                   VALUES (?, ?, ?, ?, ?, ?, ?)'''
        self.db.execute_update(query, (
            task.user_id, task.title, task.description, task.category,
            task.recurrence, task.priority, task.due_date
        ))
        
        # Get the created task with ID
        created_task = self.get_task_by_title_and_user(task.title, task.user_id)
        return created_task
    
    def get_task_by_title_and_user(self, title: str, user_id: int) -> Optional[Task]:
        """Get task by title and user ID"""
        query = 'SELECT * FROM tasks WHERE title = ? AND user_id = ? ORDER BY id DESC LIMIT 1'
        result = self.db.execute_query(query, (title, user_id))
        if result:
            return self._row_to_task(result[0])
        return None
    
    def get_tasks_by_user(self, user_id: int, completed: Optional[bool] = None) -> List[Task]:
        """Get tasks for a user"""
        if completed is not None:
            query = 'SELECT * FROM tasks WHERE user_id = ? AND completed = ?'
            result = self.db.execute_query(query, (user_id, int(completed)))
        else:
            query = 'SELECT * FROM tasks WHERE user_id = ?'
            result = self.db.execute_query(query, (user_id,))
        
        tasks = [self._row_to_task(row) for row in result]
        return tasks
    
    def get_task_by_id(self, task_id: int, user_id: int) -> Optional[Task]:
        """Get task by ID for a specific user"""
        query = 'SELECT * FROM tasks WHERE id = ? AND user_id = ?'
        result = self.db.execute_query(query, (task_id, user_id))
        if result:
            return self._row_to_task(result[0])
        return None
    
    def update_task(self, task_id: int, user_id: int, updates: Dict[str, Any]) -> bool:
        """Update a task"""
        if not updates:
            return False
        
        fields = []
        values = []
        for field, value in updates.items():
            if field in ['title', 'description', 'category', 'recurrence', 'priority', 'due_date']:
                fields.append(f"{field} = ?")
                values.append(value)
            elif field == 'completed':
                fields.append("completed = ?")
                values.append(int(value))
        
        if fields:
            values.extend([task_id, user_id])
            query = f"UPDATE tasks SET {', '.join(fields)} WHERE id = ? AND user_id = ?"
            affected_rows = self.db.execute_update(query, tuple(values))
            return affected_rows > 0
        return False
    
    def delete_task(self, task_id: int, user_id: int) -> bool:
        """Delete a task"""
        query = 'DELETE FROM tasks WHERE id = ? AND user_id = ?'
        affected_rows = self.db.execute_update(query, (task_id, user_id))
        return affected_rows > 0
    
    def get_tasks_due_soon(self, user_id: int, hours: int = 1) -> List[Task]:
        """Get tasks due within specified hours"""
        from datetime import datetime, timedelta
        now = datetime.now()
        future_time = now + timedelta(hours=hours)
        
        query = '''SELECT * FROM tasks 
                   WHERE user_id = ? AND completed = 0 AND due_date IS NOT NULL
                   AND due_date BETWEEN ? AND ?'''
        result = self.db.execute_query(query, (
            user_id, 
            now.strftime(Config.DATE_FORMAT), 
            future_time.strftime(Config.DATE_FORMAT)
        ))
        return [self._row_to_task(row) for row in result]
    
    def get_overdue_tasks(self, user_id: int) -> List[Task]:
        """Get overdue tasks for a user"""
        from datetime import datetime
        now = datetime.now()
        
        query = '''SELECT * FROM tasks 
                   WHERE user_id = ? AND completed = 0 AND due_date IS NOT NULL
                   AND due_date < ?'''
        result = self.db.execute_query(query, (user_id, now.strftime(Config.DATE_FORMAT)))
        return [self._row_to_task(row) for row in result]
    
    def _row_to_task(self, row: Dict[str, Any]) -> Task:
        """Convert database row to Task object"""
        task = Task(
            id=row['id'],
            user_id=row['user_id'],
            title=row['title'],
            description=row['description'] or '',
            category=row['category'] or '',
            recurrence=row['recurrence'] or '',
            priority=row['priority'] or '',
            due_date=row['due_date'],
            completed=bool(row['completed'])
        )
        
        # Load subtasks
        task.subtasks = self.subtask_repo.get_subtasks_by_task(task.id)
        return task

class SQLiteSubtaskRepository(SubtaskRepositoryInterface):
    """SQLite subtask repository implementation following Liskov Substitution Principle"""
    
    def __init__(self, database: DatabaseInterface):
        self.db = database
        self._init_table()
    
    def _init_table(self):
        """Initialize subtasks table"""
        self.db.execute_update('''CREATE TABLE IF NOT EXISTS subtasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER,
            title TEXT,
            completed BOOLEAN,
            FOREIGN KEY(task_id) REFERENCES tasks(id))''')
    
    def create_subtask(self, subtask: Subtask) -> Subtask:
        """Create a new subtask"""
        query = 'INSERT INTO subtasks (task_id, title, completed) VALUES (?, ?, ?)'
        self.db.execute_update(query, (subtask.task_id, subtask.title, int(subtask.completed)))
        
        # Get the created subtask with ID
        created_subtask = self.get_subtask_by_title_and_task(subtask.title, subtask.task_id)
        return created_subtask
    
    def get_subtask_by_title_and_task(self, title: str, task_id: int) -> Optional[Subtask]:
        """Get subtask by title and task ID"""
        query = 'SELECT * FROM subtasks WHERE title = ? AND task_id = ? ORDER BY id DESC LIMIT 1'
        result = self.db.execute_query(query, (title, task_id))
        if result:
            row = result[0]
            return Subtask(
                id=row['id'],
                task_id=row['task_id'],
                title=row['title'],
                completed=bool(row['completed'])
            )
        return None
    
    def get_subtasks_by_task(self, task_id: int) -> List[Subtask]:
        """Get subtasks for a task"""
        query = 'SELECT * FROM subtasks WHERE task_id = ?'
        result = self.db.execute_query(query, (task_id,))
        return [
            Subtask(
                id=row['id'],
                task_id=row['task_id'],
                title=row['title'],
                completed=bool(row['completed'])
            )
            for row in result
        ]
    
    def update_subtask(self, subtask_id: int, task_id: int, updates: Dict[str, Any]) -> bool:
        """Update a subtask"""
        if not updates:
            return False
        
        fields = []
        values = []
        for field, value in updates.items():
            if field == 'title':
                fields.append("title = ?")
                values.append(value)
            elif field == 'completed':
                fields.append("completed = ?")
                values.append(int(value))
        
        if fields:
            values.extend([subtask_id, task_id])
            query = f"UPDATE subtasks SET {', '.join(fields)} WHERE id = ? AND task_id = ?"
            affected_rows = self.db.execute_update(query, tuple(values))
            return affected_rows > 0
        return False
    
    def delete_subtask(self, subtask_id: int, task_id: int) -> bool:
        """Delete a subtask"""
        query = 'DELETE FROM subtasks WHERE id = ? AND task_id = ?'
        affected_rows = self.db.execute_update(query, (subtask_id, task_id))
        return affected_rows > 0 