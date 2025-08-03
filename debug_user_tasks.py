#!/usr/bin/env python3
"""
Debug script to check user task retrieval
"""

import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def debug_user_tasks():
    """Debug user task retrieval"""
    try:
        print("Debugging user task retrieval...")
        
        # Import after setting up the path
        from dependency_injection import DependencyContainer
        
        # Initialize dependency container
        container = DependencyContainer()
        
        # Get services
        task_service = container.get_task_service()
        user_repo = container.get_user_repository()
        
        # Test with the actual usernames
        test_usernames = ['caps123', 'jm1234']
        
        for username in test_usernames:
            print(f"\n--- Testing username: {username} ---")
            
            # Get user by username
            user = user_repo.get_user_by_username(username)
            if user:
                print(f"User found: ID={user.id}, Username={user.username}, UserCode={user.user_code}")
                
                # Get tasks for this user
                tasks = task_service.get_user_tasks(str(user.id), None)
                print(f"Retrieved {len(tasks)} tasks for user {user.id}")
                
                for task in tasks:
                    print(f"  Task {task.id}: '{task.title}' (Owner: {task.user_id})")
            else:
                print(f"User '{username}' not found")
        
        # Cleanup
        container.cleanup()
        
    except Exception as e:
        print(f"Debug failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_user_tasks() 