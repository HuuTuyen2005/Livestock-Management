from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit,
    QPushButton
)


class GroupDialog(QDialog):
    def __init__(self, parent=None, group=None):
        super().__init__(parent)
        self.group = group
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Nhóm người dùng")

        layout = QVBoxLayout(self)

        self.name_input = QLineEdit()
        self.desc_input = QTextEdit()

        layout.addWidget(QLabel("Tên nhóm:"))
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel("Mô tả:"))
        layout.addWidget(self.desc_input)

        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton("Lưu")
        self.btn_cancel = QPushButton("Hủy")

        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_cancel)

        layout.addLayout(btn_layout)

        self.btn_cancel.clicked.connect(self.reject)
        self.btn_save.clicked.connect(self.accept)

        if self.group:
            self.name_input.setText(self.group["name"])
            self.desc_input.setText(self.group["description"] or "")

    def get_data(self):
        return {
            "name": self.name_input.text().strip(),
            "description": self.desc_input.toPlainText().strip()
        }
