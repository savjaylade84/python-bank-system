'''
        hold the data for the account

'''

from Account.Transaction import Transaction
from storage_accounts_v3.storage import Storage

_storage = Storage()

class Account:

    def __init__(self):
        self.__name:str = ''
        self.__account_id:str = ''
        self.__pin:str = ''
        self.__balance:float = ''
        self.__transaction_history:list[Transaction] = []
        self.__json = {}

    '''
        :Description: show list of a accounts

        :Parameter:
                    :id: string - :default: ''
        :Return: None
    ''' 
    def Setup(self,id:str) -> None:
        self.__json = _storage.fetch(id)
        try:
            self.__name = self.__json['Name']
            self.__account_id = self.__json['Account-ID']
            self.__pin = self.__json['Pin']
            self.__balance = self.__json['Balance']
            self.__transaction_history = self.__json['Transaction-History']
        except Exception as e:
            raise e('Json Error: Data or File Does Not Exist')
        
#-------------------[ Name ]-----------------------------------    

    '''
        :Description: get account name

        :Parameter: None
        :Return: String
    ''' 
    @property
    def Name(self) -> str:
        return self.__name

    '''
        :Description: set account name

        :Parameter:
                    :name: string - :default: ''
        :Return: None
    '''  
    @Name.setter    
    def Name(self,name:str) -> None:
        if(name != ""):
            self.__name = name
        pass    

#-------------------[ Account ID ]-----------------------------------         

    '''
        :Description: get account identification number

        :Parameter: None
        :Return: String
    '''
    @property
    def Account_ID(self) -> str:
        return self.__account_id
 
    '''
        :Description: set account identification number

        :Parameter:
                    :acc_id: string - :default: ''
        :Return: None
    '''
    @Account_ID.setter
    def Account_ID(self,acc_id:str) -> None:
        if(acc_id != ""):
            self.__account_id = acc_id
        pass

#-------------------[ Pin ]----------------------------------- 

    '''
        :Description: get the account pin number

        :Parameter: None
        :Return: String
    '''
    @property
    def Pin(self) -> str:
        return self.__pin
    
    '''
        :Description: set the account pin number

        :Parameter:
                    :pin: string - :default: ''
        :Return: None
    '''
    @Pin.setter
    def Pin(self,pin:str) -> None:
        if(pin != ""):
            self.__pin = pin
        pass

#-------------------[ Balance ]-----------------------------------     

    '''
        :Description: get the account balance 

        :Parameter: None
        :Return: Float
    '''
    @property
    def Balance(self) -> float:
        return self.__balance

    '''
        :Description: set the account balance

        :Parameter:
                    :balance: Float - :default: 0.0f
        :Return: None
    '''
    @Balance.setter
    def Balance(self,balance:float) -> None:
        if(balance > 0):
            self.__balance = balance
        pass

#-------------------[ Transaction ]-----------------------------------     

    '''
        :Description: set the account transaction list

        :Parameter: None
        :Return: List
    '''
    @property
    def Transaction_History(self) -> list:
        return self.__transaction_history

    '''
        :Description: set the account transaction list

        :Parameter:
                    :transaction_history: List - :default: []
        :Return: None
    '''
    @Transaction_History.setter
    def Transaction_History(self,transaction_history:list) -> None:
        if(transaction_history != []):
            self.__transaction_history = transaction_history
        pass
    
#-------------------[ Other ]----------------------------------- 

    '''
        :Description: call the storage function to store the account information
                      in the database folder

        :Parameter: None
        :Return: None
    '''
    def Save(self) -> None:
        _storage.store(id=self.__account_id,data={
            'Name':self.Name,
            'Account-ID':self.Account_ID,
            'Pin':self.Pin,
            'Balance':self.Balance,
            'Transaction-History':self.Transaction_History
        })
        pass

    '''
        :Description: set the given information into the account information

        :Parameter: None
        :Return: None
    '''
    def get_copy(self) ->dict:
        return  {
            'Name':self.__name,
            'Account-ID':self.__account_id,
            'Pin':self.__pin,
            'Balance':self.__balance,
            'Transaction-History':self.__transaction_history
            }

