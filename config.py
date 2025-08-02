import os
from datetime import timedelta

class Config:
    """Configuration class following Single Responsibility Principle"""
    
    # Database Configuration
    DATABASE_PATH = 'database/task_manager.db'
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your_jwt_secret_key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret_key')
    
    # CORS Configuration
    CORS_ORIGINS = ["*"]
    CORS_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
    CORS_HEADERS = ["Content-Type", "Authorization", "Access-Control-Allow-Origin"]
    
    # API Configuration
    API_PREFIX = '/api'
    
    # Validation Configuration
    DATE_FORMAT = '%Y-%m-%d %H:%M'
    MIN_PASSWORD_LENGTH = 6
    MAX_TITLE_LENGTH = 255
    MAX_DESCRIPTION_LENGTH = 1000 