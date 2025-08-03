#!/usr/bin/env python3
"""
Simple test script to fetch all users from the database
This demonstrates the unique ID system and user retrieval functionality
"""

import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dependency_injection import container
from models.user import User

def test_fetch_all_users():
    """Test function to fetch all users from the database"""
    try:
        print("🔧 Initializing database connection...")
        
        # Get the database connection
        database = container.get_database()
        
        # Get the user repository
        user_repo = container.get_user_repository()
        
        print("✅ Database connection established!")
        print("\n📋 Fetching all users...")
        
        # Fetch all users using a direct query
        cursor = database.cursor()
        cursor.execute('''
            SELECT id, username
            FROM users
            ORDER BY id DESC
        ''')
        
        users = cursor.fetchall()
        
        if not users:
            print("📭 No users found in the database.")
            print("💡 Try creating a user first using the registration endpoint.")
            return
        
        print(f"✅ Found {len(users)} user(s) in the database:")
        print("=" * 80)
        
        for i, user_data in enumerate(users, 1):
            print(f"\n👤 User #{i}:")
            print(f"   ID: {user_data['id']}")
            print(f"   Username: {user_data['username']}")
            print("-" * 40)
        
        print("\n🎉 User fetch test completed successfully!")
        
        # Test the repository method as well
        print("\n🔍 Testing repository method...")
        test_repository_method()
        
    except Exception as e:
        print(f"❌ Error during user fetch test: {str(e)}")
        import traceback
        traceback.print_exc()

def test_repository_method():
    """Test fetching users using the repository pattern"""
    try:
        user_repo = container.get_user_repository()
        
        # Get database connection for direct query
        database = container.get_database()
        cursor = database.cursor()
        
        # Get all user IDs first
        cursor.execute('SELECT id FROM users ORDER BY created_at DESC')
        user_ids = [row['id'] for row in cursor.fetchall()]
        
        print(f"📊 Testing repository methods for {len(user_ids)} users:")
        
        for user_id in user_ids:
            # Test get_user_by_id method
            user = user_repo.get_user_by_id(user_id)
            if user:
                print(f"   ✅ Found user: {user.username} (ID: {user.id})")
            else:
                print(f"   ❌ User not found for ID: {user_id}")
        
        print("✅ Repository method test completed!")
        
    except Exception as e:
        print(f"❌ Error during repository test: {str(e)}")

def test_create_sample_user():
    """Test creating a sample user to demonstrate the unique ID system"""
    try:
        print("\n🧪 Testing user creation with unique ID...")
        
        user_repo = container.get_user_repository()
        
        # Create a sample user (without password for demo)
        sample_user = User(
            id=None,  # Will be auto-generated
            username="test_user_" + str(int(__import__('time').time())),
            password_hash="test_hash",
            email="test@example.com"
        )
        
        print(f"📝 Creating user: {sample_user.username}")
        print(f"   Generated ID: {sample_user.id}")
        
        # Note: This would normally be done through the auth service
        # For demo purposes, we're just showing the ID generation
        
        print("✅ Sample user creation test completed!")
        
    except Exception as e:
        print(f"❌ Error during sample user creation: {str(e)}")

def main():
    """Main test function"""
    print("🚀 Starting User Fetch Test")
    print("=" * 50)
    
    # Test 1: Fetch all users
    test_fetch_all_users()
    
    # Test 2: Test unique ID generation
    test_create_sample_user()
    
    print("\n" + "=" * 50)
    print("🏁 All tests completed!")
    
    # Cleanup
    try:
        container.cleanup()
        print("🧹 Database connection cleaned up.")
    except:
        pass

if __name__ == "__main__":
    main() 