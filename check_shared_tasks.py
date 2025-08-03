#!/usr/bin/env python3
"""
Script to check what shared tasks exist in the database
"""

import sqlite3
import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_shared_tasks():
    """Check what shared tasks exist in the database"""
    try:
        print("Checking shared tasks in database...")
        
        # Connect to database
        db = sqlite3.connect('remindly.db')
        db.row_factory = sqlite3.Row
        
        # Check task_shares table
        cursor = db.cursor()
        cursor.execute('SELECT * FROM task_shares')
        shares = cursor.fetchall()
        
        print(f"Found {len(shares)} task shares in database:")
        for share in shares:
            print(f"  - Task ID: {share['task_id']}, Shared with: {share['shared_with_code']}, Permission: {share['permission_level']}")
        
        # Check users table
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        
        print(f"\nFound {len(users)} users in database:")
        for user in users:
            print(f"  - User ID: {user['id']}, Username: {user['username']}")
        
        # Check tasks table
        cursor.execute('SELECT * FROM tasks')
        tasks = cursor.fetchall()
        
        print(f"\nFound {len(tasks)} tasks in database:")
        for task in tasks:
            print(f"  - Task ID: {task['id']}, Title: '{task['title']}', Owner: {task['user_id']}")
        
        # Check if user 2 exists
        cursor.execute('SELECT * FROM users WHERE id = 2')
        user2 = cursor.fetchone()
        if user2:
            print(f"\nUser 2 exists: {user2['username']}")
            
            # Check if there are any shares for user 2's user_code
            cursor.execute('SELECT * FROM task_shares WHERE shared_with_code = ?', (user2['user_code'],))
            user2_shares = cursor.fetchall()
            print(f"Found {len(user2_shares)} shares for user 2's code '{user2['user_code']}':")
            for share in user2_shares:
                print(f"  - Task ID: {share['task_id']}, Permission: {share['permission_level']}")
        else:
            print("\nUser 2 does not exist")
        
        db.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_shared_tasks() 