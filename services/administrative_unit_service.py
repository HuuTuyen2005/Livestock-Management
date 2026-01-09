from database.mysql_connector import MySQLConnector

class AdministrativeUnitService:
    def __init__(self):
        self.db = MySQLConnector()

    def get_districts(self):
        """Lấy danh sách huyện/quận (level_id = 1)"""
        return self.db.fetch_all("""
            SELECT id, name
            FROM administrative_unit
            WHERE level_id = 1
            ORDER BY name
        """)

    def get_wards_by_district(self, district_id):
        """Lấy danh sách xã/phường theo huyện"""
        return self.db.fetch_all("""
            SELECT id, name
            FROM administrative_unit
            WHERE level_id = 2
              AND administrative_id = %s
            ORDER BY name
        """, (district_id,))
    
    def get_wards_with_parent(self):
        """
        Lấy tất cả xã/phường (level_id = 2)
        kèm tên quận/huyện cha
        """
        return self.db.fetch_all("""
            SELECT 
                u.id,
                u.name AS unit_name,
                p.name AS parent_name
            FROM administrative_unit u
            LEFT JOIN administrative_unit p
                ON u.administrative_id = p.id
            WHERE u.level_id = 2
            ORDER BY p.name, u.name
        """)
