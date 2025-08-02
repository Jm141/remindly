import sqlite3
import os
from pathlib import Path
from repositories.user_repository import UserRepository
from repositories.task_repository import TaskRepository
from repositories.subtask_repository import SubtaskRepository
from repositories.task_share_repository import SQLiteTaskShareRepository
from services.auth_service import AuthService
from services.task_service import TaskService
from services.task_share_service import TaskShareService
from controllers.auth_controller import AuthController
from controllers.task_controller import TaskController
from controllers.task_share_controller import TaskShareController
from config import Config

class DependencyContainer:
    """Dependency Injection Container following SOLID Principles"""
    
    def __init__(self):
        self._database = None
        self._user_repository = None
        self._task_repository = None
        self._subtask_repository = None
        self._task_share_repository = None
        self._auth_service = None
        self._task_service = None
        self._task_share_service = None
        self._auth_controller = None
        self._task_controller = None
        self._task_share_controller = None
    
    def get_database(self):
        """Get database connection"""
        if self._database is None:
            # Ensure database directory exists
            db_dir = os.path.dirname(Config.DATABASE_PATH)
            if db_dir:
                Path(db_dir).mkdir(parents=True, exist_ok=True)
            
            self._database = sqlite3.connect(Config.DATABASE_PATH)
            self._database.row_factory = sqlite3.Row
            self._initialize_tables()
        return self._database
    
    def get_user_repository(self):
        """Get user repository"""
        if self._user_repository is None:
            self._user_repository = UserRepository(self.get_database())
        return self._user_repository
    
    def get_task_repository(self):
        """Get task repository"""
        if self._task_repository is None:
            self._task_repository = TaskRepository(self.get_database())
        return self._task_repository
    
    def get_subtask_repository(self):
        """Get subtask repository"""
        if self._subtask_repository is None:
            self._subtask_repository = SubtaskRepository(self.get_database())
        return self._subtask_repository
    
    def get_task_share_repository(self):
        """Get task share repository"""
        if self._task_share_repository is None:
            self._task_share_repository = SQLiteTaskShareRepository(self.get_database())
        return self._task_share_repository
    
    def get_auth_service(self, bcrypt):
        """Get auth service"""
        if self._auth_service is None:
            self._auth_service = AuthService(
                self.get_user_repository(),
                bcrypt
            )
        return self._auth_service
    
    def get_task_service(self):
        """Get task service"""
        if self._task_service is None:
            self._task_service = TaskService(
                self.get_task_repository(),
                self.get_subtask_repository(),
                self.get_user_repository(),
                self.get_task_share_service()
            )
        return self._task_service
    
    def get_task_share_service(self):
        """Get task share service"""
        if self._task_share_service is None:
            self._task_share_service = TaskShareService(
                self.get_task_share_repository(),
                self.get_task_repository(),
                self.get_user_repository()
            )
        return self._task_share_service
    
    def get_auth_controller(self, bcrypt):
        """Get auth controller"""
        if self._auth_controller is None:
            self._auth_controller = AuthController(
                self.get_auth_service(bcrypt)
            )
        return self._auth_controller
    
    def get_task_controller(self, bcrypt):
        """Get task controller"""
        if self._task_controller is None:
            self._task_controller = TaskController(
                self.get_task_service(),
                self.get_auth_service(bcrypt)
            )
        return self._task_controller
    
    def get_task_share_controller(self, bcrypt):
        """Get task share controller"""
        if self._task_share_controller is None:
            self._task_share_controller = TaskShareController(
                self.get_task_share_service()
            )
        return self._task_share_controller
    
    def _initialize_tables(self):
        """Initialize database tables"""
        db = self.get_database()
        
        # Users table
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tasks table
        db.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                due_date TIMESTAMP,
                priority TEXT DEFAULT 'medium',
                status TEXT DEFAULT 'pending',
                completed BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        ''')
        
        # Subtasks table
        db.execute('''
            CREATE TABLE IF NOT EXISTS subtasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                completed BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (task_id) REFERENCES tasks (id) ON DELETE CASCADE
            )
        ''')
        
        # Create indexes for better performance
        db.execute('CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id)')
        db.execute('CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)')
        db.execute('CREATE INDEX IF NOT EXISTS idx_subtasks_task_id ON subtasks(task_id)')
        
        # Task sharing table for collaboration
        db.execute('''
            CREATE TABLE IF NOT EXISTS task_shares (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER NOT NULL,
                owner_id INTEGER NOT NULL,
                shared_with_id INTEGER NOT NULL,
                permission_level TEXT DEFAULT 'view', -- 'view', 'edit', 'admin'
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (task_id) REFERENCES tasks (id) ON DELETE CASCADE,
                FOREIGN KEY (owner_id) REFERENCES users (id) ON DELETE CASCADE,
                FOREIGN KEY (shared_with_id) REFERENCES users (id) ON DELETE CASCADE,
                UNIQUE(task_id, shared_with_id)
            )
        ''')
        
        # Create indexes for task sharing
        db.execute('CREATE INDEX IF NOT EXISTS idx_task_shares_task_id ON task_shares(task_id)')
        db.execute('CREATE INDEX IF NOT EXISTS idx_task_shares_owner_id ON task_shares(owner_id)')
        db.execute('CREATE INDEX IF NOT EXISTS idx_task_shares_shared_with_id ON task_shares(shared_with_id)')
        
        db.execute('CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)')
        
        db.commit()
    
    def cleanup(self):
        """Cleanup resources"""
        if self._database:
            self._database.close()
            self._database = None

# Global container instance
container = DependencyContainer() 