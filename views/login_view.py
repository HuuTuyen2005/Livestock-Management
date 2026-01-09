import os
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPalette, QBrush

class LoginView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hệ thống quản lý chăn nuôi")
        self.setFixedSize(900, 600)

        # --- 1. Load background tuyệt đối ---
        current_dir = os.path.dirname(os.path.abspath(__file__))
        bg_path = os.path.join(current_dir, '..', 'image', 'background.jpg')
        bg_path = os.path.abspath(bg_path)  # đường dẫn tuyệt đối
        if not os.path.exists(bg_path):
            print("Không tìm thấy file background:", bg_path)
        else:
            pixmap = QPixmap(bg_path)
            if pixmap.isNull():
                print("Không load được pixmap từ:", bg_path)
            else:
                # Sử dụng palette để đặt background
                palette = self.palette()
                palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
                self.setPalette(palette)

        # --- 2. Layout chính căn giữa khung login ---
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- 3. Login card trắng ---
        login_card = QFrame()
        login_card.setFixedSize(380, 420)
        login_card.setObjectName("LoginCard")
        login_card.setStyleSheet("""
            #LoginCard {
                background-color: white;
                border-radius: 15px;
            }
            QLabel {
                color: #333;
                font-family: 'Segoe UI', Arial;
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
            QPushButton#LoginButton {
                background-color: #5d8233;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 12px;
                font-size: 14px;
            }
            QPushButton#LoginButton:hover {
                background-color: #4a6928;
            }
            QPushButton#ForgotButton {
                color: #2980b9;
                border: none;
                background: none;
                font-size: 12px;
            }
        """)

        # Layout trong login card
        card_layout = QVBoxLayout(login_card)
        card_layout.setContentsMargins(30, 40, 30, 40)
        card_layout.setSpacing(15)

        title = QLabel("HỆ THỐNG QUẢN LÝ CHĂN NUÔI")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: 800; margin-bottom: 10px;")

        dots = QLabel(".....")
        dots.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dots.setStyleSheet("color: #ccc; font-size: 20px; margin-bottom: 10px;")

        self.username = QLineEdit()
        self.username.setPlaceholderText("Tên đăng nhập")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Mật khẩu")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        button_layout = QHBoxLayout()
        self.button = QPushButton("Đăng nhập")
        self.button.setObjectName("LoginButton")
        self.button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.btn_forgot = QPushButton("Quên mật khẩu?")
        self.btn_forgot.setObjectName("ForgotButton")
        self.btn_forgot.setCursor(Qt.CursorShape.PointingHandCursor)

        button_layout.addWidget(self.button, 3)
        button_layout.addWidget(self.btn_forgot, 2)

        card_layout.addWidget(title)
        card_layout.addWidget(dots)
        card_layout.addWidget(self.username)
        card_layout.addWidget(self.password)
        card_layout.addLayout(button_layout)
        card_layout.addStretch()

        # Footer bản quyền
        footer = QLabel("© 2026 Livestock Management System. All Rights Reserved. Nguyen Huu Tuyen")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("color: white; font-size: 11px; margin-top: 20px;")

        main_layout.addWidget(login_card)
        main_layout.addWidget(footer)


