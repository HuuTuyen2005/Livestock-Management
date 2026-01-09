from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit,
    QTextEdit, QPushButton, QLabel,
    QListWidget, QAbstractItemView, QComboBox
)
from PyQt6.QtCore import Qt

class PermissionDialog(QDialog):
    def __init__(self, title="Permission"):
        super().__init__()
        self.setWindowTitle(title)
        layout = QVBoxLayout(self)

        self.txt_name = QLineEdit()
        self.txt_code = QLineEdit()
        self.txt_desc = QTextEdit()

        layout.addWidget(QLabel("Tên quyền"))
        layout.addWidget(self.txt_name)
        layout.addWidget(QLabel("Code"))
        layout.addWidget(self.txt_code)
        layout.addWidget(QLabel("Mô tả"))
        layout.addWidget(self.txt_desc)

        self.btn_save = QPushButton("Lưu")
        layout.addWidget(self.btn_save)


class GroupPermissionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Phân quyền cho nhóm")
        self.resize(400, 500)

        layout = QVBoxLayout(self)

        self.cbo_group = QComboBox()
        self.lst_permissions = QListWidget()
        self.lst_permissions.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection
        )

        self.btn_save = QPushButton("Lưu")

        layout.addWidget(QLabel("Chọn nhóm"))
        layout.addWidget(self.cbo_group)
        layout.addWidget(QLabel("Quyền"))
        layout.addWidget(self.lst_permissions)
        layout.addWidget(self.btn_save)
