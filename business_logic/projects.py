from __future__ import annotations

from typing import TYPE_CHECKING

from psycopg2.errors import IntegrityError

from data_access.dao import ContractsDAO, ProjectsDAO
from data_access.dto import ProjectsDTO
from errors import ContractAlreadyExistError, IncorrectIdError, ValidationError
from validators import validate_active_contract_id, validate_entered_id

if TYPE_CHECKING:
    from data_access.interfaces import DBGatewayProtocol


class ProjectLogic:
    """Contains methods for displaying project data."""

    def __init__(self, db_gateway: DBGatewayProtocol) -> None:
        self._db_gateway = db_gateway
        self._dao = ProjectsDAO(db_gateway=self._db_gateway)
        self._contracts_dao = ContractsDAO(db_gateway=self._db_gateway)

    def get_all_data(self) -> list[ProjectsDTO]:
        """Gets all projects information from the database."""

        data: list[ProjectsDTO] = self._dao.get_all_projects_info()
        return data

    def get_active_contracts_ids(self) -> list[tuple[int]]:
        """Gets list ids of active contracts"""
        contract_dao = ContractsDAO(db_gateway=self._db_gateway)
        active_contracts_list = contract_dao.get_active_contracts_ids()
        return active_contracts_list

    def create_record(self, entered_name: str) -> None:
        """Creates new record in database with entered data."""

        project_dto = ProjectsDTO(name=entered_name)
        try:
            self._dao.create_record(data=project_dto)
        except IntegrityError:
            raise

    def get_record_by_id(self, project_id: str) -> ProjectsDTO:
        """Gets project by entered id from database."""

        try:
            validate_entered_id(entered_id=project_id)
        except ValidationError:
            raise
        else:
            project_id_int = int(project_id)
        project_info = self._dao.get_info_by_id(project_id_int)
        if not project_info:
            raise IncorrectIdError("[ERROR]: There isn't a contract with entered ID in the database.")
        else:
            return project_info

    def add_contract_to_project(self, project_id: str, contract_id: str) -> None:
        """Adds contract to project."""

        try:
            validate_active_contract_id(
                entered_id=contract_id,
                contracts_ids_list=self.get_active_contracts_ids(),
            )
            project_info = self.get_record_by_id(project_id=project_id)
        except ValidationError:
            raise
        except IncorrectIdError:
            raise
        else:
            try:
                if project_info.contract_id:
                    raise ContractAlreadyExistError(
                        f"Project {project_id} already has an active contract! "
                        f"Please select another contract to add."
                    )
                else:
                    int_contract_id = int(contract_id)
                    int_project_id = int(project_id)
                    project_info.contract_id = int_contract_id
                    self._dao.update_record(project_info)
                    contract_info = self._contracts_dao.get_contract_info_by_id(contract_id=int_contract_id)
                    if contract_info:
                        contract_info.project_id = int_project_id
                        self._contracts_dao.update_record(data=contract_info)
                    else:
                        raise IncorrectIdError("[ERROR]: There isn't a contract with entered ID in the database.")
            except IntegrityError:
                raise

    def remove_active_contract_from_project(self, contract_id: str) -> None:
        """Removes active contract_id."""

        try:
            validate_entered_id(entered_id=contract_id)
        except ValidationError:
            raise
        int_contract_id = int(contract_id)
        data = self._dao.get_project_info_by_active_contract(contract_id=int_contract_id)
        if not data:
            raise IncorrectIdError(f"Project with entered active_contract_id {contract_id} does not exist.")
        else:
            data.contract_id = None
            self._dao.update_record(data=data)
