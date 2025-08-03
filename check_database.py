#!/usr/bin/env python3
"""
Script to check database contents
"""

import sqlite3
import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_database():
    """Check what's in the database"""
    try:
        print("Checking database contents...")
        
        # Connect to database
        db = sqlite3.connect('remindly.db')
        db.row_factory = sqlite3.Row
        
        cursor = db.cursor()
        
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"\nFound {len(tables)} tables:")
        for table in tables:
            print(f"  - {table['name']}")
        
        # Check users table
        try:
            cursor.execute('SELECT * FROM users')
            users = cursor.fetchall()
            print(f"\nFound {len(users)} users:")
            for user in users:
                print(f"  - ID: {user['id']}, Username: {user['username']}, UserCode: {user['user_code']}")
        except sqlite3.OperationalError:
            print("\nUsers table does not exist")
        
        # Check tasks table
        try:
            cursor.execute('SELECT * FROM tasks')
            tasks = cursor.fetchall()
            print(f"\nFound {len(tasks)} tasks:")
            for task in tasks:
                print(f"  - ID: {task['id']}, Title: '{task['title']}', Owner: {task['user_id']}")
        except sqlite3.OperationalError:
            print("\nTasks table does not exist")
        
        # Check task_shares table
        try:
            cursor.execute('SELECT * FROM task_shares')
            shares = cursor.fetchall()
            print(f"\nFound {len(shares)} task shares:")
            for share in shares:
                print(f"  - Task ID: {share['task_id']}, Shared with: {share['shared_with_code']}, Permission: {share['permission_level']}")
        except sqlite3.OperationalError:
            print("\nTask_shares table does not exist")
        
        db.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_database() 