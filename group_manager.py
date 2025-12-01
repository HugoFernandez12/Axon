import sqlite3
from connection_manager import *


class GroupManager:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def get_groups(self):
        self.cursor.execute("SELECT name FROM \"group\"")
        return self.cursor.fetchall()

    def get_group_users_scores(self, group_id):
        self.cursor.execute(
            "SELECT user_id, score FROM user_group WHERE group_id=(?)",
            (group_id,)
        )
        return self.cursor.fetchall()

    def get_user_groups(self, user_id):
        self.cursor.execute("SELECT name FROM \"group\" WHERE user_id=(?)", (user_id,))
        return self.cursor.fetchall()

    def get_group_theme_id(self, group_id):
        self.cursor.execute("SELECT theme_id FROM \"group\" WHERE id = (?)", (group_id,))
        return self.cursor.fetchone()[0]

    def get_group_id_by_name(self, name):
        self.cursor.execute("SELECT id FROM \"group\" WHERE name =(?)", (name,))
        return self.cursor.fetchone()[0]

    def get_user_group_score(self, user_id, group_id):
        self.cursor.execute(
            "SELECT score FROM user_group WHERE user_id=(?) and group_id=(?)",
            (user_id, group_id)
        )
        try:
            return self.cursor.fetchone()[0]
        except:
            return 0

    def get_user_groups_scores(self, user_id):
        self.cursor.execute(
            "SELECT group_id, score FROM user_group WHERE user_id=(?)",
            (user_id,)
        )
        return self.cursor.fetchall()

    def get_group_users(self, group_id):
        self.cursor.execute("SELECT user_id FROM user_group WHERE group_id=(?)", (group_id,))
        return self.cursor.fetchall()

    def get_group_name(self, group_id):
        self.cursor.execute("SELECT name FROM \"group\" WHERE id=(?)", (group_id,))
        return self.cursor.fetchone()[0]

    def create_group(self, theme_id, name, user_ids):
        self.cursor.execute("INSERT INTO \"group\" VALUES(NULL,?,?)", (theme_id, name))
        for user_id in user_ids:
            group_id = self.get_group_id_by_name(name)
            self.cursor.execute("INSERT INTO user_group VALUES(?,?,0)", (group_id, user_id))

    def increment_score(self, group_id, user_id):
        self.cursor.execute(
            "UPDATE user_group SET score = score + 1 WHERE user_id=(?) and group_id=(?)",
            (user_id, group_id)
        )

    def update_group_name(self, name, new_name):
        self.cursor.execute(
            "UPDATE \"group\" SET name = (?) WHERE name=(?)",
            (new_name, name)
        )

    def remove_user_from_group(self, group_id, user_id):
        self.cursor.execute(
            "DELETE FROM user_group WHERE group_id = (?) and user_id = (?)",
            (group_id, user_id)
        )

    def delete_group(self, group_id):
        self.cursor.execute("DELETE FROM \"group\" WHERE id = (?)", (group_id,))
