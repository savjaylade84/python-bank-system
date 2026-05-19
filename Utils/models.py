'''
models.py
=========
provides a collection of enumerations, dataclasses, and named tuples
used as shared data models across the bank system
includes account type classification, transaction status tracking,
divider configuration, and labeled entry structure

Author: John Jayson De Leon
Github: github.com/savjaylade
'''
from enum import StrEnum
from typing import NamedTuple
from dataclasses import dataclass


class AccountType(StrEnum):
    '''
        enumeration of account types available in the bank system
        used to classify and distinguish user roles and permissions

        Attributes:
            Admin   (str)   : represents an administrator account
            Regular (str)   : represents a regular user account

        Note:
            inherits from StrEnum so values can be used directly as strings
            
        Example:
            AccountType.Admin    -> 'Administrator'
            AccountType.Regular  -> 'Regular'
    '''
    Admin = "Administrator"
    Regular = "Regular"

class TransactionStatus(StrEnum):
    '''
        enumeration of possible transaction status types in the bank system
        used to indicate the current state or result of an operation

        Attributes:
            Info        (str)   : represents an informational status
            Success     (str)   : represents a successfully completed transaction
            Failed      (str)   : represents a failed transaction
            Pending     (str)   : represents a transaction that is still in progress
            Warning     (str)   : represents a transaction with a cautionary notice
            Cancelled   (str)   : represents a transaction that was cancelled

        Note:
            inherits from StrEnum so values can be used directly as strings
            commonly used with console.status() for styled terminal output

        Example:
            TransactionStatus.Success    -> 'success'
            TransactionStatus.Failed     -> 'failed'
            TransactionStatus.Warning    -> 'warning'
    '''
    Info = "information"
    Success = "success"
    Failed = "failed"
    Pending = "pending"
    Warning = "warning"
    Cancelled = "cancelled"
    
@dataclass
class DivConfig:
    '''
        dataclass configuration for the divider style and length
        used by console functions to control the appearance of
        borders, banners, and labels printed in the terminal

        Attributes:
            count   (int)   : number of times the style character is repeated
                              defaults to 17
            style   (str)   : the character used to build the divider
                              defaults to '='

        Note:
            used as a parameter in console.divider(), console.banner(),
            and console.label() to control output formatting

        Example:
            DivConfig()                  -> count=17, style='='
            DivConfig(count=10, style='#') -> count=10, style='#'

            Output:
                DivConfig()           -> =================
                DivConfig(count=5)    -> =====
    '''
    count: int = 17
    style: str = "="
    
class LabelEntry(NamedTuple):
    '''
        named tuple representing a single labeled data entry
        used to pair a title label with its corresponding description
        for structured display in the terminal

        Attributes:
            title   (str)   : the label or field name of the entry
                              defaults to 'No Title'
            desc    (str)   : the value or description of the entry
                              defaults to 'No Info'

        Note:
            used as a parameter in console.entry() and console.entries()
            plain tuples are automatically converted to LabelEntry in console.entry()

        Example:
            LabelEntry('Name', 'John')       -> title='Name', desc='John'
            LabelEntry('Balance', '5000.00') -> title='Balance', desc='5000.00'
            LabelEntry()                     -> title='No Title', desc='No Info'

            Output:
                [ Name ] : John
                [ Balance ] : 5000.00
    '''
    title:str = "No Title"
    desc:str = "No Info"