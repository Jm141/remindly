from typing import Optional, Tuple, List
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token
from models.user import User
from repositories.database_interface import UserRepositoryInterface
from config import Config
from datetime import datetime

class AuthService:
    """Authentication service following Single Responsibility Principle"""
    
    def __init__(self, user_repository: UserRepositoryInterface, bcrypt: Bcrypt):
        self.user_repository = user_repository
        self.bcrypt = bcrypt
    
    def register_user(self, username: str, password: str, email: str = "", first_name: str = "", last_name: str = "") -> Tuple[bool, str]:
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
        user = User(
            id=None, 
            username=username, 
            password=hashed_password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
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

    def update_user(self, user_id: int, email: str = None, first_name: str = None, last_name: str = None) -> Tuple[bool, str]:
        """Update user information"""
        try:
            user = self.user_repository.get_user_by_id(user_id)
            if not user:
                return False, "User not found"
            
            # Update fields if provided
            if email is not None:
                user.email = email
            if first_name is not None:
                user.first_name = first_name
            if last_name is not None:
                user.last_name = last_name
            
            updated_user = self.user_repository.update_user(user)
            return True, "User updated successfully"
        except Exception as e:
            return False, f"Update failed: {str(e)}"
    
    def update_password(self, user_id: int, current_password: str, new_password: str) -> Tuple[bool, str]:
        """Update user password"""
        try:
            user = self.user_repository.get_user_by_id(user_id)
            if not user:
                return False, "User not found"
            
            # Verify current password
            if not self.bcrypt.check_password_hash(user.password, current_password):
                return False, "Current password is incorrect"
            
            # Validate new password
            if len(new_password) < Config.MIN_PASSWORD_LENGTH:
                return False, f"New password must be at least {Config.MIN_PASSWORD_LENGTH} characters"
            
            # Hash and update password
            hashed_password = self.bcrypt.generate_password_hash(new_password).decode('utf-8')
            user.password = hashed_password
            
            updated_user = self.user_repository.update_user(user)
            return True, "Password updated successfully"
        except Exception as e:
            return False, f"Password update failed: {str(e)}"
    
    def update_username(self, user_id: int, new_username: str) -> Tuple[bool, str]:
        """Update username"""
        try:
            if len(new_username) < 3:
                return False, "Username must be at least 3 characters"
            
            # Check if new username already exists
            if self.user_repository.user_exists(new_username):
                return False, "Username already exists"
            
            user = self.user_repository.get_user_by_id(user_id)
            if not user:
                return False, "User not found"
            
            user.username = new_username
            updated_user = self.user_repository.update_user(user)
            return True, "Username updated successfully"
        except Exception as e:
            return False, f"Username update failed: {str(e)}"
    
    def get_all_users(self) -> List[User]:
        """Get all users (for admin purposes)"""
        try:
            return self.user_repository.get_all_users()
        except Exception as e:
            return []
    
    def delete_user(self, user_id: int) -> Tuple[bool, str]:
        """Delete user"""
        try:
            user = self.user_repository.get_user_by_id(user_id)
            if not user:
                return False, "User not found"
            
            self.user_repository.delete_user(user_id)
            return True, "User deleted successfully"
        except Exception as e:
            return False, f"Delete failed: {str(e)}" 