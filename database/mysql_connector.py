import mysql.connector
from mysql.connector import Error

class MySQLConnector:
    def __init__(self):
        self.config = {
            "host": "localhost",
            "user": "root",
            "password": "truyen123",
            "database": "livestock_app"
        }

    def connect(self):
        return mysql.connector.connect(**self.config)

    def fetch_one(self, query, params=None):
        conn = self.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result

    def fetch_all(self, query, params=None):
        conn = self.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    def execute(self, query, params=None):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        cursor.close()
        conn.close()

    def execute_insert(self, query, params=None):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        last_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return last_id