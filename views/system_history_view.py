from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem
)

class SystemHistoryView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lịch sử tác động hệ thống")
        self.resize(900, 500)

        # ==== FILTER ====
        self.txt_keyword = QLineEdit()
        self.txt_keyword.setPlaceholderText("Tìm theo username / hành động")

        self.btn_search = QPushButton("Tìm kiếm")
        self.btn_refresh = QPushButton("Làm mới")

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Tìm kiếm:"))
        filter_layout.addWidget(self.txt_keyword)
        filter_layout.addWidget(self.btn_search)
        filter_layout.addWidget(self.btn_refresh)

        # ==== TABLE ====
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels([
            "ID",
            "Username",
            "Hành động",
            "Thời gian",
            "User ID"
        ])
        self.table.setColumnHidden(4, True)  # Ẩn user_id

        # ==== MAIN LAYOUT ====
        layout = QVBoxLayout()
        layout.addLayout(filter_layout)
        layout.addWidget(self.table)

        self.setLayout(layout)
