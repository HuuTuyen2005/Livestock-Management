from database.mysql_connector import MySQLConnector

class PermissionService:
    def __init__(self):
        self.db = MySQLConnector()

    # ===== A. PERMISSION (1.8) =====
    def get_all_permissions(self):
        return self.db.fetch_all("""
            SELECT id, name, code, description, is_active
            FROM permissions
        """)

    def add_permission(self, name, code, description):
        self.db.execute("""
            INSERT INTO permissions (name, code, description)
            VALUES (%s, %s, %s)
        """, (name, code, description))


    def update_permission(self, pid, name, code, description):
        self.db.execute("""
            UPDATE permissions
            SET name=%s, code=%s, description=%s
            WHERE id=%s
        """, (name, code, description, pid))

    def toggle_permission(self, pid, active):
        self.db.execute("""
            UPDATE permissions SET is_active=%s WHERE id=%s
        """, (active, pid))

    def delete_permission(self, pid):
        cnt = self.db.fetch_one(
            """
            SELECT COUNT(*) AS cnt
            FROM group_permissions
            WHERE permissions_id = %s
            """,
            (pid,)
        )

        if cnt['cnt'] > 0:
            raise Exception(
                "Quyền này đang được gán cho nhóm, không thể xóa"
            )

        self.db.execute(
            "DELETE FROM permissions WHERE id = %s",
            (pid,)
        )



    # ===== B. GROUP PERMISSION (1.12) =====
    def get_groups(self):
        return self.db.fetch_all(
            "SELECT id, name FROM `group` WHERE is_active=1"
        )

    def get_permissions_by_group(self, group_id):
        return self.db.fetch_all("""
            SELECT p.id AS id
            FROM permissions p
            JOIN group_permissions gp ON gp.permissions_id = p.id
            WHERE gp.group_id = %s
        """, (group_id,))


    def save_group_permissions(self, group_id, permission_ids):
        self.db.execute(
            "DELETE FROM group_permissions WHERE group_id=%s",
            (group_id,)
        )
        for pid in permission_ids:
            self.db.execute("""
                INSERT INTO group_permissions (group_id, permissions_id)
                VALUES (%s, %s)
            """, (group_id, pid))

    # ===== C. VIEW GROUP PERMISSION (1.13) =====
    def view_group_permissions(self):
        return self.db.fetch_all("""
            SELECT 
                g.name AS group_name,
                p.name AS perm_name,
                p.code AS perm_code
            FROM group_permissions gp
            JOIN `group` g ON g.id = gp.group_id
            JOIN permissions p ON p.id = gp.permissions_id
            WHERE p.is_active = 1
            ORDER BY g.name
        """)

    
    def code_exists(self, code):
        r = self.db.fetch_one(
            "SELECT 1 FROM permissions WHERE code=%s",
            (code,)
        )
        return r is not None
