# projects_and_contracts

Projects_and_contracts is a Python console program for creating, modifying, and working with project and contract information

<details><summary> <h3>Logic of operation and limitations </h3></summary>

- the program offers to create contracts or projects until the user wants to finish working with the program.
- you cannot start filling a project without the existence of at least one active contract

1. Entities:
A contract contains the following fields: 
    - id
    - contract name, 
    - creation date (assigned at the moment of entity creation),
    - date of signing the contract, 
    - contract status (draft, active, completed), 
    - project (in which this contract is used)
The project contains the following fields: 
    - id
    - project name 
    - creation date (assigned at the moment of entity creation), 
    - link to the active contract
2. Logic
By default the contract is created in draft status, the user can change its status through the action "Confirm contract" (active), "Finalize contract" (completed).
At the moment of contract confirmation the date of contract signing is set. The project field from the Contract entity is not set.
You can add contracts from the project entity with the following logic:
- you cannot add the same contract;
- only active contracts can be added to the project;
- there cannot be more than one active contract in the project;
- any contract belonging to the project can be terminated from the project;
- one contract cannot be used in more than one project;
- when adding a contract to a project, the selected project is marked on the side of the contract.
</details>

## DEPENDENCIES

All necessary dependencies are described in the "pyproject.toml" file.

## USAGE

Before using the Projects_and_contracts program, check if you have a [.env] file in the main project directory with the following data:

```python
POSTGRES_DB = '<postgresql_db_name>'
POSTGRES_USER = '<postgresql_db_username>'
POSTGRES_PASSWORD = '<postgresql_db_password>'
POSTGRES_HOST = '<postgresql_db_host>'
POSTGRES_PORT = '<postgresql_db_port>'
```

Also before launching it is necessary to create a PostgreSQL database with the data specified in the .env file. The database schema is described in the file './database/create_tables.sql'. The './database/fill_tables.sql' file describes SQL commands for filling the database with default values (contract statuses).

Or you can create a database, build a program image, and run the container in the detach mode with the command

```bash
docker-compose up -d.
```
Then you can run the program inside the container using the following commands:
* The following command will open a bash terminal inside the container and run the program image.
```bash
docker-compose run app bash
```
* Next, just run the command
```python
python3 main.py
```
To exit the bash terminal inside the container, type 'exit'

Also after running the command "docker-compose up -d " you can start the container in the localhost terminal wiht ```python
python3 main.py``` command.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)