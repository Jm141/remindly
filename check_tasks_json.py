#!/usr/bin/env python3
"""
Simple script to check for tasks in the database and return JSON
"""

import sys
import os
import json
from datetime import datetime

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dependency_injection import container

def check_tasks_json():
    """Check for tasks in the database and return JSON"""
    try:
        print("🔧 Connecting to database...")
        database = container.get_database()
        cursor = database.cursor()
        
        # Get all tasks
        cursor.execute('''
            SELECT id, user_id, title, description, category, recurrence, priority, due_date, completed, image_path, status
            FROM tasks
            ORDER BY id DESC
        ''')
        
        tasks = cursor.fetchall()
        
        # Convert to list of dictionaries
        task_list = []
        for task_data in tasks:
            task_dict = {
                'id': task_data['id'],
                'user_id': task_data['user_id'],
                'title': task_data['title'],
                'description': task_data['description'],
                'category': task_data['category'],
                'recurrence': task_data['recurrence'],
                'priority': task_data['priority'],
                'due_date': task_data['due_date'],
                'completed': bool(task_data['completed']),
                'image_path': task_data['image_path'],
                'status': task_data['status']
            }
            task_list.append(task_dict)
        
        # Create response object
        response = {
            'timestamp': datetime.now().isoformat(),
            'total_tasks': len(task_list),
            'tasks': task_list,
            'status': 'success'
        }
        
        # Print JSON
        print(json.dumps(response, indent=2))
        
        return response
        
    except Exception as e:
        error_response = {
            'timestamp': datetime.now().isoformat(),
            'error': str(e),
            'status': 'error'
        }
        print(json.dumps(error_response, indent=2))
        return error_response
    finally:
        try:
            container.cleanup()
        except:
            pass

if __name__ == "__main__":
    check_tasks_json() 