from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from repositories.sqlite_repository import (
    SQLiteDatabase, SQLiteUserRepository, 
    SQLiteTaskRepository, SQLiteSubtaskRepository
)
from services.auth_service import AuthService
from services.task_service import TaskService
from controllers.auth_controller import AuthController
from controllers.task_controller import TaskController

class DependencyContainer:
    """Dependency injection container following Dependency Inversion Principle"""
    
    def __init__(self):
        self._database = None
        self._user_repository = None
        self._task_repository = None
        self._subtask_repository = None
        self._auth_service = None
        self._task_service = None
        self._auth_controller = None
        self._task_controller = None
        self._initialized = False
    
    def _initialize_database(self):
        """Initialize database and repositories"""
        if not self._initialized:
            # Create and connect database
            self._database = SQLiteDatabase()
            self._database.connect()
            
            # Create repositories
            self._subtask_repository = SQLiteSubtaskRepository(self._database)
            self._user_repository = SQLiteUserRepository(self._database)
            self._task_repository = SQLiteTaskRepository(self._database, self._subtask_repository)
            
            self._initialized = True
    
    def get_database(self):
        """Get database instance (singleton)"""
        if not self._initialized:
            self._initialize_database()
        return self._database
    
    def get_user_repository(self):
        """Get user repository instance (singleton)"""
        if not self._initialized:
            self._initialize_database()
        return self._user_repository
    
    def get_subtask_repository(self):
        """Get subtask repository instance (singleton)"""
        if not self._initialized:
            self._initialize_database()
        return self._subtask_repository
    
    def get_task_repository(self):
        """Get task repository instance (singleton)"""
        if not self._initialized:
            self._initialize_database()
        return self._task_repository
    
    def get_auth_service(self, bcrypt: Bcrypt):
        """Get auth service instance (singleton)"""
        if self._auth_service is None:
            self._auth_service = AuthService(self.get_user_repository(), bcrypt)
        return self._auth_service
    
    def get_task_service(self):
        """Get task service instance (singleton)"""
        if self._task_service is None:
            self._task_service = TaskService(
                self.get_task_repository(), 
                self.get_subtask_repository()
            )
        return self._task_service
    
    def get_auth_controller(self, bcrypt: Bcrypt):
        """Get auth controller instance (singleton)"""
        if self._auth_controller is None:
            self._auth_controller = AuthController(self.get_auth_service(bcrypt))
        return self._auth_controller
    
    def get_task_controller(self, bcrypt: Bcrypt):
        """Get task controller instance (singleton)"""
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

# Global dependency container instance
container = DependencyContainer() 