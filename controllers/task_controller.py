from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from services.task_service import TaskService
from services.auth_service import AuthService

class TaskController:
    """Task controller following Single Responsibility Principle"""
    
    def __init__(self, task_service: TaskService, auth_service: AuthService):
        self.task_service = task_service
        self.auth_service = auth_service
    
    def _get_user_id(self) -> int:
        """Get current user ID from JWT token"""
        username = get_jwt_identity()
        user = self.auth_service.get_user_by_username(username)
        return user.id if user else None
    
    def get_tasks(self):
        """Get tasks for current user"""
        try:
            user_id = self._get_user_id()
            if not user_id:
                return jsonify({'error': 'Unauthorized'}), 401
            
            completed_param = request.args.get('completed')
            completed = None
            if completed_param is not None:
                completed = completed_param.lower() == 'true'
            
            tasks = self.task_service.get_user_tasks(user_id, completed)
            return jsonify([task.to_dict() for task in tasks]), 200
            
        except Exception as e:
            return jsonify({'error': f'Failed to get tasks: {str(e)}'}), 500
    
    def create_task(self):
        """Create a new task"""
        try:
            user_id = self._get_user_id()
            if not user_id:
                return jsonify({'error': 'Unauthorized'}), 401
            
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            task, message = self.task_service.create_task(user_id, data)
            
            if task:
                return jsonify({'success': True, 'task': task.to_dict(), 'message': message}), 201
            else:
                return jsonify({'error': message}), 400
                
        except Exception as e:
            return jsonify({'error': f'Failed to create task: {str(e)}'}), 500
    
    def update_task(self, task_id: int):
        """Update a task"""
        try:
            user_id = self._get_user_id()
            if not user_id:
                return jsonify({'error': 'Unauthorized'}), 401
            
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            success, message = self.task_service.update_task(task_id, user_id, data)
            
            if success:
                return jsonify({'success': True, 'message': message}), 200
            else:
                return jsonify({'error': message}), 400
                
        except Exception as e:
            return jsonify({'error': f'Failed to update task: {str(e)}'}), 500
    
    def delete_task(self, task_id: int):
        """Delete a task"""
        try:
            user_id = self._get_user_id()
            if not user_id:
                return jsonify({'error': 'Unauthorized'}), 401
            
            success, message = self.task_service.delete_task(task_id, user_id)
            
            if success:
                return jsonify({'success': True, 'message': message}), 200
            else:
                return jsonify({'error': message}), 400
                
        except Exception as e:
            return jsonify({'error': f'Failed to delete task: {str(e)}'}), 500
    
    def get_subtasks(self, task_id: int):
        """Get subtasks for a task"""
        try:
            user_id = self._get_user_id()
            if not user_id:
                return jsonify({'error': 'Unauthorized'}), 401
            
            subtasks, message = self.task_service.get_subtasks(task_id, user_id)
            
            if subtasks is not None:
                return jsonify([subtask.to_dict() for subtask in subtasks]), 200
            else:
                return jsonify({'error': message}), 400
                
        except Exception as e:
            return jsonify({'error': f'Failed to get subtasks: {str(e)}'}), 500
    
    def create_subtask(self, task_id: int):
        """Create a new subtask"""
        try:
            user_id = self._get_user_id()
            if not user_id:
                return jsonify({'error': 'Unauthorized'}), 401
            
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            subtask, message = self.task_service.create_subtask(task_id, user_id, data)
            
            if subtask:
                return jsonify({'success': True, 'subtask': subtask.to_dict(), 'message': message}), 201
            else:
                return jsonify({'error': message}), 400
                
        except Exception as e:
            return jsonify({'error': f'Failed to create subtask: {str(e)}'}), 500
    
    def update_subtask(self, task_id: int, subtask_id: int):
        """Update a subtask"""
        try:
            user_id = self._get_user_id()
            if not user_id:
                return jsonify({'error': 'Unauthorized'}), 401
            
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            success, message = self.task_service.update_subtask(subtask_id, task_id, user_id, data)
            
            if success:
                return jsonify({'success': True, 'message': message}), 200
            else:
                return jsonify({'error': message}), 400
                
        except Exception as e:
            return jsonify({'error': f'Failed to update subtask: {str(e)}'}), 500
    
    def delete_subtask(self, task_id: int, subtask_id: int):
        """Delete a subtask"""
        try:
            user_id = self._get_user_id()
            if not user_id:
                return jsonify({'error': 'Unauthorized'}), 401
            
            success, message = self.task_service.delete_subtask(subtask_id, task_id, user_id)
            
            if success:
                return jsonify({'success': True, 'message': message}), 200
            else:
                return jsonify({'error': message}), 400
                
        except Exception as e:
            return jsonify({'error': f'Failed to delete subtask: {str(e)}'}), 500
    
    def get_notifications(self):
        """Get notification data for current user"""
        try:
            user_id = self._get_user_id()
            if not user_id:
                return jsonify({'error': 'Unauthorized'}), 401
            
            notifications = self.task_service.get_notifications(user_id)
            
            # Convert tasks to dictionaries
            result = {
                'overdue': [task.to_dict() for task in notifications['overdue']],
                'due_in_1_hour': [task.to_dict() for task in notifications['due_in_1_hour']],
                'due_in_1_day': [task.to_dict() for task in notifications['due_in_1_day']]
            }
            
            return jsonify(result), 200
            
        except Exception as e:
            return jsonify({'error': f'Failed to get notifications: {str(e)}'}), 500 