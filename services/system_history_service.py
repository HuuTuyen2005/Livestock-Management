from database.mysql_connector import MySQLConnector

class SystemHistoryService:
    def __init__(self):
        self.db = MySQLConnector()

    def get_all(self):
        return self.db.fetch_all("""
            SELECT ah.id,
                   a.username,
                   ah.activities,
                   ah.time,
                   a.user_id
            FROM activities_history ah
            JOIN account a ON ah.account_id = a.id
            ORDER BY ah.time DESC
        """)

    def search(self, keyword):
        kw = f"%{keyword}%"
        return self.db.fetch_all("""
            SELECT ah.id,
                   a.username,
                   ah.activities,
                   ah.time,
                   a.user_id
            FROM activities_history ah
            JOIN account a ON ah.account_id = a.id
            WHERE a.username LIKE %s
               OR ah.activities LIKE %s
            ORDER BY ah.time DESC
        """, (kw, kw))
