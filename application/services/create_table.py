from application.services.db_connection import DBConnection


def create_table():
    with DBConnection() as connection:
        with connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS phones (
                    PhoneID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    ContactName TEXT NOT NULL,
                    PhoneValue INTEGER NOT NULL
                )
            """
            )
