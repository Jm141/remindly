from typing import Optional, Tuple
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token
from models.user import User
from repositories.database_interface import UserRepositoryInterface
from utils.user_code_generator import UserCodeGenerator
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
        
        # Check if user already exists (case-insensitive)
        if self.user_repository.user_exists(username) or self.user_repository.user_exists_case_insensitive(username):
            return False, "Username already exists"
        
        # Generate unique user code
        try:
            user_code = UserCodeGenerator.generate_unique_user_code(Config.DATABASE_PATH)
        except Exception as e:
            return False, f"Failed to generate user code: {str(e)}"
        
        # Hash password and create user
        hashed_password = self.bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(id=None, user_code=user_code, username=username, password_hash=hashed_password)
        
        try:
            created_user = self.user_repository.create_user(user)
            return True, f"User registered successfully. Your unique code is: {user_code}"
        except Exception as e:
            return False, f"Registration failed: {str(e)}"
    
    def authenticate_user(self, username: str, password: str) -> Tuple[Optional[User], str]:
        """Authenticate a user"""
        if not username or not password:
            return None, "Username and password are required"
        
        # Try exact match first, then case-insensitive
        user = self.user_repository.get_user_by_username(username)
        if not user:
            user = self.user_repository.get_user_by_username_case_insensitive(username)
        
        if not user:
            return None, "Invalid credentials"
        
        if not self.bcrypt.check_password_hash(user.password_hash, password):
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
    
    def get_user_by_user_code(self, user_code: str) -> Optional[User]:
        """Get user by user_code"""
        return self.user_repository.get_user_by_user_code(user_code)
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.user_repository.get_user_by_id(user_id)

    def update_user_info(self, current_username: str, new_username: str, new_email: str = None) -> Tuple[bool, str]:
        """Update user information"""
        # Validate input
        if not new_username:
            return False, "Username is required"
        
        if len(new_username) < 3:
            return False, "Username must be at least 3 characters"
        
        # Check if new username already exists (if different from current)
        if new_username != current_username and self.user_repository.user_exists(new_username):
            return False, "Username already exists"
        
        try:
            # Get current user
            user = self.user_repository.get_user_by_username(current_username)
            if not user:
                return False, "User not found"
            
            # Update user info
            updated_user = User(
                id=user.id,
                username=new_username,
                password_hash=user.password_hash,
                email=new_email,
                created_at=user.created_at,
                updated_at=None  # Will be set by repository
            )
            
            self.user_repository.update_user_object(updated_user)
            return True, "User information updated successfully"
            
        except Exception as e:
            return False, f"Update failed: {str(e)}"

    def change_password(self, username: str, current_password: str, new_password: str) -> Tuple[bool, str]:
        """Change user password"""
        # Validate input
        if not current_password or not new_password:
            return False, "Current password and new password are required"
        
        if len(new_password) < 6:
            return False, "New password must be at least 6 characters"
        
        try:
            # Get current user
            user = self.user_repository.get_user_by_username(username)
            if not user:
                return False, "User not found"
            
            # Verify current password
            if not self.bcrypt.check_password_hash(user.password_hash, current_password):
                return False, "Current password is incorrect"
            
            # Hash new password
            new_password_hash = self.bcrypt.generate_password_hash(new_password).decode('utf-8')
            
            # Update user with new password
            updated_user = User(
                id=user.id,
                username=user.username,
                password_hash=new_password_hash,
                email=user.email,
                created_at=user.created_at,
                updated_at=None  # Will be set by repository
            )
            
            self.user_repository.update_user_object(updated_user)
            return True, "Password changed successfully"
            
        except Exception as e:
            return False, f"Password change failed: {str(e)}" 