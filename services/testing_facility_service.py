from database.mysql_connector import MySQLConnector

class TestingFacilityService:
    def __init__(self):
        self.db = MySQLConnector()

    def get_all(self):
        query = """
        SELECT DISTINCT
            f.id, f.name, f.address, f.phone, f.email,
            f.scale, f.status,

            xa.name AS xa_name,
            huyen.name AS huyen_name,

            GROUP_CONCAT(s.name SEPARATOR ', ') AS species_names
        FROM facility f
        LEFT JOIN administrative_unit xa ON f.unit_id = xa.id
        LEFT JOIN administrative_unit huyen ON xa.administrative_id = huyen.id
        LEFT JOIN facility_species fs ON f.id = fs.facility_id
        LEFT JOIN species s ON fs.species_id = s.id
        WHERE f.type = 'TESTING_FACILITY'
        GROUP BY f.id
        ORDER BY f.id DESC
        """
        return self.db.fetch_all(query)

    def search(self, keyword):
        query = """
        SELECT DISTINCT
            f.id, f.name, f.address, f.phone, f.email,
            f.scale, f.status,

            xa.name AS xa_name,
            huyen.name AS huyen_name,

            GROUP_CONCAT(s.name SEPARATOR ', ') AS species_names
        FROM facility f
        LEFT JOIN administrative_unit xa ON f.unit_id = xa.id
        LEFT JOIN administrative_unit huyen ON xa.administrative_id = huyen.id
        LEFT JOIN facility_species fs ON f.id = fs.facility_id
        LEFT JOIN species s ON fs.species_id = s.id
        WHERE f.type = 'TESTING_FACILITY'
          AND f.name LIKE %s
        GROUP BY f.id
        """
        return self.db.fetch_all(query, (f"%{keyword}%",))

    def get_by_id(self, facility_id):
        return self.db.fetch_one(
            "SELECT * FROM facility WHERE id=%s",
            (facility_id,)
        )

    def get_species_ids(self, facility_id):
        rows = self.db.fetch_all(
            "SELECT species_id FROM facility_species WHERE facility_id=%s",
            (facility_id,)
        )
        return [r["species_id"] for r in rows]

    def create(self, data, species_ids):
        query = """
        INSERT INTO facility
        (name, address, phone, email, type, scale, status, unit_id)
        VALUES (%s,%s,%s,%s,'TESTING_FACILITY',%s,%s,%s)
        """
        facility_id = self.db.execute_insert(query, (
            data["name"],
            data["address"],
            data["phone"],
            data["email"],
            data["scale"],
            data["status"],
            data["unit_id"]
        ))

        self._sync_species(facility_id, species_ids)

    def update(self, facility_id, data, species_ids):
        query = """
        UPDATE facility
        SET name=%s, address=%s, phone=%s, email=%s,
            scale=%s, status=%s, unit_id=%s
        WHERE id=%s
        """
        self.db.execute(query, (
            data["name"],
            data["address"],
            data["phone"],
            data["email"],
            data["scale"],
            data["status"],
            data["unit_id"],
            facility_id
        ))

        self.db.execute(
            "DELETE FROM facility_species WHERE facility_id=%s",
            (facility_id,)
        )
        self._sync_species(facility_id, species_ids)

    def delete(self, facility_id):
        self.db.execute(
            "DELETE FROM facility_species WHERE facility_id=%s",
            (facility_id,)
        )
        self.db.execute("DELETE FROM facility WHERE id=%s", (facility_id,))

    def _sync_species(self, facility_id, species_ids):
        query = """
        INSERT INTO facility_species (facility_id, species_id)
        VALUES (%s,%s)
        """
        for sid in species_ids:
            self.db.execute(query, (facility_id, sid))
