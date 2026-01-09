from database.mysql_connector import MySQLConnector

class GenService:
    def __init__(self):
        self.db = MySQLConnector()

    def search(self, keyword: str):
        sql = """
            SELECT id, name, description, 
            origin, genetic_code, status
            FROM gen
            WHERE name LIKE %s
            ORDER BY id 
        """
        like = f"%{keyword}%"
        return self.db.fetch_all(sql, (like,))
        
    def get_all(self):
        return self.db.fetch_all("""
            SELECT id, name, description, 
            origin, genetic_code, status 
            FROM gen
            ORDER BY name
        """)
    
    def create(self, name, description, origin, genetic_code, status):
        self.db.execute("""
            INSERT INTO gen (name, description, origin, genetic_code, status)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, description, origin, genetic_code, status))

    def update(self, gen_id, name, description, origin, genetic_code, status):
        self.db.execute("""
            UPDATE gen
            SET name = %s,
                description = %s,
                origin = %s,
                genetic_code = %s,
                status = %s
            WHERE id = %s
        """, (name, description, origin, genetic_code, status, gen_id))
    
    def delete(self, gen_id):
        self.db.execute("""
            DELETE FROM gen WHERE id = %s
        """, (gen_id,))