from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from .contracts_ui import Contract
from .projects_ui import Project
from .services import BaseMenu

if TYPE_CHECKING:
    from data_access.interfaces import DBGatewayProtocol


def main_menu_ui(db_connector: DBGatewayProtocol) -> None:
    main_menu_objects_dict: dict[str, Callable] = {
        "Projects": Project(db_connector=db_connector),
        "Contacts": Contract(db_connector=db_connector),
    }
    main_menu = BaseMenu(menu_objects=main_menu_objects_dict)
    main_menu()
