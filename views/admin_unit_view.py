from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTreeWidget, QLineEdit
)

class AdminUnitView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quản lý đơn vị hành chính")
        self.resize(600, 500)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Huyện / Xã")

        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Tìm huyện hoặc xã")
        self.btn_search = QPushButton("Tìm kiếm")
        self.btn_refresh = QPushButton("Làm mới")

        self.btn_add_district = QPushButton("Thêm huyện")
        self.btn_add_commune = QPushButton("Thêm xã")
        self.btn_edit = QPushButton("Sửa")
        self.btn_delete = QPushButton("Xoá")

        topbar_layout = QHBoxLayout()
        topbar_layout.addWidget(self.txt_search)
        topbar_layout.addWidget(self.btn_search)
        topbar_layout.addWidget(self.btn_refresh)
        topbar_layout.addStretch()  # đẩy các nút thao tác sang phải
        topbar_layout.addWidget(self.btn_add_district)
        topbar_layout.addWidget(self.btn_add_commune)
        topbar_layout.addWidget(self.btn_edit)
        topbar_layout.addWidget(self.btn_delete)

        layout = QVBoxLayout()
        layout.addLayout(topbar_layout)
        layout.addWidget(self.tree)

        self.setLayout(layout)
