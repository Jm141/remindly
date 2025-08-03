import random
import string
import sqlite3
from typing import Optional

class UserCodeGenerator:
    """Generate unique user codes for identification"""
    
    @staticmethod
    def generate_user_code(length: int = 8) -> str:
        """Generate a random alphanumeric user code"""
        # Use uppercase letters and numbers, excluding similar characters
        characters = string.ascii_uppercase + string.digits
        # Exclude similar characters (0, O, 1, I, L)
        characters = characters.replace('0', '').replace('O', '').replace('1', '').replace('I', '').replace('L', '')
        
        return ''.join(random.choice(characters) for _ in range(length))
    
    @staticmethod
    def generate_unique_user_code(database_path: str, length: int = 8) -> str:
        """Generate a unique user code that doesn't exist in the database"""
        max_attempts = 100  # Prevent infinite loops
        
        for attempt in range(max_attempts):
            user_code = UserCodeGenerator.generate_user_code(length)
            
            # Check if code already exists
            try:
                conn = sqlite3.connect(database_path)
                cursor = conn.cursor()
                cursor.execute('SELECT COUNT(*) FROM users WHERE user_code = ?', (user_code,))
                count = cursor.fetchone()[0]
                conn.close()
                
                if count == 0:
                    return user_code
                    
            except Exception as e:
                print(f"Error checking user code uniqueness: {e}")
                # If there's an error, just return the generated code
                return user_code
        
        # If we can't find a unique code after max attempts, add a random suffix
        base_code = UserCodeGenerator.generate_user_code(length - 2)
        suffix = ''.join(random.choice(string.digits) for _ in range(2))
        return base_code + suffix
    
    @staticmethod
    def is_valid_user_code(user_code: str) -> bool:
        """Validate user code format"""
        if not user_code or len(user_code) != 8:
            return False
        
        # Check if it only contains valid characters
        valid_chars = string.ascii_uppercase + string.digits
        valid_chars = valid_chars.replace('0', '').replace('O', '').replace('1', '').replace('I', '').replace('L', '')
        
        return all(char in valid_chars for char in user_code) 