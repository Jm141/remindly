from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, get_jwt
from services.auth_service import AuthService
from models.user import User

class AuthController:
    """Authentication controller following Single Responsibility Principle"""
    
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service
    
    def register(self):
        """Handle user registration"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            username = data.get('username')
            password = data.get('password')
            email = data.get('email', '')
            first_name = data.get('first_name', '')
            last_name = data.get('last_name', '')
            
            success, message = self.auth_service.register_user(username, password, email, first_name, last_name)
            
            if success:
                return jsonify({'success': True, 'message': message}), 201
            else:
                return jsonify({'error': message}), 400
                
        except Exception as e:
            return jsonify({'error': f'Registration failed: {str(e)}'}), 500
    
    def login(self):
        """Handle user login"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            username = data.get('username')
            password = data.get('password')
            
            user, message = self.auth_service.authenticate_user(username, password)
            
            if user:
                tokens = self.auth_service.create_tokens(user)
                return jsonify(tokens), 200
            else:
                return jsonify({'error': message}), 401
                
        except Exception as e:
            return jsonify({'error': f'Login failed: {str(e)}'}), 500
    
    def logout(self):
        """Handle user logout"""
        try:
            # Get the current JWT token
            jti = get_jwt()["jti"]
            
            # In a production environment, you might want to add the token to a blacklist
            # For now, we'll just return a success message
            # The client should remove the token from storage
            
            return jsonify({
                'success': True, 
                'message': 'Successfully logged out'
            }), 200
            
        except Exception as e:
            return jsonify({'error': f'Logout failed: {str(e)}'}), 500
    
    def get_current_user(self):
        """Get current user information"""
        try:
            username = get_jwt_identity()
            if not username:
                return jsonify({'error': 'No user identity found'}), 401
            
            user = self.auth_service.get_user_by_username(username)
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            return jsonify({'user': user.to_dict()}), 200
            
        except Exception as e:
            return jsonify({'error': f'Failed to get user: {str(e)}'}), 500 

    def update_user(self):
        """Handle user information update"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            username = get_jwt_identity()
            if not username:
                return jsonify({'error': 'No user identity found'}), 401
            
            user = self.auth_service.get_user_by_username(username)
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            email = data.get('email')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            
            success, message = self.auth_service.update_user(
                user.id, email, first_name, last_name
            )
            
            if success:
                updated_user = self.auth_service.get_user_by_id(user.id)
                return jsonify({
                    'success': True, 
                    'message': message,
                    'user': updated_user.to_dict()
                }), 200
            else:
                return jsonify({'error': message}), 400
                
        except Exception as e:
            return jsonify({'error': f'Update failed: {str(e)}'}), 500
    
    def update_password(self):
        """Handle password update"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            username = get_jwt_identity()
            if not username:
                return jsonify({'error': 'No user identity found'}), 401
            
            user = self.auth_service.get_user_by_username(username)
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            current_password = data.get('current_password')
            new_password = data.get('new_password')
            
            if not current_password or not new_password:
                return jsonify({'error': 'Current password and new password are required'}), 400
            
            success, message = self.auth_service.update_password(
                user.id, current_password, new_password
            )
            
            if success:
                return jsonify({'success': True, 'message': message}), 200
            else:
                return jsonify({'error': message}), 400
                
        except Exception as e:
            return jsonify({'error': f'Password update failed: {str(e)}'}), 500
    
    def update_username(self):
        """Handle username update"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            username = get_jwt_identity()
            if not username:
                return jsonify({'error': 'No user identity found'}), 401
            
            user = self.auth_service.get_user_by_username(username)
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            new_username = data.get('new_username')
            if not new_username:
                return jsonify({'error': 'New username is required'}), 400
            
            success, message = self.auth_service.update_username(user.id, new_username)
            
            if success:
                updated_user = self.auth_service.get_user_by_id(user.id)
                return jsonify({
                    'success': True, 
                    'message': message,
                    'user': updated_user.to_dict()
                }), 200
            else:
                return jsonify({'error': message}), 400
                
        except Exception as e:
            return jsonify({'error': f'Username update failed: {str(e)}'}), 500
    
    def get_all_users(self):
        """Get all users (admin function)"""
        try:
            users = self.auth_service.get_all_users()
            return jsonify({
                'users': [user.to_dict() for user in users]
            }), 200
        except Exception as e:
            return jsonify({'error': f'Failed to get users: {str(e)}'}), 500
    
    def delete_user(self, user_id: int):
        """Delete user (admin function)"""
        try:
            success, message = self.auth_service.delete_user(user_id)
            
            if success:
                return jsonify({'success': True, 'message': message}), 200
            else:
                return jsonify({'error': message}), 400
                
        except Exception as e:
            return jsonify({'error': f'Delete failed: {str(e)}'}), 500 