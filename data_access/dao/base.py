from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from data_access.interfaces import DBGatewayProtocol


class BaseDAO:
    """Base Data access object."""

    def __init__(self, db_gateway: DBGatewayProtocol) -> None:
        self._db_gateway = db_gateway
