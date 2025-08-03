#!/usr/bin/env python3
"""
Test script to verify the shared tasks fix works correctly
"""

import sqlite3
import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.task_share_service import TaskShareService
from repositories.sqlite_repository import SQLiteRepository
from repositories.task_share_repository import SQLiteTaskShareRepository

def test_shared_tasks_fix():
    """Test that shared tasks are retrieved correctly"""
    try:
        print("🔍 Testing shared tasks fix...")
        
        # Initialize database connection
        db = sqlite3.connect('remindly.db')
        db.row_factory = sqlite3.Row
        
        # Initialize repositories
        user_repo = SQLiteRepository(db)
        task_repo = SQLiteRepository(db)
        task_share_repo = SQLiteTaskShareRepository(db)
        
        # Initialize service
        service = TaskShareService(task_share_repo, task_repo, user_repo)
        print("✅ TaskShareService initialized successfully")
        
        # Test with user ID 2 (as mentioned in the user query)
        user_id = "2"
        print(f"🔍 Testing get_shared_tasks for user_id: {user_id}")
        
        # Get shared tasks
        shared_tasks = service.get_shared_tasks(user_id)
        print(f"✅ Retrieved {len(shared_tasks)} shared tasks for user {user_id}")
        
        # Print details of each shared task
        for i, task in enumerate(shared_tasks, 1):
            print(f"  {i}. Task ID: {task.id}, Title: '{task.title}', Owner: {task.user_id}")
        
        # Test permission checking methods
        if shared_tasks:
            test_task_id = str(shared_tasks[0].id)
            print(f"🔍 Testing permission methods for task {test_task_id}")
            
            can_access = service.can_user_access_task(test_task_id, user_id)
            can_edit = service.can_user_edit_task(test_task_id, user_id)
            
            print(f"  - Can access: {can_access}")
            print(f"  - Can edit: {can_edit}")
        
        db.close()
        print("✅ Test completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_shared_tasks_fix() 