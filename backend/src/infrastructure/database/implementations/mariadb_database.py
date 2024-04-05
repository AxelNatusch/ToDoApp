from typing import Any, Dict, List

import mysql.connector
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor

from src.infrastructure.database.database_interface import DatabaseInterface


class MariaDBDatabase(DatabaseInterface):
    """
    MariaDBDatabase class is a concrete implementation of DatabaseInterface
    that connects to a MariaDB database using the mysql-connector-python
    library.

    Attributes:
        config (Dict[str, Any]): A dictionary containing the configuration
            settings for the MariaDB connection.
        connection (MySQLConnection | None): A MySQLConnection object that
            represents the connection to the MariaDB database.

    Args:
        config (Dict[str, Any]): A dictionary containing the configuration
            settings for the MariaDB connection.

    Example Usage:
    ```python
    db.connect()

    try:
        db.transaction()  # Start the transaction

        # Perform multiple database operations
        db.execute("INSERT INTO table_name (column1, column2) VALUES (%s, %s)", ('value1', 'value2'))
        db.execute("UPDATE table_name SET column1 = %s WHERE column2 = %s", ('new_value', 'value2'))
        # More operations...

        db.commit()  # Commit the transaction if all operations succeed
    except Exception as e:
        db.rollback()  # Rollback the transaction if any operation fails
        log.ERROR(f"An error occurred: {e}")
    finally:
        db.disconnect()  # Always disconnect from the database
    ```
    """

    def __init__(self, config: Dict[str, Any]):
        self.config: Dict[str, Any] = config
        self.connection: MySQLConnection | None = None

    def connect(self) -> None:
        self.connection = mysql.connector.connect(**self.config)

    def disconnect(self) -> None:
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute(
        self, operation: str, parameters: List[Any] | None = None
    ) -> List[Any] | None:
        if self.connection is None:
            raise ConnectionError("Database connection is closed")

        cursor: MySQLCursor = self.connection.cursor()
        try:
            cursor.execute(operation, parameters)
            if cursor.with_rows:
                result: List[Any] = cursor.fetchall()
                return result
        except mysql.connector.Error as e:
            raise e
        finally:
            cursor.close()

    def transaction(self) -> None:
        if self.connection is None:
            raise ConnectionError("Database connection is closed")

        self.connection.start_transaction()

    def commit(self) -> None:
        if self.connection is None:
            raise ConnectionError("Database connection is closed")

        self.connection.commit()

    def rollback(self) -> None:
        if self.connection is None:
            raise ConnectionError("Database connection is closed")

        self.connection.rollback()
