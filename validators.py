from errors import IncorrectUserInputError, ValidationError


def validate_user_choice(user_choice: str) -> None:
    if not user_choice.isdigit():
        raise IncorrectUserInputError("[ERROR]: Choice must be digit.")


def validate_entered_id(entered_id: str) -> None:
    if not entered_id.isdigit():
        raise ValidationError("[ERROR]: Entered id must be digit!")


def validate_active_contract_id(entered_id: str, contracts_ids_list: list) -> None:
    validate_entered_id(entered_id=entered_id)
    tuple_id = (int(entered_id),)
    if tuple_id not in contracts_ids_list:
        raise ValidationError("[ERROR]: Selected contract must be active.")
