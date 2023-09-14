from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from psycopg2 import IntegrityError

from data_access.dao import ContractsDAO
from data_access.dto import ContractsDTO
from errors import IncorrectIdError, IncorrectStatusError, ValidationError
from validators import validate_entered_id

if TYPE_CHECKING:
    from data_access.interfaces import DBGatewayProtocol


class ContractsLogic:
    """Contains methods for displaying project data."""

    def __init__(self, db_gateway: DBGatewayProtocol) -> None:
        self._db_gateway = db_gateway
        self._dao = ContractsDAO(db_gateway=self._db_gateway)

    def get_all_data(self) -> list[ContractsDTO]:
        """Gets all contract information from the database."""

        data: list[ContractsDTO] = self._dao.get_all_contracts_info()
        return data

    def create_record(self, contract_name: str) -> None:
        """Creates new record in database with entered data."""

        contracts_dto = ContractsDTO(name=contract_name)
        try:
            self._dao.create_record(data=contracts_dto)
        except IntegrityError as err:
            raise err

    def update_data(self, contract_id: str, required_status: str, new_status: str) -> None:
        """Updates contract data."""

        try:
            validate_entered_id(entered_id=contract_id)
        except ValidationError:
            raise
        else:
            contract_id_int = int(contract_id)
        contract_info = self._dao.get_contract_info_by_id(contract_id_int)
        if not contract_info:
            raise IncorrectIdError("[ERROR]: There isn't a contract with entered ID in the database.")
        if contract_info.status != required_status:
            raise IncorrectStatusError(f"[ERROR]: You must specify a contract with a status '{required_status}'.")
        else:
            contract_info.status = new_status
            if not contract_info.signing_date:
                contract_info.signing_date = datetime.now(tz=timezone.utc)
            try:
                self._dao.update_record(data=contract_info)
            except IntegrityError:
                raise

    def get_record_by_id(self, contract_id: str) -> ContractsDTO:
        """Gets contract by entered id from database."""

        try:
            validate_entered_id(entered_id=contract_id)
        except ValidationError:
            raise
        else:
            contract_id_int = int(contract_id)
        contract_info = self._dao.get_contract_info_by_id(contract_id_int)
        if not contract_info:
            raise IncorrectIdError("[ERROR]: There isn't a contract with entered ID in the database.")
        else:
            return contract_info
