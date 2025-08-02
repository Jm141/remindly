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
            current_user_id = get_jwt_identity()
            data = request.get_json()
            
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            task_id = data.get('task_id')
            username = data.get('username')
            permission_level = data.get('permission_level', 'view')
            
            if not task_id or not username:
                return jsonify({'error': 'Task ID and username are required'}), 400
            
            success, message = self.task_share_service.share_task(
                task_id, current_user_id, username, permission_level
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
            current_user_id = get_jwt_identity()
            shared_tasks = self.task_share_service.get_shared_tasks(current_user_id)
            
            return jsonify({
                'shared_tasks': [task.to_dict() for task in shared_tasks]
            }), 200
                
        except Exception as e:
            return jsonify({'error': f'Failed to get shared tasks: {str(e)}'}), 500
    
    @jwt_required()
    def get_task_shares(self, task_id):
        """Get all shares for a specific task (owner only)"""
        try:
            current_user_id = get_jwt_identity()
            shares = self.task_share_service.get_task_shares(task_id, current_user_id)
            
            return jsonify({'shares': shares}), 200
                
        except Exception as e:
            return jsonify({'error': f'Failed to get task shares: {str(e)}'}), 500
    
    @jwt_required()
    def update_share_permission(self, task_id):
        """Update permission level for a shared task"""
        try:
            current_user_id = get_jwt_identity()
            data = request.get_json()
            
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            username = data.get('username')
            permission_level = data.get('permission_level')
            
            if not username or not permission_level:
                return jsonify({'error': 'Username and permission level are required'}), 400
            
            success, message = self.task_share_service.update_share_permission(
                task_id, current_user_id, username, permission_level
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
            current_user_id = get_jwt_identity()
            data = request.get_json()
            
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            username = data.get('username')
            
            if not username:
                return jsonify({'error': 'Username is required'}), 400
            
            success, message = self.task_share_service.remove_share(
                task_id, current_user_id, username
            )
            
            if success:
                return jsonify({'success': True, 'message': message}), 200
            else:
                return jsonify({'error': message}), 400
                
        except Exception as e:
            return jsonify({'error': f'Failed to remove share: {str(e)}'}), 500 