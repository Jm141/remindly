from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    """User model following Single Responsibility Principle"""
    id: Optional[int]
    username: str
    password_hash: str
    email: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    @property
    def password(self) -> str:
        """Get password hash (for backward compatibility)"""
        return self.password_hash
    
    def to_dict(self) -> dict:
        """Convert user to dictionary (excluding password)"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Create user from dictionary"""
        return cls(
            id=data.get('id'),
            username=data['username'],
            password_hash=data.get('password_hash', data.get('password', '')),
            email=data.get('email'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        ) 