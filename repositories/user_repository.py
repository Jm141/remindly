import sqlite3
from typing import Optional, List
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
                INSERT INTO users (username, password, email, first_name, last_name, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user.username, user.password, user.email, user.first_name, user.last_name, user.created_at))
            
            user.id = cursor.lastrowid
            self.database.commit()
            return user
        except sqlite3.IntegrityError:
            raise ValueError("Username already exists")
        except Exception as e:
            self.database.rollback()
            raise e
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        try:
            cursor = self.database.cursor()
            cursor.execute('''
                SELECT id, username, password, email, first_name, last_name, created_at
                FROM users WHERE username = ?
            ''', (username,))
            
            row = cursor.fetchone()
            if row:
                return User(
                    id=row[0],
                    username=row[1],
                    password=row[2],
                    email=row[3] or "",
                    first_name=row[4] or "",
                    last_name=row[5] or "",
                    created_at=row[6]
                )
            return None
        except Exception as e:
            raise e
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        try:
            cursor = self.database.cursor()
            cursor.execute('''
                SELECT id, username, password, email, first_name, last_name, created_at
                FROM users WHERE id = ?
            ''', (user_id,))
            
            row = cursor.fetchone()
            if row:
                return User(
                    id=row[0],
                    username=row[1],
                    password=row[2],
                    email=row[3] or "",
                    first_name=row[4] or "",
                    last_name=row[5] or "",
                    created_at=row[6]
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
            return row[0] > 0
        except Exception as e:
            raise e
    
    def update_user(self, user: User) -> User:
        """Update user information"""
        try:
            cursor = self.database.cursor()
            cursor.execute('''
                UPDATE users 
                SET username = ?, email = ?, first_name = ?, last_name = ?
                WHERE id = ?
            ''', (user.username, user.email, user.first_name, user.last_name, user.id))
            
            self.database.commit()
            return user
        except Exception as e:
            self.database.rollback()
            raise e
    
    def get_all_users(self) -> List[User]:
        """Get all users"""
        try:
            cursor = self.database.cursor()
            cursor.execute('''
                SELECT id, username, password, email, first_name, last_name, created_at
                FROM users
            ''')
            
            users = []
            for row in cursor.fetchall():
                users.append(User(
                    id=row[0],
                    username=row[1],
                    password=row[2],
                    email=row[3] or "",
                    first_name=row[4] or "",
                    last_name=row[5] or "",
                    created_at=row[6]
                ))
            return users
        except Exception as e:
            raise e
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user by ID"""
        try:
            cursor = self.database.cursor()
            cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            self.database.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.database.rollback()
            raise e 