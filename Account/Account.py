'''
        hold the data for the account

'''

from Account.Transaction import Transaction
from storage_accounts_v3.storage import Storage

_storage = Storage()

class Account:

    def __init__(self):
        self.__account_exist:bool = False 
        self.__name:str = ''
        self.__account_id:str = ''
        self.__pin:str = ''
        self.__balance:float = ''
        self.__transaction_history:list[Transaction] = []
        self.__json = {}

    def Setup(self,id:str) -> None:
        self.__json = _storage.fetch(id)
        try:
            if self.__json != {}:
                self.__account_exist = True
            self.__name = self.__json['Name']
            self.__account_id = self.__json['Account-ID']
            self.__pin = self.__json['Pin']
            self.__balance = self.__json['Balance']
            self.__transaction_history = self.__json['Transaction-History']
        except Exception as e:
            raise e('Json Error: Data or File Does Not Exist')
        
#-------------------[ Name ]-----------------------------------    
        
    @property
    def Name(self) -> str:
        return self.__name
        
    @Name.setter    
    def Name(self,name:str) -> None:
        if(name != ""):
            self.__name = name
        pass    

#-------------------[ Account ID ]-----------------------------------         
    
    @property
    def Account_ID(self) -> str:
        return self.__account_id
 
    @Account_ID.setter
    def Account_ID(self,acc_id:str) -> None:
        if(acc_id != ""):
            self.__account_id = acc_id
        pass

#-------------------[ Pin ]----------------------------------- 
    
    @property
    def Pin(self) -> str:
        return self.__pin
    
    @Pin.setter
    def Pin(self,pin:str) -> None:
        if(pin != ""):
            self.__pin = pin
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

#-------------------[ Transaction ]-----------------------------------     
    
    @property
    def Transaction_History(self) -> list:
        return self.__transaction_history
    
    @Transaction_History.setter
    def Transaction_History(self,transaction_history:list) -> None:
        if(transaction_history != []):
            self.__transaction_history = transaction_history
        pass
   
#-------------------[ Account Exist ]-----------------------------------     
    
    @property
    def Exist(self) -> bool:
        return self.__account_exist   
    
#-------------------[ Other ]----------------------------------- 

    def Save(self) -> None:
        _storage.store(id=self.__account_id,data={
            'Name':self.Name,
            'Account-ID':self.Account_ID,
            'Pin':self.Pin,
            'Balance':self.Balance,
            'Transaction-History':self.Transaction_History
        })
        pass


