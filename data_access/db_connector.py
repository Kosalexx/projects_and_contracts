from __future__ import annotations

from typing import TYPE_CHECKING

import psycopg2

if TYPE_CHECKING:
    from psycopg2 import connection, cursor


class PostgreSQLGateway:
    """Creates PostgreSQL connection and cursor objects to the database using passed parameters.
    :param db_name: name of PostgreSQL database
    :type db_name: str
    :param db_user: name of the user who can work with the transferred PostgreSQL database
    :type db_user: str
    :param db_password: password of the user who can work with the transferred PostgreSQL database
    :type db_password: str
    :param db_host: host address hosting the PostgreSQL database
    :type db_host: str
    :param db_port: port of the PostgreSQL database
    :type db_host: str
    """

    def __init__(self, db_name: str, db_password: str, db_user: str, db_host: str, db_port: str) -> None:
        self._db_name = db_name
        self._db_password = db_password
        self._db_user = db_user
        self._db_host = db_host
        self._db_port = db_port
        self.connection = self._create_connection()
        self.cursor = self._create_cursor()

    def _create_connection(self) -> connection:
        """Creates PostgreSQL connection object."""
        conn = psycopg2.connect(
            database=self._db_name,
            user=self._db_user,
            password=self._db_password,
            host=self._db_host,
            port=self._db_port,
        )
        with conn as connection:
            return connection

    def _create_cursor(self) -> cursor:
        """Creates PostgreSQL cursor object."""
        return self.connection.cursor()
