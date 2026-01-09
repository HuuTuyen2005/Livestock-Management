from database.mysql_connector import MySQLConnector


class GroupService:
    def __init__(self):
        self.db = MySQLConnector()

    # ===================== GROUP CRUD =====================
    def get_all_groups(self):
        return self.db.fetch_all(
            "SELECT id, name, description, is_active FROM `group`"
        )

    def search_groups(self, keyword):
        return self.db.fetch_all(
            """
            SELECT id, name, description, is_active
            FROM `group`
            WHERE name LIKE %s OR description LIKE %s
            """,
            (f"%{keyword}%", f"%{keyword}%")
        )

    def add_group(self, name, description):
        query = """
            INSERT INTO `group` (name, description, is_active)
            VALUES (%s, %s, 1)
        """
        self.db.execute(query, (name, description))

    def update_group(self, group_id, name, description):
        query = """
            UPDATE `group`
            SET name = %s, description = %s
            WHERE id = %s
        """
        self.db.execute(query, (name, description, group_id))

    def delete_group(self, group_id):
        # Xóa mapping user_groups trước (tránh lỗi FK)
        self.db.execute(
            "DELETE FROM user_groups WHERE group_id = %s",
            (group_id,)
        )

        self.db.execute(
            "DELETE FROM `group` WHERE id = %s",
            (group_id,)
        )

    def set_group_active(self, group_id, is_active):
        self.db.execute(
            "UPDATE `group` SET is_active = %s WHERE id = %s",
            (is_active, group_id)
        )

    # ===================== TRA CỨU =====================
    def get_users_in_group(self, group_id):
        return self.db.fetch_all(
            """
            SELECT u.id, u.fullname
            FROM user u
            JOIN user_groups ug ON ug.user_id = u.id
            WHERE ug.group_id = %s
            AND u.status = 1
            """,
            (group_id,)
        )

    def get_groups_of_user(self, user_id):
        return self.db.fetch_all(
            """
            SELECT g.id, g.name
            FROM `group` g
            JOIN user_groups ug ON ug.group_id = g.id
            WHERE ug.user_id = %s
            """,
            (user_id,)
        )

    def get_all_users(self):
        return self.db.fetch_all(
            "SELECT id, fullname FROM user WHERE status = 1"
        )
