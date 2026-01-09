from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QComboBox,
    QTableWidget, QLabel
)


class SubstanceView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Danh mục nguyên liệu & chất cấm")
        self.resize(900, 500)

        # ===== MAIN LAYOUT =====
        main_layout = QVBoxLayout(self)

        # ===== TOP BAR =====
        top = QHBoxLayout()

        self.cbo_filter = QComboBox()
        self.cbo_filter.addItems([
            "Tất cả",
            "Được phép sử dụng",
            "Bị cấm sử dụng"
        ])

        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Nhập tên nguyên liệu / hóa chất")

        self.btn_search = QPushButton("Tìm kiếm")
        self.btn_refresh = QPushButton("Làm mới")

        self.btn_add = QPushButton("Thêm")
        self.btn_edit = QPushButton("Sửa")
        self.btn_delete = QPushButton("Xóa")

        top.addWidget(QLabel("Lọc:"))
        top.addWidget(self.cbo_filter)
        top.addWidget(self.txt_search)
        top.addWidget(self.btn_search)
        top.addWidget(self.btn_refresh)

        top.addStretch()

        top.addWidget(self.btn_add)
        top.addWidget(self.btn_edit)
        top.addWidget(self.btn_delete)

        # ===== TABLE =====
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "ID", "Tên", "Loại", "Mô tả", "Trạng thái"
        ])

        self.table.setColumnHidden(0, True)
        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        # ===== ADD TO MAIN LAYOUT =====
        main_layout.addLayout(top)
        main_layout.addWidget(self.table)


