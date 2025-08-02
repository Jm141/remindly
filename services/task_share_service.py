from typing import List, Optional, Tuple
from models.task_share import TaskShare
from models.task import Task
from repositories.task_share_repository import TaskShareRepositoryInterface
from repositories.task_repository import TaskRepositoryInterface
from repositories.user_repository import UserRepositoryInterface

class TaskShareService:
    """Task sharing service following Single Responsibility Principle"""
    
    def __init__(self, 
                 task_share_repo: TaskShareRepositoryInterface,
                 task_repo: TaskRepositoryInterface,
                 user_repo: UserRepositoryInterface):
        self.task_share_repo = task_share_repo
        self.task_repo = task_repo
        self.user_repo = user_repo
    
    def share_task(self, task_id: int, owner_id: int, username: str, permission_level: str = "view") -> Tuple[bool, str]:
        """Share a task with another user by username"""
        try:
            # Validate permission level
            if permission_level not in ["view", "edit", "admin"]:
                return False, "Invalid permission level. Must be 'view', 'edit', or 'admin'"
            
            # Check if task exists and belongs to owner
            task = self.task_repo.get_task_by_id_only(task_id)
            if not task:
                return False, "Task not found"
            
            if task.user_id != owner_id:
                return False, "You can only share tasks you own"
            
            # Find user by username
            shared_user = self.user_repo.get_user_by_username(username)
            if not shared_user:
                return False, f"User '{username}' not found"
            
            if shared_user.id == owner_id:
                return False, "Cannot share task with yourself"
            
            # Check if already shared
            existing_share = self.task_share_repo.get_share_permission(task_id, shared_user.id)
            if existing_share:
                return False, f"Task is already shared with '{username}'"
            
            # Create share
            task_share = TaskShare(
                id=None,
                task_id=task_id,
                owner_id=owner_id,
                shared_with_id=shared_user.id,
                permission_level=permission_level
            )
            
            self.task_share_repo.create_share(task_share)
            return True, f"Task shared successfully with '{username}'"
            
        except Exception as e:
            return False, f"Failed to share task: {str(e)}"
    
    def get_shared_tasks(self, user_id: int) -> List[Task]:
        """Get all tasks shared with a user"""
        try:
            shared_task_ids = self.task_share_repo.get_shared_tasks_for_user(user_id)
            shared_tasks = []
            
            for task_id in shared_task_ids:
                task = self.task_repo.get_task_by_id(task_id)
                if task:
                    shared_tasks.append(task)
            
            return shared_tasks
            
        except Exception as e:
            print(f"Error getting shared tasks: {e}")
            return []
    
    def get_task_shares(self, task_id: int, owner_id: int) -> List[dict]:
        """Get all shares for a specific task (owner only)"""
        try:
            # Verify ownership
            task = self.task_repo.get_task_by_id_only(task_id)
            if not task or task.user_id != owner_id:
                return []
            
            shares = self.task_share_repo.get_shares_by_task(task_id)
            share_details = []
            
            for share in shares:
                shared_user = self.user_repo.get_user_by_id(share.shared_with_id)
                if shared_user:
                    share_details.append({
                        'share_id': share.id,
                        'username': shared_user.username,
                        'permission_level': share.permission_level,
                        'created_at': share.created_at
                    })
            
            return share_details
            
        except Exception as e:
            print(f"Error getting task shares: {e}")
            return []
    
    def update_share_permission(self, task_id: int, owner_id: int, username: str, permission_level: str) -> Tuple[bool, str]:
        """Update permission level for a shared task"""
        try:
            # Validate permission level
            if permission_level not in ["view", "edit", "admin"]:
                return False, "Invalid permission level"
            
            # Verify ownership
            task = self.task_repo.get_task_by_id_only(task_id)
            if not task or task.user_id != owner_id:
                return False, "Task not found or you don't own it"
            
            # Find user
            shared_user = self.user_repo.get_user_by_username(username)
            if not shared_user:
                return False, f"User '{username}' not found"
            
            # Check if share exists
            existing_permission = self.task_share_repo.get_share_permission(task_id, shared_user.id)
            if not existing_permission:
                return False, f"Task is not shared with '{username}'"
            
            # Update permission
            self.task_share_repo.update_share_permission(task_id, shared_user.id, permission_level)
            return True, f"Permission updated for '{username}'"
            
        except Exception as e:
            return False, f"Failed to update permission: {str(e)}"
    
    def remove_share(self, task_id: int, owner_id: int, username: str) -> Tuple[bool, str]:
        """Remove a task share"""
        try:
            # Verify ownership
            task = self.task_repo.get_task_by_id_only(task_id)
            if not task or task.user_id != owner_id:
                return False, "Task not found or you don't own it"
            
            # Find user
            shared_user = self.user_repo.get_user_by_username(username)
            if not shared_user:
                return False, f"User '{username}' not found"
            
            # Remove share
            self.task_share_repo.delete_share(task_id, shared_user.id)
            return True, f"Share removed for '{username}'"
            
        except Exception as e:
            return False, f"Failed to remove share: {str(e)}"
    
    def can_user_access_task(self, task_id: int, user_id: int) -> bool:
        """Check if user can access a task (owner or shared)"""
        try:
            # Check if user owns the task
            task = self.task_repo.get_task_by_id_only(task_id)
            if task and task.user_id == user_id:
                return True
            
            # Check if task is shared with user
            permission = self.task_share_repo.get_share_permission(task_id, user_id)
            return permission is not None
            
        except Exception as e:
            print(f"Error checking task access: {e}")
            return False
    
    def can_user_edit_task(self, task_id: int, user_id: int) -> bool:
        """Check if user can edit a task"""
        try:
            # Check if user owns the task
            task = self.task_repo.get_task_by_id_only(task_id)
            if task and task.user_id == user_id:
                return True
            
            # Check if user has edit permissions
            permission = self.task_share_repo.get_share_permission(task_id, user_id)
            return permission in ["edit", "admin"]
            
        except Exception as e:
            print(f"Error checking edit permission: {e}")
            return False 