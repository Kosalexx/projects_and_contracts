from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Optional

import tabulate
from psycopg2.errors import IntegrityError

from business_logic import ContractsLogic, ProjectLogic
from errors import IncorrectIdError, IncorrectStatusError, ValidationError

from .services import BaseMenu, InnerMenu

if TYPE_CHECKING:
    from data_access.dto import ContractsDTO
    from data_access.interfaces import DBGatewayProtocol


class Contract:
    def __init__(self, db_connector: DBGatewayProtocol) -> None:
        self._db_connector = db_connector
        self._logic = ContractsLogic(db_gateway=self._db_connector)

    def display_all_data(self) -> None:
        """Displays all contract information in the database."""
        data = self._logic.get_all_data()
        if data == []:
            print("There aren't any contracts in the database.")
        else:
            headers: list[str] = [
                "ID",
                "Name",
                "Creation Date",
                "Signing Date",
                "Status",
                "Related project (ID)",
            ]
            displayed_data = []
            for row in data:
                row_data = [
                    row.id,
                    row.name,
                    row.creation_date,
                    row.signing_date,
                    row.status,
                    row.project_id,
                ]
                displayed_data.append(row_data)
            result = tabulate.tabulate(tabular_data=displayed_data, headers=headers, tablefmt="psql")
            print("\nLIST OF ALL CONTRACTS\n")
            print(result)

    def create_new_contract(self) -> None:
        """Creates new contract in the database."""
        print("\nADD NEW CONTRACT\n")
        contract_name = input("Enter new contract name:")
        try:
            self._logic.create_record(contract_name=contract_name)
        except IntegrityError as err:
            print(f"\n[DB ERROR]. DETAIL:{err.pgerror}")
        else:
            print(f'New contract with name "{contract_name}" has been successfully created.')

    def update_contract(
        self,
        contract_id: Optional[str],
        header: str,
        required_status: str,
        new_status: str,
    ) -> None:
        """Updates contract data."""
        if not contract_id:
            print(header)
            entered_id = input("Enter contract ID: ")
            contract_id_value = entered_id
        else:
            contract_id_value = contract_id
        try:
            self._logic.update_data(
                contract_id=contract_id_value,
                required_status=required_status,
                new_status=new_status,
            )
        except IncorrectIdError as err:
            print(err)
        except IncorrectStatusError as err:
            print(err)
        except ValidationError as err:
            print(err)
        except IntegrityError as err:
            print(f"\n[DB ERROR]. DETAIL:{err.diag}")
        else:
            if new_status == "active":
                print(f"Contract with ID {contract_id_value} has been successfully confirmed.")
            elif new_status == "completed":
                project_logic = ProjectLogic(db_gateway=self._db_connector)
                try:
                    project_logic.remove_active_contract_from_project(contract_id=contract_id_value)
                except ValidationError:
                    raise
                except IncorrectIdError:
                    raise
                print(f"Contract with ID {contract_id_value} has been successfully completed.")

    def confirm_contract(self, contract_id: Optional[str] = None) -> None:
        """Confirms contract by entered id."""
        header = "\nCONFIRM CONTRACT\n"
        required_status = "draft"
        new_status = "active"
        self.update_contract(
            contract_id=contract_id,
            header=header,
            required_status=required_status,
            new_status=new_status,
        )

    def complete_contract(self, contract_id: Optional[str] = None) -> None:
        """Completes contract by entered id."""
        header = "\nCOMPLETE CONTRACT\n"
        required_status = "active"
        new_status = "completed"
        self.update_contract(
            contract_id=contract_id,
            header=header,
            required_status=required_status,
            new_status=new_status,
        )

    def _create_specific_contract_inner_menu(self, data: ContractsDTO) -> InnerMenu:
        title = f"Contract {data.id} menu"
        help_text = "Chose your action from menu:"
        if data.status == "draft":
            specific_contract_menu_objects_dict = {"Confirm contract": self.confirm_contract}
        elif data.status == "active":
            specific_contract_menu_objects_dict = {"Complete contract": self.complete_contract}
        else:
            specific_contract_menu_objects_dict = {}
        specific_contract_menu = InnerMenu(
            menu_objects=specific_contract_menu_objects_dict,
            title=title,
            help_text=help_text,
        )
        return specific_contract_menu

    def get_contract_by_id(self) -> None:
        """Gets specific contract from db by entered id."""

        print("\nGET CONTRACT BY ID\n")
        entered_id = input("Enter contract ID: ")
        try:
            result_data = self._logic.get_record_by_id(contract_id=entered_id)
        except IncorrectIdError as err:
            print(err)
        except ValidationError as err:
            print(err)
        else:
            headers: list[str] = [
                "ID",
                "Name",
                "Creation Date",
                "Signing Date",
                "Status",
                "Related project (ID)",
            ]
            displayed_data = [
                [
                    result_data.id,
                    result_data.name,
                    result_data.creation_date,
                    result_data.signing_date,
                    result_data.status,
                    result_data.project_id,
                ]
            ]
            result = tabulate.tabulate(tabular_data=displayed_data, headers=headers, tablefmt="psql")
            print(f"\nCONTRACT {result_data.id} INFO\n")
            print(result)
            specific_contract_menu = self._create_specific_contract_inner_menu(data=result_data)
            specific_contract_menu(entered_id=str(result_data.id))

    def __call__(self) -> None:
        title = "CONTRACTS MENU"
        contracts_menu_objects_dict: dict[str, Callable] = {
            "List of all contracts": self.display_all_data,
            "Add new contract": self.create_new_contract,
            "Get contract info by id": self.get_contract_by_id,
            "Confirm the contract": self.confirm_contract,
            "Complete the contract": self.complete_contract,
        }
        help_text = "Chose your action from Contracts menu:"
        contracts_menu = BaseMenu(menu_objects=contracts_menu_objects_dict, title=title, help_text=help_text)
        contracts_menu()
