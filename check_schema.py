#!/usr/bin/env python3
"""
Simple script to check the actual database schema
"""

import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dependency_injection import container

def check_schema():
    """Check the actual database schema"""
    try:
        print("🔧 Checking database schema...")
        
        # Get the database connection
        database = container.get_database()
        cursor = database.cursor()
        
        # Check users table schema
        print("\n📋 Users table schema:")
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        
        for column in columns:
            print(f"   - {column[1]} ({column[2]}) - {'NOT NULL' if column[3] else 'NULL'} - {'PRIMARY KEY' if column[5] else ''}")
        
        # Check if there are any users
        print("\n👥 Checking for existing users:")
        cursor.execute("SELECT COUNT(*) as count FROM users")
        user_count = cursor.fetchone()['count']
        print(f"   Found {user_count} users in the database")
        
        if user_count > 0:
            print("\n📊 Sample user data:")
            cursor.execute("SELECT * FROM users LIMIT 1")
            sample_user = cursor.fetchone()
            for key in sample_user.keys():
                print(f"   {key}: {sample_user[key]}")
        
        # Check other tables
        print("\n📋 Tasks table schema:")
        cursor.execute("PRAGMA table_info(tasks)")
        columns = cursor.fetchall()
        
        for column in columns:
            print(f"   - {column[1]} ({column[2]}) - {'NOT NULL' if column[3] else 'NULL'} - {'PRIMARY KEY' if column[5] else ''}")
        
        print("\n✅ Schema check completed!")
        
    except Exception as e:
        print(f"❌ Error during schema check: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            container.cleanup()
        except:
            pass

if __name__ == "__main__":
    check_schema() 