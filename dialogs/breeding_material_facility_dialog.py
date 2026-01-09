from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QComboBox, QHBoxLayout
)

class BreedingMaterialFacilityDialog(QDialog):
    def __init__(self, data=None):
        super().__init__()
        self.data = data
        self.setWindowTitle("Thông tin cơ sở tinh, phôi, ấp trứng")
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

        form.addRow("Tên cơ sở:", self.txt_name)
        form.addRow("Huyện:", self.cbo_huyen)
        form.addRow("Xã:", self.cbo_xa)
        form.addRow("Địa chỉ:", self.txt_address)
        form.addRow("Điện thoại:", self.txt_phone)
        form.addRow("Email:", self.txt_email)
        form.addRow("Giấy phép:", self.txt_certification)
        form.addRow("Quy mô:", self.cbo_scale)
        form.addRow("Trạng thái:", self.cbo_status)

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
