from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTableWidget,
    QLabel, QCheckBox
)

class FeedFacilityView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cơ sở sản xuất thức ăn chăn nuôi")
        self.resize(1000, 550)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()

        top_bar = QHBoxLayout()
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Tìm theo tên cơ sở...")

        self.chk_certified = QCheckBox("Chỉ hiển thị cơ sở đã được cấp phép")

        self.btn_search = QPushButton("Tìm kiếm")
        self.btn_refresh = QPushButton("Làm mới")
        self.btn_add = QPushButton("Thêm")
        self.btn_edit = QPushButton("Sửa")
        self.btn_delete = QPushButton("Xóa")

        top_bar.addWidget(QLabel("Tìm kiếm:"))
        top_bar.addWidget(self.txt_search)
        top_bar.addWidget(self.chk_certified)
        top_bar.addWidget(self.btn_search)
        top_bar.addWidget(self.btn_refresh)
        top_bar.addStretch()
        top_bar.addWidget(self.btn_add)
        top_bar.addWidget(self.btn_edit)
        top_bar.addWidget(self.btn_delete)

        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "ID", "Tên cơ sở", "Huyện", "Xã",
            "Địa chỉ", "Điện thoại", "Email",
            "Giấy phép", "Quy mô", "Trạng thái"
        ])
        self.table.setColumnHidden(0, True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        layout.addLayout(top_bar)
        layout.addWidget(self.table)
        self.setLayout(layout)
