from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import atexit
from config import Config
from dependency_injection import container
from datetime import datetime
import traceback
import os

# Initialize Flask app
app = Flask(__name__)

# Configure Flask
app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = Config.JWT_ACCESS_TOKEN_EXPIRES
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = Config.JWT_REFRESH_TOKEN_EXPIRES
app.secret_key = Config.SECRET_KEY

# Production configuration - ensure app is ready for deployment
app.config['ENV'] = 'production'
app.config['DEBUG'] = False

# Initialize extensions
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# Configure CORS
CORS(app, resources={
    r"/api/*": {
        "origins": Config.CORS_ORIGINS,
        "methods": Config.CORS_METHODS,
        "allow_headers": Config.CORS_HEADERS
    }
})

# Register cleanup function
atexit.register(container.cleanup)

# --- Routes ---
@app.route('/')
def index():
    """API root endpoint"""
    return jsonify({
        'message': 'Task Manager API is running',
        'status': 'success',
        'version': '2.0.0',
        'architecture': 'SOLID Principles',
        'endpoints': {
            'login': f'{Config.API_PREFIX}/login',
            'register': f'{Config.API_PREFIX}/register',
            'logout': f'{Config.API_PREFIX}/logout',
            'user': f'{Config.API_PREFIX}/user',
            'change_password': f'{Config.API_PREFIX}/change-password',
            'tasks': f'{Config.API_PREFIX}/tasks',
            'notifications': f'{Config.API_PREFIX}/notifications/due',
            'refresh': f'{Config.API_PREFIX}/refresh'
        }
    })

# --- Authentication Routes ---
@app.route(f'{Config.API_PREFIX}/register', methods=['POST'])
def register():
    """User registration endpoint"""
    try:
        auth_controller = container.get_auth_controller(bcrypt)
        return auth_controller.register()
    except Exception as e:
        app.logger.error(f"Registration error: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500

@app.route(f'{Config.API_PREFIX}/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        auth_controller = container.get_auth_controller(bcrypt)
        return auth_controller.login()
    except Exception as e:
        app.logger.error(f"Login error: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Login failed: {str(e)}'}), 500

@app.route(f'{Config.API_PREFIX}/logout', methods=['GET', 'POST'])
@jwt_required()
def logout():
    """User logout endpoint"""
    try:
        auth_controller = container.get_auth_controller(bcrypt)
        return auth_controller.logout()
    except Exception as e:
        app.logger.error(f"Logout error: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Logout failed: {str(e)}'}), 500

@app.route(f'{Config.API_PREFIX}/user', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user information"""
    try:
        auth_controller = container.get_auth_controller(bcrypt)
        return auth_controller.get_current_user()
    except Exception as e:
        app.logger.error(f"Get user error: {str(e)}")
        return jsonify({'error': f'Failed to get user: {str(e)}'}), 500

@app.route(f'{Config.API_PREFIX}/user', methods=['PUT'])
@jwt_required()
def update_current_user():
    """Update current user information"""
    try:
        auth_controller = container.get_auth_controller(bcrypt)
        return auth_controller.update_current_user()
    except Exception as e:
        app.logger.error(f"Update user error: {str(e)}")
        return jsonify({'error': f'Failed to update user: {str(e)}'}), 500

@app.route(f'{Config.API_PREFIX}/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    """Change user password"""
    try:
        auth_controller = container.get_auth_controller(bcrypt)
        return auth_controller.change_password()
    except Exception as e:
        app.logger.error(f"Change password error: {str(e)}")
        return jsonify({'error': f'Failed to change password: {str(e)}'}), 500

@app.route(f'{Config.API_PREFIX}/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token"""
    try:
        from flask_jwt_extended import get_jwt_identity
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return jsonify({'access_token': access_token})
    except Exception as e:
        app.logger.error(f"Refresh error: {str(e)}")
        return jsonify({'error': f'Token refresh failed: {str(e)}'}), 500

# --- Task Routes ---
@app.route(f'{Config.API_PREFIX}/tasks', methods=['GET', 'POST'])
@jwt_required()
def tasks():
    """Tasks endpoint - GET: retrieve tasks, POST: create task"""
    try:
        task_controller = container.get_task_controller(bcrypt)
        
        if request.method == 'GET':
            return task_controller.get_tasks()
        elif request.method == 'POST':
            return task_controller.create_task()
    except Exception as e:
        app.logger.error(f"Tasks error: {str(e)}")
        return jsonify({'error': f'Task operation failed: {str(e)}'}), 500

@app.route(f'{Config.API_PREFIX}/tasks/<string:task_id>', methods=['PUT', 'PATCH', 'DELETE'])
@jwt_required()
def task_operations(task_id):
    """Task operations endpoint - PUT/PATCH: update task, DELETE: delete task"""
    try:
        task_controller = container.get_task_controller(bcrypt)
        
        if request.method in ['PUT', 'PATCH']:
            return task_controller.update_task(task_id)
        elif request.method == 'DELETE':
            return task_controller.delete_task(task_id)
    except Exception as e:
        app.logger.error(f"Task operation error: {str(e)}")
        return jsonify({'error': f'Task operation failed: {str(e)}'}), 500

# --- Subtask Routes ---
@app.route(f'{Config.API_PREFIX}/tasks/<string:task_id>/subtasks', methods=['GET', 'POST'])
@jwt_required()
def subtasks(task_id):
    """Subtasks endpoint - GET: retrieve subtasks, POST: create subtask"""
    try:
        task_controller = container.get_task_controller(bcrypt)
        
        if request.method == 'GET':
            return task_controller.get_subtasks(task_id)
        elif request.method == 'POST':
            return task_controller.create_subtask(task_id)
    except Exception as e:
        app.logger.error(f"Subtask error: {str(e)}")
        return jsonify({'error': f'Subtask operation failed: {str(e)}'}), 500

@app.route(f'{Config.API_PREFIX}/tasks/<string:task_id>/subtasks/<string:subtask_id>', methods=['PUT', 'PATCH', 'DELETE'])
@jwt_required()
def subtask_operations(task_id, subtask_id):
    """Subtask operations endpoint - PUT/PATCH: update subtask, DELETE: delete subtask"""
    try:
        task_controller = container.get_task_controller(bcrypt)
        
        if request.method in ['PUT', 'PATCH']:
            return task_controller.update_subtask(task_id, subtask_id)
        elif request.method == 'DELETE':
            return task_controller.delete_subtask(task_id, subtask_id)
    except Exception as e:
        app.logger.error(f"Subtask operation error: {str(e)}")
        return jsonify({'error': f'Subtask operation failed: {str(e)}'}), 500

# --- Notification Routes ---
@app.route(f'{Config.API_PREFIX}/notifications/due', methods=['GET'])
@jwt_required()
def notifications():
    """Get due notifications endpoint"""
    try:
        task_controller = container.get_task_controller(bcrypt)
        return task_controller.get_notifications()
    except Exception as e:
        app.logger.error(f"Notifications error: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to get notifications: {str(e)}'}), 500

# --- Task Sharing Routes ---
@app.route(f'{Config.API_PREFIX}/tasks/share', methods=['POST'])
@jwt_required()
def share_task():
    """Share a task with another user"""
    try:
        task_share_controller = container.get_task_share_controller(bcrypt)
        return task_share_controller.share_task()
    except Exception as e:
        app.logger.error(f"Share task error: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to share task: {str(e)}'}), 500

@app.route(f'{Config.API_PREFIX}/tasks/shared', methods=['GET'])
@jwt_required()
def get_shared_tasks():
    """Get all tasks shared with current user"""
    try:
        task_share_controller = container.get_task_share_controller(bcrypt)
        return task_share_controller.get_shared_tasks()
    except Exception as e:
        app.logger.error(f"Get shared tasks error: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to get shared tasks: {str(e)}'}), 500

@app.route(f'{Config.API_PREFIX}/tasks/<string:task_id>/shares', methods=['GET'])
@jwt_required()
def get_task_shares(task_id):
    """Get all shares for a specific task (owner only)"""
    try:
        task_share_controller = container.get_task_share_controller(bcrypt)
        return task_share_controller.get_task_shares(task_id)
    except Exception as e:
        app.logger.error(f"Get task shares error: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to get task shares: {str(e)}'}), 500

@app.route(f'{Config.API_PREFIX}/tasks/<string:task_id>/shares/permission', methods=['PUT'])
@jwt_required()
def update_share_permission(task_id):
    """Update permission level for a shared task"""
    try:
        task_share_controller = container.get_task_share_controller(bcrypt)
        return task_share_controller.update_share_permission(task_id)
    except Exception as e:
        app.logger.error(f"Update share permission error: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to update permission: {str(e)}'}), 500

@app.route(f'{Config.API_PREFIX}/tasks/<string:task_id>/shares', methods=['DELETE'])
@jwt_required()
def remove_share(task_id):
    """Remove a task share"""
    try:
        task_share_controller = container.get_task_share_controller(bcrypt)
        return task_share_controller.remove_share(task_id)
    except Exception as e:
        app.logger.error(f"Remove share error: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to remove share: {str(e)}'}), 500

@app.route(f'{Config.API_PREFIX}/users', methods=['GET'])
def get_all_users():
    """Get all users (for testing purposes)"""
    try:
        user_repo = container.get_user_repository()
        database = container.get_database()
        
        # Fetch all users using direct query
        cursor = database.cursor()
        cursor.execute('''
            SELECT id, username
            FROM users
            ORDER BY id DESC
        ''')
        
        users = cursor.fetchall()
        
        # Convert to list of dictionaries
        user_list = []
        for user_data in users:
            user_list.append({
                'id': user_data['id'],
                'username': user_data['username']
            })
        
        return jsonify({
            'users': user_list,
            'count': len(user_list),
            'message': f'Successfully fetched {len(user_list)} users'
        }), 200
        
    except Exception as e:
        app.logger.error(f"Get all users error: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to fetch users: {str(e)}'}), 500

# --- Error Handlers ---
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({'error': 'Method not allowed'}), 405

# --- Health Check ---
@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        database = container.get_database()
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    try:
        # Initialize database tables
        print("🔧 Initializing database and repositories...")
        database = container.get_database()
        user_repo = container.get_user_repository()
        task_repo = container.get_task_repository()
        subtask_repo = container.get_subtask_repository()
        print("✅ Database initialization successful!")
        
        print("🚀 Starting Task Manager API with SOLID Architecture...")
        print("📁 Project Structure:")
        print("   ├── config.py (Configuration)")
        print("   ├── models/ (Data Models)")
        print("   ├── repositories/ (Data Access)")
        print("   ├── services/ (Business Logic)")
        print("   ├── controllers/ (Request Handling)")
        print("   └── dependency_injection.py (DI Container)")
        print("\n✅ SOLID Principles Implemented:")
        print("   ✅ Single Responsibility Principle")
        print("   ✅ Open/Closed Principle")
        print("   ✅ Liskov Substitution Principle")
        print("   ✅ Interface Segregation Principle")
        print("   ✅ Dependency Inversion Principle")
        
        # Use PORT environment variable (provided by Render) or default to 5000 for local development
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=False)
    except Exception as e:
        print(f"❌ Failed to start application: {str(e)}")
        print("Stack trace:")
        traceback.print_exc() 