from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from services.task_share_service import TaskShareService

class TaskShareController:
    """Task sharing controller following Single Responsibility Principle"""
    
    def __init__(self, task_share_service: TaskShareService):
        self.task_share_service = task_share_service
    
    @jwt_required()
    def share_task(self):
        """Share a task with another user"""
        try:
            current_username = get_jwt_identity()
            data = request.get_json()
            
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            task_id = data.get('task_id')
            recipient_identifier = data.get('recipient_identifier')  # Can be username or user_code
            permission_level = data.get('permission_level', 'view')
            
            # Debug logging
            print(f"🔍 TaskShareController.share_task: Received data:")
            print(f"  - task_id: {task_id} (type: {type(task_id)})")
            print(f"  - recipient_identifier: {recipient_identifier} (type: {type(recipient_identifier)})")
            print(f"  - permission_level: {permission_level} (type: {type(permission_level)})")
            print(f"  - current_username: {current_username} (type: {type(current_username)})")
            
            if not task_id or not recipient_identifier:
                return jsonify({'error': 'Task ID and recipient identifier (username or user code) are required'}), 400
            
            success, message = self.task_share_service.share_task(
                task_id, current_username, recipient_identifier, permission_level
            )
            
            if success:
                return jsonify({'success': True, 'message': message}), 200
            else:
                return jsonify({'error': message}), 400
                
        except Exception as e:
            return jsonify({'error': f'Failed to share task: {str(e)}'}), 500
    
    @jwt_required()
    def get_shared_tasks(self):
        """Get all tasks shared with current user"""
        try:
            current_username = get_jwt_identity()
            
            # Get user by username to get their user_id
            user = self.task_share_service.user_repo.get_user_by_username(current_username)
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            shared_tasks = self.task_share_service.get_shared_tasks(str(user.id))
            
            return jsonify({
                'shared_tasks': [task.to_dict() for task in shared_tasks]
            }), 200
                
        except Exception as e:
            return jsonify({'error': f'Failed to get shared tasks: {str(e)}'}), 500
    
    @jwt_required()
    def get_task_shares(self, task_id):
        """Get all shares for a specific task (owner only)"""
        try:
            current_username = get_jwt_identity()
            shares = self.task_share_service.get_task_shares(task_id, current_username)
            
            return jsonify({'shares': shares}), 200
                
        except Exception as e:
            return jsonify({'error': f'Failed to get task shares: {str(e)}'}), 500
    
    @jwt_required()
    def update_share_permission(self, task_id):
        """Update permission level for a shared task"""
        try:
            current_username = get_jwt_identity()
            data = request.get_json()
            
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            user_code = data.get('user_code')
            permission_level = data.get('permission_level')
            
            if not user_code or not permission_level:
                return jsonify({'error': 'User code and permission level are required'}), 400
            
            success, message = self.task_share_service.update_share_permission(
                task_id, current_username, user_code, permission_level
            )
            
            if success:
                return jsonify({'success': True, 'message': message}), 200
            else:
                return jsonify({'error': message}), 400
                
        except Exception as e:
            return jsonify({'error': f'Failed to update permission: {str(e)}'}), 500
    
    @jwt_required()
    def remove_share(self, task_id):
        """Remove a task share"""
        try:
            current_username = get_jwt_identity()
            data = request.get_json()
            
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            user_code = data.get('user_code')
            
            if not user_code:
                return jsonify({'error': 'User code is required'}), 400
            
            success, message = self.task_share_service.remove_share(
                task_id, current_username, user_code
            )
            
            if success:
                return jsonify({'success': True, 'message': message}), 200
            else:
                return jsonify({'error': message}), 400
                
        except Exception as e:
            return jsonify({'error': f'Failed to remove share: {str(e)}'}), 500 