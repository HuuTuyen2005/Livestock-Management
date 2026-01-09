from database.mysql_connector import MySQLConnector

class ManualService:
    def __init__(self):
        self.db = MySQLConnector()

    def get_all_manuals(self):
        return self.db.fetch_all("SELECT * FROM instructions ORDER BY id DESC")

    def get_manual_by_id(self, manual_id):
        return self.db.fetch_one("SELECT * FROM instructions WHERE id=%s", (manual_id,))

    def create_manual(self, title, content):
        return self.db.execute_insert("INSERT INTO instructions (title, content) VALUES (%s, %s)", (title, content))

    def update_manual(self, manual_id, title, content):
        self.db.execute("UPDATE instructions SET title=%s, content=%s WHERE id=%s", (title, content, manual_id))

    def delete_manual(self, manual_id):
        self.db.execute("DELETE FROM instructions WHERE id=%s", (manual_id,))
