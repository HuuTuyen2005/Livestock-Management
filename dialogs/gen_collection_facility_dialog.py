from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QComboBox,
    QListWidget, QListWidgetItem, QHBoxLayout
)
from PyQt6.QtCore import Qt

class GenCollectionFacilityDialog(QDialog):
    def __init__(self, data=None, gens=None):
        super().__init__()
        self.data = data
        self.gens = gens or []
        self.setWindowTitle("Thông tin cơ sở thu thập nguồn gen")
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
        self.txt_certification = QLineEdit()

        self.cbo_scale = QComboBox()
        self.cbo_scale.addItems(["Nhỏ", "Vừa", "Lớn"])

        self.cbo_status = QComboBox()
        self.cbo_status.addItems(["Ngừng hoạt động", "Hoạt động"])

        self.lst_gen = QListWidget()
        self.lst_gen.setSelectionMode(
            QListWidget.SelectionMode.MultiSelection
        )

        for g in self.gens:
            item = QListWidgetItem(g["name"])
            item.setData(Qt.ItemDataRole.UserRole, g["id"])
            self.lst_gen.addItem(item)

        form.addRow("Tên tổ chức/cá nhân:", self.txt_name)
        form.addRow("Huyện:", self.cbo_huyen)
        form.addRow("Xã:", self.cbo_xa)
        form.addRow("Địa chỉ:", self.txt_address)
        form.addRow("Điện thoại:", self.txt_phone)
        form.addRow("Email:", self.txt_email)
        form.addRow("Giấy phép:", self.txt_certification)
        form.addRow("Quy mô:", self.cbo_scale)
        form.addRow("Trạng thái:", self.cbo_status)
        form.addRow("Nguồn gen thu thập:", self.lst_gen)

        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton("Lưu")
        self.btn_cancel = QPushButton("Hủy")

        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_cancel)

        layout.addLayout(form)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

        self.btn_cancel.clicked.connect(self.reject)
        self.btn_save.clicked.connect(self.accept)

    def _load_data(self):
        self.txt_name.setText(self.data["name"])
        self.txt_address.setText(self.data["address"])
        self.txt_phone.setText(self.data["phone"])
        self.txt_email.setText(self.data["email"])
        self.txt_certification.setText(self.data["certification"])
        self.cbo_scale.setCurrentText(self.data["scale"])
        self.cbo_status.setCurrentIndex(self.data["status"])

        for i in range(self.lst_gen.count()):
            item = self.lst_gen.item(i)
            if item.data(Qt.ItemDataRole.UserRole) in self.data["gen_ids"]:
                item.setSelected(True)

    def get_selected_gens(self):
        return [
            item.data(Qt.ItemDataRole.UserRole)
            for item in self.lst_gen.selectedItems()
        ]
