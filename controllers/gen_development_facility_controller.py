from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from views.gen_development_facility_view import GenDevelopmentFacilityView
from dialogs.gen_collection_facility_dialog import GenCollectionFacilityDialog
from services.gen_development_facility_service import GenDevelopmentFacilityService
from services.gen_service import GenService
from services.administrative_unit_service import AdministrativeUnitService
from services.activity_service import ActivityService
from auth.session import Session


class GenDevelopmentFacilityController:
    def __init__(self):
        self.view = GenDevelopmentFacilityView()
        self.service = GenDevelopmentFacilityService()
        self.gen_service = GenService()
        self.activity_service = ActivityService()
        self._connect_events()
        self.load_data()

    def show(self):
        self.view.show()

    def _connect_events(self):
        self.view.btn_search.clicked.connect(self.search)
        self.view.txt_search.returnPressed.connect(self.search)
        self.view.btn_refresh.clicked.connect(self.load_data)
        self.view.btn_add.clicked.connect(self.add)
        self.view.btn_edit.clicked.connect(self.edit)
        self.view.btn_delete.clicked.connect(self.delete)

    def load_data(self):
        self._render_table(self.service.get_all())

    def search(self):
        self._render_table(
            self.service.search(self.view.txt_search.text())
        )

    # ================= ADD =================
    def add(self):
        gens = self.gen_service.get_all()
        dialog = GenCollectionFacilityDialog(gens=gens)
        self._load_huyen_xa(dialog)

        if dialog.exec():
            data = {
                "name": dialog.txt_name.text(),
                "address": dialog.txt_address.text(),
                "phone": dialog.txt_phone.text(),
                "email": dialog.txt_email.text(),
                "certification": dialog.txt_certification.text(),
                "scale": dialog.cbo_scale.currentText(),
                "status": dialog.cbo_status.currentIndex(),
                "unit_id": dialog.cbo_xa.currentData()
            }

            self.service.create(data, dialog.get_selected_gens())

            if Session.current_user:
                self.activity_service.log(
                    Session.current_user["id"],
                    f"Thêm cơ sở phát triển nguồn gen: {data['name']}"
                )

            self.load_data()

    # ================= EDIT =================
    def edit(self):
        row = self.view.table.currentRow()
        if row < 0:
            QMessageBox.warning(self.view, "Cảnh báo", "Vui lòng chọn dòng")
            return

        facility_id = int(self.view.table.item(row, 0).text())
        old_data = self.service.get_by_id(facility_id)
        gens = self.gen_service.get_all()

        dialog = GenCollectionFacilityDialog(old_data, gens)
        self._load_huyen_xa(dialog, old_data["huyen_id"], old_data["xa_id"])

        if dialog.exec():
            update_data = {
                "name": dialog.txt_name.text(),
                "address": dialog.txt_address.text(),
                "phone": dialog.txt_phone.text(),
                "email": dialog.txt_email.text(),
                "certification": dialog.txt_certification.text(),
                "scale": dialog.cbo_scale.currentText(),
                "status": dialog.cbo_status.currentIndex(),
                "unit_id": dialog.cbo_xa.currentData()
            }

            self.service.update(
                facility_id,
                update_data,
                dialog.get_selected_gens()
            )

            if Session.current_user:
                self.activity_service.log(
                    Session.current_user["id"],
                    f"Cập nhật cơ sở phát triển nguồn gen: {old_data['name']}"
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
                f"Xóa cơ sở phát triển nguồn gen: {name}"
            )

        self.load_data()

    # ================= TABLE =================
    def _render_table(self, data):
        table = self.view.table
        table.setRowCount(len(data))

        for r, item in enumerate(data):
            table.setItem(r, 0, QTableWidgetItem(str(item["id"])))
            table.setItem(r, 1, QTableWidgetItem(item["name"]))
            table.setItem(r, 2, QTableWidgetItem(item["huyen_name"] or ""))
            table.setItem(r, 3, QTableWidgetItem(item["xa_name"] or ""))
            table.setItem(r, 4, QTableWidgetItem(item["gen_names"] or ""))
            table.setItem(r, 5, QTableWidgetItem(item["address"]))
            table.setItem(r, 6, QTableWidgetItem(item["phone"]))
            table.setItem(r, 7, QTableWidgetItem(item["email"]))
            table.setItem(r, 8, QTableWidgetItem(item["certification"]))
            table.setItem(r, 9, QTableWidgetItem(item["scale"]))
            table.setItem(
                r, 10,
                QTableWidgetItem(
                    "Hoạt động" if item["status"] == 1 else "Ngừng"
                )
            )

    # ================= ADMIN UNIT =================
    def _load_huyen_xa(self, dialog, selected_huyen=None, selected_xa=None):
        admin = AdministrativeUnitService()

        dialog.cbo_huyen.clear()
        for d in admin.get_districts():
            dialog.cbo_huyen.addItem(d["name"], d["id"])

        def load_xa():
            dialog.cbo_xa.clear()
            for w in admin.get_wards_by_district(
                dialog.cbo_huyen.currentData()
            ):
                dialog.cbo_xa.addItem(w["name"], w["id"])

        dialog.cbo_huyen.currentIndexChanged.connect(load_xa)

        if selected_huyen:
            dialog.cbo_huyen.setCurrentIndex(
                dialog.cbo_huyen.findData(selected_huyen)
            )

        load_xa()

        if selected_xa:
            dialog.cbo_xa.setCurrentIndex(
                dialog.cbo_xa.findData(selected_xa)
            )
