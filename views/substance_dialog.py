from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout,
    QLineEdit, QTextEdit, QComboBox,
    QPushButton, QHBoxLayout
)

class SubstanceDialog(QDialog):
    def __init__(self, data=None):
        super().__init__()
        self.setWindowTitle("Nguyên liệu / Hóa chất")
        self.resize(400, 300)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.txt_name = QLineEdit()
        self.txt_type = QLineEdit()
        self.txt_desc = QTextEdit()

        self.cbo_banned = QComboBox()
        self.cbo_banned.addItems([
            "Được phép sử dụng",
            "Bị cấm sử dụng"
        ])

        form.addRow("Tên:", self.txt_name)
        form.addRow("Loại:", self.txt_type)
        form.addRow("Mô tả:", self.txt_desc)
        form.addRow("Trạng thái:", self.cbo_banned)

        btn = QHBoxLayout()
        self.btn_save = QPushButton("Lưu")
        self.btn_cancel = QPushButton("Hủy")
        btn.addStretch()
        btn.addWidget(self.btn_save)
        btn.addWidget(self.btn_cancel)

        layout.addLayout(form)
        layout.addLayout(btn)

        self.btn_cancel.clicked.connect(self.reject)
        self.btn_save.clicked.connect(self.accept)

        if data:
            self.txt_name.setText(data["name"])
            self.txt_type.setText(data["type"])
            self.txt_desc.setPlainText(data["description"] or "")
            self.cbo_banned.setCurrentIndex(
                1 if data["banned"] == 1 else 0
            )
