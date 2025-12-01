import sqlite3
from connection_manager import *


class DatabaseLister:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def list_database(self):
        print("----theme----")
        self.cursor.execute("SELECT * FROM theme")
        for row in self.cursor.fetchall():
            print(row)

        print("----user----")
        self.cursor.execute("SELECT * FROM user")
        for row in self.cursor.fetchall():
            print(row)

        print("----answer----")
        self.cursor.execute("SELECT * FROM answer")
        for row in self.cursor.fetchall():
            print(row)

        print("----friend----")
        self.cursor.execute("SELECT * FROM friend")
        for row in self.cursor.fetchall():
            print(row)

        print("----group----")
        self.cursor.execute("SELECT * FROM \"group\"")
        for row in self.cursor.fetchall():
            print(row)

        print("----user_group----")
        self.cursor.execute("SELECT * FROM user_group")
        for row in self.cursor.fetchall():
            print(row)

        print("----question----")
        self.cursor.execute("SELECT * FROM question")
        for row in self.cursor.fetchall():
            print(row)
