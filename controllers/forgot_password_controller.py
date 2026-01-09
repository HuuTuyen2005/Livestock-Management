from views.forgot_password_view import ForgotPasswordView
from auth.auth_service import AuthService
from PyQt6.QtWidgets import QMessageBox

class ForgotPasswordController:
    def __init__(self):
        self.view = ForgotPasswordView()
        self.auth = AuthService()

        self.view.btn_send.clicked.connect(self.send_email)

    def send_email(self):
        email = self.view.email.text()

        ok, msg = self.auth.forgot_password(email)
        if ok:
            QMessageBox.information(self.view, "Thành công", msg)
            self.view.close()
        else:
            QMessageBox.warning(self.view, "Lỗi", msg)

    def show(self):
        self.view.show()
