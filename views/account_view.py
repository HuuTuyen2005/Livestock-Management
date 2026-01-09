from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFormLayout

class AccountView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Thông tin tài khoản")
        self.resize(400, 300)

        layout = QVBoxLayout()
        self.form = QFormLayout()

        self.lbl_fullname = QLabel()
        self.lbl_email = QLabel()
        self.lbl_phone = QLabel()
        self.lbl_username = QLabel()

        self.form.addRow("Họ tên:", self.lbl_fullname)
        self.form.addRow("Email:", self.lbl_email)
        self.form.addRow("Điện thoại:", self.lbl_phone)
        self.form.addRow("Username:", self.lbl_username)

        layout.addLayout(self.form)
        self.setLayout(layout)
