from views.manual_view import ManualView
from services.manual_service import ManualService
from PyQt6.QtWidgets import QInputDialog, QMessageBox, QTableWidgetItem
from auth.session import Session

class ManualController:
    def __init__(self):
        # Quyền của người dùng hiện tại
        can_view = "MANUAL_VIEW" in Session.permissions
        can_manage = "MANUAL_MANAGE" in Session.permissions

        if not can_view:
            raise PermissionError("Bạn không có quyền xem hướng dẫn")

        self.view = ManualView(can_manage=can_manage)
        self.service = ManualService()
        self.load_manuals()

        # Hiển thị nội dung khi chọn
        self.view.table.itemSelectionChanged.connect(self.show_manual_content)

        # Nút thêm/sửa/xoá chỉ bật nếu có quyền
        if can_manage:
            self.view.btn_add.clicked.connect(self.add_manual)
            self.view.btn_edit.clicked.connect(self.edit_manual)
            self.view.btn_delete.clicked.connect(self.delete_manual)

    def load_manuals(self):
        manuals = self.service.get_all_manuals()
        self.view.table.setRowCount(len(manuals))
        for r, m in enumerate(manuals):
            self.view.table.setItem(r, 0, QTableWidgetItem(str(m["id"])))
            self.view.table.setItem(r, 1, QTableWidgetItem(m["title"]))
        self.view.txt_content.clear()

    def show_manual_content(self):
        row = self.view.table.currentRow()
        if row < 0:
            return
        manual_id = int(self.view.table.item(row, 0).text())
        manual = self.service.get_manual_by_id(manual_id)
        if manual:
            self.view.txt_content.setText(manual["content"])

    def add_manual(self):
        title, ok1 = QInputDialog.getText(self.view, "Thêm hướng dẫn", "Tiêu đề")
        if not ok1 or not title.strip():
            return
        content, ok2 = QInputDialog.getMultiLineText(self.view, "Thêm hướng dẫn", "Nội dung")
        if not ok2:
            return
        self.service.create_manual(title.strip(), content)
        self.load_manuals()

    def edit_manual(self):
        row = self.view.table.currentRow()
        if row < 0:
            return
        manual_id = int(self.view.table.item(row, 0).text())
        manual = self.service.get_manual_by_id(manual_id)
        title, ok1 = QInputDialog.getText(self.view, "Sửa hướng dẫn", "Tiêu đề", text=manual["title"])
        if not ok1 or not title.strip():
            return
        content, ok2 = QInputDialog.getMultiLineText(self.view, "Sửa hướng dẫn", "Nội dung", text=manual["content"])
        if not ok2:
            return
        self.service.update_manual(manual_id, title.strip(), content)
        self.load_manuals()

    def delete_manual(self):
        row = self.view.table.currentRow()
        if row < 0:
            return
        manual_id = int(self.view.table.item(row, 0).text())
        reply = QMessageBox.question(
            self.view, "Xác nhận",
            "Bạn có chắc muốn xoá hướng dẫn này không?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return
        self.service.delete_manual(manual_id)
        self.load_manuals()
