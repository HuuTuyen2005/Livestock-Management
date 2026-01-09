# from services.gen_service import GenService
# from views.gen_view import GenView
# from views.gen_dialog import GenDialog
# from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
# from services.activity_service import ActivityService
# from auth.session import Session

# class GenController:
#     def __init__(self):
#         self.view = GenView()
#         self.service = GenService()
#         self.log_service = ActivityService()

#         self.load_data()

#         self.view.btn_add.clicked.connect(self.add)
#         self.view.btn_edit.clicked.connect(self.edit)
#         self.view.btn_delete.clicked.connect(self.delete)

#         self.view.btn_search.clicked.connect(self.search)
#         self.view.txt_search.returnPressed.connect(self.search)

#         self.view.btn_refresh.clicked.connect(self.refresh)

#     def load_data(self):
#         data = self.service.get_all()
#         self.view.table.setRowCount(len(data))

#         for r, s in enumerate(data):
#             self.view.table.setItem(r, 0, QTableWidgetItem(str(s["id"])))
#             self.view.table.setItem(r, 1, QTableWidgetItem(s["name"]))
#             self.view.table.setItem(r, 2, QTableWidgetItem(s["description"]))
#             self.view.table.setItem(r, 3, QTableWidgetItem(s["origin"] or ""))
#             self.view.table.setItem(r, 4, QTableWidgetItem(s["genetic_code" or ""]))
#             # self.view.table.setItem(r, 5, QTableWidgetItem(s["status" or ""]))
#             status_text = "Hoạt động" if s["status"] == 1 else "Ngừng"
#             self.view.table.setItem(r, 5, QTableWidgetItem(status_text))

#     def load_table(self, data):
#         self.view.table.setRowCount(len(data))

#         for r, s in enumerate(data):
#             self.view.table.setItem(r, 0, QTableWidgetItem(str(s["id"])))
#             self.view.table.setItem(r, 1, QTableWidgetItem(s["name"]))
#             self.view.table.setItem(r, 2, QTableWidgetItem(s["description"]))
#             self.view.table.setItem(r, 3, QTableWidgetItem(s["origin"] or ""))
#             self.view.table.setItem(r, 4, QTableWidgetItem(s["genetic_code" or ""]))
#             # self.view.table.setItem(r, 5, QTableWidgetItem(s["status"] or ""))
#             status_text = "Hoạt động" if s["status"] == 1 else "Ngừng"
#             self.view.table.setItem(r, 5, QTableWidgetItem(status_text))
    
#     def get_selected_id(self):
#         row = self.view.table.currentRow()
#         # if row < 0:
#         #     return None
#         # return int(self.view.table.item(row, 0).text())
#         item = self.view.table.item(row, 0)
#         if not item:
#             return None
#         return int(item.text())

#     def add(self):
#         dlg = GenDialog()
#         dlg.btn_save.clicked.connect(lambda: self.save_new(dlg))
#         dlg.exec()
    
#     def save_new(self, dlg):
#         if not dlg.txt_name.text().strip():
#             QMessageBox.warning(dlg, "Lỗi", "Tên gen không được để trống")
#             return 
        
#         self.service.create(
#             dlg.txt_name.text(),
#             dlg.txt_description.text(),
#             dlg.txt_origin.text(),
#             dlg.txt_genetic_code.text(), 
#             dlg.cbo_status.currentData() 
#         )

#         self.log_service.log(
#             Session.current_user["id"],
#             "Thêm nguồn gen"
#         )

#         dlg.accept()
#         self.load_data()
    
#     def edit(self):
#         row = self.view.table.currentRow()
#         if row < 0:
#             return
    
#         data = {
#             "id": int(self.view.table.item(row, 0).text()),
#             "name": self.view.table.item(row, 1).text(),
#             "description": self.view.table.item(row, 2).text(),
#             "origin": self.view.table.item(row, 3).text(),
#             "genetic_code": self.view.table.item(row, 4).text(),
#             "status": self.view.table.item(row, 5).text()
#         }

#         dlg = GenDialog(data)
#         dlg.btn_save.clicked.connect(lambda: self.save_edit(dlg, data["id"]))
#         dlg.exec()

#     def save_edit(self, dlg, gen_id):
#         self.service.update(
#             gen_id,
#             dlg.txt_name.text(),
#             dlg.txt_description.text(),
#             dlg.txt_origin.text(),
#             dlg.txt_genetic_code.text(), 
#             dlg.cbo_status.currentData() 
#         )

#         self.log_service.log(
#             Session.current_user["id"],
#             f"Sửa nguồn gen ID={gen_id}"
#         )

#         dlg.accept()
#         self.load_data()
    
#     def delete(self):
#         sid = self.get_selected_id()
#         if not sid:
#             return

#         if QMessageBox.question(
#             self.view,
#             "Xác nhận",
#             "Xoá gen này?"            
#         ) == QMessageBox.StandardButton.Yes:
#             self.service.delete(sid)

#             self.log_service.log(
#                 Session.current_user["id"],
#                 f"Xoá gen ID={sid}"
#             )

#             self.load_data()
#     def search(self):
#         keyword = self.view.txt_search.text().strip()

#         if not keyword:
#             self.load_data()
#             return
        
#         data = self.service.search(keyword)
#         self.load_table(data)
    
#     def refresh(self):
#         self.view.txt_search.clear()
#         self.load_data()



from services.gen_service import GenService
from views.gen_view import GenView
from views.gen_dialog import GenDialog
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from services.activity_service import ActivityService
from auth.session import Session

STATUS_MAP = {
    0: "Bình thường",
    1: "Đang bảo tồn"
}

STATUS_TEXT_TO_VALUE = {
    "Bình thường": 0,
    "Đang bảo tồn": 1
}


class GenController:
    def __init__(self):
        self.view = GenView()
        self.service = GenService()
        self.log_service = ActivityService()

        self.load_data()

        self.view.btn_add.clicked.connect(self.add)
        self.view.btn_edit.clicked.connect(self.edit)
        self.view.btn_delete.clicked.connect(self.delete)

        self.view.btn_search.clicked.connect(self.search)
        self.view.txt_search.returnPressed.connect(self.search)

        self.view.btn_refresh.clicked.connect(self.refresh)

    # ================= LOAD TABLE =================
    def load_data(self):
        self.load_table(self.service.get_all())

    def load_table(self, data):
        self.view.table.setRowCount(len(data))

        for r, s in enumerate(data):
            self.view.table.setItem(r, 0, QTableWidgetItem(str(s["id"])))
            self.view.table.setItem(r, 1, QTableWidgetItem(s["name"]))
            self.view.table.setItem(r, 2, QTableWidgetItem(s["description"] or ""))
            self.view.table.setItem(r, 3, QTableWidgetItem(s["origin"] or ""))
            self.view.table.setItem(r, 4, QTableWidgetItem(s["genetic_code"] or ""))

            status_text = STATUS_MAP.get(s["status"], "")
            self.view.table.setItem(r, 5, QTableWidgetItem(status_text))

    # ================= COMMON =================
    def get_selected_id(self):
        row = self.view.table.currentRow()
        item = self.view.table.item(row, 0)
        if not item:
            return None
        return int(item.text())

    # ================= ADD =================
    def add(self):
        dlg = GenDialog()
        dlg.btn_save.clicked.connect(lambda: self.save_new(dlg))
        dlg.exec()

    def save_new(self, dlg):
        if not dlg.txt_name.text().strip():
            QMessageBox.warning(dlg, "Lỗi", "Tên gen không được để trống")
            return

        self.service.create(
            dlg.txt_name.text(),
            dlg.txt_description.text(),
            dlg.txt_origin.text(),
            dlg.txt_genetic_code.text(),
            dlg.cbo_status.currentData()   # INT 0/1
        )

        self.log_service.log(
            Session.current_user["id"],
            "Thêm nguồn gen"
        )

        dlg.accept()
        self.load_data()

    # ================= EDIT =================
    def edit(self):
        row = self.view.table.currentRow()
        if row < 0:
            return

        status_text = self.view.table.item(row, 5).text()

        data = {
            "id": int(self.view.table.item(row, 0).text()),
            "name": self.view.table.item(row, 1).text(),
            "description": self.view.table.item(row, 2).text(),
            "origin": self.view.table.item(row, 3).text(),
            "genetic_code": self.view.table.item(row, 4).text(),
            "status": STATUS_TEXT_TO_VALUE.get(status_text, 0)
        }

        dlg = GenDialog(data)
        dlg.btn_save.clicked.connect(lambda: self.save_edit(dlg, data["id"]))
        dlg.exec()

    def save_edit(self, dlg, gen_id):
        self.service.update(
            gen_id,
            dlg.txt_name.text(),
            dlg.txt_description.text(),
            dlg.txt_origin.text(),
            dlg.txt_genetic_code.text(),
            dlg.cbo_status.currentData()   # INT 0/1
        )

        self.log_service.log(
            Session.current_user["id"],
            f"Sửa nguồn gen ID={gen_id}"
        )

        dlg.accept()
        self.load_data()

    # ================= DELETE =================
    def delete(self):
        sid = self.get_selected_id()
        if not sid:
            return

        if QMessageBox.question(
            self.view,
            "Xác nhận",
            "Xoá gen này?"
        ) == QMessageBox.StandardButton.Yes:

            self.service.delete(sid)

            self.log_service.log(
                Session.current_user["id"],
                f"Xoá gen ID={sid}"
            )

            self.load_data()

    # ================= SEARCH / REFRESH =================
    def search(self):
        keyword = self.view.txt_search.text().strip()
        if not keyword:
            self.load_data()
            return

        self.load_table(self.service.search(keyword))

    def refresh(self):
        self.view.txt_search.clear()
        self.load_data()
