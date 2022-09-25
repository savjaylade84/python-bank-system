''' 
form or process for the client/user
        
'''

from email import message
import json
from time import gmtime, strftime

from Account.Account import Account
from Account.Transaction import Transaction
from Terminal.print import Print
from Terminal.bank_form import validate_pin,validate_userid
from storage_accounts_v3.storage import Storage
from Log.log import Log


transaction_log = Log('transaction.log').open()
form_log = Log('form.log').open()
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
        transaction_log.info(f'account:{self.__account.Account_ID} => [Deposite]: Starting')
        
        self.__transaction.Date_Time = self.__date
        self.__transaction.Type = "Deposite"
        self.__transaction.Balance = self.__account.Balance
        
        while True:
            self.__transaction.Amount = float(_print.input('Enter a Amount'))

            if(self.__transaction.Amount < 0):
                _print.status(state='Warning',message='Ineffecient Amount')

            answer:str = _print.input('Confirm Transaction [Y] yes / [N] no')
            if(answer == 'N'):
                answer = _print.input('Proceed To Exit [Y] yes / [N] no')
                if(answer == 'Y'):
                    transaction_log.info(f'account:{self.__account.Account_ID} => [Deposite]: Terminate')
                    break
            elif(answer == 'Y'):
                self.__account.Balance = self.__account.Balance + self.__transaction.Amount
                self.__transaction.Balance = self.__account.Balance
                self.__account.Transaction_History.append(self.__transaction.Data())
                self.__account.Save()
                _print.status(state='Success', message='Process is Successfully Done!')
                _print.data(header='',data_header='Balance',data=f'{self.__account.Balance}')
                transaction_log.info(f'account:{self.__account.Account_ID} => [Deposite]: Successful')
                break
            else:
                _print(state='Failed',message='Wrong Input!')
                
        transaction_log.info(f'account:{self.__account.Account_ID} => [Deposite]: Ended')
        self.__transaction.Clear()
        pass
    
    def Withdraw(self) -> None:
        _print.header('Withdraw Process')
        transaction_log.info(f'account:{self.__account.Account_ID} => [Withdraw]: Starting')
        
        self.__transaction.Date_Time = self.__date
        self.__transaction.Type = "Withdraw"
        self.__transaction.Balance = self.__account.Balance
        
        while True:
            self.__transaction.Amount = float(_print.input('Enter a Amount'))

            if(self.__transaction.Amount > self.__account.Balance or self.__transaction.Amount < 0):
                _print.status(state='Warning',message='Ineffecient Amount!')

            answer:str = _print.input('Confirm Transaction [Y] yes / [N] no')
            if(answer == 'N'):
                answer = _print.input('Proceed To Exit [Y] yes / [N] no')
                if(answer == 'Y'):
                    transaction_log.info(f'account:{self.__account.Account_ID} => [Withdraw]: Terminate')
                    break
            elif(answer == 'Y'):
                self.__account.Balance = self.__account.Balance - self.__transaction.Amount
                self.__transaction.Balance = self.__account.Balance
                self.__account.Transaction_History.append(self.__transaction.Data())
                self.__account.Save()
                _print.status(state='Success',message='Process is Successfully Done!')
                _print.data(header='',data_header='Balance',data=f'{self.__account.Balance}')
                transaction_log.info(f'account:{self.__account.Account_ID} => [Withdraw]: Successful')
                break
            else:
                _print.status(state='Failed',message='Wrong Input!')

        transaction_log.info(f'account:{self.__account.Account_ID} => [Withdraw]: Ended')
        self.__transaction.Clear()
        pass
    
    def Balance(self) -> None:
        _print.header('Current Balance')
        _print.data(header='',data_header='Balance',data=f'{self.__account.Balance}')
        transaction_log.info(f'account:{self.__account.Account_ID} => [Balance]: Show')
        pass
    
    def Transaction_History(self) -> None:
        _print.header('Transaction History')
        transaction_log.info(f'account:{self.__account.Account_ID} => [Transaction History]: Show')
        __index:int = 1
        for transaction in self.__account.Transaction_History:
            _print.datas(header='Transaction',
                         data_header=[
                             'Date',
                             'Type',
                             'Amount',
                             'Balance'
                         ],datas=[
                             transaction['Date-Time'],
                             transaction['Type'],
                             transaction['Amount'],
                             transaction['Balance']
                         ])
            __index = __index + 1
        pass

#-------------------[ Bank Menu Command ]----------------------------------- 


    def Save(self) -> None:
        transaction_log.info(f'account:{self.__account.Account_ID} => [Account]: Save Information')
        self.__account.Save()
        self.__transaction.Clear()

    def Login(self) -> bool:
        _print.header('Account Login')
        form_log.info(f'user:anonymous => [Login]: Starting')
        
        __user_id:str = _print.input('Enter Account-ID')
        '''
            validate user id format before passing 
            for fetching and setup the account 
            information in the account object
        '''
        index:int = 1
        while True:
            if validate_userid(__user_id):
                form_log.info(f'user:anonymous => [Login]: Success Input => user-id({__user_id})')
                break
            if not validate_userid(__user_id):
                _print.status(state='Warning',message='Wrong format of user id  - Pls! Try again')
            
            if index > 3:
                form_log.info(f'user:anonymous => [Login]: Failed User-ID input')
                _print.header('Login Attempt Failed!')
                exit(1)
            __user_id:str = _print.input('Enter Account-ID Again')  
            index = index + 1
            
        __pin:str = _print.password('Enter Pin')
        '''
            validate user id format before passing 
            for fetching and setup the account 
            information in the account object
        '''
        index = 1
        while True:
            if validate_pin(__pin):
                form_log.info(f'user:anonymous => [Login]: Success Input => pin({__pin})')
                break
            if not validate_pin(__pin):
                _print.status(state='Warning',message='Only 6 digit pin number only - Pls! Try again')
            if index > 3:
                form_log.info(f'user:anonymous => [Login]: Failed Pin input')
                _print.header('Login Attempt Failed!')
                exit(1)
            __pin:str = _print.password('Enter Pin Again')
            index = index + 1
            
        self.__account.Setup(__user_id)
        print(self.__account.Balance)
        if self.__account.Exist:
            if self.__account.Account_ID == __user_id and self.__account.Pin:
                form_log.info(f'user:anonymous => [Login]: Success Login => account-id({self.__account.Account_ID})')
                form_log.info(f'user:anonymous => [Login]: Ended')
                return True
            
        return False
    
    def Signup(self) -> None:
        _print.header("Registration")
        self.__account_list:dict = _storage.fetch(list=True)

        #get basic information
        __account_id:str = f"000-000-{(len(self.__account_list['Account-List']) + 1):4}" 
        __name:str = _print.input('Enter Name')
        
        # re-ask pin number until the exact number is given
        __balance:float = float(_print.input('Enter First Deposite ( Min: 1000 )'))
        if __balance < 1000:
            while True:
                
                __balance:float = float(_print.input('Enter First Deposite ( Min: 1000 ) Again'))
                if __balance >= 1000:
                    break
        
        # re-ask pin number until the right format of pin is given
        __pin:str = _print.input('Enter 6-Digit Pin')
        if validate_pin(__pin):
            while True:
                
                __pin:str = _print.input('Enter Pin Again')
                
                if validate_pin(__pin):
                    break
                
        _print.datas(header='Summary Details',
                     data_header=[
                         'Name',
                         'Account-ID',
                         'Pin',
                         'Balance'
                     ],datas=[
                         __name,
                         __account_id,
                         __balance
                     ])
        __confirm = _print.input('Confirm Register [Y] yes / [N] no')
        
        
        if __confirm == 'Y':
            
            #update list
            self.__account_list['Account-List'].append({
                'Name': __name,
                'Account-ID':__account_id,
                'Path':f'accounts_v3/account-{__account_id}.json'
                })
            _storage.store(self.__account_list,list=True)
              
            #create account file  
            __template = {
            'Name':__name,
            'Account-ID':__account_id,
            'Pin':__pin,
            'Balance':__balance,
            'Transaction-History':[]
            }
            _storage.store(id=__account_id,data=__template)
            
            self.__account_list = {}
            _print.header("Successfully Register!")
            pass
        
        if __confirm == 'N':
            _print.header("Failed Registration!")
            pass
        
        pass
    
    def Change_Pin(self) -> None:
        _print.header("Change Pin")
        
        __index:int = 1
        __pin:str = _print.input('Enter 6-Digit Pin')
        if not validate_pin(__pin):
            while True:
                
                __pin = _print.input('Enter Pin Again')
                
                if validate_pin(__pin):
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
                
        if validate_pin(__pin):
            __confirm = _print.input('Confirm New Pin [Y] yes / [N] no')
            if __confirm == 'Y':
                self.__account.Pin = __pin
                self.__account.Save()
                _print.header("Successfully to Change Pin!")    
                      
        pass