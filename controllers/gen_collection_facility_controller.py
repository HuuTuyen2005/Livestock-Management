from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from views.gen_collection_facility_view import GenCollectionFacilityView
from dialogs.gen_collection_facility_dialog import GenCollectionFacilityDialog
from services.gen_collection_facility_service import GenCollectionFacilityService
from services.gen_service import GenService
from services.administrative_unit_service import AdministrativeUnitService
from services.activity_service import ActivityService
from auth.session import Session


class GenCollectionFacilityController:
    def __init__(self):
        self.view = GenCollectionFacilityView()
        self.service = GenCollectionFacilityService()
        self.gen_service = GenService()
        self.log_service = ActivityService()

        self._connect_events()
        self.load_data()

    # ================= SHOW =================
    def show(self):
        self.view.show()

    # ================= CONNECT EVENTS =================
    def _connect_events(self):
        self.view.btn_search.clicked.connect(self.search)
        self.view.txt_search.returnPressed.connect(self.search)
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
        self._render_table(self.service.get_all())

    # ================= SEARCH =================
    def search(self):
        keyword = self.view.txt_search.text().strip()
        if not keyword:
            self.load_data()
            return
        self._render_table(self.service.search(keyword))

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

            self.service.create(
                data,
                dialog.get_selected_gens()
            )

            if Session.current_user:
                self.log_service.log(
                    Session.current_user["id"],
                    f"Thêm cơ sở thu thập nguồn gen: {data['name']}"
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
        gens = self.gen_service.get_all()

        dialog = GenCollectionFacilityDialog(data, gens)
        self._load_huyen_xa(
            dialog,
            selected_huyen=data.get("huyen_id"),
            selected_xa=data.get("xa_id")
        )

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
                self.log_service.log(
                    Session.current_user["id"],
                    f"Cập nhật cơ sở thu thập nguồn gen (ID={facility_id}): {update_data['name']}"
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
                f"Xoá cơ sở thu thập nguồn gen (ID={facility_id}): {data['name']}"
            )

        self.load_data()

    # ================= RENDER TABLE =================
    def _render_table(self, data):
        table = self.view.table
        table.setRowCount(len(data))

        for r, item in enumerate(data):
            table.setItem(r, 0, QTableWidgetItem(str(item["id"])))
            table.setItem(r, 1, QTableWidgetItem(item["name"]))
            table.setItem(r, 2, QTableWidgetItem(item["huyen_name"] or ""))
            table.setItem(r, 3, QTableWidgetItem(item["xa_name"] or ""))
            table.setItem(r, 4, QTableWidgetItem(item["gen_names"] or ""))
            table.setItem(r, 5, QTableWidgetItem(item["address"] or ""))
            table.setItem(r, 6, QTableWidgetItem(item["phone"] or ""))
            table.setItem(r, 7, QTableWidgetItem(item["email"] or ""))
            table.setItem(r, 8, QTableWidgetItem(item["certification"] or ""))
            table.setItem(r, 9, QTableWidgetItem(item["scale"] or ""))
            table.setItem(
                r, 10,
                QTableWidgetItem(
                    "Hoạt động" if item["status"] == 1 else "Ngừng"
                )
            )

    # ================= LOAD HUYEN / XA =================
    def _load_huyen_xa(self, dialog, selected_huyen=None, selected_xa=None):
        admin = AdministrativeUnitService()

        dialog.cbo_huyen.clear()
        for d in admin.get_districts():
            dialog.cbo_huyen.addItem(d["name"], d["id"])

        def load_xa():
            dialog.cbo_xa.clear()
            huyen_id = dialog.cbo_huyen.currentData()
            if not huyen_id:
                return
            for w in admin.get_wards_by_district(huyen_id):
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
