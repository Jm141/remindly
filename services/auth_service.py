from typing import Optional, Tuple
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token
from models.user import User
from repositories.database_interface import UserRepositoryInterface
from config import Config

class AuthService:
    """Authentication service following Single Responsibility Principle"""
    
    def __init__(self, user_repository: UserRepositoryInterface, bcrypt: Bcrypt):
        self.user_repository = user_repository
        self.bcrypt = bcrypt
    
    def register_user(self, username: str, password: str) -> Tuple[bool, str]:
        """Register a new user"""
        # Validate input
        if not username or not password:
            return False, "Username and password are required"
        
        if len(password) < Config.MIN_PASSWORD_LENGTH:
            return False, f"Password must be at least {Config.MIN_PASSWORD_LENGTH} characters"
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters"
        
        # Check if user already exists
        if self.user_repository.user_exists(username):
            return False, "Username already exists"
        
        # Hash password and create user
        hashed_password = self.bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(id=None, username=username, password=hashed_password)
        
        try:
            created_user = self.user_repository.create_user(user)
            return True, "User registered successfully"
        except Exception as e:
            return False, f"Registration failed: {str(e)}"
    
    def authenticate_user(self, username: str, password: str) -> Tuple[Optional[User], str]:
        """Authenticate a user"""
        if not username or not password:
            return None, "Username and password are required"
        
        user = self.user_repository.get_user_by_username(username)
        if not user:
            return None, "Invalid credentials"
        
        if not self.bcrypt.check_password_hash(user.password, password):
            return None, "Invalid credentials"
        
        return user, "Authentication successful"
    
    def create_tokens(self, user: User) -> dict:
        """Create JWT tokens for user"""
        access_token = create_access_token(identity=user.username)
        refresh_token = create_refresh_token(identity=user.username)
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.user_repository.get_user_by_username(username)
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.user_repository.get_user_by_id(user_id) 