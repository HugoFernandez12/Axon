import sqlite3
from connection_manager import *


class ThemeManager:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def get_themes(self):
        self.cursor.execute("SELECT name FROM theme")
        return self.cursor.fetchall()

    def get_theme_ids(self):
        self.cursor.execute("SELECT id FROM theme")
        return self.cursor.fetchall()

    def get_group_theme(self, group_id):
        self.cursor.execute(
            "SELECT name FROM theme WHERE id =(SELECT theme_id FROM \"group\" WHERE id = (?))",
            (group_id,)
        )
        return self.cursor.fetchone()[0]

    def get_theme_id_by_name(self, theme_name):
        self.cursor.execute("SELECT id FROM theme WHERE name =(?)", (theme_name,))
        return self.cursor.fetchone()[0]

    def get_theme_name_by_id(self, theme_id):
        self.cursor.execute("SELECT name FROM theme WHERE id =(?)", (theme_id,))
        return self.cursor.fetchone()[0]

    def get_question_theme_id(self, question_id):
        self.cursor.execute("SELECT theme_id FROM question WHERE id=(?)", (question_id,))
        return self.cursor.fetchone()[0]

    def add_theme(self, theme_name):
        self.cursor.execute("INSERT INTO theme VALUES (NULL,(?))", (theme_name,))
