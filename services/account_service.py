from database.mysql_connector import MySQLConnector

class AccountService:
    def __init__(self):
        self.db = MySQLConnector()

    def get_account_info(self, user_id):
        """Lấy thông tin user và username, không lấy password"""
        return self.db.fetch_one("""
            SELECT u.fullname, u.email, u.phone, a.username, u.unit_id
            FROM user u
            LEFT JOIN account a ON a.user_id = u.id
            WHERE u.id=%s
        """, (user_id,))

