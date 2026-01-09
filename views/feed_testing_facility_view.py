from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTableWidget, QLabel
)

class FeedTestingFacilityView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cơ sở khảo nghiệm thức ăn chăn nuôi")
        self.resize(1100, 550)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()

        top = QHBoxLayout()
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Tìm theo tên cơ sở...")

        self.btn_search = QPushButton("Tìm kiếm")
        self.btn_refresh = QPushButton("Làm mới")
        self.btn_add = QPushButton("Thêm")
        self.btn_edit = QPushButton("Sửa")
        self.btn_delete = QPushButton("Xóa")

        top.addWidget(QLabel("Tìm kiếm:"))
        top.addWidget(self.txt_search)
        top.addWidget(self.btn_search)
        top.addWidget(self.btn_refresh)
        top.addStretch()
        top.addWidget(self.btn_add)
        top.addWidget(self.btn_edit)
        top.addWidget(self.btn_delete)

        self.table = QTableWidget()
        self.table.setColumnCount(11)
        self.table.setHorizontalHeaderLabels([
            "ID", "Tên cơ sở", "Huyện", "Xã",
            "Địa chỉ", "Điện thoại", "Email",
            "Giấy phép", "Quy mô",
            "Thức ăn khảo nghiệm", "Trạng thái"
        ])
        self.table.setColumnHidden(0, True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        layout.addLayout(top)
        layout.addWidget(self.table)
        self.setLayout(layout)
