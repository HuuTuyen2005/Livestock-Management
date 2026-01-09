from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox, QListWidgetItem
from views.feed_testing_facility_view import FeedTestingFacilityView
from dialogs.feed_testing_facility_dialog import FeedTestingFacilityDialog
from services.feed_testing_facility_service import FeedTestingFacilityService
from services.administrative_unit_service import AdministrativeUnitService
from services.food_service import FoodService
from services.activity_service import ActivityService
from auth.session import Session

class FeedTestingFacilityController:
    def __init__(self):
        self.view = FeedTestingFacilityView()
        self.service = FeedTestingFacilityService()
        self.food_service = FoodService()
        self.activity_service = ActivityService()
        self._connect()
        self.load_data()

    def show(self):
        self.view.show()

    def _connect(self):
        self.view.btn_search.clicked.connect(self.search)
        self.view.btn_refresh.clicked.connect(self.load_data)
        self.view.btn_add.clicked.connect(self.add)
        self.view.btn_edit.clicked.connect(self.edit)
        self.view.btn_delete.clicked.connect(self.delete)

    def load_data(self):
        self._render(self.service.get_all())

    def search(self):
        self._render(self.service.search(self.view.txt_search.text()))

    # ================= ADD =================
    def add(self):
        dialog = FeedTestingFacilityDialog()
        self._load_huyen_xa(dialog)
        self._load_food(dialog)

        if dialog.exec():
            data = self._collect_data(dialog)
            food_ids = self._collect_food(dialog)
            self.service.create(data, food_ids)

            if Session.current_user:
                self.activity_service.log(
                    Session.current_user["id"],
                    f"Thêm cơ sở kiểm nghiệm thức ăn: {data['name']}"
                )

            self.load_data()

    # ================= EDIT =================
    def edit(self):
        row = self.view.table.currentRow()
        if row < 0:
            return

        facility_id = int(self.view.table.item(row, 0).text())
        old_data = self.service.get_by_id(facility_id)
        dialog = FeedTestingFacilityDialog(old_data)

        self._load_huyen_xa(dialog, old_data["huyen_id"], old_data["xa_id"])
        self._load_food(dialog, self.service.get_food_ids(facility_id))

        if dialog.exec():
            self.service.update(
                facility_id,
                self._collect_data(dialog),
                self._collect_food(dialog)
            )

            if Session.current_user:
                self.activity_service.log(
                    Session.current_user["id"],
                    f"Cập nhật cơ sở kiểm nghiệm thức ăn: {old_data['name']}"
                )

            self.load_data()

    # ================= DELETE =================
    def delete(self):
        row = self.view.table.currentRow()
        if row < 0:
            return

        facility_id = int(self.view.table.item(row, 0).text())
        name = self.view.table.item(row, 1).text()

        self.service.delete(facility_id)

        if Session.current_user:
            self.activity_service.log(
                Session.current_user["id"],
                f"Xóa cơ sở kiểm nghiệm thức ăn: {name}"
            )

        self.load_data()

    # ================= TABLE =================
    def _render(self, data):
        t = self.view.table
        t.setRowCount(len(data))
        for r, i in enumerate(data):
            t.setItem(r, 0, QTableWidgetItem(str(i["id"])))
            t.setItem(r, 1, QTableWidgetItem(i["name"]))
            t.setItem(r, 2, QTableWidgetItem(i["huyen_name"] or ""))
            t.setItem(r, 3, QTableWidgetItem(i["xa_name"] or ""))
            t.setItem(r, 4, QTableWidgetItem(i["address"]))
            t.setItem(r, 5, QTableWidgetItem(i["phone"]))
            t.setItem(r, 6, QTableWidgetItem(i["email"]))
            t.setItem(r, 7, QTableWidgetItem(i["certification"]))
            t.setItem(r, 8, QTableWidgetItem(i["scale"]))
            t.setItem(r, 9, QTableWidgetItem(i["foods"] or ""))
            t.setItem(r, 10, QTableWidgetItem(
                "Hoạt động" if i["status"] == 1 else "Ngừng"
            ))

    # ================= ADMIN UNIT =================
    def _load_huyen_xa(self, dialog, huyen_id=None, xa_id=None):
        admin = AdministrativeUnitService()
        dialog.cbo_huyen.clear()
        for d in admin.get_districts():
            dialog.cbo_huyen.addItem(d["name"], d["id"])

        def load_xa():
            dialog.cbo_xa.clear()
            for x in admin.get_wards_by_district(dialog.cbo_huyen.currentData()):
                dialog.cbo_xa.addItem(x["name"], x["id"])

        dialog.cbo_huyen.currentIndexChanged.connect(load_xa)

        if huyen_id:
            dialog.cbo_huyen.setCurrentIndex(dialog.cbo_huyen.findData(huyen_id))
        load_xa()
        if xa_id:
            dialog.cbo_xa.setCurrentIndex(dialog.cbo_xa.findData(xa_id))

    # ================= FOOD =================
    def _load_food(self, dialog, selected_ids=None):
        dialog.lst_food.clear()
        for f in self.food_service.get_all():
            item = QListWidgetItem(f["name"])
            item.setData(1, f["id"])
            if selected_ids and f["id"] in selected_ids:
                item.setSelected(True)
            dialog.lst_food.addItem(item)

    def _collect_food(self, dialog):
        return [i.data(1) for i in dialog.lst_food.selectedItems()]

    # ================= COLLECT DATA =================
    def _collect_data(self, dialog):
        return {
            "name": dialog.txt_name.text(),
            "address": dialog.txt_address.text(),
            "phone": dialog.txt_phone.text(),
            "email": dialog.txt_email.text(),
            "certification": dialog.txt_certification.text(),
            "scale": dialog.cbo_scale.currentText(),
            "status": dialog.cbo_status.currentIndex(),
            "unit_id": dialog.cbo_xa.currentData()
        }
