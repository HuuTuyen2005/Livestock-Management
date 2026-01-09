# from PyQt6.QtWidgets import (
#     QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
# )

# class ForgotPasswordView(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Quên mật khẩu")
#         self.setFixedSize(320, 160)

#         self.email = QLineEdit()
#         self.email.setPlaceholderText("Nhập email đã đăng ký")

#         self.btn_send = QPushButton("Gửi mật khẩu mới")

#         layout = QVBoxLayout()
#         layout.addWidget(QLabel("Quên mật khẩu"))
#         layout.addWidget(self.email)
#         layout.addWidget(self.btn_send)

#         self.setLayout(layout)

import sys
import os
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame, QApplication
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class ForgotPasswordView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quên mật khẩu")
        self.setFixedSize(500, 350)
        self.setStyleSheet("background-color: #f0f2f5;")  # nền nhẹ nhàng

        # --- Layout chính căn giữa ---
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- Card trắng ---
        card = QFrame()
        card.setFixedSize(400, 300)
        card.setStyleSheet("""
            QFrame {
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
            QPushButton#SendButton {
                background-color: #5d8233;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 12px;
                font-size: 14px;
            }
            QPushButton#SendButton:hover {
                background-color: #4a6928;
            }
        """)

        # Layout bên trong card
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(20)

        # Tiêu đề
        title = QLabel("QUÊN MẬT KHẨU")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))

        # Hướng dẫn
        subtitle = QLabel("Nhập email đã đăng ký để nhận mật khẩu mới")
        subtitle.setWordWrap(True)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #555; font-size: 13px;")

        # Input email
        self.email = QLineEdit()
        self.email.setPlaceholderText("Email của bạn")

        # Nút gửi
        self.btn_send = QPushButton("Gửi mật khẩu mới")
        self.btn_send.setObjectName("SendButton")
        self.btn_send.setCursor(Qt.CursorShape.PointingHandCursor)

        # Thêm vào layout
        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addWidget(self.email)
        card_layout.addWidget(self.btn_send)

        # Thêm card vào layout chính
        main_layout.addWidget(card)

