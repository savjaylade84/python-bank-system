from Utils import console
from typing import Final

# list of available list on the admin part
MENU:Final[list[str]] = [
                        'View Account List',
                        'View Account Information',
                        'View Account History',
                        'View Edited Account History',
                        'Change Account Pin',
                        'Change Password',
                        'Delete Account',
                        'AI Analysis',
                       'Exit'  
                    ] 

MENU_PROMPT: Final[str] = 'Enter An Instruction'

def get_menu_selection(self) -> int:

    """
    Display the admin menu options and capture the user's selection.

    Returns:
        int: The selected menu option index.
    """

    return int(console.menu(
                        instruction= MENU_PROMPT,
                        menu = MENU,
                        prompt='Enter',
                        start="\n"
                    )) 