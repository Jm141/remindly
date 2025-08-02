from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from utils.id_generator import generate_task_id, generate_subtask_id

@dataclass
class Subtask:
    """Subtask model following Single Responsibility Principle"""
    id: Optional[str]
    task_id: str
    title: str
    description: str = ""
    completed: bool = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    def __post_init__(self):
        """Auto-generate unique ID if not provided"""
        if self.id is None:
            self.id = generate_subtask_id()
    
    def to_dict(self) -> dict:
        """Convert subtask to dictionary"""
        return {
            'id': self.id,
            'task_id': self.task_id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Subtask':
        """Create subtask from dictionary"""
        return cls(
            id=data.get('id'),
            task_id=data['task_id'],
            title=data['title'],
            description=data.get('description', ''),
            completed=data.get('completed', False),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )

@dataclass
class Task:
    """Task model following Single Responsibility Principle"""
    id: Optional[str]
    user_id: str
    title: str
    description: str = ""
    category: str = ""
    recurrence: str = ""
    priority: str = ""
    due_date: Optional[str] = None
    status: Optional[str] = None
    completed: bool = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    subtasks: List[Subtask] = field(default_factory=list)
    
    def __post_init__(self):
        """Auto-generate unique ID if not provided"""
        if self.id is None:
            self.id = generate_task_id()
    
    def to_dict(self) -> dict:
        """Convert task to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'recurrence': self.recurrence,
            'priority': self.priority,
            'due_date': self.due_date,
            'status': self.status,
            'completed': self.completed,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'subtasks': [subtask.to_dict() for subtask in self.subtasks]
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """Create task from dictionary"""
        subtasks = [Subtask.from_dict(st) for st in data.get('subtasks', [])]
        return cls(
            id=data.get('id'),
            user_id=data['user_id'],
            title=data['title'],
            description=data.get('description', ''),
            category=data.get('category', ''),
            recurrence=data.get('recurrence', ''),
            priority=data.get('priority', ''),
            due_date=data.get('due_date'),
            status=data.get('status'),
            completed=data.get('completed', False),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
            subtasks=subtasks
        )
    
    def is_overdue(self) -> bool:
        """Check if task is overdue"""
        if not self.due_date:
            return False
        try:
            due_datetime = datetime.strptime(self.due_date, '%Y-%m-%d %H:%M')
            return due_datetime < datetime.now()
        except ValueError:
            return False
    
    def is_due_soon(self, hours: int = 1) -> bool:
        """Check if task is due within specified hours"""
        if not self.due_date:
            return False
        try:
            due_datetime = datetime.strptime(self.due_date, '%Y-%m-%d %H:%M')
            now = datetime.now()
            time_diff = due_datetime - now
            return 0 <= time_diff.total_seconds() <= hours * 3600
        except ValueError:
            return False 