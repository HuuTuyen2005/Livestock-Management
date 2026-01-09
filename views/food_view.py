from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem,
    QLineEdit
)

class FoodView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quản lý thức ăn chăn nuôi")
        self.resize(900, 500)

        layout = QVBoxLayout(self)

        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Nhập tên hoặc loại thức ăn")
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

        # ===== Table =====
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels([
            "ID", "Tên thức ăn", "Loại", "Mô tả", "Chất dinh dưỡng"
        ])
        self.table.setSelectionBehavior(
            self.table.SelectionBehavior.SelectRows
        )
        self.table.setEditTriggers(
            self.table.EditTrigger.NoEditTriggers
        )

        # ===== Main layout =====
        layout.addLayout(topbar_layout)
        layout.addWidget(self.table)
        self.setLayout(layout)
