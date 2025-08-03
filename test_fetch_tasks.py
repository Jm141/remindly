#!/usr/bin/env python3
"""
Simple test script to fetch all tasks from the database
This demonstrates the unique ID system and task retrieval functionality
"""

import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dependency_injection import container
from models.task import Task

def test_fetch_all_tasks():
    """Test function to fetch all tasks from the database"""
    try:
        print("🔧 Initializing database connection...")
        
        # Get the database connection
        database = container.get_database()
        
        # Get the task repository
        task_repo = container.get_task_repository()
        
        print("✅ Database connection established!")
        print("\n📋 Fetching all tasks...")
        
        # Fetch all tasks using a direct query
        cursor = database.cursor()
        cursor.execute('''
            SELECT id, user_id, title, description, category, recurrence, priority, due_date, completed, image_path, status
            FROM tasks
            ORDER BY id DESC
        ''')
        
        tasks = cursor.fetchall()
        
        if not tasks:
            print("📭 No tasks found in the database.")
            print("💡 Try creating a task first using the task creation endpoint.")
            return
        
        print(f"✅ Found {len(tasks)} task(s) in the database:")
        print("=" * 100)
        
        for i, task_data in enumerate(tasks, 1):
            print(f"\n📝 Task #{i}:")
            print(f"   ID: {task_data['id']}")
            print(f"   User ID: {task_data['user_id']}")
            print(f"   Title: {task_data['title'] or 'No title'}")
            print(f"   Description: {task_data['description'] or 'No description'}")
            print(f"   Category: {task_data['category'] or 'No category'}")
            print(f"   Recurrence: {task_data['recurrence'] or 'No recurrence'}")
            print(f"   Priority: {task_data['priority'] or 'Not set'}")
            print(f"   Due Date: {task_data['due_date'] or 'No due date'}")
            print(f"   Status: {task_data['status'] or 'Not set'}")
            print(f"   Completed: {'Yes' if task_data['completed'] else 'No'}")
            print(f"   Image Path: {task_data['image_path'] or 'No image'}")
            print("-" * 60)
        
        print("\n🎉 Task fetch test completed successfully!")
        
        # Test the repository method as well
        print("\n🔍 Testing repository methods...")
        test_repository_methods()
        
    except Exception as e:
        print(f"❌ Error during task fetch test: {str(e)}")
        import traceback
        traceback.print_exc()

def test_repository_methods():
    """Test fetching tasks using the repository pattern"""
    try:
        task_repo = container.get_task_repository()
        
        # Get database connection for direct query
        database = container.get_database()
        cursor = database.cursor()
        
        # Get all user IDs first
        cursor.execute('SELECT DISTINCT user_id FROM tasks ORDER BY user_id')
        user_ids = [row['user_id'] for row in cursor.fetchall()]
        
        print(f"📊 Testing repository methods for {len(user_ids)} users:")
        
        for user_id in user_ids:
            print(f"\n👤 User ID: {user_id}")
            
            # Test get_tasks_by_user method
            try:
                tasks = task_repo.get_tasks_by_user(user_id)
                print(f"   ✅ Found {len(tasks)} tasks for user {user_id}")
                
                for task in tasks[:3]:  # Show first 3 tasks
                    print(f"      - {task.title} (ID: {task.id})")
                if len(tasks) > 3:
                    print(f"      ... and {len(tasks) - 3} more tasks")
                    
            except Exception as e:
                print(f"   ❌ Error getting tasks for user {user_id}: {str(e)}")
        
        print("\n✅ Repository method test completed!")
        
    except Exception as e:
        print(f"❌ Error during repository test: {str(e)}")

def test_task_statistics():
    """Test task statistics and analytics"""
    try:
        print("\n📈 Testing task statistics...")
        
        database = container.get_database()
        cursor = database.cursor()
        
        # Total tasks
        cursor.execute('SELECT COUNT(*) as count FROM tasks')
        total_tasks = cursor.fetchone()['count']
        
        # Completed tasks
        cursor.execute('SELECT COUNT(*) as count FROM tasks WHERE completed = 1')
        completed_tasks = cursor.fetchone()['count']
        
        # Pending tasks
        cursor.execute('SELECT COUNT(*) as count FROM tasks WHERE completed = 0')
        pending_tasks = cursor.fetchone()['count']
        
        # Tasks by priority
        cursor.execute('SELECT priority, COUNT(*) as count FROM tasks GROUP BY priority')
        priority_stats = cursor.fetchall()
        
        # Tasks by status
        cursor.execute('SELECT status, COUNT(*) as count FROM tasks GROUP BY status')
        status_stats = cursor.fetchall()
        
        print(f"📊 Task Statistics:")
        print(f"   Total Tasks: {total_tasks}")
        print(f"   Completed: {completed_tasks}")
        print(f"   Pending: {pending_tasks}")
        print(f"   Completion Rate: {(completed_tasks/total_tasks*100):.1f}%" if total_tasks > 0 else "   Completion Rate: N/A")
        
        print(f"\n📊 Priority Distribution:")
        for stat in priority_stats:
            print(f"   {stat['priority'] or 'Not set'}: {stat['count']}")
        
        print(f"\n📊 Status Distribution:")
        for stat in status_stats:
            print(f"   {stat['status'] or 'Not set'}: {stat['count']}")
        
        print("✅ Task statistics test completed!")
        
    except Exception as e:
        print(f"❌ Error during statistics test: {str(e)}")

def test_create_sample_task():
    """Test creating a sample task to demonstrate the unique ID system"""
    try:
        print("\n🧪 Testing task creation with unique ID...")
        
        # Create a sample task (without saving to DB for demo)
        sample_task = Task(
            id=None,  # Will be auto-generated
            user_id="user_123",  # Sample user ID
            title="Sample Task " + str(int(__import__('time').time())),
            description="This is a sample task for testing",
            priority="high",
            status="pending"
        )
        
        print(f"📝 Creating task: {sample_task.title}")
        print(f"   Generated ID: {sample_task.id}")
        print(f"   User ID: {sample_task.user_id}")
        print(f"   Priority: {sample_task.priority}")
        print(f"   Status: {sample_task.status}")
        
        # Note: This would normally be done through the task service
        # For demo purposes, we're just showing the ID generation
        
        print("✅ Sample task creation test completed!")
        
    except Exception as e:
        print(f"❌ Error during sample task creation: {str(e)}")

def main():
    """Main test function"""
    print("🚀 Starting Task Fetch Test")
    print("=" * 60)
    
    # Test 1: Fetch all tasks
    test_fetch_all_tasks()
    
    # Test 2: Task statistics
    test_task_statistics()
    
    # Test 3: Test unique ID generation
    test_create_sample_task()
    
    print("\n" + "=" * 60)
    print("🏁 All task tests completed!")
    
    # Cleanup
    try:
        container.cleanup()
        print("🧹 Database connection cleaned up.")
    except:
        pass

if __name__ == "__main__":
    main() 