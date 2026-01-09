from database.mysql_connector import MySQLConnector

class AdminUnitService:
    def __init__(self):
        self.db = MySQLConnector()

    def get_districts(self):
        return self.db.fetch_all("""
            SELECT id, name FROM administrative_unit
            WHERE level_id = 1
            ORDER BY name
        """)

    def get_communes_by_district(self, district_id):
        return self.db.fetch_all("""
            SELECT id, name FROM administrative_unit
            WHERE level_id = 2 AND administrative_id = %s
            ORDER BY name
        """, (district_id,))

    def create_unit(self, name, level_id, parent_id=None):
        self.db.execute("""
            INSERT INTO administrative_unit (name, level_id, administrative_id)
            VALUES (%s, %s, %s)
        """, (name, level_id, parent_id))

    def update_unit(self, unit_id, name):
        self.db.execute("""
            UPDATE administrative_unit SET name=%s WHERE id=%s
        """, (name, unit_id))

    def delete_unit(self, unit_id):
        self.db.execute("""
            DELETE FROM administrative_unit WHERE id=%s
        """, (unit_id,))

    def search_units(self, keyword):
        return self.db.fetch_all("""
            SELECT 
                au.id,
                au.name,
                au.level_id,
                au.administrative_id
            FROM administrative_unit au
            WHERE au.name LIKE %s
            ORDER BY au.level_id, au.name
        """, (f"%{keyword}%",))
    
    def get_all_units(self):
        return self.db.fetch_all("""
            SELECT id, name FROM administrative_unit
            ORDER BY name
        """)
