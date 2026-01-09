from services.species_service import SpeciesService
from views.species_view import SpeciesView
from views.species_dialog import SpeciesDialog
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from services.activity_service import ActivityService
from auth.session import Session

class SpeciesController:
    def __init__(self):
        self.view = SpeciesView()
        self.service = SpeciesService()
        self.log_service = ActivityService()

        self.load_data()

        self.view.btn_add.clicked.connect(self.add)
        self.view.btn_edit.clicked.connect(self.edit)
        self.view.btn_delete.clicked.connect(self.delete)

        self.view.btn_search.clicked.connect(self.on_search)
        self.view.txt_search.returnPressed.connect(self.on_search)

        self.view.btn_refresh.clicked.connect(self.refresh)

    def load_data(self):
        data = self.service.get_all()
        self.view.table.setRowCount(len(data))

        for r, s in enumerate(data):
            self.view.table.setItem(r, 0, QTableWidgetItem(str(s["id"])))
            self.view.table.setItem(r, 1, QTableWidgetItem(s["name"]))
            self.view.table.setItem(r, 2, QTableWidgetItem(s["scientific_name"]))
            self.view.table.setItem(r, 3, QTableWidgetItem(s["conservation_status"] or ""))
            self.view.table.setItem(r, 4, QTableWidgetItem(s["export_restriction_status"] or ""))
            
    def load_table(self, data):
        self.view.table.setRowCount(len(data))

        for r, s in enumerate(data):
            self.view.table.setItem(r, 0, QTableWidgetItem(str(s["id"])))
            self.view.table.setItem(r, 1, QTableWidgetItem(s["name"]))
            self.view.table.setItem(r, 2, QTableWidgetItem(s["scientific_name"]))
            self.view.table.setItem(r, 3, QTableWidgetItem(s["conservation_status"] or ""))
            self.view.table.setItem(r, 4, QTableWidgetItem(s["export_restriction_status"] or ""))


    def get_selected_id(self):
        row = self.view.table.currentRow()
        if row < 0:
            return None
        return int(self.view.table.item(row, 0).text())
    
    def add(self):
        dlg = SpeciesDialog()
        dlg.btn_save.clicked.connect(lambda: self.save_new(dlg))
        dlg.exec()

    def save_new(self, dlg):
        self.service.create(
            dlg.txt_name.text(),
            dlg.txt_scientific.text(),
            dlg.txt_conservation.text(),
            dlg.txt_export.text()
        )

        self.log_service.log(
            Session.current_user["id"],
            "Thêm giống vật nuôi"
        )

        dlg.accept()
        self.load_data()

    def edit(self):
        row = self.view.table.currentRow()
        if row < 0:
            return

        data = {
            "id": int(self.view.table.item(row, 0).text()),
            "name": self.view.table.item(row, 1).text(),
            "scientific_name": self.view.table.item(row, 2).text(),
            "conservation_status": self.view.table.item(row, 3).text(),
            "export_restriction_status": self.view.table.item(row, 4).text()
        }

        dlg = SpeciesDialog(data)
        dlg.btn_save.clicked.connect(lambda: self.save_edit(dlg, data["id"]))
        dlg.exec()

    def save_edit(self, dlg, species_id):
        self.service.update(
            species_id,
            dlg.txt_name.text(),
            dlg.txt_scientific.text(),
            dlg.txt_conservation.text(),
            dlg.txt_export.text()
        )

        self.log_service.log(
            Session.current_user["id"],
            f"Sửa giống ID={species_id}"
        )

        dlg.accept()
        self.load_data()

    # def delete(self):
    #     sid = self.get_selected_id()
    #     if not sid:
    #         return

    #     if QMessageBox.question(
    #         self.view,
    #         "Xác nhận",
    #         "Xoá giống này?"
    #     ) == QMessageBox.StandardButton.Yes:
    #         self.service.delete(sid)

    #         self.log_service.log(
    #             Session.current_user["id"],
    #             f"Xoá giống ID={sid}"
    #         )

    #         self.load_data()

    def delete(self):
        sid = self.get_selected_id()
        if not sid:
            return

        # kiểm tra đang được sử dụng
        if self.service.is_used(sid):
            QMessageBox.warning(
                self.view,
                "Không thể xoá",
                "Giống này đang được sử dụng bởi cơ sở chăn nuôi.\n"
                "Vui lòng xoá liên kết trước."
            )
            return

        if QMessageBox.question(
            self.view,
            "Xác nhận",
            "Xoá giống này?"
        ) != QMessageBox.StandardButton.Yes:
            return

        try:
            self.service.delete(sid)

            self.log_service.log(
                Session.current_user["id"],
                f"Xoá giống ID={sid}"
            )

            self.load_data()

        except Exception as e:
            QMessageBox.warning(
                self.view,
                "Lỗi",
                f"Không thể xoá giống này.\nChi tiết: {str(e)}"
            )



    def on_search(self):
        keyword = self.view.txt_search.text().strip()

        if not keyword:
            self.load_data()
            return
        
        data = self.service.search(keyword)
        self.load_table(data)

    def refresh(self):
        self.view.txt_search.clear()
        self.load_data()