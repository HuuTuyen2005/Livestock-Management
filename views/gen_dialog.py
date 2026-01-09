from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QComboBox
)

class GenDialog(QDialog):
    def __init__(self, data=None):
        super().__init__()
        # self.setWindowTitle("Thông tin Gen")
        if data:
            self.setWindowTitle("Sửa nguồn gen")
        else:
            self.setWindowTitle("Thêm nguồn gen")

        self.txt_name = QLineEdit()
        self.txt_description = QLineEdit()
        self.txt_origin = QLineEdit()
        self.txt_genetic_code = QLineEdit()

        self.cbo_status = QComboBox()
        self.cbo_status.addItem("Bình thường", 0)
        self.cbo_status.addItem("Đang bảo tồn", 1)

        self.btn_save = QPushButton("Lưu")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Tên Gen"))
        layout.addWidget(self.txt_name)
        layout.addWidget(QLabel("Mô tả"))
        layout.addWidget(self.txt_description)
        layout.addWidget(QLabel("Nguồn gốc"))
        layout.addWidget(self.txt_origin)
        layout.addWidget(QLabel("Mã Gen"))
        layout.addWidget(self.txt_genetic_code)
        # layout.addWidget(QLabel("Trạng thái"))
        # layout.addWidget(self.txt_status)
        layout.addWidget(QLabel("Trạng thái"))
        layout.addWidget(self.cbo_status)
        layout.addWidget(self.btn_save)      

        self.setLayout(layout)

        if data:
            self.txt_name.setText(data["name"])
            self.txt_description.setText(data["description"])
            self.txt_origin.setText(data["origin"] or "")
            self.txt_genetic_code.setText(data["genetic_code"] or "")
            # self.cbo_status.currentData(data["status"] or "")
            index = self.cbo_status.findData(int(data["status"]))
            if index >= 0:
                self.cbo_status.setCurrentIndex(index)