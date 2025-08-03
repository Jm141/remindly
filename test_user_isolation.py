#!/usr/bin/env python3
"""
Test script to verify user task isolation
"""

import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_user_isolation():
    """Test that users can only see their own tasks"""
    try:
        print("🧪 Testing user task isolation...")
        
        # Import after setting up the path
        from dependency_injection import DependencyContainer
        from models.user import User
        
        # Initialize dependency container
        container = DependencyContainer()
        
        # Get services
        task_service = container.get_task_service()
        user_repo = container.get_user_repository()
        
        print("\n1️⃣ Creating users...")
        
        # Create user 1 (caps123) directly
        user1 = User(
            id=None,
            username="testuser1",
            password_hash="dummy_hash",
            user_code="TEST1234"
        )
        user1 = user_repo.create_user(user1)
        print(f"User 1 created: ID={user1.id}, Username={user1.username}, UserCode={user1.user_code}")
        
        # Create user 2 (jm1234) directly
        user2 = User(
            id=None,
            username="testuser2",
            password_hash="dummy_hash",
            user_code="TEST5678"
        )
        user2 = user_repo.create_user(user2)
        print(f"User 2 created: ID={user2.id}, Username={user2.username}, UserCode={user2.user_code}")
        
        print(f"\n📋 User details:")
        print(f"  User 1: ID={user1.id}, Username={user1.username}, UserCode={user1.user_code}")
        print(f"  User 2: ID={user2.id}, Username={user2.username}, UserCode={user2.user_code}")
        
        print("\n2️⃣ Adding task for user 1...")
        
        # Add a task for user 1
        task_data = {
            'title': 'Test Task for User 1',
            'description': 'This task belongs to user 1 only',
            'category': 'Work',
            'priority': 'High',
            'due_date': '2025-08-10 14:00'
        }
        
        task, message = task_service.create_task(str(user1.id), task_data)
        if task:
            print(f"✅ Task created: ID={task.id}, Title='{task.title}', Owner={task.user_id}")
        else:
            print(f"❌ Failed to create task: {message}")
            return
        
        print("\n3️⃣ Testing task visibility...")
        
        # Test user 1 can see their own task
        print(f"\n🔍 User 1 ({user1.username}) tasks:")
        user1_tasks = task_service.get_user_tasks(str(user1.id), None)
        print(f"  Found {len(user1_tasks)} tasks")
        for task in user1_tasks:
            print(f"    - Task {task.id}: '{task.title}' (Owner: {task.user_id})")
        
        # Test user 2 cannot see user 1's task
        print(f"\n🔍 User 2 ({user2.username}) tasks:")
        user2_tasks = task_service.get_user_tasks(str(user2.id), None)
        print(f"  Found {len(user2_tasks)} tasks")
        for task in user2_tasks:
            print(f"    - Task {task.id}: '{task.title}' (Owner: {task.user_id})")
        
        print("\n4️⃣ Verification...")
        
        # Verify user 1 has exactly 1 task
        if len(user1_tasks) == 1 and user1_tasks[0].user_id == user1.id:
            print("✅ User 1 can see their own task")
        else:
            print("❌ User 1 cannot see their task or sees wrong task")
        
        # Verify user 2 has 0 tasks
        if len(user2_tasks) == 0:
            print("✅ User 2 cannot see user 1's task (correct isolation)")
        else:
            print("❌ User 2 can see user 1's task (security breach!)")
        
        print("\n5️⃣ Testing task access methods...")
        
        # Test get_task_by_id method (should only work for owner)
        task_id = str(task.id)
        
        # User 1 should be able to access their task
        user1_task = task_service.get_task(task_id, str(user1.id))
        if user1_task:
            print("✅ User 1 can access their own task via get_task")
        else:
            print("❌ User 1 cannot access their own task")
        
        # User 2 should NOT be able to access user 1's task
        user2_task = task_service.get_task(task_id, str(user2.id))
        if user2_task is None:
            print("✅ User 2 cannot access user 1's task (correct security)")
        else:
            print("❌ User 2 can access user 1's task (security breach!)")
        
        print("\n🎉 Test completed!")
        
        # Cleanup
        container.cleanup()
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_user_isolation() 