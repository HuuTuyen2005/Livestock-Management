from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton,
    QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt


# class FoodDialog(QDialog):
#     def __init__(self, data=None):
#         super().__init__()
#         self.setWindowTitle("Thức ăn")
#         self.resize(400, 300)

#         layout = QVBoxLayout(self)

#         self.txt_name = QLineEdit()
#         self.txt_type = QLineEdit()
#         self.txt_description = QTextEdit()

#         layout.addWidget(QLabel("Tên thức ăn"))
#         layout.addWidget(self.txt_name)

#         layout.addWidget(QLabel("Loại"))
#         layout.addWidget(self.txt_type)

#         layout.addWidget(QLabel("Mô tả"))
#         layout.addWidget(self.txt_description)

#         # Buttons
#         btn_layout = QHBoxLayout()
#         self.btn_save = QPushButton("Lưu")
#         self.btn_cancel = QPushButton("Huỷ")

#         btn_layout.addWidget(self.btn_save)
#         btn_layout.addWidget(self.btn_cancel)

#         layout.addLayout(btn_layout)

#         self.btn_cancel.clicked.connect(self.reject)

#         if data:
#             self.txt_name.setText(data["name"])
#             self.txt_type.setText(data["type"])
#             self.txt_description.setPlainText(
#                 data["description"] or ""
#             )

class FoodDialog(QDialog):
    def __init__(self, data=None, substances=None, selected_substances=None):
        super().__init__()
        self.setWindowTitle("Thức ăn")
        self.resize(450, 450)

        layout = QVBoxLayout(self)

        self.txt_name = QLineEdit()
        self.txt_type = QLineEdit()
        self.txt_description = QTextEdit()

        layout.addWidget(QLabel("Tên thức ăn"))
        layout.addWidget(self.txt_name)

        layout.addWidget(QLabel("Loại"))
        layout.addWidget(self.txt_type)

        layout.addWidget(QLabel("Mô tả"))
        layout.addWidget(self.txt_description)

        # ===== SUBSTANCE =====
        layout.addWidget(QLabel("Chất / phụ gia"))

        self.lst_substance = QListWidget()
        self.lst_substance.setSelectionMode(
            QListWidget.SelectionMode.MultiSelection
        )

        if substances:
            for s in substances:
                item = QListWidgetItem(s["name"])
                item.setData(Qt.ItemDataRole.UserRole, s["id"])

                if s["banned"] == 1:
                    item.setFlags(Qt.ItemFlag.NoItemFlags)  # ❌ cấm chọn

                self.lst_substance.addItem(item)

        layout.addWidget(self.lst_substance)

        # Buttons
        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton("Lưu")
        self.btn_cancel = QPushButton("Huỷ")

        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)

        self.btn_cancel.clicked.connect(self.reject)

        # ===== EDIT MODE =====
        if data:
            self.txt_name.setText(data["name"])
            self.txt_type.setText(data["type"])
            self.txt_description.setPlainText(data["description"] or "")

        if selected_substances:
            for i in range(self.lst_substance.count()):
                item = self.lst_substance.item(i)
                if item.data(Qt.ItemDataRole.UserRole) in selected_substances:
                    item.setSelected(True)

    def get_selected_substances(self):
        return [
            item.data(Qt.ItemDataRole.UserRole)
            for item in self.lst_substance.selectedItems()
        ]

