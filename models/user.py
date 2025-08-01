from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class User:
    """User model following Single Responsibility Principle"""
    id: Optional[int]
    username: str
    password: str
    email: str = ""
    first_name: str = ""
    last_name: str = ""
    created_at: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert user to dictionary (excluding password)"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Create user from dictionary"""
        return cls(
            id=data.get('id'),
            username=data['username'],
            password=data.get('password', ''),
            email=data.get('email', ''),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            created_at=data.get('created_at')
        ) 