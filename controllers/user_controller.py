from services.user_service import UserService
from services.group_service import GroupService
from views.user_view import UserView
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from services.activity_service import ActivityService
from auth.session import Session
from controllers.user_group_controller import UserGroupController
from views.user_dialog import UserDialog
from services.admin_unit_service import AdminUnitService
from mysql.connector.errors import IntegrityError

class UserController:
    def __init__(self):
        self.view = UserView()
        self.user_service = UserService()
        self.group_service = GroupService()
        self.admin_unit_service = AdminUnitService()

        self.load_users()

        self.view.btn_add.clicked.connect(self.add_user)
        self.view.btn_lock.clicked.connect(self.toggle_status)
        self.view.btn_edit.clicked.connect(self.edit_user)
        self.view.btn_delete.clicked.connect(self.delete_user)
        self.view.btn_reset.clicked.connect(self.reset_password)
        # self.view.btn_group.clicked.connect(self.manage_groups)

        self.view.btn_search.clicked.connect(self.search)
        self.view.txt_search.returnPressed.connect(self.search)
        self.view.btn_refresh.clicked.connect(self.refresh)


    def load_users(self):
        users = self.user_service.get_users()
        self.view.table.setRowCount(len(users))

        for r, u in enumerate(users):
            self.view.table.setItem(r, 0, QTableWidgetItem(str(u["id"])))
            self.view.table.setItem(r, 1, QTableWidgetItem(u["fullname"]))
            self.view.table.setItem(r, 2, QTableWidgetItem(u["email"]))
            self.view.table.setItem(r, 3, QTableWidgetItem(u["phone"]))
            self.view.table.setItem(r, 4, QTableWidgetItem(u["username"] or ""))
            self.view.table.setItem(r, 5, QTableWidgetItem(u["unit_name"] or ""))
            self.view.table.setItem(r, 6, QTableWidgetItem("Hoạt động" if u["status"] else "Khoá"))

    def get_selected_user_id(self):
        row = self.view.table.currentRow()
        if row < 0:
            return None
        return int(self.view.table.item(row, 0).text())

    def toggle_status(self):
        uid = self.get_selected_user_id()
        if not uid:
            return

        current = self.user_service.get_status(uid)
        new_status = 0 if current == 1 else 1

        self.user_service.set_status(uid, new_status)

        ActivityService().log(
            Session.current_user["id"],
            f"{'Khoá' if new_status == 0 else 'Mở'} user ID={uid}"
        )

        self.load_users()


    def reset_password(self):
        uid = self.get_selected_user_id()
        if not uid:
            return
        self.user_service.reset_password(uid)
        # QMessageBox.information(self.view, "OK", "Mật khẩu reset = 123456")
        ActivityService().log(
            Session.current_user["id"],
            f"Reset mật khẩu user ID={uid}"
        )

    # def manage_groups(self):
    #     row = self.view.table.currentRow()
    #     if row < 0:
    #         return

    #     user = {
    #         "id": int(self.view.table.item(row, 0).text()),
    #         "fullname": self.view.table.item(row, 1).text()
    #     }

    #     dlg = UserGroupController(user)
    #     dlg.view.exec()

    def search(self):
        keyword = self.view.txt_search.text().strip()
        if not keyword:
            self.load_users()
            return

        users = self.user_service.search_users(keyword)
        self.view.table.setRowCount(len(users))

        for r, u in enumerate(users):
            self.view.table.setItem(r, 0, QTableWidgetItem(str(u["id"])))
            self.view.table.setItem(r, 1, QTableWidgetItem(u["fullname"]))
            self.view.table.setItem(r, 2, QTableWidgetItem(u["email"]))
            self.view.table.setItem(r, 3, QTableWidgetItem(u["phone"]))
            self.view.table.setItem(r, 4, QTableWidgetItem(u["username"] or ""))
            self.view.table.setItem(r, 5, QTableWidgetItem(u["unit_name"] or ""))
            self.view.table.setItem(r, 6, QTableWidgetItem("Hoạt động" if u["status"] else "Khoá"))

    def refresh(self):
        self.view.txt_search.clear()
        self.load_users()

    def add_user(self):
        units = self.admin_unit_service.get_all_units()
        dlg = UserDialog(units)

        dlg.btn_save.clicked.connect(lambda: self.save_new_user(dlg))
        dlg.exec()

    # def save_new_user(self, dlg):
    #     if not dlg.txt_fullname.text().strip():
    #         QMessageBox.warning(dlg, "Lỗi", "Họ tên không được trống")
    #         return

    #     self.user_service.create_user(
    #         dlg.txt_fullname.text(),
    #         dlg.txt_email.text(),
    #         dlg.txt_phone.text(),
    #         dlg.cbo_unit.currentData(),
    #         dlg.txt_username.text(),
    #         dlg.txt_password.text()
    #     )

    #     ActivityService().log(
    #         Session.current_user["id"],
    #         "Thêm người dùng"
    #     )

    #     dlg.accept()
    #     self.load_users()

    def save_new_user(self, dlg):
        if not dlg.txt_fullname.text().strip():
            QMessageBox.warning(dlg, "Lỗi", "Họ tên không được để trống")
            return

        if not dlg.txt_username.text().strip():
            QMessageBox.warning(dlg, "Lỗi", "Username không được để trống")
            return

        if not dlg.txt_password.text().strip():
            QMessageBox.warning(dlg, "Lỗi", "Mật khẩu không được để trống")
            return

        try:
            self.user_service.create_user(
                fullname=dlg.txt_fullname.text().strip(),
                email=dlg.txt_email.text().strip(),
                phone=dlg.txt_phone.text().strip(),
                unit_id=dlg.cbo_unit.currentData(),
                username=dlg.txt_username.text().strip(),
                password=dlg.txt_password.text().strip()
            )

            ActivityService().log(
                Session.current_user["id"],
                "Thêm người dùng"
            )

            QMessageBox.information(dlg, "Thành công", "Thêm user thành công")
            dlg.accept()
            self.load_users()

        except IntegrityError:
            QMessageBox.warning(
                dlg,
                "Lỗi",
                "Username đã tồn tại. Vui lòng chọn username khác!"
            )



    def delete_user(self):
        uid = self.get_selected_user_id()
        if not uid:
            QMessageBox.warning(self.view, "Lỗi", "Chưa chọn người dùng")
            return

        reply = QMessageBox.question(
            self.view,
            "Xác nhận",
            "Bạn có chắc muốn xoá người dùng này không?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        self.user_service.delete_user(uid)

        ActivityService().log(
            Session.current_user["id"],
            f"Xoá user ID={uid}"
        )

        self.load_users()

        if uid == Session.current_user["id"]:
            QMessageBox.warning(
                self.view, "Lỗi",
                "Không thể xoá chính tài khoản đang đăng nhập"
            )
            return

    
    def edit_user(self):
        uid = self.get_selected_user_id()
        if not uid:
            QMessageBox.warning(self.view, "Lỗi", "Chưa chọn người dùng")
            return

        user = self.user_service.get_user_by_id(uid)
        units = self.admin_unit_service.get_all_units()

        dlg = UserDialog(units, user)
        dlg.btn_save.clicked.connect(lambda: self.save_edit_user(dlg, user["id"]))
        dlg.exec()

    # def save_edit_user(self, dlg):
    #     self.user_service.update_user(
    #         dlg.user["id"],
    #         dlg.txt_fullname.text(),
    #         dlg.txt_email.text(),
    #         dlg.txt_phone.text(),
    #         dlg.cbo_unit.currentData()
    #     )

    #     ActivityService().log(
    #         Session.current_user["id"],
    #         f"Cập nhật user ID={dlg.user['id']}"
    #     )

    #     dlg.accept()
    #     self.load_users()

    def save_edit_user(self, dlg, user_id):
        if not dlg.txt_fullname.text().strip():
            QMessageBox.warning(dlg, "Lỗi", "Họ tên không được để trống")
            return

        try:
            self.user_service.update_user(
                user_id=user_id,
                fullname=dlg.txt_fullname.text().strip(),
                email=dlg.txt_email.text().strip(),
                phone=dlg.txt_phone.text().strip(),
                unit_id=dlg.cbo_unit.currentData()
            )

            ActivityService().log(
                Session.current_user["id"],
                f"Cập nhật user ID={user_id}"
            )

            QMessageBox.information(dlg, "Thành công", "Cập nhật user thành công")
            dlg.accept()
            self.load_users()

        except IntegrityError as e:
            QMessageBox.warning(
                dlg,
                "Lỗi",
                f"Lỗi khi cập nhật user: {str(e)}"
            )

