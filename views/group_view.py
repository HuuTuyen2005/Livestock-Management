from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem,
    QLineEdit, QLabel
)
from PyQt6.QtCore import Qt


class GroupView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        # ===== Search =====
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Tìm kiếm nhóm...")

        self.btn_search = QPushButton("Tìm")

        self.btn_add = QPushButton("Thêm")
        self.btn_edit = QPushButton("Sửa")
        self.btn_delete = QPushButton("Xóa")
        self.btn_toggle = QPushButton("Bật / Tắt")
        self.btn_lookup = QPushButton("Tra cứu")

        topbar_layout = QHBoxLayout()
        topbar_layout.addWidget(QLabel("Tìm kiếm:"))
        topbar_layout.addWidget(self.search_input)
        topbar_layout.addWidget(self.btn_search)
        topbar_layout.addStretch()  
        topbar_layout.addWidget(self.btn_add)
        topbar_layout.addWidget(self.btn_edit)
        topbar_layout.addWidget(self.btn_delete)
        topbar_layout.addWidget(self.btn_toggle)
        topbar_layout.addWidget(self.btn_lookup)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Tên nhóm", "Mô tả", "Trạng thái"]
        )
        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        # ===== Main layout =====
        main_layout.addLayout(topbar_layout)
        main_layout.addWidget(self.table)

    # ===== Helpers =====
    def get_selected_group_id(self):
        row = self.table.currentRow()
        if row < 0:
            return None
        return int(self.table.item(row, 0).text())

    def load_data(self, groups):
        self.table.setRowCount(len(groups))
        for row, g in enumerate(groups):
            self.table.setItem(row, 0, QTableWidgetItem(str(g["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(g["name"]))
            self.table.setItem(row, 2, QTableWidgetItem(g["description"] or ""))

            status = "Bật" if g["is_active"] else "Tắt"
            status_item = QTableWidgetItem(status)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 3, status_item)
