from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QTableWidget,
    QTableWidgetItem
)
from PyQt6.QtCore import Qt


class GroupLookupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tra cứu nhóm & người dùng")
        self.resize(600, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # ===== SELECT MODE =====
        select_layout = QHBoxLayout()
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([
            "Nhóm → Danh sách User",
            "User → Danh sách Nhóm"
        ])

        self.select_combo = QComboBox()

        select_layout.addWidget(QLabel("Chế độ:"))
        select_layout.addWidget(self.mode_combo)
        select_layout.addWidget(QLabel("Chọn:"))
        select_layout.addWidget(self.select_combo)

        # ===== TABLE =====
        self.table = QTableWidget()
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        layout.addLayout(select_layout)
        layout.addWidget(self.table)

    # ================= LOAD DATA =================
    def load_select_items(self, items, mode):
        self.select_combo.clear()

        if mode == "group":
            for g in items:
                self.select_combo.addItem(g["name"], g["id"])
        else:
            for u in items:
                self.select_combo.addItem(u["fullname"], u["id"])


    def load_table(self, headers, rows):
        self.table.clear()
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(rows))

        for r, row in enumerate(rows):
            for c, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(r, c, item)
