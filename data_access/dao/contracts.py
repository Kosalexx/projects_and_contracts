from __future__ import annotations

from typing import Optional

from psycopg2.errors import IntegrityError

from data_access.dto import ContractsDTO

from .base import BaseDAO
from .statuses import StatusesDAO


class ContractsDAO(BaseDAO):
    """Contains methods for working with the "contracts" table from the database."""

    def get_ids_list(self) -> list[tuple[int,]]:
        """Gets ids from projects table."""

        self._db_gateway.cursor.execute("SELECT id FROM contracts;")
        final_result: list[tuple[int,]] = self._db_gateway.cursor.fetchall()
        return final_result

    def get_active_contracts_ids(self) -> list[tuple[int,]]:
        """Gets contract ids with 'active' status."""

        self._db_gateway.cursor.execute(
            "SELECT contracts.id FROM contracts "
            "JOIN statuses on status_id = statuses.id "
            "WHERE statuses.name = 'active';"
        )
        final_result: list[tuple[int,]] = self._db_gateway.cursor.fetchall()
        return final_result

    def get_all_contracts_info(self) -> list[ContractsDTO]:
        """Gets all data from contracts table."""

        self._db_gateway.cursor.execute(
            "SELECT contracts.id AS id, contracts.name AS name, contracts.creation_date AS creation_date, "
            "contracts.signing_date AS signing_date, statuses.name AS status, contracts.project_id AS project_id "
            "FROM contracts "
            "JOIN statuses ON contracts.status_id = statuses.id;"
        )
        fetched_list: list[tuple] = self._db_gateway.cursor.fetchall()
        final_dto_list: list[ContractsDTO] = []
        for row in fetched_list:
            contract_id, name, creation_date, signing_date, status, project_id = row
            row_dto = ContractsDTO(
                id=contract_id,
                name=name,
                creation_date=creation_date,
                signing_date=signing_date,
                status=status,
                project_id=project_id,
            )
            final_dto_list.append(row_dto)
        return final_dto_list

    def create_record(self, data: ContractsDTO) -> None:
        """Creates record in table 'contracts'."""

        status_id = StatusesDAO(db_gateway=self._db_gateway).get_status_id(data.status)
        try:
            self._db_gateway.cursor.execute(
                "INSERT INTO contracts (name, status_id) VALUES " "(%s, %s);",
                (data.name, status_id),
            )
        except IntegrityError as err:
            self._db_gateway.connection.rollback()
            raise err
        else:
            self._db_gateway.connection.commit()

    def get_contract_info_by_id(self, contract_id: int) -> Optional[ContractsDTO]:
        """Gets contract info by entered contract_id."""

        self._db_gateway.cursor.execute(
            "SELECT contracts.id AS id, contracts.name AS name, contracts.creation_date AS creation_date, "
            "contracts.signing_date AS signing_date, statuses.name AS status, contracts.project_id AS project_id "
            "FROM contracts "
            "JOIN statuses ON contracts.status_id = statuses.id "
            "WHERE contracts.id = %s;",
            (contract_id,),
        )
        fetched_tuple: tuple = self._db_gateway.cursor.fetchone()

        if fetched_tuple:
            (
                contract_id_from_db,
                name,
                creation_date,
                signing_date,
                status,
                project_id,
            ) = fetched_tuple
            return ContractsDTO(
                id=contract_id_from_db,
                name=name,
                creation_date=creation_date,
                signing_date=signing_date,
                status=status,
                project_id=project_id,
            )
        return None

    def update_record(self, data: ContractsDTO) -> None:
        """Updates record in the database."""

        try:
            self._db_gateway.cursor.execute(
                "UPDATE contracts SET name = %s, signing_date = %s, status_id = "
                "(SELECT id FROM statuses WHERE statuses.name = %s), project_id = %s "
                "WHERE id = %s;",
                (data.name, data.signing_date, data.status, data.project_id, data.id),
            )
        except IntegrityError as err:
            self._db_gateway.connection.rollback()
            raise err
        else:
            self._db_gateway.connection.commit()
