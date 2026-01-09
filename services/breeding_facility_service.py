from database.mysql_connector import MySQLConnector

class BreedingFacilityService:
    def __init__(self):
        self.db = MySQLConnector()

    def get_all(self):
        query = """
        SELECT 
            f.id, f.name, f.address, f.phone, f.email,
            f.certification, f.scale, f.status,

            xa.id AS xa_id,
            xa.name AS xa_name,
            huyen.id AS huyen_id,
            huyen.name AS huyen_name

        FROM facility f
        LEFT JOIN administrative_unit xa 
            ON f.unit_id = xa.id
        LEFT JOIN administrative_unit huyen 
            ON xa.administrative_id = huyen.id

        WHERE f.type = 'BREEDING_FACILITY'
        ORDER BY f.id DESC
        """
        return self.db.fetch_all(query)

    def search(self, keyword):
        query = """
        SELECT 
            f.id, f.name, f.address, f.phone, f.email,
            f.certification, f.scale, f.status,

            xa.id AS xa_id,
            xa.name AS xa_name,
            huyen.id AS huyen_id,
            huyen.name AS huyen_name

        FROM facility f
        LEFT JOIN administrative_unit xa 
            ON f.unit_id = xa.id
        LEFT JOIN administrative_unit huyen 
            ON xa.administrative_id = huyen.id

        WHERE f.type = 'BREEDING_FACILITY'
          AND f.name LIKE %s
        """
        return self.db.fetch_all(query, (f"%{keyword}%",))

    def create(self, data):
        query = """
        INSERT INTO facility
        (name, address, phone, email, certification,
         type, status, scale, unit_id)
        VALUES (%s,%s,%s,%s,%s,'BREEDING_FACILITY',%s,%s,%s)
        """
        self.db.execute_insert(query, (
            data["name"],
            data["address"],
            data["phone"],
            data["email"],
            data["certification"],
            data["status"],
            data["scale"],
            data["unit_id"]   # ID xã
        ))

    def update(self, facility_id, data):
        query = """
        UPDATE facility
        SET name=%s,
            address=%s,
            phone=%s,
            email=%s,
            certification=%s,
            scale=%s,
            status=%s,
            unit_id=%s
        WHERE id=%s
        """
        self.db.execute(query, (
            data["name"],
            data["address"],
            data["phone"],
            data["email"],
            data["certification"],
            data["scale"],
            data["status"],
            data["unit_id"],
            facility_id
        ))

    def delete(self, facility_id):
        self.db.execute("DELETE FROM facility WHERE id=%s", (facility_id,))

    def get_by_id(self, facility_id):
        query = """
        SELECT 
            f.*,
            xa.id AS xa_id,
            huyen.id AS huyen_id
        FROM facility f
        LEFT JOIN administrative_unit xa ON f.unit_id = xa.id
        LEFT JOIN administrative_unit huyen ON xa.administrative_id = huyen.id
        WHERE f.id=%s
        """
        return self.db.fetch_one(query, (facility_id,))
