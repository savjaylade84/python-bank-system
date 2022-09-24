''' 
        hold the data for the transaction history data
        
'''
class Transaction:
    
    def __init__(self):
        self.__date_time:str = ""
        self.__type:str = ""
        self.__amount:float = 0.0
        self.__balance:float = 0.0
  

    
    @property
    def Date_Time(self) -> str:
        return self.__date_time
         
    @Date_Time.setter
    def Date_Time(self,date_time:str) -> None:
        if(date_time != ""):
            self.__date_time = date_time
        pass

#-------------------[ Type ]----------------------------------- 
    
    @property
    def Type(self) -> str:
        return self.__type
 
    @Type.setter
    def Type(self,type:str) -> None:
        if(type != ""):
            self.__type = type
        pass
   
#-------------------[ Amount ]-----------------------------------     
    
    @property
    def Amount(self) -> float:
        return self.__amount
     
    @Amount.setter
    def Amount(self,amount:float) -> None:
        if(amount > 0):
            self.__amount = amount
        pass

#-------------------[ Balance ]----------------------------------- 
    
    @property
    def Balance(self) -> float:
        return self.__balance
 
    @Balance.setter
    def Balance(self,balance:float) -> None:
        if(balance > 0):
            self.__balance = balance
        pass
   
#-------------------[ Other ]-----------------------------------    
    
    def Data(self) -> dict:
        return {
            'Date-Time':self.__date_time,
            'Type':self.__type,
            'Amount':self.__amount,
            'Balance':self.__balance
        }
    
    def Clear(self) -> None:  
        self.__date_time:str = ""
        self.__type:str = ""
        self.__amount:float = 0.0
        self.__balance:float = 0.0
        pass