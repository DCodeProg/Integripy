import os
from rich.prompt import IntPrompt, Prompt
from typing import NoReturn


def ask_choice(choices: None | list[tuple[str]] = None, show_choices: bool = False) -> int:
    """Ask the user to choice a number corresponding to the given choices

    Args:
        choices (None | list[tuple[str]], optional): List of choices. Defaults to None.
        show_choices (bool, optional): Display the possibles choices in the prompt line. Defaults to False.

    Returns:
        int: The choosen number
    """    
    # If a list of choices was given, deducting the valid choice number
    if choices:
        valid_number = [str(i+1) for i in range(len(choices))]
    
    # Ask for the choice number
    choice: int = IntPrompt.ask("\n[cyan]⇒ Your choice[/cyan]", choices=valid_number, show_choices=show_choices)
    
    # Return the choice number
    return choice


def ask_path() -> str:
    """Ask the user for the path of a file

    Raises:
        FileExistsError: If the file does not exist

    Returns:
        str: Path to the file
    """
    
    # Ask for a file path
    path = Prompt.ask("[blue]File path[/blue]")
    
    # Test if the file path exist
    if os.path.isfile(path):
        return path
    
    elif os.path.isfile(path.strip('"')):
        return path.strip('"')
    
    else:
        raise FileExistsError("The file doesn't exist")
    
    
def ask_hash() -> str:
    """Ask the user a hash

    Returns:
        str: The given hash
    """
    
    # Ask for a hash
    hash: str = Prompt.ask("[purple]Expected hash[/purple]").upper()
    
    # Returns the hash
    return hash
    
    
def ask_continue() -> NoReturn:
    """Ask the user to press enter to continue
    """
    Prompt.ask("\n[cyan]⇒ Press [ENTER] to continue[/cyan]")


def back_to_main_menu() -> NoReturn:
    """Ask the user to press enter to return in main menu
    """    
    Prompt.ask("\n[cyan]⇒ Press [ENTER] to go back to the main menu[/cyan]")