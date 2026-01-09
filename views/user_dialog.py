from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QHBoxLayout, QComboBox
)

class UserDialog(QDialog):
    def __init__(self, units, user=None):
        super().__init__()
        self.user = user
        self.resize(400, 400)

        layout = QVBoxLayout(self)

        self.txt_fullname = QLineEdit()
        self.txt_email = QLineEdit()
        self.txt_phone = QLineEdit()
        self.txt_username = QLineEdit()
        self.txt_password = QLineEdit()
        self.txt_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.cbo_unit = QComboBox()
        for u in units:
            self.cbo_unit.addItem(u["name"], u["id"])

        layout.addWidget(QLabel("Họ tên"))
        layout.addWidget(self.txt_fullname)
        layout.addWidget(QLabel("Email"))
        layout.addWidget(self.txt_email)
        layout.addWidget(QLabel("Điện thoại"))
        layout.addWidget(self.txt_phone)
        layout.addWidget(QLabel("Đơn vị"))
        layout.addWidget(self.cbo_unit)
        layout.addWidget(QLabel("Username"))
        layout.addWidget(self.txt_username)
        layout.addWidget(QLabel("Mật khẩu"))
        layout.addWidget(self.txt_password)

        btns = QHBoxLayout()
        self.btn_save = QPushButton("Lưu")
        self.btn_cancel = QPushButton("Huỷ")
        btns.addWidget(self.btn_save)
        btns.addWidget(self.btn_cancel)
        layout.addLayout(btns)

        self.btn_cancel.clicked.connect(self.reject)

        # ===== SET DATA EDIT =====
        if user:
            self.setWindowTitle("Cập nhật người dùng")

            self.txt_fullname.setText(user["fullname"])
            self.txt_email.setText(user["email"])
            self.txt_phone.setText(user["phone"])

            index = self.cbo_unit.findData(user["unit_id"])
            if index >= 0:
                self.cbo_unit.setCurrentIndex(index)

            self.txt_username.hide()
            self.txt_password.hide()
        else:
            self.setWindowTitle("Thêm người dùng")
