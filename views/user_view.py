from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QLineEdit
)

class UserView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quản lý người dùng")
        self.resize(1500, 1000)

        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Tìm theo tên")
        self.btn_search = QPushButton("Tìm kiếm")
        self.btn_refresh = QPushButton("Làm mới")

        self.btn_add = QPushButton("Thêm")
        self.btn_edit = QPushButton("Sửa")
        self.btn_lock = QPushButton("Khoá / Mở")
        self.btn_reset = QPushButton("Reset mật khẩu")
        self.btn_delete = QPushButton("Xoá")

        topbar_layout = QHBoxLayout()
        topbar_layout.addWidget(self.txt_search)
        topbar_layout.addWidget(self.btn_search)
        topbar_layout.addWidget(self.btn_refresh)
        topbar_layout.addStretch() 
        topbar_layout.addWidget(self.btn_add)
        topbar_layout.addWidget(self.btn_edit)
        topbar_layout.addWidget(self.btn_lock)
        topbar_layout.addWidget(self.btn_reset)
        topbar_layout.addWidget(self.btn_delete)

        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Họ tên", "Email", "Điện thoại", "Username", "Đơn vị", "Trạng thái"
        ])

        layout = QVBoxLayout()
        layout.addLayout(topbar_layout)
        layout.addWidget(self.table)

        self.setLayout(layout)
