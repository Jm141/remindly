#!/usr/bin/env python3
"""
Simple test script to verify the shared tasks fix works correctly
"""

import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_shared_tasks_fix():
    """Test that shared tasks are retrieved correctly"""
    try:
        print("Testing shared tasks fix...")
        
        # Import after setting up the path
        from dependency_injection import DependencyContainer
        
        # Initialize dependency container
        container = DependencyContainer()
        
        # Get services
        task_share_service = container.get_task_share_service()
        print("TaskShareService initialized successfully")
        
        # Test with user ID 2 (as mentioned in the user query)
        user_id = "2"
        print(f"Testing get_shared_tasks for user_id: {user_id}")
        
        # Get shared tasks
        shared_tasks = task_share_service.get_shared_tasks(user_id)
        print(f"Retrieved {len(shared_tasks)} shared tasks for user {user_id}")
        
        # Print details of each shared task
        for i, task in enumerate(shared_tasks, 1):
            print(f"  {i}. Task ID: {task.id}, Title: '{task.title}', Owner: {task.user_id}")
        
        # Test permission checking methods
        if shared_tasks:
            test_task_id = str(shared_tasks[0].id)
            print(f"Testing permission methods for task {test_task_id}")
            
            can_access = task_share_service.can_user_access_task(test_task_id, user_id)
            can_edit = task_share_service.can_user_edit_task(test_task_id, user_id)
            
            print(f"  - Can access: {can_access}")
            print(f"  - Can edit: {can_edit}")
        
        # Cleanup
        container.cleanup()
        print("Test completed successfully!")
        
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_shared_tasks_fix() 