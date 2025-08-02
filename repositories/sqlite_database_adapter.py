import sqlite3
from typing import List, Dict, Any
from repositories.database_interface import DatabaseInterface

class SQLiteDatabaseAdapter(DatabaseInterface):
    """SQLite database adapter that wraps sqlite3.Connection to implement DatabaseInterface"""
    
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection
    
    def connect(self):
        """Establish database connection (no-op for adapter)"""
        pass
    
    def close(self):
        """Close database connection"""
        self.connection.close()
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute a query and return results"""
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute an update query and return affected rows"""
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        return cursor.rowcount 