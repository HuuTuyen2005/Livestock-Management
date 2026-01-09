from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt

class UserGroupDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gán nhóm & phân quyền")
        self.resize(400, 500)

        self.lbl_user = QLabel()

        self.group_list = QListWidget()
        self.permission_list = QListWidget()
        self.permission_list.setEnabled(False)

        self.btn_save = QPushButton("Lưu")
        self.btn_close = QPushButton("Đóng")

        btns = QHBoxLayout()
        btns.addWidget(self.btn_save)
        btns.addWidget(self.btn_close)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_user)
        layout.addWidget(QLabel("Nhóm người dùng"))
        layout.addWidget(self.group_list)
        layout.addWidget(QLabel("Quyền hiệu lực (từ nhóm)"))
        layout.addWidget(self.permission_list)
        layout.addLayout(btns)

        self.setLayout(layout)
