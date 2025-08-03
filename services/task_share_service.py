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
    
    def share_task(self, task_id: str, owner_username: str, recipient_identifier: str, permission_level: str = "view") -> Tuple[bool, str]:
        """Share a task with another user by username or user_code"""
        try:
            print(f"🔍 TaskShareService.share_task: Starting with:")
            print(f"  - task_id: {task_id} (type: {type(task_id)})")
            print(f"  - owner_username: {owner_username} (type: {type(owner_username)})")
            print(f"  - recipient_identifier: {recipient_identifier} (type: {type(recipient_identifier)})")
            print(f"  - permission_level: {permission_level} (type: {type(permission_level)})")
            
            # Validate permission level
            if permission_level not in ["view", "edit", "admin"]:
                return False, "Invalid permission level. Must be 'view', 'edit', or 'admin'"
            
            # Check if task exists and belongs to owner
            print(f"🔍 TaskShareService.share_task: Converting task_id to int: {task_id}")
            task = self.task_repo.get_task_by_id_only(int(task_id))
            if not task:
                return False, "Task not found"
            
            # Get owner by username to get their user_code
            owner_user = self.user_repo.get_user_by_username(owner_username)
            if not owner_user:
                return False, "Owner user not found"
            
            # Verify ownership
            if task.user_id != owner_user.id:
                return False, "You can only share tasks you own"
            
            # Find recipient by username or user_code
            recipient_user = None
            if len(recipient_identifier) == 8 and self._is_valid_user_code(recipient_identifier):
                # Try as user_code first
                print(f"🔍 TaskShareService.share_task: Looking up recipient by user_code: {recipient_identifier}")
                recipient_user = self.user_repo.get_user_by_user_code(recipient_identifier.upper())
            
            if not recipient_user:
                # Try as username
                print(f"🔍 TaskShareService.share_task: Looking up recipient by username: {recipient_identifier}")
                recipient_user = self.user_repo.get_user_by_username(recipient_identifier)
            
            if not recipient_user:
                return False, f"User '{recipient_identifier}' not found. Please check the username or user code."
            
            if recipient_user.user_code == owner_user.user_code:
                return False, "Cannot share task with yourself"
            
            # Check if already shared
            existing_share = self.task_share_repo.get_share_permission(int(task_id), recipient_user.user_code)
            if existing_share:
                return False, f"Task is already shared with '{recipient_user.username}' ({recipient_user.user_code})"
            
            # Create share using user codes
            task_share = TaskShare(
                id=None,
                task_id=int(task_id),
                owner_code=owner_user.user_code,
                shared_with_code=recipient_user.user_code,
                permission_level=permission_level
            )
            
            self.task_share_repo.create_share(task_share)
            return True, f"Task shared successfully with '{recipient_user.username}' ({recipient_user.user_code})"
            
        except ValueError as e:
            print(f"❌ TaskShareService.share_task: ValueError: {e}")
            return False, f"Invalid task ID or user ID format: {str(e)}"
        except Exception as e:
            print(f"❌ TaskShareService.share_task: Exception: {e}")
            return False, f"Failed to share task: {str(e)}"
    
    def _is_valid_user_code(self, user_code: str) -> bool:
        """Check if string looks like a valid user code"""
        import string
        if not user_code or len(user_code) != 8:
            return False
        
        # Check if it only contains valid characters (uppercase letters and numbers, excluding similar ones)
        valid_chars = string.ascii_uppercase + string.digits
        valid_chars = valid_chars.replace('0', '').replace('O', '').replace('1', '').replace('I', '').replace('L', '')
        
        return all(char in valid_chars for char in user_code.upper())
    
    def get_shared_tasks(self, user_id: str) -> List[Task]:
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
    
    def get_task_shares(self, task_id: str, owner_username: str) -> List[dict]:
        """Get all shares for a specific task (owner only)"""
        try:
            print(f"🔍 TaskShareService.get_task_shares: Starting with:")
            print(f"  - task_id: {task_id} (type: {type(task_id)})")
            print(f"  - owner_username: {owner_username} (type: {type(owner_username)})")
            
            # Get owner by username to get their user_code
            owner_user = self.user_repo.get_user_by_username(owner_username)
            if not owner_user:
                return []
            
            # Verify ownership
            print(f"🔍 TaskShareService.get_task_shares: Converting task_id to int: {task_id}")
            task = self.task_repo.get_task_by_id_only(int(task_id))
            if not task or task.user_id != owner_user.id:
                return []
            
            shares = self.task_share_repo.get_shares_by_task(int(task_id))
            share_details = []
            
            for share in shares:
                # Get user details by user_code
                shared_user = self.user_repo.get_user_by_user_code(share.shared_with_code)
                if shared_user:
                    share_details.append({
                        'share_id': share.id,
                        'username': shared_user.username,
                        'user_code': shared_user.user_code,
                        'permission_level': share.permission_level,
                        'created_at': share.created_at
                    })
            
            return share_details
            
        except ValueError as e:
            print(f"❌ TaskShareService.get_task_shares: ValueError: {e}")
            print(f"Invalid task ID or user ID format: {e}")
            return []
        except Exception as e:
            print(f"❌ TaskShareService.get_task_shares: Exception: {e}")
            print(f"Error getting task shares: {e}")
            return []
    
    def update_share_permission(self, task_id: str, owner_username: str, user_code: str, permission_level: str) -> Tuple[bool, str]:
        """Update permission level for a shared task"""
        try:
            # Validate permission level
            if permission_level not in ["view", "edit", "admin"]:
                return False, "Invalid permission level"
            
            # Get owner by username
            owner_user = self.user_repo.get_user_by_username(owner_username)
            if not owner_user:
                return False, "Owner user not found"
            
            # Verify ownership
            task = self.task_repo.get_task_by_id_only(int(task_id))
            if not task or task.user_id != owner_user.id:
                return False, "Task not found or you don't own it"
            
            # Check if share exists
            existing_permission = self.task_share_repo.get_share_permission(int(task_id), user_code)
            if not existing_permission:
                return False, f"Task is not shared with user code '{user_code}'"
            
            # Get user details for better error messages
            shared_user = self.user_repo.get_user_by_user_code(user_code)
            username = shared_user.username if shared_user else user_code
            
            # Update permission
            self.task_share_repo.update_share_permission(int(task_id), user_code, permission_level)
            return True, f"Permission updated for '{username}' ({user_code})"
            
        except ValueError as e:
            return False, f"Invalid task ID or user ID format: {str(e)}"
        except Exception as e:
            return False, f"Failed to update permission: {str(e)}"
    
    def remove_share(self, task_id: str, owner_username: str, user_code: str) -> Tuple[bool, str]:
        """Remove a task share"""
        try:
            # Get owner by username
            owner_user = self.user_repo.get_user_by_username(owner_username)
            if not owner_user:
                return False, "Owner user not found"
            
            # Verify ownership
            task = self.task_repo.get_task_by_id_only(int(task_id))
            if not task or task.user_id != owner_user.id:
                return False, "Task not found or you don't own it"
            
            # Get user details for better error messages
            shared_user = self.user_repo.get_user_by_user_code(user_code)
            if not shared_user:
                return False, f"User with code '{user_code}' not found"
            
            # Remove share
            self.task_share_repo.delete_share(int(task_id), user_code)
            return True, f"Share removed for '{shared_user.username}' ({user_code})"
            
        except ValueError as e:
            return False, f"Invalid task ID or user ID format: {str(e)}"
        except Exception as e:
            return False, f"Failed to remove share: {str(e)}"
    
    def can_user_access_task(self, task_id: str, user_id: str) -> bool:
        """Check if user can access a task (owner or shared)"""
        try:
            # Check if user owns the task
            task = self.task_repo.get_task_by_id_only(int(task_id))
            user_id_int = int(user_id)
            if task and task.user_id == user_id_int:
                return True
            
            # Check if task is shared with user
            permission = self.task_share_repo.get_share_permission(int(task_id), user_id_int)
            return permission is not None
            
        except ValueError as e:
            print(f"Invalid task ID or user ID format: {e}")
            return False
        except Exception as e:
            print(f"Error checking task access: {e}")
            return False
    
    def can_user_edit_task(self, task_id: str, user_id: str) -> bool:
        """Check if user can edit a task"""
        try:
            # Check if user owns the task
            task = self.task_repo.get_task_by_id_only(int(task_id))
            user_id_int = int(user_id)
            if task and task.user_id == user_id_int:
                return True
            
            # Check if user has edit permissions
            permission = self.task_share_repo.get_share_permission(int(task_id), user_id_int)
            return permission in ["edit", "admin"]
            
        except ValueError as e:
            print(f"Invalid task ID or user ID format: {e}")
            return False
        except Exception as e:
            print(f"Error checking edit permission: {e}")
            return False 