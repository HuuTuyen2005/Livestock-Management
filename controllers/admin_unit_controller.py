from services.admin_unit_service import AdminUnitService
from views.admin_unit_view import AdminUnitView
from PyQt6.QtWidgets import QTreeWidgetItem, QMessageBox, QInputDialog

class AdminUnitController:
    def __init__(self):
        self.view = AdminUnitView()
        self.service = AdminUnitService()

        self.load_tree()

        self.view.btn_add_district.clicked.connect(self.add_district)
        self.view.btn_add_commune.clicked.connect(self.add_commune)
        self.view.btn_edit.clicked.connect(self.edit_unit)
        self.view.btn_delete.clicked.connect(self.delete_unit)

        self.view.btn_search.clicked.connect(self.search)
        self.view.txt_search.returnPressed.connect(self.search)
        self.view.btn_refresh.clicked.connect(self.refresh)


    def load_tree(self):
        self.view.tree.clear()

        districts = self.service.get_districts()
        for d in districts:
            district_item = QTreeWidgetItem([d["name"]])
            district_item.setData(0, 1, ("district", d["id"]))
            self.view.tree.addTopLevelItem(district_item)

            communes = self.service.get_communes_by_district(d["id"])
            for c in communes:
                commune_item = QTreeWidgetItem([c["name"]])
                commune_item.setData(0, 1, ("commune", c["id"]))
                district_item.addChild(commune_item)

        self.view.tree.expandAll()

    def add_district(self):
        name, ok = QInputDialog.getText(self.view, "Thêm huyện", "Tên huyện:")
        if ok and name:
            self.service.create_unit(name, 1)
            self.load_tree()

    def add_commune(self):
        item = self.view.tree.currentItem()
        if not item:
            QMessageBox.warning(self.view, "Lỗi", "Chọn huyện trước")
            return

        data = item.data(0, 1)
        if data[0] != "district":
            QMessageBox.warning(self.view, "Lỗi", "Xã phải thuộc huyện")
            return

        name, ok = QInputDialog.getText(self.view, "Thêm xã", "Tên xã:")
        if ok and name:
            self.service.create_unit(name, 2, data[1])
            self.load_tree()

    def edit_unit(self):
        item = self.view.tree.currentItem()
        if not item:
            return

        data = item.data(0, 1)
        old_name = item.text(0)

        name, ok = QInputDialog.getText(
            self.view, "Sửa tên", "Tên mới:", text=old_name
        )
        if ok and name:
            self.service.update_unit(data[1], name)
            self.load_tree()

    def delete_unit(self):
        item = self.view.tree.currentItem()
        if not item:
            return

        data = item.data(0, 1)

        if QMessageBox.question(
            self.view, "Xác nhận", "Xoá đơn vị này?"
        ) == QMessageBox.StandardButton.Yes:
            try:
                self.service.delete_unit(data[1])
                self.load_tree()
            except Exception:
                QMessageBox.warning(
                    self.view,
                    "Lỗi",
                    "Không thể xoá (có dữ liệu liên quan)"
                )

    def search(self):
        keyword = self.view.txt_search.text().strip()
        if not keyword:
            self.load_tree()
            return

        self.view.tree.clear()

        rows = self.service.search_units(keyword)

        districts = {}
        communes = []

        for r in rows:
            if r["level_id"] == 1:
                districts[r["id"]] = r
            else:
                communes.append(r)

        # Load huyện match trực tiếp
        for d in districts.values():
            item = QTreeWidgetItem([d["name"]])
            item.setData(0, 1, ("district", d["id"]))
            self.view.tree.addTopLevelItem(item)

        # Load xã match -> kèm huyện cha
        for c in communes:
            parent_id = c["administrative_id"]

            if parent_id not in districts:
                parent = self.service.db.fetch_one("""
                    SELECT id, name FROM administrative_unit
                    WHERE id=%s
                """, (parent_id,))
                parent_item = QTreeWidgetItem([parent["name"]])
                parent_item.setData(0, 1, ("district", parent["id"]))
                self.view.tree.addTopLevelItem(parent_item)
                districts[parent_id] = parent
            else:
                parent_item = self.find_district_item(parent_id)

            commune_item = QTreeWidgetItem([c["name"]])
            commune_item.setData(0, 1, ("commune", c["id"]))
            parent_item.addChild(commune_item)

        self.view.tree.expandAll()

    def find_district_item(self, district_id):
        for i in range(self.view.tree.topLevelItemCount()):
            item = self.view.tree.topLevelItem(i)
            data = item.data(0, 1)
            if data and data[1] == district_id:
                return item
        return None

    def refresh(self):
        self.view.txt_search.clear()
        self.load_tree()
