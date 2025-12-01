import sqlite3


def get_connection():
    connection = sqlite3.connect("database/axon.db", check_same_thread=False)
    return connection


def get_cursor():
    connection = get_connection()
    cursor = connection.cursor()
    return connection, cursor
