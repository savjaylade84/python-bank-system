from dataclasses import dataclass, field
from enum import StrEnum

class TransactionType(StrEnum):
    Deposit = 'Deposite'
    Withdraw = 'Withdraw'
    Balance = 'Balance'

@dataclass
class Transaction:
    Date_Time:str = field(str)
    Type: TransactionType = field(default=TransactionType)
    Amount:float = field(default=float)
    Balance:float = field(default=float)

@dataclass
class Account:
    Name:str = field(default=str)
    Account_ID:str = field(default=str)
    Pin:str = field(default=str)
    Balance:float = field(default=float)