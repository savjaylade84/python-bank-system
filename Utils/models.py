from enum import StrEnum
from typing import NamedTuple
from dataclasses import dataclass

# status of the trasaction
class TransactionStatus(StrEnum):
    Info = "information"
    Success = "success"
    Failed = "failed"
    Pending = "pending"
    Warning = "warning"
    Cancelled = "cancelled"
    
# divider configuration
@dataclass
class DivConfig:
    count: int = 17
    style: str = "="
    
class LabelEntry(NamedTuple):
    title:str = "No Title"
    desc:str = "No Info"