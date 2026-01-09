from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from services.food_service import FoodService
from views.food_view import FoodView
from views.food_dialog import FoodDialog
from services.activity_service import ActivityService
from auth.session import Session

class FoodController:
    def __init__(self):
        self.view = FoodView()
        self.service = FoodService()
        self.log_service = ActivityService()

        self.load_data()

        self.view.btn_add.clicked.connect(self.add)
        self.view.btn_edit.clicked.connect(self.edit)
        self.view.btn_delete.clicked.connect(self.delete)
        self.view.btn_search.clicked.connect(self.search)
        self.view.txt_search.returnPressed.connect(self.search)
        self.view.btn_refresh.clicked.connect(self.refresh)

    def load_data(self):
        data = self.service.get_all_with_substances()
        self.load_table(data)

    def load_table(self, data):
        self.view.table.setRowCount(len(data))
        for r, f in enumerate(data):
            self.view.table.setItem(r, 0, QTableWidgetItem(str(f["id"])))
            self.view.table.setItem(r, 1, QTableWidgetItem(f["name"]))
            self.view.table.setItem(r, 2, QTableWidgetItem(f["type"]))
            self.view.table.setItem(
                r, 3,
                QTableWidgetItem(f["description"] or "")
            )
            self.view.table.setItem(
                r, 4,
                QTableWidgetItem(f["substances"] or "")
            )

    def get_selected_id(self):
        row = self.view.table.currentRow()
        if row < 0:
            return None
        return int(self.view.table.item(row, 0).text())



    def delete(self):
        food_id = self.get_selected_id()
        if not food_id:
            return

        if QMessageBox.question(
            self.view,
            "Xác nhận",
            "Xoá thức ăn này?"
        ) != QMessageBox.StandardButton.Yes:
            return

        try:
            self.service.delete(food_id)

            self.log_service.log(
                Session.current_user["id"],
                f"Xoá thức ăn ID={food_id}"
            )

            self.load_data()

        except Exception as e:
            QMessageBox.warning(
                self.view,
                "Lỗi",
                f"Không thể xoá thức ăn này.\nChi tiết: {str(e)}"
            )


    def search(self):
        keyword = self.view.txt_search.text().strip()
        if not keyword:
            self.load_data()
            return

        self.load_table(self.service.search(keyword))

    def refresh(self):
        self.view.txt_search.clear()
        self.load_data()

    def add(self):
        dlg = FoodDialog(
            substances=self.service.get_substances()
        )
        dlg.btn_save.clicked.connect(lambda: self.save_new(dlg))
        dlg.exec()

    def save_new(self, dlg):
        if not dlg.txt_name.text().strip():
            QMessageBox.warning(dlg, "Lỗi", "Tên thức ăn không được trống")
            return

        self.service.create(
            dlg.txt_name.text(),
            dlg.txt_type.text(),
            dlg.txt_description.toPlainText()
        )

        # lấy food_id mới nhất
        food_id = self.service.db.fetch_one(
            "SELECT MAX(id) AS id FROM food"
        )["id"]

        self.service.save_substances(
            food_id,
            dlg.get_selected_substances()
        )

        self.log_service.log(
            Session.current_user["id"],
            "Thêm thức ăn + chất"
        )

        dlg.accept()
        self.load_data()

    def edit(self):
        row = self.view.table.currentRow()
        if row < 0:
            return

        food_id = int(self.view.table.item(row, 0).text())

        data = {
            "id": food_id,
            "name": self.view.table.item(row, 1).text(),
            "type": self.view.table.item(row, 2).text(),
            "description": self.view.table.item(row, 3).text()
        }

        dlg = FoodDialog(
            data=data,
            substances=self.service.get_substances(),
            selected_substances=self.service.get_selected_substances(food_id)
        )

        dlg.btn_save.clicked.connect(
            lambda: self.save_edit(dlg, food_id)
        )
        dlg.exec()

    def save_edit(self, dlg, food_id):
        self.service.update(
            food_id,
            dlg.txt_name.text(),
            dlg.txt_type.text(),
            dlg.txt_description.toPlainText()
        )

        self.service.save_substances(
            food_id,
            dlg.get_selected_substances()
        )

        self.log_service.log(
            Session.current_user["id"],
            f"Sửa thức ăn ID={food_id}"
        )

        dlg.accept()
        self.load_data()

    # def add(self):
    #     dlg = FoodDialog()
    #     dlg.btn_save.clicked.connect(lambda: self.save_new(dlg))
    #     dlg.exec()

    # def save_new(self, dlg):
    #     if not dlg.txt_name.text().strip():
    #         QMessageBox.warning(dlg, "Lỗi", "Tên thức ăn không được trống")
    #         return

    #     self.service.create(
    #         dlg.txt_name.text(),
    #         dlg.txt_type.text(),
    #         dlg.txt_description.toPlainText()
    #     )

    #     self.log_service.log(
    #         Session.current_user["id"],
    #         "Thêm thức ăn"
    #     )

    #     dlg.accept()
    #     self.load_data()

    # def edit(self):
    #     row = self.view.table.currentRow()
    #     if row < 0:
    #         return

    #     data = {
    #         "id": int(self.view.table.item(row, 0).text()),
    #         "name": self.view.table.item(row, 1).text(),
    #         "type": self.view.table.item(row, 2).text(),
    #         "description": self.view.table.item(row, 3).text()
    #     }

    #     dlg = FoodDialog(data)
    #     dlg.btn_save.clicked.connect(
    #         lambda: self.save_edit(dlg, data["id"])
    #     )
    #     dlg.exec()

    # def save_edit(self, dlg, food_id):
    #     self.service.update(
    #         food_id,
    #         dlg.txt_name.text(),
    #         dlg.txt_type.text(),
    #         dlg.txt_description.toPlainText()
    #     )

    #     self.log_service.log(
    #         Session.current_user["id"],
    #         f"Sửa thức ăn ID={food_id}"
    #     )

    #     dlg.accept()
    #     self.load_data()