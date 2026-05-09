from abc import ABC, abstractmethod
from typing import List



class IAccount(ABC):
        
    # common functionality
    
    @abstractmethod
    def Setup(self,id:str) -> None:
        pass
    
    @abstractmethod
    def Save(self) -> None:
        pass
    
    @abstractmethod
    def get_copy(self) -> None:
        pass
    
    # getter / setter
    
    @property
    @abstractmethod
    def Name(self) -> str:
        pass
    
    @Name.setter
    @abstractmethod
    def Name(self,name:str) -> None:
        pass
    
    @property
    @abstractmethod
    def Account_ID(self) -> str:
        pass
    
    @Account_ID.setter
    @abstractmethod
    def Account_ID(self,acc_id:str) -> None:
        pass
    
    @property
    @abstractmethod
    def Pin(self) -> str:
        pass
    
    @Pin.setter
    @abstractmethod
    def Pin(self,pin:str) -> None:
        pass
    
    
    @property
    @abstractmethod
    def Balance(self) -> float:
        pass
    
    @Balance.setter
    @abstractmethod
    def Balance(self,balance:float) -> None:
        pass
    
    @property
    @abstractmethod
    def Transaction_History(self) -> List:
        pass
    
    @Transaction_History.setter
    @abstractmethod
    def Transaction_History(self,transaction_history:list) -> None:
        pass
    
    
    
    