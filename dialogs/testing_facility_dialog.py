from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QComboBox,
    QListWidget, QListWidgetItem, QHBoxLayout
)
from PyQt6.QtCore import Qt
from services.species_service import SpeciesService

class TestingFacilityDialog(QDialog):
    def __init__(self, data=None, selected_species=None):
        super().__init__()
        self.data = data
        self.selected_species = selected_species or []
        self.setWindowTitle("Thông tin cơ sở khảo nghiệm giống")
        self._init_ui()
        if data:
            self._load_data()

    def _init_ui(self):
        layout = QVBoxLayout()
        form = QFormLayout()

        self.txt_name = QLineEdit()
        self.cbo_huyen = QComboBox()
        self.cbo_xa = QComboBox()
        self.txt_address = QLineEdit()
        self.txt_phone = QLineEdit()
        self.txt_email = QLineEdit()

        self.lst_species = QListWidget()
        self.lst_species.setSelectionMode(
            QListWidget.SelectionMode.MultiSelection
        )

        for s in SpeciesService().get_all():
            item = QListWidgetItem(s["name"])
            item.setData(Qt.ItemDataRole.UserRole, s["id"])
            self.lst_species.addItem(item)

        self.cbo_scale = QComboBox()
        self.cbo_scale.addItems(["Nhỏ", "Vừa", "Lớn"])

        self.cbo_status = QComboBox()
        self.cbo_status.addItems(["Ngừng hoạt động", "Hoạt động"])

        form.addRow("Tên cơ sở:", self.txt_name)
        form.addRow("Huyện:", self.cbo_huyen)
        form.addRow("Xã:", self.cbo_xa)
        form.addRow("Địa chỉ:", self.txt_address)
        form.addRow("Điện thoại:", self.txt_phone)
        form.addRow("Email:", self.txt_email)
        form.addRow("Giống khảo nghiệm:", self.lst_species)
        form.addRow("Quy mô:", self.cbo_scale)
        form.addRow("Trạng thái:", self.cbo_status)

        btns = QHBoxLayout()
        self.btn_save = QPushButton("Lưu")
        self.btn_cancel = QPushButton("Hủy")

        btns.addStretch()
        btns.addWidget(self.btn_save)
        btns.addWidget(self.btn_cancel)

        layout.addLayout(form)
        layout.addLayout(btns)
        self.setLayout(layout)

        self.btn_cancel.clicked.connect(self.reject)
        self.btn_save.clicked.connect(self.accept)

    def _load_data(self):
        self.txt_name.setText(self.data["name"])
        self.txt_address.setText(self.data["address"])
        self.txt_phone.setText(self.data["phone"])
        self.txt_email.setText(self.data["email"])
        self.cbo_scale.setCurrentText(self.data["scale"])
        self.cbo_status.setCurrentIndex(self.data["status"])

        for i in range(self.lst_species.count()):
            item = self.lst_species.item(i)
            if item.data(Qt.ItemDataRole.UserRole) in self.selected_species:
                item.setSelected(True)

    def get_selected_species_ids(self):
        return [
            i.data(Qt.ItemDataRole.UserRole)
            for i in self.lst_species.selectedItems()
        ]
