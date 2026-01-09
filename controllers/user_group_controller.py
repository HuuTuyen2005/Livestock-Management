from views.user_group_dialog import UserGroupDialog
from services.group_service import GroupService
from services.permission_service import PermissionService
from services.activity_service import ActivityService
from PyQt6.QtWidgets import QListWidgetItem, QMessageBox
from PyQt6.QtCore import Qt
from auth.session import Session

class UserGroupController:
    def __init__(self, user):
        self.user = user
        self.view = UserGroupDialog()

        self.group_service = GroupService()
        self.permission_service = PermissionService()
        self.log_service = ActivityService()

        self.view.lbl_user.setText(
            f"User: {user['fullname']} (ID={user['id']})"
        )

        self.load_groups()
        self.update_permissions()

        self.view.group_list.itemChanged.connect(self.update_permissions)
        self.view.btn_save.clicked.connect(self.save)
        self.view.btn_close.clicked.connect(self.view.close)

    def load_groups(self):
        self.groups = self.group_service.get_groups()
        user_groups = self.group_service.get_user_groups(self.user["id"])
        user_group_ids = {g["id"] for g in user_groups}

        for g in self.groups:
            item = QListWidgetItem(g["name"])
            item.setData(Qt.ItemDataRole.UserRole, g["id"])
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(
                Qt.CheckState.Checked
                if g["id"] in user_group_ids
                else Qt.CheckState.Unchecked
            )
            self.view.group_list.addItem(item)

    def get_selected_group_ids(self):
        ids = []
        for i in range(self.view.group_list.count()):
            item = self.view.group_list.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                ids.append(item.data(Qt.ItemDataRole.UserRole))
        return ids

    def update_permissions(self):
        self.view.permission_list.clear()
        group_ids = self.get_selected_group_ids()
        perms = self.permission_service.get_permissions_by_groups(group_ids)

        for p in perms:
            item = QListWidgetItem(f"{p['code']} – {p['name']}")
            item.setCheckState(Qt.CheckState.Checked)
            self.view.permission_list.addItem(item)

    def save(self):
        user_id = self.user["id"]

        # Xoá group cũ
        self.group_service.db.execute(
            "DELETE FROM user_groups WHERE user_id=%s",
            (user_id,)
        )

        # Gán lại
        for gid in self.get_selected_group_ids():
            self.group_service.assign_group(user_id, gid)

        self.log_service.log(
            Session.current_user["id"],
            f"Gán nhóm cho user ID={user_id}"
        )

        QMessageBox.information(self.view, "OK", "Cập nhật nhóm thành công")
        self.view.close()
