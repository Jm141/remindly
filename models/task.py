from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime

@dataclass
class Subtask:
    """Subtask model following Single Responsibility Principle"""
    id: Optional[int]
    task_id: int
    title: str
    completed: bool = False
    
    def to_dict(self) -> dict:
        """Convert subtask to dictionary"""
        return {
            'id': self.id,
            'task_id': self.task_id,
            'title': self.title,
            'completed': self.completed
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Subtask':
        """Create subtask from dictionary"""
        return cls(
            id=data.get('id'),
            task_id=data['task_id'],
            title=data['title'],
            completed=data.get('completed', False)
        )

@dataclass
class Task:
    """Task model following Single Responsibility Principle"""
    id: Optional[int]
    user_id: int
    title: str
    description: str = ""
    category: str = ""
    recurrence: str = ""
    priority: str = ""
    due_date: Optional[str] = None
    completed: bool = False
    subtasks: List[Subtask] = field(default_factory=list)
    
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
            'completed': self.completed,
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
            completed=data.get('completed', False),
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