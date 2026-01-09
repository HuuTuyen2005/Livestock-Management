from auth.auth_service import AuthService
from views.login_view import LoginView
from views.main_window import MainWindow
from PyQt6.QtWidgets import QMessageBox
from controllers.forgot_password_controller import ForgotPasswordController

class LoginController:
    def __init__(self):
        self.view = LoginView()
        self.auth = AuthService()
        self.view.button.clicked.connect(self.handle_login)
        self.view.btn_forgot.clicked.connect(self.open_forgot_password)


    def handle_login(self):
        ok, msg = self.auth.login(
            self.view.username.text(),
            self.view.password.text()
        )
        if ok:
            self.main = MainWindow()
            self.main.show()
            self.view.close()
        else:
            QMessageBox.warning(self.view, "Lỗi", msg)
        
    def open_forgot_password(self):
        self.forgot = ForgotPasswordController()
        self.forgot.show()


