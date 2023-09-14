from typing import Any, Callable

from errors import IncorrectUserInputError
from validators import validate_user_choice


class BaseMenu:
    """Contains methods and logic for creating and displaying a console menu."""

    def __init__(
        self,
        menu_objects: dict[str, Callable],
        title: str = "MAIN MENU",
        help_text: str = "Chose your action from main menu:",
    ) -> None:
        self._title = title
        self._help_text = help_text
        self._menu_objects = menu_objects
        self._menu = self.create_menu()

    def create_menu(self) -> str:
        """Creates console menu."""

        menu = f"\n======================= {self._title} ============================"
        first_string_length = len(menu) - 1
        menu += f"\n{self._help_text}\n"
        for ind, key in enumerate(self._menu_objects.keys()):
            menu += f"{ind + 1} - {str(key)}\n"
        if self._title == "MAIN MENU":
            menu += f"{len(self._menu_objects) + 1} - Exit\n"
        else:
            menu += f"{len(self._menu_objects) + 1} - Return to the previous menu\n"
        menu += "=" * first_string_length
        return menu

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        while True:
            print(self._menu)
            user_choice = input("Your choice: ")
            try:
                validate_user_choice(user_choice=user_choice)
            except IncorrectUserInputError as err:
                print(err)
                continue
            if 0 < int(user_choice) <= len(self._menu_objects):
                for ind, key in enumerate(self._menu_objects.keys()):
                    if int(user_choice) == ind + 1:
                        func = self._menu_objects[key]
                        func(*args, **kwargs)
            elif int(user_choice) == len(self._menu_objects) + 1:
                break
            else:
                print(f"Choice must be in digit from 1 to {len(self._menu_objects) + 1}")
                continue


class InnerMenu(BaseMenu):
    """Contains methods and logic for creating and displaying a small console menu for using in inner functions."""

    def __call__(self, entered_id: str) -> None:
        while True:
            print(self._menu)
            user_choice = input("Your choice: ")
            try:
                validate_user_choice(user_choice=user_choice)
            except IncorrectUserInputError as err:
                print(err)
                continue
            if 0 < int(user_choice) <= len(self._menu_objects):
                for ind, key in enumerate(self._menu_objects.keys()):
                    if int(user_choice) == ind + 1:
                        func = self._menu_objects[key]
                        func(entered_id)
                break
            elif int(user_choice) == len(self._menu_objects) + 1:
                break
            else:
                print(f"Choice must be in digit from 1 to {len(self._menu_objects) + 1}")
                continue

    def create_menu(self) -> str:
        """Creates inner console menu."""

        menu = f"\n----------- {self._title} -----------"
        first_string_length = len(menu) - 1
        menu += f"\n{self._help_text}\n"
        for ind, key in enumerate(self._menu_objects.keys()):
            menu += f"*   {ind + 1} - {str(key)}\n"
        if self._title == "MAIN MENU":
            menu += f"*   {len(self._menu_objects) + 1} - Exit\n"
        else:
            menu += f"*   {len(self._menu_objects) + 1} - Return to the previous menu\n"
        menu += "-" * first_string_length
        return menu
