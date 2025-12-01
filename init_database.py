import os
from connection_manager import get_cursor
from database_setup import DatabaseSetup


def init_database():
    if not os.path.exists('database'):
        os.makedirs('database')

    connection, cursor = get_cursor()

    db_setup = DatabaseSetup(connection, cursor)

    db_setup.create_database()

    db_setup.load_database()

    connection.commit()

    connection.close()


if __name__ == "__main__":
    try:
        init_database()
    except:
        pass
