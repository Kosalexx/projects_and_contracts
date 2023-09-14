class IncorrectUserInputError(Exception):
    """Raises when the user enters incorrect data."""


class IncorrectIdError(Exception):
    """Raises when an invalid id is entered (does not exist in the database)."""


class ValidationError(Exception):
    """Raises when validation is unsuccessful."""


class IncorrectStatusError(Exception):
    """Raises when a contract with an incorrect status is selected."""


class ContractAlreadyExistError(Exception):
    """Raises when project already has an active contract."""
