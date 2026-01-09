from PyQt6.QtWidgets import QMessageBox

from views.group_view import GroupView
from views.group_dialog import GroupDialog
from services.group_service import GroupService
from views.group_lookup_dialog import GroupLookupDialog


class GroupController:
    def __init__(self):
        self.view = GroupView()
        self.service = GroupService()

        self.load_groups()
        self.bind_events()


    def bind_events(self):
        self.view.btn_search.clicked.connect(self.search_groups)
        self.view.btn_add.clicked.connect(self.add_group)
        self.view.btn_edit.clicked.connect(self.edit_group)
        self.view.btn_delete.clicked.connect(self.delete_group)
        self.view.btn_toggle.clicked.connect(self.toggle_group)
        self.view.btn_lookup.clicked.connect(self.open_lookup)

    # ================= LOAD =================
    def load_groups(self):
        groups = self.service.get_all_groups()
        self.view.load_data(groups)

    # ================= ACTIONS =================
    def search_groups(self):
        keyword = self.view.search_input.text().strip()
        if not keyword:
            self.load_groups()
            return
        groups = self.service.search_groups(keyword)
        self.view.load_data(groups)

    def add_group(self):
        dialog = GroupDialog(self.view)
        if dialog.exec():
            data = dialog.get_data()
            if not data["name"]:
                QMessageBox.warning(self.view, "Lỗi", "Tên nhóm không được để trống")
                return

            self.service.add_group(data["name"], data["description"])
            self.load_groups()

    def edit_group(self):
        group_id = self.view.get_selected_group_id()
        if not group_id:
            QMessageBox.warning(self.view, "Lỗi", "Chọn một nhóm để sửa")
            return

        groups = self.service.get_all_groups()
        group = next(g for g in groups if g["id"] == group_id)

        dialog = GroupDialog(self.view, group)
        if dialog.exec():
            data = dialog.get_data()
            self.service.update_group(
                group_id,
                data["name"],
                data["description"]
            )
            self.load_groups()

    def delete_group(self):
        group_id = self.view.get_selected_group_id()
        if not group_id:
            QMessageBox.warning(self.view, "Lỗi", "Chọn một nhóm để xóa")
            return

        reply = QMessageBox.question(
            self.view,
            "Xác nhận",
            "Bạn có chắc chắn muốn xóa nhóm này?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.service.delete_group(group_id)
            self.load_groups()

    def toggle_group(self):
        group_id = self.view.get_selected_group_id()
        if not group_id:
            QMessageBox.warning(self.view, "Lỗi", "Chọn một nhóm")
            return

        groups = self.service.get_all_groups()
        group = next(g for g in groups if g["id"] == group_id)

        new_status = 0 if group["is_active"] else 1
        self.service.set_group_active(group_id, new_status)
        self.load_groups()

    def open_lookup(self):
        dialog = GroupLookupDialog(self.view)

        groups = self.service.get_all_groups()
        users = self.service.get_all_users()

        # mặc định: GROUP -> USER
        dialog.load_select_items(groups, "group")
        dialog.mode_combo.currentIndexChanged.connect(
            lambda: self.on_lookup_mode_changed(dialog, groups, users)
        )
        dialog.select_combo.currentIndexChanged.connect(
            lambda: self.on_lookup_selection(dialog)
        )

        dialog.exec()

    def on_lookup_mode_changed(self, dialog, groups, users):
        if dialog.mode_combo.currentIndex() == 0:
            dialog.load_select_items(groups, "group")
        else:
            dialog.load_select_items(users, "user")

        dialog.table.setRowCount(0)

    def on_lookup_selection(self, dialog):
        item_id = dialog.select_combo.currentData()
        if not item_id:
            return

        # GROUP -> USERS
        if dialog.mode_combo.currentIndex() == 0:
            users = self.service.get_users_in_group(item_id)
            dialog.load_table(
                ["ID", "Họ tên"],
                [(u["id"], u["fullname"]) for u in users]
            )
        else:
            # USER -> GROUPS
            groups = self.service.get_groups_of_user(item_id)
            dialog.load_table(
                ["ID", "Tên nhóm"],
                [(g["id"], g["name"]) for g in groups]
            )


