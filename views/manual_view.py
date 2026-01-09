from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTextEdit, QLabel
)

class ManualView(QWidget):
    def __init__(self, can_manage=False):
        super().__init__()
        self.setWindowTitle("Hướng dẫn sử dụng")
        self.resize(800, 600)
        self.can_manage = can_manage

        layout = QVBoxLayout()

        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["ID", "Tiêu đề"])

        if can_manage:
            self.btn_add = QPushButton("Thêm")
            self.btn_edit = QPushButton("Sửa")
            self.btn_delete = QPushButton("Xoá")

            topbar_layout = QHBoxLayout()
            topbar_layout.addStretch() 
            topbar_layout.addWidget(self.btn_add)
            topbar_layout.addWidget(self.btn_edit)
            topbar_layout.addWidget(self.btn_delete)

            layout.addLayout(topbar_layout)

        layout.addWidget(self.table)

        layout.addWidget(QLabel("Nội dung"))
        self.txt_content = QTextEdit()
        self.txt_content.setReadOnly(True)
        layout.addWidget(self.txt_content)

        self.setLayout(layout)
