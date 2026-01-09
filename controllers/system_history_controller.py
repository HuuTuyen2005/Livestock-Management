from views.system_history_view import SystemHistoryView
from services.system_history_service import SystemHistoryService
from PyQt6.QtWidgets import QTableWidgetItem

class SystemHistoryController:
    def __init__(self):
        self.view = SystemHistoryView()
        self.service = SystemHistoryService()

        self.load_data()

        self.view.btn_search.clicked.connect(self.search)
        self.view.btn_refresh.clicked.connect(self.load_data)

    def load_data(self):
        records = self.service.get_all()
        self._fill_table(records)

    def search(self):
        keyword = self.view.txt_keyword.text().strip()
        if not keyword:
            self.load_data()
            return

        records = self.service.search(keyword)
        self._fill_table(records)

    def _fill_table(self, records):
        self.view.table.setRowCount(len(records))

        for row, r in enumerate(records):
            self.view.table.setItem(row, 0, QTableWidgetItem(str(r["id"])))
            self.view.table.setItem(row, 1, QTableWidgetItem(r["username"]))
            self.view.table.setItem(row, 2, QTableWidgetItem(r["activities"]))
            self.view.table.setItem(row, 3, QTableWidgetItem(str(r["time"])))
            self.view.table.setItem(row, 4, QTableWidgetItem(str(r["user_id"])))
