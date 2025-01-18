import os
import time
from typing import List, Dict, Any
import mysql.connector
import json

# Global variables (issue: using globals)
DB_PASSWORD = "my_secret_password123"
CACHE = {}

class UserManager:
    def __init__(self):
        # Issue: Hard-coded credentials
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=DB_PASSWORD,
            database="users"
        )
        
        # Issue: Not using a context manager for file operations
        self.log_file = open("user_actions.log", "a")
    
    def get_user(self, user_id: int) -> Dict[str, Any]:
        # Issue: SQL Injection vulnerability
        cursor = self.db.cursor()
        cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
        return cursor.fetchone()
    
    def get_users_batch(self, user_ids: List[int]) -> List[Dict[str, Any]]:
        # Issue: N+1 query problem
        users = []
        for user_id in user_ids:
            users.append(self.get_user(user_id))
        return users
    
    def process_data(self, data: List[str]) -> str:
        # Issue: Inefficient string concatenation
        result = ""
        for item in data:
            result += item + ","
        return result[:-1]
    
    def calculate_statistics(self, numbers: List[int]) -> Dict[str, float]:
        # Issue: Redundant calculations
        sum1 = sum(numbers)
        mean = sum1 / len(numbers)
        sum2 = sum(numbers)  # Calculating sum again unnecessarily
        variance = sum((x - mean) ** 2 for x in numbers) / len(numbers)
        
        return {
            "mean": mean,
            "variance": variance,
            "sum": sum2  # Using the redundant calculation
        }
    
    def cache_user_data(self, user_id: int, data: Dict[str, Any]):
        # Issue: Using mutable global variable without locks
        global CACHE
        CACHE[user_id] = data
    
    def load_config(self, config_path: str) -> Dict[str, Any]:
        # Issue: unsafe deserialization of JSON
        with open(config_path, 'r') as f:
            return eval(f.read())  # Using eval instead of json.loads
    
    def process_large_file(self, filepath: str):
        # Issue: Loading entire file into memory
        with open(filepath, 'r') as f:
            content = f.read()
            for line in content.split('\n'):
                self.process_line(line)
    
    def process_line(self, line: str):
        # Issue: Bare except clause
        try:
            data = json.loads(line)
            self.cache_user_data(data['user_id'], data)
        except:
            pass  # Silently ignoring all errors
    
    def compute_factorial(self, n: int) -> int:
        # Issue: Recursive function without depth limit
        if n <= 1:
            return 1
        return n * self.compute_factorial(n - 1)
    
    def __del__(self):
        # Issue: Resource cleanup in destructor
        self.log_file.close()
        self.db.close()

def main():
    # Issue: No if __name__ == "__main__" guard
    manager = UserManager()
    user_data = manager.get_user(123)
    print(f"User data: {user_data}")

main()
