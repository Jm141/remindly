from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
from models.task import Task, Subtask
from repositories.database_interface import TaskRepositoryInterface, SubtaskRepositoryInterface, UserRepositoryInterface
from services.task_share_service import TaskShareService
from config import Config

class TaskService:
    """Task service following Single Responsibility Principle"""
    
    def __init__(self, 
                 task_repository: TaskRepositoryInterface, 
                 subtask_repository: SubtaskRepositoryInterface, 
                 user_repository: UserRepositoryInterface,
                 task_share_service: Optional[TaskShareService] = None):
        self.task_repository = task_repository
        self.subtask_repository = subtask_repository
        self.user_repository = user_repository
        self.task_share_service = task_share_service
    
    def create_task(self, user_id: str, task_data: Dict[str, Any]) -> Tuple[Optional[Task], str]:
        """Create a new task"""
        # Validate required fields
        if not task_data.get('title'):
            return None, "Task title is required"
        
        if len(task_data['title']) > Config.MAX_TITLE_LENGTH:
            return None, f"Title must be less than {Config.MAX_TITLE_LENGTH} characters"
        
        # Validate due date
        due_date = task_data.get('due_date')
        if due_date:
            validation_result = self._validate_due_date(due_date)
            if not validation_result[0]:
                return None, validation_result[1]
        
        # Create task object
        task = Task(
            id=None,
            user_id=user_id,
            title=task_data['title'],
            description=task_data.get('description', ''),
            category=task_data.get('category', ''),
            recurrence=task_data.get('recurrence', ''),
            priority=task_data.get('priority', ''),
            due_date=due_date,
            completed=False
        )
        
        try:
            created_task = self.task_repository.create_task(task)
            return created_task, "Task created successfully"
        except Exception as e:
            return None, f"Failed to create task: {str(e)}"
    
    def get_user_tasks(self, user_id: str, completed: Optional[bool] = None) -> List[Task]:
        """Get tasks for a user (including shared tasks)"""
        # Get user's own tasks
        user_tasks = self.task_repository.get_tasks_by_user(user_id, completed)
        
        # Get shared tasks if task share service is available
        if self.task_share_service:
            shared_tasks = self.task_share_service.get_shared_tasks(user_id)
            
            # Filter shared tasks by completion status if specified
            if completed is not None:
                shared_tasks = [task for task in shared_tasks if task.completed == completed]
            
            # Combine user tasks and shared tasks
            all_tasks = user_tasks + shared_tasks
            
            # Sort by creation date (newest first)
            all_tasks.sort(key=lambda x: x.created_at or '', reverse=True)
            
            return all_tasks
        
        return user_tasks
    
    def get_task(self, task_id: str, user_id: str) -> Optional[Task]:
        """Get a specific task"""
        return self.task_repository.get_task_by_id(task_id, user_id)
    
    def update_task(self, task_id: str, user_id: str, updates: Dict[str, Any]) -> Tuple[bool, str]:
        """Update a task"""
        # Validate task exists and belongs to user
        task = self.task_repository.get_task_by_id(task_id, user_id)
        if not task:
            return False, "Task not found or unauthorized"
        
        # Validate due date if being updated
        if 'due_date' in updates and updates['due_date']:
            validation_result = self._validate_due_date(updates['due_date'])
            if not validation_result[0]:
                return False, validation_result[1]
        
        # Validate title length if being updated
        if 'title' in updates and updates['title']:
            if len(updates['title']) > Config.MAX_TITLE_LENGTH:
                return False, f"Title must be less than {Config.MAX_TITLE_LENGTH} characters"
        
        try:
            success = self.task_repository.update_task(task_id, user_id, updates)
            if success:
                return True, "Task updated successfully"
            else:
                return False, "Failed to update task"
        except Exception as e:
            return False, f"Failed to update task: {str(e)}"
    
    def delete_task(self, task_id: str, user_id: str) -> Tuple[bool, str]:
        """Delete a task"""
        # Validate task exists and belongs to user
        task = self.task_repository.get_task_by_id(task_id, user_id)
        if not task:
            return False, "Task not found or unauthorized"
        
        try:
            success = self.task_repository.delete_task(task_id, user_id)
            if success:
                return True, "Task deleted successfully"
            else:
                return False, "Failed to delete task"
        except Exception as e:
            return False, f"Failed to delete task: {str(e)}"
    
    def create_subtask(self, task_id: str, user_id: str, subtask_data: Dict[str, Any]) -> Tuple[Optional[Subtask], str]:
        """Create a new subtask"""
        # Validate task exists and belongs to user
        task = self.task_repository.get_task_by_id(task_id, user_id)
        if not task:
            return None, "Task not found or unauthorized"
        
        # Validate required fields
        if not subtask_data.get('title'):
            return None, "Subtask title is required"
        
        if len(subtask_data['title']) > Config.MAX_TITLE_LENGTH:
            return None, f"Title must be less than {Config.MAX_TITLE_LENGTH} characters"
        
        # Create subtask object
        subtask = Subtask(
            id=None,
            task_id=task_id,
            title=subtask_data['title'],
            completed=subtask_data.get('completed', False)
        )
        
        try:
            created_subtask = self.subtask_repository.create_subtask(subtask)
            return created_subtask, "Subtask created successfully"
        except Exception as e:
            return None, f"Failed to create subtask: {str(e)}"
    
    def get_subtasks(self, task_id: str, user_id: str) -> Tuple[List[Subtask], str]:
        """Get subtasks for a task"""
        # Validate task exists and belongs to user
        task = self.task_repository.get_task_by_id(task_id, user_id)
        if not task:
            return [], "Task not found or unauthorized"
        
        subtasks = self.subtask_repository.get_subtasks_by_task(task_id)
        return subtasks, "Subtasks retrieved successfully"
    
    def update_subtask(self, subtask_id: str, task_id: str, user_id: str, updates: Dict[str, Any]) -> Tuple[bool, str]:
        """Update a subtask"""
        # Validate task exists and belongs to user
        task = self.task_repository.get_task_by_id(task_id, user_id)
        if not task:
            return False, "Task not found or unauthorized"
        
        # Validate title length if being updated
        if 'title' in updates and updates['title']:
            if len(updates['title']) > Config.MAX_TITLE_LENGTH:
                return False, f"Title must be less than {Config.MAX_TITLE_LENGTH} characters"
        
        try:
            success = self.subtask_repository.update_subtask(subtask_id, task_id, updates)
            if success:
                return True, "Subtask updated successfully"
            else:
                return False, "Failed to update subtask"
        except Exception as e:
            return False, f"Failed to update subtask: {str(e)}"
    
    def delete_subtask(self, subtask_id: str, task_id: str, user_id: str) -> Tuple[bool, str]:
        """Delete a subtask"""
        # Validate task exists and belongs to user
        task = self.task_repository.get_task_by_id(task_id, user_id)
        if not task:
            return False, "Task not found or unauthorized"
        
        try:
            success = self.subtask_repository.delete_subtask(subtask_id, task_id)
            if success:
                return True, "Subtask deleted successfully"
            else:
                return False, "Failed to delete subtask"
        except Exception as e:
            return False, f"Failed to delete subtask: {str(e)}"
    
    def get_notifications(self, user_id: str) -> Dict[str, List[Task]]:
        """Get notification data for user"""
        overdue_tasks = self.task_repository.get_overdue_tasks(user_id)
        due_in_1_hour = self.task_repository.get_tasks_due_soon(user_id, hours=1)
        due_in_1_day = self.task_repository.get_tasks_due_soon(user_id, hours=24)
        
        return {
            'overdue': overdue_tasks,
            'due_in_1_hour': due_in_1_hour,
            'due_in_1_day': due_in_1_day
        }
    
    def _validate_due_date(self, due_date_str: str) -> Tuple[bool, str]:
        """Validate due date format and ensure it's not in the past"""
        try:
            due_date = datetime.strptime(due_date_str, Config.DATE_FORMAT)
            if due_date < datetime.now():
                return False, "Cannot set due dates in the past"
            return True, "Valid due date"
        except ValueError:
            return False, f"Invalid due date format. Use {Config.DATE_FORMAT}" 