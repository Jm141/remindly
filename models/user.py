from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    """User model following Single Responsibility Principle"""
    id: Optional[int]
    username: str
    password: str
    
    def to_dict(self) -> dict:
        """Convert user to dictionary (excluding password)"""
        return {
            'id': self.id,
            'username': self.username
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Create user from dictionary"""
        return cls(
            id=data.get('id'),
            username=data['username'],
            password=data['password']
        ) 