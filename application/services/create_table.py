from application.services.db_connection import DBConnection


def create_table():
    with DBConnection() as connection:
        with connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS phones (
                    phoneID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    contactName TEXT NOT NULL,
                    phoneValue INTEGER NOT NULL
                )
            """
            )
