from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from psycopg2 import connection, cursor  # noqa: F401


class DBGatewayProtocol(Protocol):
    """Describes interface of object that creates cursor and connection objects for working with the database."""

    cursor: cursor
    connection: connection
