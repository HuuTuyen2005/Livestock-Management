# from views.report_view import ReportView
# from services.report_service import ReportService
# from PyQt6.QtWidgets import QTableWidgetItem

# class ReportController:
#     def __init__(self):
#         self.view = ReportView()
#         self.service = ReportService()

#         self.load_user_statistics()
#         self.load_user_access_history()
#         self.load_system_action_history()
#         self.load_summary_report()

#     def load_user_statistics(self):
#         stats = self.service.user_statistics()
#         table = self.view.tab_user_stats
#         rows = []

#         # By status
#         for s in stats['by_status']:
#             rows.append((f"Trạng thái {s['status']}", str(s['count'])))
#         # By unit
#         for u in stats['by_unit']:
#             rows.append((f"Đơn vị {u['unit_id']}", str(u['count'])))
#         table.setRowCount(len(rows))
#         for r, (name, count) in enumerate(rows):
#             table.setItem(r, 0, QTableWidgetItem(name))
#             table.setItem(r, 1, QTableWidgetItem(count))

#     def load_user_access_history(self):
#         data = self.service.user_access_history()
#         table = self.view.tab_access
#         table.setRowCount(len(data))
#         for r, row in enumerate(data):
#             table.setItem(r, 0, QTableWidgetItem(row['fullname']))
#             table.setItem(r, 1, QTableWidgetItem(row['activities']))
#             table.setItem(r, 2, QTableWidgetItem(str(row['time'])))

#     def load_system_action_history(self):
#         data = self.service.system_action_history()
#         table = self.view.tab_actions
#         table.setRowCount(len(data))
#         for r, row in enumerate(data):
#             table.setItem(r, 0, QTableWidgetItem(row['fullname']))
#             table.setItem(r, 1, QTableWidgetItem(row['activities']))
#             table.setItem(r, 2, QTableWidgetItem(str(row['time'])))

#     def load_summary_report(self):
#         data = self.service.summary_report()
#         self.view.lbl_total_users.setText(f"Tổng số người dùng: {data['total_users']}")
#         self.view.lbl_total_activities.setText(f"Tổng số hành động: {data['total_activities']}")
#         self.view.lbl_total_actions.setText(f"Tổng số hành động tạo/sửa/xóa: {data['total_actions']}")



from views.report_view import ReportView
from services.report_service import ReportService
from PyQt6.QtWidgets import QTableWidgetItem, QFileDialog

class ReportController:
    def __init__(self):
        self.view = ReportView()
        self.service = ReportService()

        self.load_user_statistics()
        self.load_user_access_history()
        self.load_system_action_history()
        self.load_summary_report()

        # Kết nối nút xuất PDF
        self.view.btn_export_user_stats.clicked.connect(self.export_user_stats_pdf)
        self.view.btn_export_access.clicked.connect(self.export_access_pdf)
        self.view.btn_export_actions.clicked.connect(self.export_actions_pdf)
        self.view.btn_export_summary.clicked.connect(self.export_summary_pdf)

    # --- Load dữ liệu vào bảng ---
    def load_user_statistics(self):
        stats = self.service.user_statistics()
        table = self.view.tab_user_stats
        rows = []

        # By status
        for s in stats['by_status']:
            rows.append((f"Trạng thái {s['status']}", str(s['count'])))
        # By unit
        for u in stats['by_unit']:
            rows.append((f"Đơn vị {u['unit_id']}", str(u['count'])))

        table.setRowCount(len(rows))
        for r, (name, count) in enumerate(rows):
            table.setItem(r, 0, QTableWidgetItem(name))
            table.setItem(r, 1, QTableWidgetItem(count))

    def load_user_access_history(self):
        data = self.service.user_access_history()
        table = self.view.tab_access
        table.setRowCount(len(data))
        for r, row in enumerate(data):
            table.setItem(r, 0, QTableWidgetItem(row['fullname']))
            table.setItem(r, 1, QTableWidgetItem(row['activities']))
            table.setItem(r, 2, QTableWidgetItem(str(row['time'])))

    def load_system_action_history(self):
        data = self.service.system_action_history()
        table = self.view.tab_actions
        table.setRowCount(len(data))
        for r, row in enumerate(data):
            table.setItem(r, 0, QTableWidgetItem(row['fullname']))
            table.setItem(r, 1, QTableWidgetItem(row['activities']))
            table.setItem(r, 2, QTableWidgetItem(str(row['time'])))

    def load_summary_report(self):
        data = self.service.summary_report()
        self.view.lbl_total_users.setText(f"Tổng số người dùng: {data['total_users']}")
        self.view.lbl_total_activities.setText(f"Tổng số hành động: {data['total_activities']}")
        self.view.lbl_total_actions.setText(f"Tổng số hành động tạo/sửa/xóa: {data['total_actions']}")

    # --- Xuất PDF ---
    def export_user_stats_pdf(self):
        path, _ = QFileDialog.getSaveFileName(self.view, "Lưu PDF", "", "PDF Files (*.pdf)")
        if path:
            table = self.view.tab_user_stats
            headers = [table.horizontalHeaderItem(i).text() for i in range(table.columnCount())]
            rows = []
            for r in range(table.rowCount()):
                row_data = [table.item(r, c).text() if table.item(r, c) else "" for c in range(table.columnCount())]
                rows.append(row_data)
            self.service.export_pdf(path, "Thống kê người dùng", headers, rows)

    def export_access_pdf(self):
        path, _ = QFileDialog.getSaveFileName(self.view, "Lưu PDF", "", "PDF Files (*.pdf)")
        if path:
            table = self.view.tab_access
            headers = [table.horizontalHeaderItem(i).text() for i in range(table.columnCount())]
            rows = []
            for r in range(table.rowCount()):
                row_data = [table.item(r, c).text() if table.item(r, c) else "" for c in range(table.columnCount())]
                rows.append(row_data)
            self.service.export_pdf(path, "Lịch sử truy cập", headers, rows)

    def export_actions_pdf(self):
        path, _ = QFileDialog.getSaveFileName(self.view, "Lưu PDF", "", "PDF Files (*.pdf)")
        if path:
            table = self.view.tab_actions
            headers = [table.horizontalHeaderItem(i).text() for i in range(table.columnCount())]
            rows = []
            for r in range(table.rowCount()):
                row_data = [table.item(r, c).text() if table.item(r, c) else "" for c in range(table.columnCount())]
                rows.append(row_data)
            self.service.export_pdf(path, "Lịch sử tác động hệ thống", headers, rows)

    def export_summary_pdf(self):
        path, _ = QFileDialog.getSaveFileName(self.view, "Lưu PDF", "", "PDF Files (*.pdf)")
        if path:
            headers = ["Thông tin", "Giá trị"]
            data = [
                ["Tổng số người dùng", self.view.lbl_total_users.text().replace("Tổng số người dùng: ", "")],
                ["Tổng số hành động", self.view.lbl_total_activities.text().replace("Tổng số hành động: ", "")],
                ["Tổng số hành động tạo/sửa/xóa", self.view.lbl_total_actions.text().replace("Tổng số hành động tạo/sửa/xóa: ", "")]
            ]
            self.service.export_pdf(path, "Báo cáo tổng hợp", headers, data)

