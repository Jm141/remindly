import sqlite3
import os
from pathlib import Path
from repositories.sqlite_repository import SQLiteDatabase, SQLiteUserRepository, SQLiteTaskRepository, SQLiteSubtaskRepository
from services.auth_service import AuthService
from services.task_service import TaskService
from controllers.auth_controller import AuthController
from controllers.task_controller import TaskController
from config import Config

class DependencyContainer:
    """Dependency Injection Container following SOLID Principles"""
    
    def __init__(self):
        self._database = None
        self._user_repository = None
        self._task_repository = None
        self._subtask_repository = None
        self._auth_service = None
        self._task_service = None
        self._auth_controller = None
        self._task_controller = None
    
    def get_database(self):
        """Get database connection"""
        if self._database is None:
            # Ensure database directory exists
            db_dir = os.path.dirname(Config.DATABASE_PATH)
            if db_dir:
                Path(db_dir).mkdir(parents=True, exist_ok=True)
            
            self._database = SQLiteDatabase(Config.DATABASE_PATH)
        return self._database
    
    def get_user_repository(self):
        """Get user repository"""
        if self._user_repository is None:
            self._user_repository = SQLiteUserRepository(self.get_database())
        return self._user_repository
    
    def get_task_repository(self):
        """Get task repository"""
        if self._task_repository is None:
            self._task_repository = SQLiteTaskRepository(self.get_database(), self.get_subtask_repository())
        return self._task_repository
    
    def get_subtask_repository(self):
        """Get subtask repository"""
        if self._subtask_repository is None:
            self._subtask_repository = SQLiteSubtaskRepository(self.get_database())
        return self._subtask_repository
    
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
                self.get_user_repository()
            )
        return self._task_service
    
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
    
    def cleanup(self):
        """Cleanup resources"""
        if self._database:
            self._database.close()
            self._database = None

# Global container instance
container = DependencyContainer() 