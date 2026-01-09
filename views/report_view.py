# from PyQt6.QtWidgets import (
#     QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
#     QTabWidget, QLabel
# )
# from PyQt6.QtCore import Qt

# class ReportView(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Báo cáo hệ thống")
#         self.resize(1000, 600)

#         layout = QVBoxLayout(self)

#         self.tabs = QTabWidget()
#         layout.addWidget(self.tabs)

#         # Tab 1: Thống kê người dùng
#         self.tab_user_stats = QTableWidget()
#         self.tab_user_stats.setColumnCount(2)
#         self.tab_user_stats.setHorizontalHeaderLabels(["Tên / Mã", "Số lượng"])
#         self.tabs.addTab(self.tab_user_stats, "Thống kê người dùng")

#         # Tab 2: Lịch sử truy cập
#         self.tab_access = QTableWidget()
#         self.tab_access.setColumnCount(3)
#         self.tab_access.setHorizontalHeaderLabels(["Người dùng", "Hành động", "Thời gian"])
#         self.tabs.addTab(self.tab_access, "Lịch sử truy cập")

#         # Tab 3: Lịch sử tác động hệ thống
#         self.tab_actions = QTableWidget()
#         self.tab_actions.setColumnCount(3)
#         self.tab_actions.setHorizontalHeaderLabels(["Người dùng", "Hành động", "Thời gian"])
#         self.tabs.addTab(self.tab_actions, "Lịch sử tác động")

#         # Tab 4: Báo cáo tổng hợp
#         self.tab_summary = QWidget()
#         self.summary_layout = QVBoxLayout(self.tab_summary)
#         self.lbl_total_users = QLabel()
#         self.lbl_total_activities = QLabel()
#         self.lbl_total_actions = QLabel()
#         self.summary_layout.addWidget(self.lbl_total_users)
#         self.summary_layout.addWidget(self.lbl_total_activities)
#         self.summary_layout.addWidget(self.lbl_total_actions)
#         self.summary_layout.addStretch()
#         self.tabs.addTab(self.tab_summary, "Tổng hợp")

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QTabWidget, QLabel, QPushButton
)
from PyQt6.QtCore import Qt

class ReportView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Báo cáo hệ thống")
        self.resize(1000, 600)

        layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Tab 1: Thống kê người dùng
        self.tab_user_stats_container = QWidget()
        self.tab_user_stats_layout = QVBoxLayout(self.tab_user_stats_container)
        self.tab_user_stats = QTableWidget()
        self.tab_user_stats.setColumnCount(2)
        self.tab_user_stats.setHorizontalHeaderLabels(["Tên / Mã", "Số lượng"])
        self.btn_export_user_stats = QPushButton("Xuất PDF")
        self.tab_user_stats_layout.addWidget(self.tab_user_stats)
        self.tab_user_stats_layout.addWidget(self.btn_export_user_stats)
        self.tabs.addTab(self.tab_user_stats_container, "Thống kê người dùng")

        # Tab 2: Lịch sử truy cập
        self.tab_access_container = QWidget()
        self.tab_access_layout = QVBoxLayout(self.tab_access_container)
        self.tab_access = QTableWidget()
        self.tab_access.setColumnCount(3)
        self.tab_access.setHorizontalHeaderLabels(["Người dùng", "Hành động", "Thời gian"])
        self.btn_export_access = QPushButton("Xuất PDF")
        self.tab_access_layout.addWidget(self.tab_access)
        self.tab_access_layout.addWidget(self.btn_export_access)
        self.tabs.addTab(self.tab_access_container, "Lịch sử truy cập")

        # Tab 3: Lịch sử tác động hệ thống
        self.tab_actions_container = QWidget()
        self.tab_actions_layout = QVBoxLayout(self.tab_actions_container)
        self.tab_actions = QTableWidget()
        self.tab_actions.setColumnCount(3)
        self.tab_actions.setHorizontalHeaderLabels(["Người dùng", "Hành động", "Thời gian"])
        self.btn_export_actions = QPushButton("Xuất PDF")
        self.tab_actions_layout.addWidget(self.tab_actions)
        self.tab_actions_layout.addWidget(self.btn_export_actions)
        self.tabs.addTab(self.tab_actions_container, "Lịch sử tác động")

        # Tab 4: Báo cáo tổng hợp
        self.tab_summary = QWidget()
        self.summary_layout = QVBoxLayout(self.tab_summary)
        self.lbl_total_users = QLabel()
        self.lbl_total_activities = QLabel()
        self.lbl_total_actions = QLabel()
        self.btn_export_summary = QPushButton("Xuất PDF")
        self.summary_layout.addWidget(self.lbl_total_users)
        self.summary_layout.addWidget(self.lbl_total_activities)
        self.summary_layout.addWidget(self.lbl_total_actions)
        self.summary_layout.addWidget(self.btn_export_summary)
        self.summary_layout.addStretch()
        self.tabs.addTab(self.tab_summary, "Tổng hợp")
