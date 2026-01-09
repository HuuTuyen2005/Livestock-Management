import sys
from PyQt6.QtWidgets import QApplication
from controllers.login_controller import LoginController

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = LoginController()
    login.view.show()
    sys.exit(app.exec())
