from database.mysql_connector import MySQLConnector

class SpeciesService:
    def __init__(self):
        self.db = MySQLConnector()

    def search(self, keyword: str):
        sql = """
            SELECT id, name, scientific_name,
                   conservation_status, export_restriction_status
            FROM species
            WHERE name LIKE %s
               OR scientific_name LIKE %s
            ORDER BY id DESC
        """
        like = f"%{keyword}%"
        return self.db.fetch_all(sql, (like, like))
    
    def get_all(self):
        return self.db.fetch_all("""
            SELECT id, name, scientific_name,
                   conservation_status, export_restriction_status
            FROM species
            ORDER BY name
        """)

    # def get_all(self):
    #     return self.db.fetch_all("""
    #         SELECT * FROM species
    #         ORDER BY name
    #     """)

    def create(self, name, scientific_name, conservation_status, export_status):
        self.db.execute("""
            INSERT INTO species (name, scientific_name, conservation_status, export_restriction_status)
            VALUES (%s, %s, %s, %s)
        """, (name, scientific_name, conservation_status, export_status))

    def update(self, species_id, name, scientific_name, conservation_status, export_status):
        self.db.execute("""
            UPDATE species
            SET name=%s,
                scientific_name=%s,
                conservation_status=%s,
                export_restriction_status=%s
            WHERE id=%s
        """, (name, scientific_name, conservation_status, export_status, species_id))

    # def delete(self, species_id):
    #     self.db.execute("""
    #         DELETE FROM species WHERE id=%s
    #     """, (species_id,))

    def delete(self, species_id):
        # Xoá liên kết với cơ sở nếu cần, hoặc check trước trong controller
        self.db.execute(
            "DELETE FROM facility_species WHERE species_id=%s",
            (species_id,)
        )
        # Xoá species
        self.db.execute(
            "DELETE FROM species WHERE id=%s",
            (species_id,)
        )

    def is_used(self, species_id):
        sql = """
            SELECT COUNT(*) AS cnt
            FROM facility_species
            WHERE species_id = %s
        """
        row = self.db.fetch_one(sql, (species_id,))
        return row["cnt"] > 0
