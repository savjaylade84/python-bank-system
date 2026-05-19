''' 
form or process for the client/user
        
'''

from email import message
import json
from time import gmtime, strftime

from Account.Account import Account
from Account.Transaction import Transaction
from Utils.console import Print
from Utils.credential import encrypt_pin, validate_pin,validate_userid,compare_pin,generate_id
from AccountVault.storage import Storage
from LogService.src import logger


transaction_log = logger.Log.initLogging('transaction.log')
form_log = logger.Log.initLogging('form.log')
_print = Print()
_storage = Storage()

class Operation:
    
    def __init__(self) -> None:
        self.__account:Account = Account()
        self.__transaction:Transaction = Transaction()
        self.__date:str = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        self.__account_list:dict = _storage.fetch(as_list=True)
        
    
#-------------------[ print account information ]-----------------------------------   

    '''
        :Description: print the short information on specific account

        :Parameter: None
        :Return: None
    '''  
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

    '''
        :Description: deposite amount of (x) on specific account

        :Parameter: None
        :Return: None
    '''
    def Deposite(self) -> None:
        _print.header('Deposite Process')
        transaction_log.info(f'account:{self.__account.Account_ID} => [Deposite]: Starting')
        
        self.__transaction.Date_Time = self.__date
        self.__transaction.Type = "Deposite"
        self.__transaction.Balance = self.__account.Balance
        
        while True:
            self.__transaction.Amount = float(_print.input('Enter a Amount'))

            # checking for valid min amount
            if(self.__transaction.Amount < 0):
                _print.status(state='Warning',message='Ineffecient Amount')

            # confirmation of the transaction
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
                _print.status(state='Failed',message='Wrong Input!')
         
        transaction_log.info(f'account:{self.__account.Account_ID} => [Deposite]: Ended')
        self.__transaction.Clear()
        pass

    '''
        :Description: withraw amount of (x) in specific account

        :Parameter: None
        :Return: None
    '''
    def Withdraw(self) -> None:
        _print.header('Withdraw Process')
        transaction_log.info(f'account:{self.__account.Account_ID} => [Withdraw]: Starting')
        
        self.__transaction.Date_Time = self.__date
        self.__transaction.Type = "Withdraw"
        self.__transaction.Balance = self.__account.Balance
        
        while True:
            self.__transaction.Amount = float(_print.input('Enter a Amount'))

            # checking for valid min amount
            if(self.__transaction.Amount > self.__account.Balance or self.__transaction.Amount < 0):
                _print.status(state='Warning',message='Ineffecient Amount!')

            # confirmation of the transaction
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

    '''
        :Description: show the amount of (x) in specific account

        :Parameter: None
        :Return: None
    '''    
    def Balance(self) -> None:
        _print.header('Current Balance')
        _print.data(header='',data_header='Balance',data=f'{self.__account.Balance}')
        transaction_log.info(f'account:{self.__account.Account_ID} => [Balance]: Show')

    '''
        :Description: show transaction history of specific account

        :Parameter: None
        :Return: None
    ''' 
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

#-------------------[ Bank Menu Command ]----------------------------------- 

    '''
        :Description: update the information of specific account in
                      the database folder and clear all memories

        :Parameter: None
        :Return: None
    '''
    def Save(self) -> None:
        transaction_log.info(f'account:{self.__account.Account_ID} => [Account]: Save Information')
        self.__account.Save()
        self.__transaction.Clear()

    '''
        :Description: change the specific account's pin number

        :Parameter: None
        :Return: None
    '''
    def Change_Pin(self) -> None:
        _print.header("Change Pin")
        form_log.info(f'user:anonymous => [Change Pin]: Started')
        __index:int = 1
        __pin:str = _print.password('Enter 6-Digit Pin')
        if not validate_pin(__pin):
            while True:
                
                __pin = _print.password('Enter Pin Again')
                
                if validate_pin(__pin):
                    __confirm = _print.input('Confirm New Pin [Y] yes / [N] no')
                    if __confirm == 'Y':
                        self.__account.Pin = bytes(encrypt_pin(__pin)).decode()
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
                self.__account.Pin = bytes(encrypt_pin(__pin)).decode()
                self.__account.Save()
                _print.header("Successfully to Change Pin!")    
                      
        pass
