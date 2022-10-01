from application.services.db_connection import DBConnection


def create_table():
    with DBConnection() as connection:
        with connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS phones (
                    phone_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    contact_name TEXT NOT NULL,
                    phone_value INTEGER NOT NULL
                )
            """
            )
