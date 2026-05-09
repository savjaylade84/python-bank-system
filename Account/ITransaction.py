from abc import ABC, abstractmethod

class ITransaction(ABC):
    
    # functionality
    
    @abstractmethod
    def Data(self) -> dict:
        pass
    
    @abstractmethod
    def Clear(self) -> None:
        pass
    
    # getter / setter
    
    @property
    @abstractmethod
    def Date_Time(self) -> str:
        pass
    
    @Date_Time.setter
    @abstractmethod
    def Date_Time(self,date_time:str) -> None:
        pass
    
    @property
    @abstractmethod
    def Type(self) -> str:
        pass
    
    @Type.setter
    def Type(self,type:str) -> None:
        pass
    
    @property
    @abstractmethod
    def Amount(self) -> float:
        pass
    
    @Amount.setter
    @abstractmethod
    def Amount(self,amount:float) -> None:
        pass
    
    @property
    @abstractmethod
    def Balance(self) -> float:
        pass
    
    @Balance.setter
    @abstractmethod
    def Balance(self,balance:float) -> None:
        pass