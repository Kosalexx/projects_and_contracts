from data_access.db_connector import PostgreSQLGateway
from settings import (
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
)
from ui_layer import main_menu_ui

db_gateway = PostgreSQLGateway(
    db_name=POSTGRES_DB,
    db_user=POSTGRES_USER,
    db_password=POSTGRES_PASSWORD,
    db_host=POSTGRES_HOST,
    db_port=POSTGRES_PORT,
)

if __name__ == "__main__":
    main_menu_ui(db_connector=db_gateway)
