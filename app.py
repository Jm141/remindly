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

# Production configuration
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)

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

@app.route(f'{Config.API_PREFIX}/tasks/<int:task_id>', methods=['PUT', 'PATCH', 'DELETE'])
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
@app.route(f'{Config.API_PREFIX}/tasks/<int:task_id>/subtasks', methods=['GET', 'POST'])
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

@app.route(f'{Config.API_PREFIX}/tasks/<int:task_id>/subtasks/<int:subtask_id>', methods=['PUT', 'PATCH', 'DELETE'])
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
    """Get due notifications for current user"""
    try:
        task_controller = container.get_task_controller(bcrypt)
        return task_controller.get_notifications()
    except Exception as e:
        app.logger.error(f"Notifications error: {str(e)}")
        return jsonify({'error': f'Failed to get notifications: {str(e)}'}), 500

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
        
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        print(f"❌ Failed to start application: {str(e)}")
        print("Stack trace:")
        traceback.print_exc() 