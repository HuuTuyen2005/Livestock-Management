from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame
)
from PyQt6.QtCore import Qt

class ChangePasswordDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Đổi mật khẩu")
        self.setFixedSize(400, 350)

        # --- Tạo card trắng giống login ---
        card = QFrame()
        card.setObjectName("ChangePasswordCard")
        card.setStyleSheet("""
            #ChangePasswordCard {
                background-color: white;
                border-radius: 15px;
            }
            QLabel#TitleLabel {
                color: #333;
                font-family: 'Segoe UI', Arial;
                font-size: 16px;
                font-weight: 700;
                margin-bottom: 10px;
            }
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                background-color: #fcfcfc;
            }
            QLineEdit:focus {
                border: 2px solid #5d8233;
            }
            QPushButton#OkButton {
                background-color: #5d8233;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 12px;
                font-size: 14px;
            }
            QPushButton#OkButton:hover {
                background-color: #4a6928;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(15)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QLabel("Đổi mật khẩu")
        title.setObjectName("TitleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.old_pwd = QLineEdit()
        self.old_pwd.setEchoMode(QLineEdit.EchoMode.Password)
        self.old_pwd.setPlaceholderText("Mật khẩu cũ")

        self.new_pwd = QLineEdit()
        self.new_pwd.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_pwd.setPlaceholderText("Mật khẩu mới")

        self.confirm_pwd = QLineEdit()
        self.confirm_pwd.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_pwd.setPlaceholderText("Xác nhận mật khẩu")

        self.btn_ok = QPushButton("Đổi mật khẩu")
        self.btn_ok.setObjectName("OkButton")
        self.btn_ok.setCursor(Qt.CursorShape.PointingHandCursor)

        card_layout.addWidget(title)
        card_layout.addWidget(self.old_pwd)
        card_layout.addWidget(self.new_pwd)
        card_layout.addWidget(self.confirm_pwd)
        card_layout.addWidget(self.btn_ok)
        card_layout.addStretch()

        main_layout = QVBoxLayout(self)
        main_layout.addStretch()
        main_layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch()
