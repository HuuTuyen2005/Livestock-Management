from database.mysql_connector import MySQLConnector

class ActivityService:
    def __init__(self):
        self.db = MySQLConnector()

    def log(self, account_id, action):
        self.db.execute("""
            INSERT INTO activities_history (account_id, activities)
            VALUES (%s, %s)
        """, (account_id, action))
