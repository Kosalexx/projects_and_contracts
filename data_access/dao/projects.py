from __future__ import annotations

from typing import Optional

from psycopg2.errors import IntegrityError

from data_access.dto import ProjectsDTO

from .base import BaseDAO


class ProjectsDAO(BaseDAO):
    """Contains methods for working with the "projects" table from the database."""

    def get_ids_list(self) -> list[tuple[int,]]:
        """Gets ids from projects table."""

        self._db_gateway.cursor.execute("SELECT id FROM projects;")
        final_result: list[tuple[int,]] = self._db_gateway.cursor.fetchall()
        return final_result

    def get_all_projects_info(self) -> list[ProjectsDTO]:
        """Gets all data from projects table."""

        self._db_gateway.cursor.execute("SELECT * FROM projects;")
        fetched_list: list[tuple] = self._db_gateway.cursor.fetchall()
        final_dto_list: list[ProjectsDTO] = []
        for row in fetched_list:
            project_id, name, creation_date, contract_id = row
            row_dto = ProjectsDTO(
                id=project_id,
                name=name,
                creation_date=creation_date,
                contract_id=contract_id,
            )
            final_dto_list.append(row_dto)
        return final_dto_list

    def create_record(self, data: ProjectsDTO) -> None:
        """Creates record in table 'projects'."""

        try:
            self._db_gateway.cursor.execute(
                "INSERT INTO projects (name, active_contract_id) VALUES " "(%s, %s);",
                (data.name, data.contract_id),
            )
        except IntegrityError:
            self._db_gateway.connection.rollback()
            raise
        else:
            print("Record successfully added!")
            self._db_gateway.connection.commit()

    def get_info_by_id(self, entered_id: int) -> Optional[ProjectsDTO]:
        """Gets info about project with entered id."""

        self._db_gateway.cursor.execute("SELECT * FROM projects " "WHERE id = %s;", (entered_id,))
        fetched_tuple: tuple = self._db_gateway.cursor.fetchone()
        if fetched_tuple:
            project_id_from_db, name, creation_date, active_contract_id = fetched_tuple
            return ProjectsDTO(
                id=project_id_from_db,
                name=name,
                creation_date=creation_date,
                contract_id=active_contract_id,
            )
        else:
            return None

    def update_record(self, data: ProjectsDTO) -> None:
        """Updates record in the database."""
        try:
            self._db_gateway.cursor.execute(
                "UPDATE projects SET name = %s, active_contract_id = %s " "WHERE id = %s;",
                (data.name, data.contract_id, data.id),
            )
        except IntegrityError:
            self._db_gateway.connection.rollback()
            raise
        else:
            self._db_gateway.connection.commit()

    def get_project_info_by_active_contract(self, contract_id: int) -> Optional[ProjectsDTO]:
        """Gets info about project by active contract id."""

        self._db_gateway.cursor.execute("SELECT * FROM projects " "WHERE active_contract_id = %s;", (contract_id,))
        fetched_tuple: tuple = self._db_gateway.cursor.fetchone()
        if fetched_tuple:
            project_id_from_db, name, creation_date, active_contract_id = fetched_tuple
            return ProjectsDTO(
                id=project_id_from_db,
                name=name,
                creation_date=creation_date,
                contract_id=active_contract_id,
            )
        return None
