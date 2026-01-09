# from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
# from services.substance_service import SubstanceService
# from services.activity_service import ActivityService
# from views.substance_view import SubstanceView
# from views.substance_dialog import SubstanceDialog
# from auth.session import Session


# class SubstanceController:
#     def __init__(self):
#         self.view = SubstanceView()
#         self.service = SubstanceService()
#         self.log = ActivityService()

#         self.load_data()

#         self.view.btn_add.clicked.connect(self.add)
#         self.view.btn_edit.clicked.connect(self.edit)
#         self.view.btn_delete.clicked.connect(self.delete)
#         self.view.btn_search.clicked.connect(self.search)
#         self.view.btn_refresh.clicked.connect(self.refresh)

#     def load_data(self):
#         self._load_table(self.service.get_all())

#     def search(self):
#         keyword = self.view.txt_search.text().strip()

#         if not keyword:
#             self.load_data()
#             return
        
#         data = self.service.search(keyword)
#         self._load_table(data)

#     def refresh(self):
#         self.view.txt_search.clear()
#         self.load_data()

#     def add(self):
#         dlg = SubstanceDialog()
#         dlg.btn_save.clicked.connect(lambda: self.save_new(dlg))
#         dlg.exec()

#     def edit(self):
#         row = self.view.table.currentRow()
#         if row < 0:
#             return

#         sid = int(self.view.table.item(row, 0).text())
#         dlg = SubstanceDialog(self.service.get_by_id(sid))
#         dlg.btn_save.clicked.connect(lambda: self.save_edit(dlg, sid))
#         dlg.exec()

#     def delete(self):
#         row = self.view.table.currentRow()
#         if row < 0:
#             return

#         sid = int(self.view.table.item(row, 0).text())
#         if QMessageBox.question(self.view, "Xác nhận", "Xoá chất này?") \
#                 == QMessageBox.StandardButton.Yes:
#             self.service.delete(sid)
#             self.load_data()

#     # ===== SAVE =====
#     def save_new(self, dlg):
#         self.service.create(self._form(dlg))
#         self.log.log(Session.current_user["id"], "Thêm substance")
#         dlg.accept()
#         self.load_data()

#     def save_edit(self, dlg, sid):
#         self.service.update(sid, self._form(dlg))
#         self.log.log(Session.current_user["id"], f"Sửa substance ID={sid}")
#         dlg.accept()
#         self.load_data()

#     def _form(self, dlg):
#         return {
#             "name": dlg.txt_name.text(),
#             "type": dlg.txt_type.text(),
#             "description": dlg.txt_desc.text(),
#             "banned": dlg.cbo_banned.currentData()
#         }

#     def _load_table(self, data):
#         self.view.table.setRowCount(len(data))
#         for r, s in enumerate(data):
#             self.view.table.setItem(r, 0, QTableWidgetItem(str(s["id"])))
#             self.view.table.setItem(r, 1, QTableWidgetItem(s["name"]))
#             self.view.table.setItem(r, 2, QTableWidgetItem(s["type"]))
#             self.view.table.setItem(r, 3, QTableWidgetItem(s["description"] or ""))
#             self.view.table.setItem(
#                 r, 4,
#                 QTableWidgetItem("Có" if s["banned"] else "Không")
#             )

from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from services.substance_service import SubstanceService
from views.substance_view import SubstanceView
from views.substance_dialog import SubstanceDialog
from services.activity_service import ActivityService
from auth.session import Session

class SubstanceController:
    def __init__(self):
        self.view = SubstanceView()
        self.service = SubstanceService()
        self.log = ActivityService()

        self._connect()
        self.load_data()

    def show(self):
        self.view.show()

    def _connect(self):
        self.view.btn_search.clicked.connect(self.search)
        self.view.btn_refresh.clicked.connect(self.refresh)
        self.view.cbo_filter.currentIndexChanged.connect(self.on_filter_changed)
        self.view.btn_add.clicked.connect(self.add)
        self.view.btn_edit.clicked.connect(self.edit)
        self.view.btn_delete.clicked.connect(self.delete)
    
    def on_filter_changed(self):
        keyword = self.view.txt_search.text().strip()
        if keyword:
            self.search()
        else:
            self.load_data()


    def _get_filter(self):
        idx = self.view.cbo_filter.currentIndex()
        if idx == 1:
            return 0
        if idx == 2:
            return 1
        return None

    def load_data(self):
        data = self.service.get_all(self._get_filter())
        self._render(data)

    def search(self):
        keyword = self.view.txt_search.text()
        data = self.service.search(keyword, self._get_filter())
        self._render(data)

    def refresh(self):
        self.view.txt_search.clear()
        self.view.cbo_filter.setCurrentIndex(0)
        self.load_data()

    def _render(self, data):
        t = self.view.table
        t.setRowCount(len(data))
        for r, s in enumerate(data):
            t.setItem(r, 0, QTableWidgetItem(str(s["id"])))
            t.setItem(r, 1, QTableWidgetItem(s["name"]))
            t.setItem(r, 2, QTableWidgetItem(s["type"]))
            t.setItem(r, 3, QTableWidgetItem(s["description"] or ""))
            t.setItem(
                r, 4,
                QTableWidgetItem(
                    "Bị cấm" if s["banned"] == 1 else "Được phép"
                )
            )

    def _selected_id(self):
        row = self.view.table.currentRow()
        if row < 0:
            return None
        return int(self.view.table.item(row, 0).text())

    def add(self):
        dlg = SubstanceDialog()
        if dlg.exec():
            data = {
                "name": dlg.txt_name.text(),
                "type": dlg.txt_type.text(),
                "description": dlg.txt_desc.toPlainText(),
                "banned": dlg.cbo_banned.currentIndex()
            }
            self.service.create(data)
            self.log.log(Session.current_user["id"], f"Thêm nguyên liệu: {data['name']}")
            self.load_data()

    def edit(self):
        sid = self._selected_id()
        if not sid:
            return

        row = self.view.table.currentRow()
        data = {
            "name": self.view.table.item(row, 1).text(),
            "type": self.view.table.item(row, 2).text(),
            "description": self.view.table.item(row, 3).text(),
            "banned": 1 if self.view.table.item(row, 4).text() == "Bị cấm" else 0
        }

        dlg = SubstanceDialog(data)
        if dlg.exec():
            data["name"] = dlg.txt_name.text()
            data["type"] = dlg.txt_type.text()
            data["description"] = dlg.txt_desc.toPlainText()
            data["banned"] = dlg.cbo_banned.currentIndex()
            self.service.update(sid, data)
            self.log.log(Session.current_user["id"], f"Sửa nguyên liệu ID={sid}")
            self.load_data()

    def delete(self):
        sid = self._selected_id()
        if not sid:
            return

        if QMessageBox.question(
            self.view, "Xác nhận", "Xóa mục này?"
        ) == QMessageBox.StandardButton.Yes:
            self.service.delete(sid)
            self.log.log(Session.current_user["id"], f"Xóa nguyên liệu ID={sid}")
            self.load_data()
