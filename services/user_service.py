from database.mysql_connector import MySQLConnector
import bcrypt

class UserService:
    def __init__(self):
        self.db = MySQLConnector()

    def get_users(self):
        return self.db.fetch_all("""
            SELECT u.id, u.fullname, u.email, u.phone, a.username, u.status,
                   au.name AS unit_name
            FROM user u
            LEFT JOIN account a ON a.user_id = u.id
            LEFT JOIN administrative_unit au ON u.unit_id = au.id
            WHERE u.status != -1
            ORDER BY u.fullname
        """)

    # def create_user(self, fullname, email, phone, unit_id, username, password):
    #     self.db.execute("""
    #         INSERT INTO user (fullname, email, phone, status, unit_id)
    #         VALUES (%s, %s, %s, 1, %s)
    #     """, (fullname, email, phone, unit_id))

    #     user_id = self.db.fetch_one("SELECT LAST_INSERT_ID() AS id")["id"]

    #     hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    #     self.db.execute("""
    #         INSERT INTO account (username, password, user_id)
    #         VALUES (%s, %s, %s)
    #     """, (username, hashed, user_id))

    def create_user(self, fullname, email, phone, unit_id, username, password):
        user_id = self.db.execute_insert("""
            INSERT INTO user (fullname, email, phone, status, unit_id)
            VALUES (%s, %s, %s, 1, %s)
        """, (fullname, email, phone, unit_id))

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        self.db.execute("""
            INSERT INTO account (username, password, user_id)
            VALUES (%s, %s, %s)
        """, (username, hashed, user_id))

    def update_user(self, user_id, fullname, email, phone, unit_id):
        self.db.execute("""
            UPDATE user SET fullname=%s, email=%s, phone=%s, unit_id=%s
            WHERE id=%s
        """, (fullname, email, phone, unit_id, user_id))


    def set_status(self, user_id, status):
        self.db.execute("""
            UPDATE user SET status=%s WHERE id=%s
        """, (status, user_id))

    def reset_password(self, user_id, new_password="123456"):
        hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        self.db.execute("""
            UPDATE account SET password=%s WHERE user_id=%s
        """, (hashed, user_id))

    def search_users(self, keyword):
        like = f"%{keyword}%"
        return self.db.fetch_all("""
            SELECT u.id, u.fullname, u.email, u.phone, a.username, u.status,
                au.name AS unit_name
            FROM user u
            LEFT JOIN account a ON a.user_id = u.id
            LEFT JOIN administrative_unit au ON u.unit_id = au.id
            WHERE u.fullname LIKE %s
                AND u.status != -1
            ORDER BY u.fullname
        """, (like,))
    
    def get_status(self, user_id):
        return self.db.fetch_one(
            "SELECT status FROM user WHERE id=%s",
            (user_id,)
        )["status"]


    def delete_user(self, user_id):
    # Xoá mềm
        self.db.execute("""
            UPDATE user SET status = -1 WHERE id = %s
        """, (user_id,))

    def get_user_by_id(self, user_id):
        return self.db.fetch_one("""
            SELECT id, fullname, email, phone, unit_id
            FROM user
            WHERE id = %s
        """, (user_id,))