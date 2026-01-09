from database.mysql_connector import MySQLConnector

class FoodService:
    def __init__(self):
        self.db = MySQLConnector()

    def get_all(self):
        return self.db.fetch_all("""
            SELECT id, name, type, description
            FROM food
            ORDER BY id DESC
        """)

    # def search(self, keyword):

    #     return self.db.fetch_all("""
    #         SELECT id, name, type, description
    #         FROM food
    #         WHERE name LIKE %s OR type LIKE %s
    #     """, (f"%{keyword}%", f"%{keyword}%"))

    # def search(self, keyword: str):
    #     sql = """
    #         SELECT id, name, type, description
    #         FROM food
    #         WHERE name LIKE %s 
    #     """
    #     like = f"%{keyword}%"
    #     return self.db.fetch_all(sql, (like,))

    def create(self, name, type_, description):
        self.db.execute("""
            INSERT INTO food(name, type, description)
            VALUES (%s, %s, %s)
        """, (name, type_, description))

    def update(self, food_id, name, type_, description):
        self.db.execute("""
            UPDATE food
            SET name=%s, type=%s, description=%s
            WHERE id=%s
        """, (name, type_, description, food_id))

    def delete(self, food_id):
        # Xoá các substances liên quan trước để tránh lỗi FK
        self.db.execute(
            "DELETE FROM food_substance WHERE food_id=%s",
            (food_id,)
        )
        # Xoá food
        self.db.execute(
            "DELETE FROM food WHERE id=%s",
            (food_id,)
        )


    # ===== SUBSTANCE =====
    def get_substances(self):
        return self.db.fetch_all("""
            SELECT id, name, banned
            FROM substances
            ORDER BY name
        """)

    def get_selected_substances(self, food_id):
        rows = self.db.fetch_all("""
            SELECT substances_id AS id
            FROM food_substance
            WHERE food_id=%s
        """, (food_id,))
        return [r["id"] for r in rows]

    def save_substances(self, food_id, substance_ids):
        self.db.execute(
            "DELETE FROM food_substance WHERE food_id=%s",
            (food_id,)
        )
        for sid in substance_ids:
            self.db.execute("""
                INSERT INTO food_substance (food_id, substances_id)
                VALUES (%s, %s)
            """, (food_id, sid))


    def get_all_with_substances(self):
            return self.db.fetch_all("""
                SELECT 
                    f.id,
                    f.name,
                    f.type,
                    f.description,
                    GROUP_CONCAT(s.name SEPARATOR ', ') AS substances
                FROM food f
                LEFT JOIN food_substance fs 
                    ON f.id = fs.food_id
                LEFT JOIN substances s 
                    ON fs.substances_id = s.id
                GROUP BY f.id
                ORDER BY f.id DESC
            """)

    def search(self, keyword: str):
        sql = """
            SELECT 
                f.id,
                f.name,
                f.type,
                f.description,
                GROUP_CONCAT(s.name SEPARATOR ', ') AS substances
            FROM food f
            LEFT JOIN food_substance fs 
                ON f.id = fs.food_id
            LEFT JOIN substances s 
                ON fs.substances_id = s.id
            WHERE f.name LIKE %s
            GROUP BY f.id
            ORDER BY f.id DESC
        """
        like = f"%{keyword}%"
        return self.db.fetch_all(sql, (like,))
