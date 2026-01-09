from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel,
    QLineEdit, QPushButton
)

class SpeciesDialog(QDialog):
    def __init__(self, data=None):
        super().__init__()
        self.setWindowTitle("Thông tin giống")

        self.txt_name = QLineEdit()
        self.txt_scientific = QLineEdit()
        self.txt_conservation = QLineEdit()
        self.txt_export = QLineEdit()

        self.btn_save = QPushButton("Lưu")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Tên giống"))
        layout.addWidget(self.txt_name)
        layout.addWidget(QLabel("Tên khoa học"))
        layout.addWidget(self.txt_scientific)
        layout.addWidget(QLabel("Tình trạng bảo tồn"))
        layout.addWidget(self.txt_conservation)
        layout.addWidget(QLabel("Tình trạng cấm xuất khẩu"))
        layout.addWidget(self.txt_export)
        layout.addWidget(self.btn_save)

        self.setLayout(layout)

        if data:
            self.txt_name.setText(data["name"])
            self.txt_scientific.setText(data["scientific_name"])
            self.txt_conservation.setText(data["conservation_status"] or "")
            self.txt_export.setText(data["export_restriction_status"] or "")
