import uuid
from typing import Optional

class UniqueIDGenerator:
    """Utility class for generating unique identifiers"""
    
    @staticmethod
    def generate_uuid() -> str:
        """Generate a unique UUID string"""
        return str(uuid.uuid4())
    
    @staticmethod
    def generate_short_uuid() -> str:
        """Generate a shorter unique ID (first 8 characters of UUID)"""
        return str(uuid.uuid4())[:8]
    
    @staticmethod
    def generate_numeric_uuid() -> str:
        """Generate a numeric-only unique ID"""
        return str(uuid.uuid4().int)[:12]  # First 12 digits
    
    @staticmethod
    def generate_readable_uuid() -> str:
        """Generate a more readable unique ID with prefix"""
        import time
        timestamp = int(time.time())
        random_part = str(uuid.uuid4())[:8]
        return f"{timestamp}{random_part}"
    
    @staticmethod
    def generate_id_with_prefix(prefix: str) -> str:
        """Generate a unique ID with a custom prefix"""
        random_part = str(uuid.uuid4())[:8]
        return f"{prefix}_{random_part}"
    
    @staticmethod
    def generate_user_id() -> str:
        """Generate a unique user ID"""
        return UniqueIDGenerator.generate_id_with_prefix("user")
    
    @staticmethod
    def generate_task_id() -> str:
        """Generate a unique task ID"""
        return UniqueIDGenerator.generate_id_with_prefix("task")
    
    @staticmethod
    def generate_subtask_id() -> str:
        """Generate a unique subtask ID"""
        return UniqueIDGenerator.generate_id_with_prefix("subtask")
    
    @staticmethod
    def generate_share_id() -> str:
        """Generate a unique task share ID"""
        return UniqueIDGenerator.generate_id_with_prefix("share")

# Convenience functions
def generate_uuid() -> str:
    """Generate a unique UUID string"""
    return UniqueIDGenerator.generate_uuid()

def generate_user_id() -> str:
    """Generate a unique user ID"""
    return UniqueIDGenerator.generate_user_id()

def generate_task_id() -> str:
    """Generate a unique task ID"""
    return UniqueIDGenerator.generate_task_id()

def generate_subtask_id() -> str:
    """Generate a unique subtask ID"""
    return UniqueIDGenerator.generate_subtask_id()

def generate_share_id() -> str:
    """Generate a unique task share ID"""
    return UniqueIDGenerator.generate_share_id() 