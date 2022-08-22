# Author: John Jayson B. De Leon
# Github: github.com/savjaylade84
# Email: savjaylade84@gmail.com

from textwrap import indent
from time import gmtime, strftime
from pathlib import Path
import json
from dataclasses import dataclass

class BankError(Exception):
    ''' 
        Custom made error class for any error that
        may occur in the bank system
    '''

    def __init__(self,message:str) -> None:
        self.message = message


'''
        hold the data for the account

'''

class Account:
    
    def __init__(self,account_id:str):
        
        self.__json:dict = {}
        self.__account_exist:bool = False
        
        #check if the file is available
        try:
            with open(f'accounts_v3/account-{account_id}.json','r') as file:
                self.__json = json.load(file)
            self.__account_exist = True
        except:
            self.__account_exist = False    
            
        #check if the data is available
        if(self.__json == None or self.__json == {}):
            self.__account_exist = False
        else:
            self.__account_exist = True
        
        self.__name:str = self.__json['Name']
        self.__account_id:str = self.__json['Account-ID']
        self.__pin:str = self.__json['Pin']
        self.__balance:float = self.__json['Balance']
        self.__transaction_history:list = self.__json['Transaction-History']
        self.__json = {}
   
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
        self.__json = {
            'Name':self.Name,
            'Account-ID':self.Account_ID,
            'Pin':self.Pin,
            'Balance':self.Balance,
            'Transaction-History':self.Transaction_History
        }
        print(self.__json)
        with open(f'accounts_v3/account-{self.__account_id}.json','w+') as file:
            json.dump(self.__json,file,indent=4)
        pass

''' 
        hold the data for the transaction history data
        
'''

class Transaction:
    
    def __init__(self):
        self.__date_time:str = ""
        self.__type:str = ""
        self.__amount:float = 0.0
        self.__balance:float = 0.0
  
#-------------------[ Date Time ]----------------------------------- 
    
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

class Bank_v3:
    
    def __init__(self) -> None:
        self.__account:Account
        self.__transaction:Transaction = Transaction()
        self.__date:str = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        self.__account_list:dict = {}
        
        with open(f'accounts_v3/account-list.json','r') as file:
            self.__account_list = json.load(file)
        

#-------------------[ instruction command ]-----------------------------------    

    def get_instruction(self) -> int:
        print(f'\n==========[New Transaction]==========\n'+
              f'[ Enter A Instruction ]\n'+
              f'[ 1 ]: Deposite\n'+
              f'[ 2 ]: Withdraw\n'+
              f'[ 3 ]: Balance\n'+
              f'[ 4 ]: Transaction History\n'+
              f'[ 5 ]: Change Pin\n'+
              f'[ 6 ]: Exist')
        return int(input('[Enter]: '))
    
#-------------------[ print account information ]-----------------------------------   
    
    def print_account_info(self) -> None:
        print(f'\n==========[ Account Information ]==========\n'+
              f'( Date ): {self.__date}\n'+
              f'( Account Name ): {self.__account.Name}\n'+
              f'( Account ID ): {self.__account.Account_ID}\n'+
              f'( Account Balance ): {self.__account.Balance}')

#-------------------[ Transaction Command ]----------------------------------- 

    def Deposite(self) -> None:
        print('\n==========[ Deposite Process ]==========')
        
        self.__transaction.Date_Time = self.__date
        self.__transaction.Type = "Deposite"
        self.__transaction.Balance = self.__account.Balance
        
        while True:
            self.__transaction.Amount = float(input('[ Enter a Amount ]: '))

            if(self.__transaction.Amount < 0):
                print('[ Ineffecient Amount ]')

            answer:str = input('[ Confirm Transaction [Y] yes / [N] no ]: ')
            if(answer == 'N'):
                answer = input('[ Proceed To Exit [Y] yes / [N] no ]: ')
                if(answer == 'Y'):
                    break
            elif(answer == 'Y'):
                self.__account.Balance = self.__account.Balance + self.__transaction.Amount
                self.__transaction.Balance = self.__account.Balance
                self.__account.Transaction_History.append(self.__transaction.Data())
                self.__account.Save()
                print('[ Success ]: Process is Successfully Done!')
                print(f'( Balance ): {self.__account.Balance}')
                break
            else:
                print('[Wrong Input!]')

        self.__transaction.Clear()
        pass
    
    def Withdraw(self) -> None:
        print('\n==========[ Withdraw Process ]==========')
        
        self.__transaction.Date_Time = self.__date
        self.__transaction.Type = "Withdraw"
        self.__transaction.Balance = self.__account.Balance
        
        while True:
            self.__transaction.Amount = float(input('[ Enter a Amount ]: '))

            if(self.__transaction.Amount > self.__account.Balance or self.__transaction.Amount < 0):
                print('[ Ineffecient Amount ]')

            answer:str = input('[ Confirm Transaction [Y] yes / [N] no ]: ')
            if(answer == 'N'):
                answer = input('[ Proceed To Exit [Y] yes / [N] no ]: ')
                if(answer == 'Y'):
                    break
            elif(answer == 'Y'):
                self.__account.Balance = self.__account.Balance - self.__transaction.Amount
                self.__transaction.Balance = self.__account.Balance
                self.__account.Transaction_History.append(self.__transaction.Data())
                self.__account.Save()
                print('[ Success ]: Process is Successfully Done!')
                print(f'( Balance ): {self.__account.Balance}')
                break
            else:
                print('[ Wrong Input! ]')

        self.__transaction.Clear()
        pass
    
    def Balance(self) -> None:
        print('\n==========[Current Balance]==========')
        print(f'(Balance):{self.__account.Balance}')
        pass
    
    def Transaction_History(self) -> None:
        print('\n==========[ Transaction History ]==========')
        __index:int = 1
        for transaction in self.__account.Transaction_History:
            print(f'\n==========[ Transaction {__index} ]==========\n'+
                '( Date ): {}\n'.format(transaction['Date-Time'])+
                '( Type ): {}\n'.format(transaction['Type'])+
                '( Amount ): {}\n'.format(transaction['Amount'])+
                '( Balance ): {}'.format(transaction['Balance']))
            __index = __index + 1
        pass

#-------------------[ Bank Menu Command ]----------------------------------- 


    def Save(self) -> None:
        self.__account.Save()
        self.__transaction.Clear()

    def Login(self) -> bool:
        print('\n==========[ Account Login ]==========')
        __user_id:str = input('[ Enter Account-ID ]: ')
        __pin:str = input('[ Enter Pin ]: ')
        print(__user_id)
        self.__account = Account(__user_id) 

        #retry until the login is success
        index:int = 1
        if self.__account.Exist:
            while True:
                if __pin == self.__account.Pin and len(__pin) < 7:
                    return True
                if index < 3 or __user_id != self.__account.Account_ID:
                    print('==========[ Login Attempt Failed! ]==========')
                    exit(1)
                index = index + 1
        
        return False
    
    def Signup(self) -> None:
        print("\n==========[ Registration ]==========")

        with open(f'accounts_v3/account-list.json','r') as file:
            self.__account_list:dict = json.load(file)

        #get basic information
        __account_id:str = '000-000-{}'.format(len(self.__account_list['Account-List']) + 1)  
        __name:str = input('[ Enter Name ]: ')
        
        # re-ask pin number until the exact number is given
        __balance:float = float(input('[ Enter First Deposite ( Min: 1000 ) ]: '))
        if __balance < 1000:
            while True:
                
                __balance:float = float(input('[ Enter First Deposite ( Min: 1000 ) Again ]: '))
                if __balance >= 1000:
                    break
        
        # re-ask pin number until the exact number is given    
        __pin:str = input('[ Enter 6-Digit Pin ]: ')
        if len(__pin) > 7:
            while True:
                
                __pin:str = input('[ Enter Pin Again ]: ')
                
                if len(__pin) < 7 and len(__pin) == 6:
                    break
            
        print("\n==========[ Summary Details ]==========")
        print(f'[ Name ]: {__name}\n'+
              f'[ Account-ID ]:{__account_id}\n'+
              f'[ Pin ]: ******\n'+
              f'[ Balance ]:{__balance}')
        __confirm = input('[ Confirm Register [Y] yes / [N] no]: ')
        
        if __confirm == 'Y':
            
            #update list
            self.__account_list['Account-List'].append({
                'Name': __name,
                'Account-ID':__account_id,
                'Path':f'accounts_v3/account-{__account_id}.json'
                })
            with open(f'accounts_v3/account-list.json','w') as file:
                json.dump(self.__account_list,file,indent=4)
              
            #create account file  
            __template = {
            'Name':__name,
            'Account-ID':__account_id,
            'Pin':__pin,
            'Balance':__balance,
            'Transaction-History':[]
            }
            with open(f'accounts_v3/account-{__account_id}.json','w') as file:
                json.dump(__template,file,indent=4)
            
            self.__account_list = {}
            print("\n==========[ Successfully Register! ]==========")
            pass
        
        if __confirm == 'N':
            print("\n==========[ Failed Registration! ]==========")
            pass
        
        pass
    
    def Change_Pin(self) -> None:
        print("\n==========[ Change Pin ]==========")
        
        __index:int = 1
        __pin:str = input('[ Enter 6-Digit Pin ]: ')
        if len(__pin) > 7:
            while True:
                
                __pin = input('[ Enter Pin Again ]: ')
                
                if len(__pin) < 7 and len(__pin) == 6:
                    __confirm = input('[ Confirm New Pin [Y] yes / [N] no]: ')
                    if __confirm == 'Y':
                        self.__account.Pin = __pin
                        self.__account.Save()
                    break
                
                if __index > 3:
                    print("\n==========[ Failed to Change Pin ]==========")
                    break
                
                __index = __index + 1
                
        if len(__pin) < 7 and len(__pin) == 6:
            __confirm = input('[ Confirm New Pin [Y] yes / [N] no]: ')
            if __confirm == 'Y':
                self.__account.Pin = __pin
                self.__account.Save()    
                      
        pass
    
bank_system = Bank_v3()
exit_answer = False
answer = ''


if __name__ == '__main__':

    print("<<<<<<<<<<( Welcome to Mock Bank System! )>>>>>>>>>>>")
    print(f"\n[ Creator ]: John Jayson B. De Leon\n"+
          f"[ Gmail ]: savjaylade84@gmail.com\n"+
          f"[ Github ]: savjaylade84\n"+
          f"[ Version ]: 3.9v\n")
    while True:
        print("\n==========[ Main Menu ]==========")
        answer:int = int(input(f'Enter a the command\n'+
                               f'( 1 ) Login\n'+
                               f'( 2 ) Signup\n'+
                               f'( 3 ) Quit / Exit\n'+
                               f'[ Enter ]:'))

        if answer == 1:
            #get account info
            if bank_system.Login():
                bank_system.print_account_info()
                while not exit_answer:

                    #get user instruction
                    answer = bank_system.get_instruction()

                    if answer == 1:
                        bank_system.Deposite()
                    elif answer == 2:
                        bank_system.Withdraw()
                    elif answer == 3: 
                        bank_system.Balance()
                    elif answer == 4:
                        bank_system.Transaction_History()
                    elif answer == 5:
                        bank_system.Change_Pin()
                    elif answer == 6:
                        print('==========[ Exit Successful! ]==========')
                        #bank_system.Save()
                        break
                    else:
                        print("[ Invalid Input ]")

        elif answer == 2:
            bank_system.Signup()
        elif answer == 3:
            print('\n==========[ Exit Successful! ]==========')
            exit(0)
        else:
            print('[ Wrong Input! ]')
del bank_system