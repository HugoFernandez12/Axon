import sqlite3
from connection_manager import *


class FriendManager:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def get_friends(self, user_id):
        self.cursor.execute(
            "SELECT name FROM user WHERE id IN (SELECT user_id_2 FROM friend WHERE user_id_1=(?))",
            (user_id,)
        )
        return self.cursor.fetchall()

    def add_friend(self, user_id_1, user_id_2):
        self.cursor.execute("INSERT INTO friend VALUES(NULL,?,?)", (user_id_1, user_id_2))
