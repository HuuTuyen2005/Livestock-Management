from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem,
    QLineEdit
)

class GenView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quản lý nguồn gen giống vật nuôi")
        self.resize(900, 500)

        # ===== Table =====
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Tên Gen", "Mô Tả",
            "Nguồn gốc", "Mã Gen", "Trạng thái"
        ])

        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Nhập tên gen")

        self.btn_search = QPushButton("Tìm kiếm")
        self.btn_refresh = QPushButton("Làm mới")

        self.btn_add = QPushButton("Thêm")
        self.btn_edit = QPushButton("Sửa")
        self.btn_delete = QPushButton("Xoá")

        topbar_layout = QHBoxLayout()
        topbar_layout.addWidget(self.txt_search)
        topbar_layout.addWidget(self.btn_search)
        topbar_layout.addWidget(self.btn_refresh)
        topbar_layout.addStretch()  # đẩy các nút thao tác sang phải
        topbar_layout.addWidget(self.btn_add)
        topbar_layout.addWidget(self.btn_edit)
        topbar_layout.addWidget(self.btn_delete)

        # ===== Main layout =====
        layout = QVBoxLayout()
        layout.addLayout(topbar_layout)
        layout.addWidget(self.table)

        self.setLayout(layout)
