from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox

from views.testing_facility_view import TestingFacilityView
from dialogs.testing_facility_dialog import TestingFacilityDialog

from services.testing_facility_service import TestingFacilityService
from services.administrative_unit_service import AdministrativeUnitService
from services.activity_service import ActivityService

from auth.session import Session


class TestingFacilityController:
    def __init__(self):
        self.view = TestingFacilityView()
        self.service = TestingFacilityService()
        self.log_service = ActivityService()

        self._connect()
        self.load_data()

    # ================= SHOW =================
    def show(self):
        self.view.show()

    # ================= CONNECT =================
    def _connect(self):
        self.view.btn_search.clicked.connect(self.search)
        self.view.btn_refresh.clicked.connect(self.load_data)
        self.view.btn_add.clicked.connect(self.add)
        self.view.btn_edit.clicked.connect(self.edit)
        self.view.btn_delete.clicked.connect(self.delete)

        # Double click = Edit
        self.view.table.itemDoubleClicked.connect(
            lambda _: self.edit()
        )

    # ================= LOAD =================
    def load_data(self):
        self._render(self.service.get_all())

    # ================= SEARCH =================
    def search(self):
        keyword = self.view.txt_search.text().strip()
        if not keyword:
            self.load_data()
            return
        self._render(self.service.search(keyword))

    # ================= ADD =================
    def add(self):
        dialog = TestingFacilityDialog()
        self._load_huyen_xa(dialog)

        if dialog.exec():
            data = self._collect(dialog)
            species_ids = dialog.get_selected_species_ids()

            self.service.create(data, species_ids)

            if Session.current_user:
                self.log_service.log(
                    Session.current_user["id"],
                    f"Thêm cơ sở khảo nghiệm thức ăn chăn nuôi: {data['name']}"
                )

            self.load_data()

    # ================= EDIT =================
    def edit(self):
        row = self.view.table.currentRow()
        if row < 0:
            QMessageBox.warning(self.view, "Cảnh báo", "Vui lòng chọn một dòng")
            return

        facility_id = int(self.view.table.item(row, 0).text())
        data = self.service.get_by_id(facility_id)
        species_ids = self.service.get_species_ids(facility_id)

        dialog = TestingFacilityDialog(data, species_ids)
        self._load_huyen_xa(dialog)

        if dialog.exec():
            update_data = self._collect(dialog)
            new_species_ids = dialog.get_selected_species_ids()

            self.service.update(
                facility_id,
                update_data,
                new_species_ids
            )

            if Session.current_user:
                self.log_service.log(
                    Session.current_user["id"],
                    f"Cập nhật cơ sở khảo nghiệm thức ăn chăn nuôi (ID={facility_id}): {update_data['name']}"
                )

            self.load_data()

    # ================= DELETE =================
    def delete(self):
        row = self.view.table.currentRow()
        if row < 0:
            QMessageBox.warning(self.view, "Cảnh báo", "Vui lòng chọn một dòng")
            return

        facility_id = int(self.view.table.item(row, 0).text())

        if QMessageBox.question(
            self.view,
            "Xác nhận",
            "Bạn có chắc chắn muốn xoá cơ sở này?"
        ) != QMessageBox.StandardButton.Yes:
            return

        data = self.service.get_by_id(facility_id)
        self.service.delete(facility_id)

        if Session.current_user:
            self.log_service.log(
                Session.current_user["id"],
                f"Xoá cơ sở khảo nghiệm thức ăn chăn nuôi (ID={facility_id}): {data['name']}"
            )

        self.load_data()

    # ================= HELPERS =================
    def _collect(self, dialog):
        return {
            "name": dialog.txt_name.text(),
            "address": dialog.txt_address.text(),
            "phone": dialog.txt_phone.text(),
            "email": dialog.txt_email.text(),
            "scale": dialog.cbo_scale.currentText(),
            "status": dialog.cbo_status.currentIndex(),
            "unit_id": dialog.cbo_xa.currentData()
        }

    def _render(self, data):
        t = self.view.table
        t.setRowCount(len(data))
        for r, i in enumerate(data):
            t.setItem(r, 0, QTableWidgetItem(str(i["id"])))
            t.setItem(r, 1, QTableWidgetItem(i["name"]))
            t.setItem(r, 2, QTableWidgetItem(i["huyen_name"] or ""))
            t.setItem(r, 3, QTableWidgetItem(i["xa_name"] or ""))
            t.setItem(r, 4, QTableWidgetItem(i["species_names"] or ""))
            t.setItem(r, 5, QTableWidgetItem(i["phone"] or ""))
            t.setItem(r, 6, QTableWidgetItem(i["scale"] or ""))
            t.setItem(
                r, 7,
                QTableWidgetItem(
                    "Hoạt động" if i["status"] == 1 else "Ngừng"
                )
            )

    def _load_huyen_xa(self, dialog):
        admin = AdministrativeUnitService()
        dialog.cbo_huyen.clear()

        for d in admin.get_districts():
            dialog.cbo_huyen.addItem(d["name"], d["id"])

        def load_xa():
            dialog.cbo_xa.clear()
            huyen_id = dialog.cbo_huyen.currentData()
            if not huyen_id:
                return
            wards = admin.get_wards_by_district(huyen_id)
            for w in wards:
                dialog.cbo_xa.addItem(w["name"], w["id"])

        dialog.cbo_huyen.currentIndexChanged.connect(load_xa)
        load_xa()
