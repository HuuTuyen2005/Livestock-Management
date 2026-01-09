from PyQt6.QtWidgets import (
    QTableWidgetItem, QListWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt

from services.permission_service import PermissionService
from views.permission_view import PermissionView
from views.permission_dialog import (
    PermissionDialog, GroupPermissionDialog
)
from mysql.connector.errors import IntegrityError

class PermissionController:
    def __init__(self):
        self.service = PermissionService()
        self.view = PermissionView()

        self.load_permissions()

        self.view.btn_add.clicked.connect(self.add_permission)
        self.view.btn_edit.clicked.connect(self.edit_permission)
        self.view.btn_delete.clicked.connect(self.delete_permission)
        self.view.btn_assign.clicked.connect(self.assign_group_permission)
        self.view.btn_view.clicked.connect(self.view_group_permission)
        self.view.table.itemChanged.connect(self.on_active_changed)

        self.view.show()

        # ===== LOAD =====
    def load_permissions(self):
        data = self.service.get_all_permissions()

        self.view.table.blockSignals(True)   # tránh trigger itemChanged
        self.view.table.setRowCount(0)

        for r, p in enumerate(data):
            self.view.table.insertRow(r)

            # ID (ẩn)
            id_item = QTableWidgetItem()
            id_item.setData(Qt.ItemDataRole.UserRole, p['id'])
            self.view.table.setItem(r, 0, id_item)

            self.view.table.setItem(r, 1, QTableWidgetItem(p['name']))
            self.view.table.setItem(r, 2, QTableWidgetItem(p['code']))
            self.view.table.setItem(r, 3, QTableWidgetItem(p['description'] or ""))

            # ===== ACTIVE CHECKBOX =====
            active_item = QTableWidgetItem()
            active_item.setFlags(
                Qt.ItemFlag.ItemIsUserCheckable |
                Qt.ItemFlag.ItemIsEnabled
            )
            active_item.setCheckState(
                Qt.CheckState.Checked if p['is_active']
                else Qt.CheckState.Unchecked
            )
            self.view.table.setItem(r, 4, active_item)

        self.view.table.blockSignals(False)

    # ===== A. PERMISSION =====
    def add_permission(self):
        dlg = PermissionDialog("Thêm quyền")
        dlg.btn_save.clicked.connect(lambda: self._save_new(dlg))
        dlg.exec()


    def _save_new(self, dlg):
        name = dlg.txt_name.text().strip()
        code = dlg.txt_code.text().strip()

        if not name or not code:
            QMessageBox.warning(dlg, "Lỗi", "Tên và Code không được để trống")
            return
    
        if self.service.code_exists(code):
            QMessageBox.warning(dlg, "Lỗi", "Code đã tồn tại")
            return

        try:
            self.service.add_permission(
                name,
                code,
                dlg.txt_desc.toPlainText()
            )
        except IntegrityError:
            QMessageBox.warning(
                dlg,
                "Trùng code",
                f"Code '{code}' đã tồn tại. Vui lòng nhập code khác."
            )
            return
        except Exception as e:
            QMessageBox.critical(dlg, "Lỗi", str(e))
            return

        dlg.accept()
        self.load_permissions()

    def edit_permission(self):
        pid = self.get_selected_id()
        if pid is None:
            return

        row = self.view.table.currentRow()
        dlg = PermissionDialog("Sửa quyền")

        dlg.txt_name.setText(self.view.table.item(row, 1).text())
        dlg.txt_code.setText(self.view.table.item(row, 2).text())
        dlg.txt_desc.setPlainText(self.view.table.item(row, 3).text())

        dlg.btn_save.clicked.connect(
            lambda: self._update(pid, dlg)
        )
        dlg.exec()

    def _update(self, pid, dlg):
        self.service.update_permission(
            pid,
            dlg.txt_name.text(),
            dlg.txt_code.text(),
            dlg.txt_desc.toPlainText()
        )
        dlg.accept()
        self.load_permissions()

    def delete_permission(self):
        pid = self.get_selected_id()
        if pid is None:
            return

        if QMessageBox.question(
            self.view,
            "Xác nhận",
            "Xóa quyền này?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) != QMessageBox.StandardButton.Yes:
            return

        try:
            self.service.delete_permission(pid)
            self.load_permissions()
        except IntegrityError:
            QMessageBox.warning(
                self.view,
                "Không thể xóa",
                "Quyền này đang được gán cho nhóm. Vui lòng gỡ quyền khỏi nhóm trước."
            )

    # ===== B. GROUP PERMISSION =====
    def assign_group_permission(self):
        dlg = GroupPermissionDialog()

        for g in self.service.get_groups():
            dlg.cbo_group.addItem(g['name'], g['id'])

        perms = self.service.get_all_permissions()
        for p in perms:
            if not p['is_active']:
                continue
            item = QListWidgetItem(p['name'])
            item.setData(Qt.ItemDataRole.UserRole, p['id'])
            item.setCheckState(Qt.CheckState.Unchecked)
            dlg.lst_permissions.addItem(item)

        dlg.cbo_group.currentIndexChanged.connect(
            lambda: self._load_group_perm(dlg)
        )

        self._load_group_perm(dlg)
        dlg.btn_save.clicked.connect(
            lambda: self._save_group_perm(dlg)
        )

        dlg.exec()

    def _load_group_perm(self, dlg):
        gid = dlg.cbo_group.currentData()
        if gid is None:
            return

        assigned = {
            x['id']
            for x in self.service.get_permissions_by_group(gid)
        }

        for i in range(dlg.lst_permissions.count()):
            item = dlg.lst_permissions.item(i)
            item.setCheckState(
                Qt.CheckState.Checked
                if item.data(Qt.ItemDataRole.UserRole) in assigned
                else Qt.CheckState.Unchecked
            )


    def _save_group_perm(self, dlg):
        gid = dlg.cbo_group.currentData()
        if gid is None:
            QMessageBox.warning(dlg, "Lỗi", "Chưa chọn nhóm")
            return

        pids = [
            dlg.lst_permissions.item(i).data(Qt.ItemDataRole.UserRole)
            for i in range(dlg.lst_permissions.count())
            if dlg.lst_permissions.item(i).checkState() == Qt.CheckState.Checked
        ]

        self.service.save_group_permissions(gid, pids)
        dlg.accept()

    # ===== C. VIEW =====
    def view_group_permission(self):
        data = self.service.view_group_permissions()

        if not data:
            QMessageBox.information(
                self.view, "Thông tin", "Chưa có dữ liệu"
            )
            return

        result = {}
        for row in data:
            g = row['group_name']
            line = f" - {row['perm_name']} ({row['perm_code']})"
            result.setdefault(g, []).append(line)

        msg = ""
        for g, perms in result.items():
            msg += f"[{g}]\n"
            msg += "\n".join(perms)
            msg += "\n\n"

        QMessageBox.information(
            self.view, "Phân quyền theo nhóm", msg.strip()
        )



    def get_selected_id(self):
        row = self.view.table.currentRow()
        if row < 0:
            QMessageBox.warning(self.view, "Lỗi", "Chưa chọn dòng")
            return None

        item = self.view.table.item(row, 0)
        return item.data(Qt.ItemDataRole.UserRole)

    def on_active_changed(self, item):
        # chỉ xử lý cột Active (cột 4)
        if item.column() != 4:
            return

        row = item.row()
        id_item = self.view.table.item(row, 0)
        pid = id_item.data(Qt.ItemDataRole.UserRole)

        is_active = (
            item.checkState() == Qt.CheckState.Checked
        )

        try:
            self.service.toggle_permission(pid, int(is_active))
        except Exception as e:
            QMessageBox.critical(self.view, "Lỗi", str(e))

