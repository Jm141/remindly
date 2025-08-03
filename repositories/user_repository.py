import sqlite3
from typing import Optional
from models.user import User
from repositories.database_interface import UserRepositoryInterface

class UserRepository(UserRepositoryInterface):
    """User repository implementation following Single Responsibility Principle"""
    
    def __init__(self, database: sqlite3.Connection):
        self.database = database
    
    def create_user(self, user: User) -> User:
        """Create a new user"""
        try:
            cursor = self.database.cursor()
            cursor.execute('''
                INSERT INTO users (user_code, username, password_hash, email)
                VALUES (?, ?, ?, ?)
            ''', (user.user_code, user.username, user.password_hash, user.email))
            
            user.id = cursor.lastrowid
            self.database.commit()
            return user
        except sqlite3.IntegrityError:
            raise ValueError("Username or user_code already exists")
        except Exception as e:
            self.database.rollback()
            raise e
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        try:
            cursor = self.database.cursor()
            cursor.execute('''
                SELECT id, user_code, username, password_hash, email, created_at, updated_at
                FROM users WHERE username = ?
            ''', (username,))
            
            row = cursor.fetchone()
            if row:
                return User(
                    id=row['id'],
                    user_code=row['user_code'],
                    username=row['username'],
                    password_hash=row['password_hash'],
                    email=row['email'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
            return None
        except Exception as e:
            raise e
    
    def get_user_by_user_code(self, user_code: str) -> Optional[User]:
        """Get user by user_code"""
        try:
            cursor = self.database.cursor()
            cursor.execute('''
                SELECT id, user_code, username, password_hash, email, created_at, updated_at
                FROM users WHERE user_code = ?
            ''', (user_code,))
            
            row = cursor.fetchone()
            if row:
                return User(
                    id=row['id'],
                    user_code=row['user_code'],
                    username=row['username'],
                    password_hash=row['password_hash'],
                    email=row['email'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
            return None
        except Exception as e:
            raise e
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        try:
            cursor = self.database.cursor()
            cursor.execute('''
                SELECT id, user_code, username, password_hash, email, created_at, updated_at
                FROM users WHERE id = ?
            ''', (user_id,))
            
            row = cursor.fetchone()
            if row:
                return User(
                    id=row['id'],
                    user_code=row['user_code'],
                    username=row['username'],
                    password_hash=row['password_hash'],
                    email=row['email'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
            return None
        except Exception as e:
            raise e
    
    def user_exists(self, username: str) -> bool:
        """Check if user exists"""
        try:
            cursor = self.database.cursor()
            cursor.execute('SELECT COUNT(*) as count FROM users WHERE username = ?', (username,))
            row = cursor.fetchone()
            return row['count'] > 0
        except Exception as e:
            raise e
    
    def user_code_exists(self, user_code: str) -> bool:
        """Check if user_code exists"""
        try:
            cursor = self.database.cursor()
            cursor.execute('SELECT COUNT(*) as count FROM users WHERE user_code = ?', (user_code,))
            row = cursor.fetchone()
            return row['count'] > 0
        except Exception as e:
            raise e
    
    def update_user(self, user_id: int, updates: dict) -> bool:
        """Update user information"""
        try:
            cursor = self.database.cursor()
            
            # Build update query dynamically
            set_clauses = []
            params = []
            
            for key, value in updates.items():
                if key in ['username', 'email', 'password_hash']:
                    set_clauses.append(f"{key} = ?")
                    params.append(value)
            
            if not set_clauses:
                return False
            
            set_clauses.append("updated_at = CURRENT_TIMESTAMP")
            params.append(user_id)
            
            query = f"UPDATE users SET {', '.join(set_clauses)} WHERE id = ?"
            cursor.execute(query, params)
            
            self.database.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.database.rollback()
            raise e

    def update_user_object(self, user: User) -> bool:
        """Update user information using User object"""
        try:
            cursor = self.database.cursor()
            cursor.execute('''
                UPDATE users 
                SET username = ?, email = ?, password_hash = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (user.username, user.email, user.password_hash, user.id))
            
            self.database.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.database.rollback()
            raise e 