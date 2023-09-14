from __future__ import annotations

from .base import BaseDAO


class StatusesDAO(BaseDAO):
    """Contains methods for working with the "Statuses" table from the database."""

    def get_status_id(self, status_name: str) -> int:
        """Gets the status ID with entered status_name."""

        self._db_gateway.cursor.execute("SELECT id FROM statuses WHERE name = (%s);", (status_name,))
        tuple_res = self._db_gateway.cursor.fetchone()
        status_id = int(tuple_res[0])
        return status_id
