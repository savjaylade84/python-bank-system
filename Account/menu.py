
from Utils import console
from typing import Final

MENU:Final[list[str]] = [
                            'Deposit',
                            'Withdraw',
                            'Balance',
                            'Transaction History',
                            'Change Pin',
                            'Exist'
                        ]

MENU_PROMPT:Final[str] = 'Enter An Instruction'

def get_menu_selection() -> int:
    return int(console.menu(
                                instruction=MENU_PROMPT,
                                items=MENU,
                                prompt_label='Enter',
                                start='\n'
                            ))