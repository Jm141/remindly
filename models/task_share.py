from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class TaskShare:
    """Task sharing model for collaboration"""
    id: Optional[int]
    task_id: int
    owner_code: str
    shared_with_code: str
    permission_level: str = "view"  # 'view', 'edit', 'admin'
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert task share to dictionary"""
        return {
            'id': self.id,
            'task_id': self.task_id,
            'owner_code': self.owner_code,
            'shared_with_code': self.shared_with_code,
            'permission_level': self.permission_level,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'TaskShare':
        """Create task share from dictionary"""
        return cls(
            id=data.get('id'),
            task_id=data['task_id'],
            owner_code=data['owner_code'],
            shared_with_code=data['shared_with_code'],
            permission_level=data.get('permission_level', 'view'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def can_edit(self) -> bool:
        """Check if user can edit the shared task"""
        return self.permission_level in ['edit', 'admin']
    
    def can_admin(self) -> bool:
        """Check if user has admin permissions"""
        return self.permission_level == 'admin' 