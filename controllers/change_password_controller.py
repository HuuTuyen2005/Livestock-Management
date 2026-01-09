from views.change_password_dialog import ChangePasswordDialog
from services.change_password_service import ChangePasswordService
from services.activity_service import ActivityService
from auth.session import Session
from PyQt6.QtWidgets import QMessageBox

class ChangePasswordController:
    def __init__(self):
        self.view = ChangePasswordDialog()
        self.service = ChangePasswordService()
        self.log_service = ActivityService()

        self.view.btn_ok.clicked.connect(self.submit)

    # def submit(self):
    #     old_pwd = self.view.old_pwd.text()
    #     new_pwd = self.view.new_pwd.text()
    #     confirm = self.view.confirm_pwd.text()

    #     if new_pwd != confirm:
    #         QMessageBox.warning(self.view, "Lỗi", "Mật khẩu xác nhận không khớp")
    #         return

    #     ok, msg = self.service.change_password(
    #         Session.current_user["id"],
    #         old_pwd,
    #         new_pwd
    #     )

    #     if ok:
    #         self.log_service.log(
    #             Session.current_user["id"],
    #             "Đổi mật khẩu"
    #         )
    #         QMessageBox.information(self.view, "OK", "Đổi mật khẩu thành công")
    #         self.view.accept()
    #     else:
    #         QMessageBox.warning(self.view, "Lỗi", msg)

    def submit(self):
        old_pwd = self.view.old_pwd.text()
        new_pwd = self.view.new_pwd.text()
        confirm = self.view.confirm_pwd.text()

        if new_pwd != confirm:
            QMessageBox.warning(self.view, "Lỗi", "Mật khẩu xác nhận không khớp")
            return

        ok, msg = self.service.change_password(
            Session.current_user["id"],
            old_pwd,
            new_pwd
        )

        if ok:
            # Lấy account_id từ user_id
            from database.mysql_connector import MySQLConnector
            db = MySQLConnector()
            account = db.fetch_one(
                "SELECT id FROM account WHERE user_id=%s", 
                (Session.current_user["id"],)
            )

            if account:
                self.log_service.log(
                    account["id"],
                    "Đổi mật khẩu"
                )

            QMessageBox.information(self.view, "OK", "Đổi mật khẩu thành công")
            self.view.accept()
        else:
            QMessageBox.warning(self.view, "Lỗi", msg)
