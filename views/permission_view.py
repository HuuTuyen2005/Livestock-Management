from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt

class PermissionView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quản lý phân quyền")
        self.resize(900, 600)

        layout = QVBoxLayout(self)

        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("Thêm")
        self.btn_edit = QPushButton("Sửa")
        self.btn_delete = QPushButton("Xóa")
        self.btn_assign = QPushButton("Phân quyền nhóm")
        self.btn_view = QPushButton("Tra cứu")

        for b in [
            self.btn_add, self.btn_edit,
            self.btn_delete, self.btn_assign,
            self.btn_view
        ]:
            btn_layout.addWidget(b)

        layout.addLayout(btn_layout)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Tên", "Code", "Mô tả", "Hoạt động"]
        )
        self.table.setColumnHidden(0, True)

        layout.addWidget(self.table)
