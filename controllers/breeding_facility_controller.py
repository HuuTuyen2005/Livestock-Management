from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox

from views.breeding_facility_view import BreedingFacilityView
from dialogs.breeding_facility_dialog import BreedingFacilityDialog

from services.breeding_facility_service import BreedingFacilityService
from services.administrative_unit_service import AdministrativeUnitService
from services.activity_service import ActivityService

from auth.session import Session


class BreedingFacilityController:
    def __init__(self):
        self.view = BreedingFacilityView()
        self.service = BreedingFacilityService()
        self.log_service = ActivityService()

        self._connect_events()
        self.load_data()

    # ================= SHOW =================
    def show(self):
        self.view.show()

    # ================= CONNECT EVENTS =================
    def _connect_events(self):
        self.view.btn_add.clicked.connect(self.add)
        self.view.btn_edit.clicked.connect(self.edit)
        self.view.btn_delete.clicked.connect(self.delete)

        self.view.btn_search.clicked.connect(self.search)
        self.view.txt_search.returnPressed.connect(self.search)
        self.view.btn_refresh.clicked.connect(self.refresh)

        # Double click = Edit
        self.view.table.itemDoubleClicked.connect(
            lambda _: self.edit()
        )

    # ================= LOAD TABLE =================
    def load_data(self):
        self.load_table(self.service.get_all())

    def load_table(self, data):
        table = self.view.table
        table.setRowCount(len(data))

        for r, item in enumerate(data):
            table.setItem(r, 0, QTableWidgetItem(str(item["id"])))
            table.setItem(r, 1, QTableWidgetItem(item["name"]))
            table.setItem(r, 2, QTableWidgetItem(item["huyen_name"] or ""))
            table.setItem(r, 3, QTableWidgetItem(item["xa_name"] or ""))
            table.setItem(r, 4, QTableWidgetItem(item["address"] or ""))
            table.setItem(r, 5, QTableWidgetItem(item["phone"] or ""))
            table.setItem(r, 6, QTableWidgetItem(item["email"] or ""))
            table.setItem(r, 7, QTableWidgetItem(item["certification"] or ""))
            table.setItem(r, 8, QTableWidgetItem(item["scale"] or ""))
            table.setItem(
                r, 9,
                QTableWidgetItem("Hoạt động" if item["status"] == 1 else "Ngừng")
            )

    # ================= COMMON =================
    def get_selected_id(self):
        row = self.view.table.currentRow()
        if row < 0:
            return None
        item = self.view.table.item(row, 0)
        return int(item.text()) if item else None

    # ================= ADD =================
    def add(self):
        dlg = BreedingFacilityDialog()
        self._load_huyen_xa(dlg)

        dlg.btn_save.clicked.connect(
            lambda: self.save_add(dlg)
        )
        dlg.exec()

    def save_add(self, dlg):
        data = self._collect_form_data(dlg)

        self.service.create(data)

        if Session.current_user:
            self.log_service.log(
                Session.current_user["id"],
                f"Thêm cơ sở sản xuất con giống: {data['name']}"
            )

        dlg.accept()
        self.load_data()

    # ================= EDIT =================
    def edit(self):
        facility_id = self.get_selected_id()
        if not facility_id:
            QMessageBox.warning(self.view, "Cảnh báo", "Vui lòng chọn một dòng")
            return

        data = self.service.get_by_id(facility_id)

        dlg = BreedingFacilityDialog(data)
        self._load_huyen_xa(
            dlg,
            selected_huyen=data.get("huyen_id"),
            selected_xa=data.get("xa_id")
        )

        dlg.btn_save.clicked.connect(
            lambda: self.save_edit(dlg, facility_id)
        )
        dlg.exec()

    def save_edit(self, dlg, facility_id):
        update_data = self._collect_form_data(dlg)

        self.service.update(facility_id, update_data)

        if Session.current_user:
            self.log_service.log(
                Session.current_user["id"],
                f"Cập nhật cơ sở sản xuất con giống (ID={facility_id}): {update_data['name']}"
            )

        dlg.accept()
        self.load_data()

    # ================= DELETE =================
    def delete(self):
        facility_id = self.get_selected_id()
        if not facility_id:
            QMessageBox.warning(self.view, "Cảnh báo", "Vui lòng chọn một dòng")
            return

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
                f"Xoá cơ sở sản xuất con giống (ID={facility_id}): {data['name']}"
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

    # ================= HELPERS =================
    def _collect_form_data(self, dlg):
        return {
            "name": dlg.txt_name.text(),
            "address": dlg.txt_address.text(),
            "phone": dlg.txt_phone.text(),
            "email": dlg.txt_email.text(),
            "certification": dlg.txt_certification.text(),
            "scale": dlg.cbo_scale.currentText(),
            "status": dlg.cbo_status.currentIndex(),
            "unit_id": dlg.cbo_xa.currentData()
        }

    def _load_huyen_xa(self, dlg, selected_huyen=None, selected_xa=None):
        admin = AdministrativeUnitService()

        dlg.cbo_huyen.clear()
        districts = admin.get_districts()
        for d in districts:
            dlg.cbo_huyen.addItem(d["name"], d["id"])

        def load_xa():
            dlg.cbo_xa.clear()
            huyen_id = dlg.cbo_huyen.currentData()
            if not huyen_id:
                return
            wards = admin.get_wards_by_district(huyen_id)
            for w in wards:
                dlg.cbo_xa.addItem(w["name"], w["id"])

        dlg.cbo_huyen.currentIndexChanged.connect(load_xa)

        if selected_huyen:
            dlg.cbo_huyen.setCurrentIndex(
                dlg.cbo_huyen.findData(selected_huyen)
            )

        load_xa()

        if selected_xa:
            dlg.cbo_xa.setCurrentIndex(
                dlg.cbo_xa.findData(selected_xa)
            )
