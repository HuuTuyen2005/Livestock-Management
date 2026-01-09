# from database.mysql_connector import MySQLConnector

# class ReportService:
#     def __init__(self):
#         self.db = MySQLConnector()

#     # Thống kê người dùng theo status và unit
#     def user_statistics(self):
#         stats = {}
#         stats['by_status'] = self.db.fetch_all(
#             "SELECT status, COUNT(*) AS count FROM user GROUP BY status"
#         )
#         stats['by_unit'] = self.db.fetch_all(
#             "SELECT unit_id, COUNT(*) AS count FROM user GROUP BY unit_id"
#         )
#         stats['total'] = self.db.fetch_one(
#             "SELECT COUNT(*) AS total_users FROM user"
#         )
#         return stats

#     # Lịch sử truy cập tất cả user
#     def user_access_history(self):
#         return self.db.fetch_all("""
#             SELECT u.fullname, a.activities, a.time
#             FROM activities_history a
#             JOIN user u ON u.id = a.account_id
#             WHERE a.activities LIKE '%Đăng nhập%'
#             ORDER BY a.time DESC
#         """)

#     # Lịch sử tác động hệ thống (create/update/delete)
#     def system_action_history(self):
#         return self.db.fetch_all("""
#             SELECT u.fullname, a.activities, a.time
#             FROM activities_history a
#             JOIN user u ON u.id = a.account_id
#             WHERE a.activities NOT LIKE '%Đăng nhập%' 
#             ORDER BY a.time DESC
#         """)

#     # Báo cáo tổng hợp
#     def summary_report(self):
#         return self.db.fetch_one("""
#             SELECT
#                 (SELECT COUNT(*) FROM user) AS total_users,
#                 (SELECT COUNT(*) FROM activities_history) AS total_activities,
#                 (SELECT COUNT(*) FROM activities_history 
#                  WHERE activities LIKE 'create%' OR activities LIKE 'update%' OR activities LIKE 'delete%') AS total_actions
#         """)



from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from datetime import datetime
from database.mysql_connector import MySQLConnector
from datetime import datetime
import os

class ReportService:
    def __init__(self):
        self.db = MySQLConnector()
        base_dir = os.path.dirname(os.path.dirname(__file__))  # livestock_app/
        font_path = os.path.join(base_dir, "fonts", "DejaVuSans.ttf")
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Font không tồn tại: {font_path}")
        pdfmetrics.registerFont(TTFont("DejaVuSans", font_path))

    # Thống kê người dùng theo status và unit
    def user_statistics(self):
        stats = {}
        stats['by_status'] = self.db.fetch_all(
            "SELECT status, COUNT(*) AS count FROM user GROUP BY status"
        )
        stats['by_unit'] = self.db.fetch_all(
            "SELECT unit_id, COUNT(*) AS count FROM user GROUP BY unit_id"
        )
        stats['total'] = self.db.fetch_one(
            "SELECT COUNT(*) AS total_users FROM user"
        )
        return stats

    # Lịch sử truy cập tất cả user
    def user_access_history(self):
        return self.db.fetch_all("""
            SELECT u.fullname, a.activities, a.time
            FROM activities_history a
            JOIN user u ON u.id = a.account_id
            WHERE a.activities LIKE '%Đăng nhập%'
            ORDER BY a.time DESC
        """)

    # Lịch sử tác động hệ thống (create/update/delete)
    def system_action_history(self):
        return self.db.fetch_all("""
            SELECT u.fullname, a.activities, a.time
            FROM activities_history a
            JOIN user u ON u.id = a.account_id
            WHERE a.activities NOT LIKE '%Đăng nhập%' 
            ORDER BY a.time DESC
        """)

    # Báo cáo tổng hợp
    def summary_report(self):
        return self.db.fetch_one("""
            SELECT
                (SELECT COUNT(*) FROM user) AS total_users,
                (SELECT COUNT(*) FROM activities_history) AS total_activities,
                (SELECT COUNT(*) FROM activities_history 
                 WHERE activities NOT LIKE '%Đăng%') AS total_actions
        """)

    # Hàm xuất PDF
    def export_pdf(self, filename, title="Báo cáo", columns=None, data=None):
        """
        Xuất PDF với ReportLab Platypus.
        filename: đường dẫn file PDF
        title: tiêu đề báo cáo
        columns: list tên cột
        data: list of list hoặc list of dict
        """
        if not data:
            data = []

        doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=30,
            leftMargin=30,
            topMargin=50,
            bottomMargin=30
        )

        elements = []
        styles = getSampleStyleSheet()

        # Header
        elements.append(Paragraph(f"<b>{title}</b>", styles['Title']))
        elements.append(Paragraph(f"Ngày xuất: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        elements.append(Spacer(1, 12))

        # Chuẩn hóa dữ liệu table
        table_data = []
        if columns:
            table_data.append(columns)
        else:
            if data and isinstance(data[0], dict):
                table_data.append(list(data[0].keys()))
            elif data:
                table_data.append([f"Cột {i+1}" for i in range(len(data[0]))])
            else:
                table_data.append([])  # table trống

        for row in data:
            if isinstance(row, dict):
                table_data.append([row.get(col, "") for col in table_data[0]])
            else:  # list
                table_data.append(row)

        # Table style
        table = Table(table_data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightgreen),
            ('TEXTCOLOR', (0,0), (-1,0), colors.black),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('FONTNAME', (0,0), (-1,-1), 'DejaVuSans'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))

        elements.append(table)

        # Build PDF
        doc.build(elements)

        return filename
