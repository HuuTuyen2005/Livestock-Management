# from database.mysql_connector import MySQLConnector

# class SubstanceService:
#     def __init__(self):
#         self.db = MySQLConnector()

#     # ===== CRUD =====
#     def get_all(self):
#         return self.db.fetch_all("""
#             SELECT *
#             FROM substances
#             ORDER BY id DESC
#         """)

#     def search(self, keyword):
#         kw = f"%{keyword}%"
#         return self.db.fetch_all("""
#             SELECT *
#             FROM substances
#             WHERE name LIKE %s
#             ORDER BY id DESC
#         """, (kw,))

#     def get_by_id(self, sid):
#         return self.db.fetch_one("""
#             SELECT *
#             FROM substances
#             WHERE id=%s
#         """, (sid,))

#     def create(self, data):
#         return self.db.execute_insert("""
#             INSERT INTO substances (name, type, description, banned)
#             VALUES (%s, %s, %s, %s)
#         """, (
#             data["name"],
#             data["type"],
#             data["description"],
#             data["banned"]
#         ))

#     def update(self, sid, data):
#         self.db.execute("""
#             UPDATE substances
#             SET name=%s,
#                 type=%s,
#                 description=%s,
#                 banned=%s
#             WHERE id=%s
#         """, (
#             data["name"],
#             data["type"],
#             data["description"],
#             data["banned"],
#             sid
#         ))

#     def delete(self, sid):
#         # xoá quan hệ trước
#         self.db.execute(
#             "DELETE FROM food_substance WHERE substances_id=%s", (sid,)
#         )
#         self.db.execute(
#             "DELETE FROM substances WHERE id=%s", (sid,)
#         )


from database.mysql_connector import MySQLConnector

class SubstanceService:
    def __init__(self):
        self.db = MySQLConnector()

    def get_all(self, banned=None):
        sql = """
            SELECT id, name, type, description, banned
            FROM substances
        """
        params = []

        if banned is not None:
            sql += " WHERE banned=%s"
            params.append(banned)

        sql += " ORDER BY name"
        return self.db.fetch_all(sql, tuple(params))

    def search(self, keyword, banned=None):
        sql = """
            SELECT id, name, type, description, banned
            FROM substances
            WHERE name LIKE %s
        """
        params = [f"%{keyword}%"]

        if banned is not None:
            sql += " AND banned=%s"
            params.append(banned)

        sql += " ORDER BY name"
        return self.db.fetch_all(sql, tuple(params))

    def create(self, data):
        self.db.execute("""
            INSERT INTO substances(name, type, description, banned)
            VALUES (%s,%s,%s,%s)
        """, (
            data["name"],
            data["type"],
            data["description"],
            data["banned"]
        ))

    def update(self, sid, data):
        self.db.execute("""
            UPDATE substances
            SET name=%s, type=%s, description=%s, banned=%s
            WHERE id=%s
        """, (
            data["name"],
            data["type"],
            data["description"],
            data["banned"],
            sid
        ))

    def delete(self, sid):
        self.db.execute("DELETE FROM substances WHERE id=%s", (sid,))
