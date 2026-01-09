import bcrypt
from database.mysql_connector import MySQLConnector
from utils.password_utils import check_password

class ChangePasswordService:
    def __init__(self):
        self.db = MySQLConnector()

    def change_password(self, user_id, old_pwd, new_pwd):
        account = self.db.fetch_one("""
            SELECT * FROM account WHERE user_id=%s
        """, (user_id,))

        if not account:
            return False, "Không tìm thấy tài khoản"

        if not check_password(old_pwd, account["password"]):
            return False, "Mật khẩu cũ không đúng"

        hashed = bcrypt.hashpw(new_pwd.encode(), bcrypt.gensalt()).decode()

        self.db.execute("""
            UPDATE account SET password=%s WHERE user_id=%s
        """, (hashed, user_id))

        return True, "OK"
