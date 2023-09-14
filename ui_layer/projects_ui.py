from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Optional

import tabulate
from psycopg2.errors import IntegrityError

from business_logic import ContractsLogic, ProjectLogic
from data_access.dto import ProjectsDTO
from errors import ContractAlreadyExistError, IncorrectIdError, ValidationError

from .services import BaseMenu, InnerMenu

if TYPE_CHECKING:
    from data_access.interfaces import DBGatewayProtocol


class Project:
    def __init__(self, db_connector: DBGatewayProtocol) -> None:
        self._db_connector = db_connector
        self._logic = ProjectLogic(db_gateway=self._db_connector)
        self._contract_logic = ContractsLogic(db_gateway=self._db_connector)

    def display_all_data(self) -> None:
        """Displays all projects information in the database."""
        data = self._logic.get_all_data()
        if data == []:
            print("There aren't any contracts in the database.")
        else:
            headers: list[str] = [
                "ID",
                "Name",
                "Creation Date",
                "Active contract (ID)",
            ]
            displayed_data = []
            for row in data:
                row_data = [row.id, row.name, row.creation_date, row.contract_id]
                displayed_data.append(row_data)
            result = tabulate.tabulate(tabular_data=displayed_data, headers=headers, tablefmt="psql")
            print("\nLIST OF ALL PROJECTS\n")
            print(result)

    def create_new_project(self) -> None:
        """Creates new project in the database."""
        active_contracts = self._logic.get_active_contracts_ids()
        if active_contracts == []:
            print(
                "There aren't any active contracts in the database!\n"
                "Please create and/or confirm at least one contract!"
            )
        else:
            print("\nADD NEW PROJECTS\n")
            project_name = input("Enter project name: ")
            try:
                self._logic.create_record(entered_name=project_name)
            except IntegrityError as err:
                print(f'\nDB ERROR. DETAIL:{str(err).split("DETAIL: ")[1]}')
            except ValidationError as err:
                print(err)
            else:
                print(f'New contract with name "{project_name}" has been successfully created.')

    def add_contract_to_project(self, project_id: Optional[str] = None) -> None:
        """Adds contract to project."""

        print("\nADD CONTRACT TO PROJECT\n")
        if not project_id:
            entered_project = input("Enter project id: ")
            result_project_id = entered_project
        else:
            result_project_id = project_id
        contract_id = input('Enter contract id (contract must be with status "active"): ')
        try:
            self._logic.add_contract_to_project(contract_id=contract_id, project_id=result_project_id)
        except ValidationError as err:
            print(err)
        except IntegrityError as err:
            print(err.pgerror)
        except IncorrectIdError as err:
            print(err)
        except ContractAlreadyExistError as err:
            print(err)
        else:
            print(f"Contract {contract_id} has been successfully added to project {result_project_id}.")

    def complete_project_active_contract(self, project_id: str) -> None:
        """Completes active contract."""
        data = self._logic.get_record_by_id(project_id=project_id)
        active_contract = data.contract_id
        if not active_contract:
            raise IncorrectIdError(f"There aren't any projects with transmitted id {project_id}")
        else:
            self._contract_logic.update_data(
                contract_id=str(data.contract_id),
                required_status="active",
                new_status="completed",
            )
            self._logic.remove_active_contract_from_project(contract_id=str(data.contract_id))
            print(f"Contract with ID {data.contract_id} has been successfully completed.")

    def _create_specific_project_inner_menu(self, data: ProjectsDTO) -> InnerMenu:
        """Creates small menu of specific project."""
        title = f"Project {data.id} menu"
        help_text = "Chose your action from menu:"
        if not data.contract_id:
            specific_contract_menu_objects_dict: dict[str, Callable] = {"Add contract": self.add_contract_to_project}
        else:
            specific_contract_menu_objects_dict = {"Complete contract": self.complete_project_active_contract}
        specific_project_menu = InnerMenu(
            menu_objects=specific_contract_menu_objects_dict,
            title=title,
            help_text=help_text,
        )
        return specific_project_menu

    def get_project_by_id(self) -> None:
        """Gets specific project from db by entered id."""
        print("\nGET PROJECT BY ID\n")
        entered_id = input("Enter project ID: ")
        try:
            result_data = self._logic.get_record_by_id(project_id=entered_id)
        except IncorrectIdError as err:
            print(err)
        except ValidationError as err:
            print(err)
        else:
            headers: list[str] = [
                "ID",
                "Name",
                "Creation Date",
                "Active contract (ID)",
            ]
            displayed_data = [
                [
                    result_data.id,
                    result_data.name,
                    result_data.creation_date,
                    result_data.contract_id,
                ]
            ]
            result = tabulate.tabulate(tabular_data=displayed_data, headers=headers, tablefmt="psql")
            print(f"\nCONTRACT {result_data.id} INFO\n")
            print(result)
            specific_project_menu = self._create_specific_project_inner_menu(data=result_data)
            specific_project_menu(entered_id=str(result_data.id))

    def __call__(self) -> None:
        title = "PROJECTS MENU"
        project_menu_objects_dict: dict[str, Callable] = {
            "List of all projects": self.display_all_data,
            "Create new project": self.create_new_project,
            "Add contract to project": self.add_contract_to_project,
            "Get project by id": self.get_project_by_id,
        }
        help_text = "Chose your action from Projects menu:"
        projects_menu = BaseMenu(menu_objects=project_menu_objects_dict, title=title, help_text=help_text)
        projects_menu()
