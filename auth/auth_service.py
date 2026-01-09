from database.mysql_connector import MySQLConnector
from utils.password_utils import check_password
from auth.session import Session
from services.activity_service import ActivityService
from utils.email_utils import send_email
from utils.password_utils import generate_password, hash_password

class AuthService:
    def __init__(self):
        self.db = MySQLConnector()

    def login(self, username, password):
        account = self.db.fetch_one(
            "SELECT * FROM account WHERE username=%s",
            (username,)
        )
        if not account:
            return False, "Sai tài khoản"

        if not check_password(password, account["password"]):
            return False, "Sai mật khẩu"

        user = self.db.fetch_one(
            "SELECT * FROM user WHERE id=%s AND status=1",
            (account["user_id"],)
        )
        if not user:
            return False, "User bị khoá"

        permissions = self.db.fetch_all("""
            SELECT p.code FROM permissions p
            JOIN group_permissions gp ON p.id = gp.permissions_id
            JOIN user_groups ug ON ug.group_id = gp.group_id
            WHERE ug.user_id = %s
        """, (user["id"],))

        ActivityService().log(
            account["id"],
            "Đăng nhập hệ thống"
        )

        Session.current_user = user
        Session.permissions = {p["code"] for p in permissions}

        return True, "OK"

    def forgot_password(self, email):
        account = self.db.fetch_one("""
            SELECT a.id, a.username, u.email
            FROM account a
            JOIN user u ON a.user_id = u.id
            WHERE u.email = %s AND u.status = 1
        """, (email,))

        if not account:
            return False, "Email không tồn tại trong hệ thống"

        new_password = generate_password()
        hashed_password = hash_password(new_password)

        self.db.execute(
            "UPDATE account SET password=%s WHERE id=%s",
            (hashed_password, account["id"])
        )

        send_email(
            account["email"],
            "Cấp lại mật khẩu hệ thống",
            f"""
            Xin chào {account['username']},

            Mật khẩu mới của bạn là: {new_password}

            Vui lòng đăng nhập và đổi mật khẩu ngay sau khi đăng nhập.
            """
        )

        return True, "Mật khẩu mới đã được gửi về email"

