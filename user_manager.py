import sqlite3
from connection_manager import *
from datetime import datetime


class UserManager:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def get_users(self):
        self.cursor.execute("SELECT name FROM user")
        return self.cursor.fetchall()

    def get_user_answers(self, user_id):
        self.cursor.execute(
            "SELECT correct_answer, date, question_id FROM answer WHERE user_id=(?)",
            (user_id,)
        )
        return self.cursor.fetchall()

    def get_user_credentials(self, user_id):
        self.cursor.execute("SELECT name, password FROM user WHERE id=(?)", (user_id,))
        return self.cursor.fetchone()[0]

    def get_username(self, user_id):
        self.cursor.execute("SELECT name FROM user WHERE id=(?)", (user_id,))
        return self.cursor.fetchone()[0]

    def get_password(self, username):
        self.cursor.execute("SELECT password FROM user WHERE name=(?)", (username,))
        return self.cursor.fetchone()[0]

    def get_user_id_by_name(self, username):
        self.cursor.execute("SELECT id FROM user WHERE name=(?)", (username,))
        return self.cursor.fetchone()[0]

    def create_user(self, username, password):
        try:
            self.get_user_id_by_name(username)
        except:
            self.cursor.execute("INSERT INTO user VALUES(NULL,?,?)", (username, password))

    def save_answer(self, user_id, question_id, is_correct):
        self.cursor.execute(
            "INSERT INTO answer VALUES(NULL,?,?,?,?)",
            (user_id, datetime.now().strftime("%Y%m%d"), question_id, is_correct)
        )

    def update_password(self, username, new_password):
        self.cursor.execute(
            "UPDATE user SET password=(?) WHERE name=(?)",
            (new_password, username)
        )
