from database.mysql_connector import MySQLConnector

class GenConservationFacilityService:
    def __init__(self):
        self.db = MySQLConnector()

    def get_all(self):
        query = """
        SELECT
            f.id,
            f.name,
            f.address,
            f.phone,
            f.email,
            f.certification,
            f.scale,
            f.status,

            xa.id AS xa_id,
            xa.name AS xa_name,
            huyen.id AS huyen_id,
            huyen.name AS huyen_name,

            GROUP_CONCAT(g.name SEPARATOR ', ') AS gen_names

        FROM facility f
        LEFT JOIN administrative_unit xa
            ON f.unit_id = xa.id
        LEFT JOIN administrative_unit huyen
            ON xa.administrative_id = huyen.id
        LEFT JOIN facility_gen fg
            ON f.id = fg.facility_id
        LEFT JOIN gen g
            ON fg.gen_id = g.id

        WHERE f.type = 'GEN_CONSERVATION'
        GROUP BY f.id
        ORDER BY f.id DESC
        """
        return self.db.fetch_all(query)

    def search(self, keyword):
        query = """
        SELECT
            f.id,
            f.name,
            f.address,
            f.phone,
            f.email,
            f.certification,
            f.scale,
            f.status,

            xa.id AS xa_id,
            xa.name AS xa_name,
            huyen.id AS huyen_id,
            huyen.name AS huyen_name,

            GROUP_CONCAT(g.name SEPARATOR ', ') AS gen_names

        FROM facility f
        LEFT JOIN administrative_unit xa
            ON f.unit_id = xa.id
        LEFT JOIN administrative_unit huyen
            ON xa.administrative_id = huyen.id
        LEFT JOIN facility_gen fg
            ON f.id = fg.facility_id
        LEFT JOIN gen g
            ON fg.gen_id = g.id

        WHERE f.type = 'GEN_CONSERVATION'
          AND f.name LIKE %s
        GROUP BY f.id
        """
        return self.db.fetch_all(query, (f"%{keyword}%",))

    def create(self, data, gen_ids):
        query = """
        INSERT INTO facility
        (name, address, phone, email, certification,
         type, status, scale, unit_id)
        VALUES (%s,%s,%s,%s,%s,'GEN_CONSERVATION',%s,%s,%s)
        """
        facility_id = self.db.execute_insert(query, (
            data["name"],
            data["address"],
            data["phone"],
            data["email"],
            data["certification"],
            data["status"],
            data["scale"],
            data["unit_id"]
        ))

        for gen_id in gen_ids:
            self.db.execute(
                "INSERT INTO facility_gen (facility_id, gen_id) VALUES (%s,%s)",
                (facility_id, gen_id)
            )

    def update(self, facility_id, data, gen_ids):
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

        self.db.execute(
            "DELETE FROM facility_gen WHERE facility_id=%s",
            (facility_id,)
        )

        for gen_id in gen_ids:
            self.db.execute(
                "INSERT INTO facility_gen (facility_id, gen_id) VALUES (%s,%s)",
                (facility_id, gen_id)
            )

    def delete(self, facility_id):
        self.db.execute(
            "DELETE FROM facility_gen WHERE facility_id=%s",
            (facility_id,)
        )
        self.db.execute(
            "DELETE FROM facility WHERE id=%s",
            (facility_id,)
        )

    def get_by_id(self, facility_id):
        facility = self.db.fetch_one("""
            SELECT f.*,
                   xa.id AS xa_id,
                   huyen.id AS huyen_id
            FROM facility f
            LEFT JOIN administrative_unit xa ON f.unit_id = xa.id
            LEFT JOIN administrative_unit huyen ON xa.administrative_id = huyen.id
            WHERE f.id=%s
        """, (facility_id,))

        gens = self.db.fetch_all("""
            SELECT gen_id
            FROM facility_gen
            WHERE facility_id=%s
        """, (facility_id,))

        facility["gen_ids"] = [g["gen_id"] for g in gens]
        return facility
