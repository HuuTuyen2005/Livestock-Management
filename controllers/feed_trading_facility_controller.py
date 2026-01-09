from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from views.feed_trading_facility_view import FeedTradingFacilityView
from dialogs.feed_trading_facility_dialog import FeedTradingFacilityDialog
from services.feed_trading_facility_service import FeedTradingFacilityService
from services.administrative_unit_service import AdministrativeUnitService
from services.activity_service import ActivityService
from auth.session import Session

class FeedTradingFacilityController:
    def __init__(self):
        self.view = FeedTradingFacilityView()
        self.service = FeedTradingFacilityService()
        self.activity_service = ActivityService()
        self._connect_events()
        self.load_data()

    def show(self):
        self.view.show()

    def _connect_events(self):
        self.view.btn_search.clicked.connect(self.search)
        self.view.txt_search.returnPressed.connect(self.search)
        self.view.btn_refresh.clicked.connect(self.refresh)
        self.view.btn_add.clicked.connect(self.add)
        self.view.btn_edit.clicked.connect(self.edit)
        self.view.btn_delete.clicked.connect(self.delete)

    def load_data(self):
        data = self.service.get_all()
        self._render_table(data)

    def search(self):
        keyword = self.view.txt_search.text()
        data = self.service.search(keyword)
        self._render_table(data)

    def refresh(self):
        self.view.txt_search.clear()
        self.load_data()

    # ================= ADD =================
    def add(self):
        dialog = FeedTradingFacilityDialog()
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
            self.service.create(data)

            if Session.current_user:
                self.activity_service.log(
                    Session.current_user["id"],
                    f"Thêm cơ sở mua bán thức ăn chăn nuôi: {data['name']}"
                )

            self.load_data()

    # ================= EDIT =================
    def edit(self):
        row = self.view.table.currentRow()
        if row < 0:
            QMessageBox.warning(self.view, "Cảnh báo", "Vui lòng chọn một dòng")
            return

        facility_id = int(self.view.table.item(row, 0).text())
        old_data = self.service.get_by_id(facility_id)

        dialog = FeedTradingFacilityDialog(old_data)
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
            self.service.update(facility_id, update_data)

            if Session.current_user:
                self.activity_service.log(
                    Session.current_user["id"],
                    f"Cập nhật cơ sở mua bán thức ăn chăn nuôi: {old_data['name']}"
                )

            self.load_data()

    # ================= DELETE =================
    def delete(self):
        row = self.view.table.currentRow()
        if row < 0:
            QMessageBox.warning(self.view, "Cảnh báo", "Vui lòng chọn một dòng")
            return

        facility_id = int(self.view.table.item(row, 0).text())
        name = self.view.table.item(row, 1).text()

        reply = QMessageBox.question(
            self.view,
            "Xác nhận",
            "Bạn có chắc chắn muốn xóa cơ sở này?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.service.delete(facility_id)

            if Session.current_user:
                self.activity_service.log(
                    Session.current_user["id"],
                    f"Xóa cơ sở mua bán thức ăn chăn nuôi: {name}"
                )

            self.load_data()

    # ================= TABLE =================
    def _render_table(self, data):
        table = self.view.table
        table.setRowCount(len(data))

        for row, item in enumerate(data):
            table.setItem(row, 0, QTableWidgetItem(str(item["id"])))
            table.setItem(row, 1, QTableWidgetItem(item["name"]))
            table.setItem(row, 2, QTableWidgetItem(item["huyen_name"] or ""))
            table.setItem(row, 3, QTableWidgetItem(item["xa_name"] or ""))
            table.setItem(row, 4, QTableWidgetItem(item["address"]))
            table.setItem(row, 5, QTableWidgetItem(item["phone"]))
            table.setItem(row, 6, QTableWidgetItem(item["email"]))
            table.setItem(row, 7, QTableWidgetItem(item["certification"] or ""))
            table.setItem(row, 8, QTableWidgetItem(item["scale"]))
            table.setItem(row, 9, QTableWidgetItem(
                "Hoạt động" if item["status"] == 1 else "Ngừng"
            ))

    # ================= ADMIN UNIT =================
    def _load_huyen_xa(self, dialog, selected_huyen=None, selected_xa=None):
        admin = AdministrativeUnitService()
        dialog.cbo_huyen.clear()

        for d in admin.get_districts():
            dialog.cbo_huyen.addItem(d["name"], d["id"])

        def load_xa():
            dialog.cbo_xa.clear()
            for w in admin.get_wards_by_district(dialog.cbo_huyen.currentData()):
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
