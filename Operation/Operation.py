''' 
        regular transaction or process for the client/user
        
'''

import json
from time import gmtime, strftime

from Account.Account import Account
from Account.Transaction import Transaction
from Terminal.print import Print
from storage_accounts_v3.storage import Storage

_print = Print()
_storage = Storage()

class Operation:
    
    def __init__(self) -> None:
        self.__account:Account = Account()
        self.__transaction:Transaction = Transaction()
        self.__date:str = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        self.__account_list:dict = _storage.fetch(list=True)
        

#-------------------[ instruction command ]-----------------------------------    

    def get_instruction(self) -> int:
        return int(_print.menu(
                            header='New Transaction',
                            menu_header='Enter A Instruction',
                            menu=[
                                'Deposite',
                                'Withdraw',
                                'Balance',
                                'Transaction History',
                                'Change Pin',
                                'Exist'   
                            ],prompt='Enter'))
        
    
#-------------------[ print account information ]-----------------------------------   
    
    def print_account_info(self) -> None:
        _print.datas(
                    header='Account Information',
                    data_header=[
                        'Date',
                        'Account Name',
                            'Account ID',
                            'Account Balance'
                    ],
                    datas=[
                        self.__date,
                        self.__account.Name,
                        self.__account.Account_ID,
                        self.__account.Balance
                    ])  

#-------------------[ Transaction Command ]----------------------------------- 

    def Deposite(self) -> None:
        _print.header('Deposite Process')
        
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
                print('[ Failed ]: Wrong Input!')

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
                print('[ Failed ]: Wrong Input!')

        self.__transaction.Clear()
        pass
    
    def Balance(self) -> None:
        print('\n==========[Current Balance]==========')
        print(f'( Balance ):{self.__account.Balance}')
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
        self.__account.Setup(__user_id)

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
        _print.header("Change Pin")
        
        __index:int = 1
        __pin:str = _print.input('Enter 6-Digit Pin')
        if len(__pin) > 7:
            while True:
                
                __pin = _print.input('Enter Pin Again')
                
                if len(__pin) < 7 and len(__pin) == 6:
                    __confirm = _print.input('Confirm New Pin [Y] yes / [N] no')
                    if __confirm == 'Y':
                        self.__account.Pin = __pin
                        self.__account.Save()
                        _print("Successfully to Change Pin!")
                    break
                
                if __index > 3:
                    _print.header("Failed to Change Pin!")
                    break
                
                __index = __index + 1
                
        if len(__pin) < 7 and len(__pin) == 6:
            __confirm = _print.input('Confirm New Pin [Y] yes / [N] no')
            if __confirm == 'Y':
                self.__account.Pin = __pin
                self.__account.Save()
                _print.header("Successfully to Change Pin!")    
                      
        pass