from PyQt6.QtWidgets import (
    QMainWindow, QMessageBox, QWidget,
    QHBoxLayout, QTreeWidget, QTreeWidgetItem,
    QStackedWidget, QLabel
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

from auth.permission_checker import has_permission
from auth.session import Session

from controllers.admin_unit_controller import AdminUnitController
from controllers.user_controller import UserController
from controllers.change_password_controller import ChangePasswordController
from controllers.group_controller import GroupController
from controllers.system_history_controller import SystemHistoryController
from controllers.species_controller import SpeciesController
from controllers.gen_controller import GenController
from controllers.food_controller import FoodController
from controllers.substance_controller import SubstanceController
from controllers.permission_controller import PermissionController
from controllers.account_controller import AccountController
from controllers.manual_controller import ManualController
from controllers.report_controller import ReportController
from controllers.breeding_facility_controller import BreedingFacilityController
from controllers.breeding_material_facility_controller import BreedingMaterialFacilityController
from controllers.male_breeding_owner_controller import MaleBreedingOwnerController
from controllers.trading_facility_controller import TradingFacilityController
from controllers.testing_facility_controller import TestingFacilityController
from controllers.gen_collection_facility_controller import GenCollectionFacilityController
from controllers.gen_conservation_facility_controller import GenConservationFacilityController
from controllers.gen_development_facility_controller import GenDevelopmentFacilityController
from controllers.feed_facility_controller import FeedFacilityController
from controllers.feed_trading_facility_controller import FeedTradingFacilityController
from controllers.feed_testing_facility_controller import FeedTestingFacilityController
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hệ thống quản lý giống và thức ăn chăn nuôi")
        self.resize(1300, 750)

        self.controllers = {}  # cache controller
        self._init_ui()

        # ===== LOAD QSS STYLE =====
        try:
            # Thư mục chứa main_window.py
            base_dir = os.path.dirname(os.path.abspath(__file__))
            qss_path = os.path.join(base_dir, "..", "fonts", "style.qss")
            qss_path = os.path.abspath(qss_path)  # chuyển thành đường dẫn tuyệt đối
            
            with open(qss_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Không tìm thấy file style.qss, sử dụng style mặc định")

    # ================= UI =================
    def _init_ui(self):
        central = QWidget()
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)

        # ===== SIDEBAR =====
        self.sidebar = QTreeWidget()
        self.sidebar.setHeaderHidden(True)
        self.sidebar.setMaximumWidth(300)
        self.sidebar.itemClicked.connect(self._handle_sidebar_click)

        self._build_sidebar()

        # ===== STACKED WIDGET =====
        self.stack = QStackedWidget()

        # Trang mặc định
        self.home = QLabel("Chào mừng bạn đến hệ thống quản lý")
        self.home.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stack.addWidget(self.home)

        layout.addWidget(self.sidebar)
        layout.addWidget(self.stack)
        self.setCentralWidget(central)

    # ================= SIDEBAR =================
    def _build_sidebar(self):
        self.sidebar.clear()

        # ===== HỆ THỐNG =====
        system = QTreeWidgetItem(["Hệ thống"])
        system.setIcon(0, QIcon.fromTheme("preferences-system"))

        if Session.current_user:  # chỉ cần user đăng nhập mới thấy
            self._add_item(system, "Thông tin tài khoản", "user-identity")

                # Chỉ hiển thị nếu user có quyền MANUAL_VIEW
        if "MANUAL_VIEW" in Session.permissions:
            self._add_item(system, "Hướng dẫn sử dụng", "help-browser")

        if has_permission("USER_MANAGE"):
            self._add_item(system, "Quản lý người dùng", "user-group-new")

        if has_permission("GROUP_MANAGE"):
            self._add_item(system, "Quản lý nhóm", "system-users")

        if has_permission("PERMISSION_MANAGE"):
            self._add_item(system, "Quản lý phân quyền", "dialog-password")

        if has_permission("ADMIN_UNIT_MANAGE"):
            self._add_item(system, "Đơn vị hành chính", "folder")

        if has_permission("HISTORY_VIEW"):
            self._add_item(system, "Lịch sử hệ thống", "view-history")

        self._add_item(system, "Đổi mật khẩu", "document-edit")
        self._add_item(system, "Đăng xuất", "system-log-out")

        # ===== NGHIỆP VỤ =====
        # livestock = QTreeWidgetItem(["Nghiệp vụ chăn nuôi"])
        # livestock.setIcon(0, QIcon.fromTheme("applications-office"))

        # if has_permission("SPECIES_MANAGE"):
        #     self._add_item(livestock, "Quản lý giống", "applications-science")

        # if has_permission("GEN_MANAGE"):
        #     self._add_item(livestock, "Quản lý nguồn gen", "network-wired")

        # if has_permission("FACILITY_MANAGE"):
        #     self._add_item(livestock, "Quản lý cơ sở", "office-building")

        if has_permission("FACILITY_MANAGE"):
            facility = QTreeWidgetItem(["Quản lý cơ sở"])
            facility.setIcon(0, QIcon.fromTheme("office-building"))

            self._add_item(facility, "Cơ sở sản xuất con giống", "list-add")
            self._add_item(facility, "Cơ sở tinh, phôi, ấp trứng", "network-server")
            self._add_item(facility, "Cơ sở sở hữu đực giống", "user-group")
            self._add_item(facility, "Cơ sở mua bán giống", "folder")
            self._add_item(facility, "Cơ sở khảo nghiệm giống", "lab")
            self._add_item(facility, "Danh mục giống đặc biệt", "special")
        
        if has_permission("GEN_MANAGE"):
            gen = QTreeWidgetItem(["Nguồn gen giống vật nuôi"])
            gen.setIcon(0, QIcon.fromTheme("gen-facility"))

            self._add_item(gen, "Quản lý nguồn gen", "gen-manage")
            self._add_item(gen, "Cơ sở thu thập nguồn gen", "collection")
            self._add_item(gen, "Cơ sở bảo tồn nguồn gen", "conservation")
            self._add_item(gen, "Cơ sở phát triển nguồn gen", "development")

        # ===== THỨC ĂN =====
        food = QTreeWidgetItem(["Thức ăn chăn nuôi"])
        food.setIcon(0, QIcon.fromTheme("applications-utilities"))

        if has_permission("FOOD_MANAGE"):
            self._add_item(food, "Thức ăn", "package-x-generic")
            self._add_item(food, "Cơ sở sản suất thức ăn chăn nuôi", "production-feed")
            self._add_item(food, "Cơ sở mua bán thức ăn chăn nuôi", "trading-feed")
            self._add_item(food, "Cơ sở khảo nghiệm thức ăn chăn nuôi", "testing-feed")

        if has_permission("SUBSTANCE_MANAGE"):
            self._add_item(food, "Danh mục nguyên liệu & chất cấm", "dialog-warning")

                # --- Báo cáo ---
        report = QTreeWidgetItem(["Báo cáo"])
        report.setIcon(0, QIcon.fromTheme("document-preview"))
        if has_permission("REPORT_VIEW"):
            self._add_item(report, "Báo cáo hệ thống", "document-preview")

        self.sidebar.addTopLevelItems([system, facility, gen, food, report])
        self.sidebar.expandAll()

    def _add_item(self, parent, text, icon_name):
        item = QTreeWidgetItem(parent, [text])
        item.setIcon(0, QIcon.fromTheme(icon_name))
        return item

    # ================= HANDLE CLICK =================
    def _handle_sidebar_click(self, item, column):
        text = item.text(0)

        if text == "Đăng xuất":
            self.logout()
            return

        if text == "Đổi mật khẩu":
            self.change_password()
            return

        mapping = {
            "Quản lý người dùng": UserController,
            "Quản lý nhóm": GroupController,
            "Quản lý phân quyền": PermissionController,
            "Đơn vị hành chính": AdminUnitController,
            "Lịch sử hệ thống": SystemHistoryController,
            # "Quản lý giống": SpeciesController,
            
            # "Quản lý cơ sở": FacilityController,
            "Cơ sở sản xuất con giống": BreedingFacilityController,
            "Cơ sở tinh, phôi, ấp trứng": BreedingMaterialFacilityController,
            "Cơ sở sở hữu đực giống": MaleBreedingOwnerController,
            "Cơ sở mua bán giống": TradingFacilityController,
            "Cơ sở khảo nghiệm giống": TestingFacilityController,
            "Danh mục giống đặc biệt": SpeciesController,

            "Quản lý nguồn gen": GenController,
            "Cơ sở thu thập nguồn gen": GenCollectionFacilityController,
            "Cơ sở bảo tồn nguồn gen": GenConservationFacilityController,
            "Cơ sở phát triển nguồn gen": GenDevelopmentFacilityController,
            "Thức ăn": FoodController,
            "Cơ sở sản suất thức ăn chăn nuôi": FeedFacilityController,
            "Cơ sở mua bán thức ăn chăn nuôi": FeedTradingFacilityController,
            "Cơ sở khảo nghiệm thức ăn chăn nuôi": FeedTestingFacilityController,
            "Danh mục nguyên liệu & chất cấm": SubstanceController,
            "Thông tin tài khoản": AccountController,
            "Hướng dẫn sử dụng": ManualController,
            "Báo cáo hệ thống": ReportController
        }

        if text not in mapping:
            return

        # Nếu đã mở rồi -> chuyển trang
        if text in self.controllers:
            self.stack.setCurrentWidget(self.controllers[text].view)
            return

        # Chưa mở -> tạo controller + add vào stack
        controller = mapping[text]()
        self.controllers[text] = controller
        self.stack.addWidget(controller.view)
        self.stack.setCurrentWidget(controller.view)

    # ================= ACTIONS =================
    def change_password(self):
        dlg = ChangePasswordController()
        dlg.view.exec()

    def logout(self):
        reply = QMessageBox.question(
            self,
            "Đăng xuất",
            "Bạn có chắc chắn muốn đăng xuất không?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            
            Session.current_user = None
            Session.permissions = set()
            QMessageBox.information(self, "Logout", "Đã đăng xuất")
            self.close()
