''' 
form or process for the client/user
        
'''

from email import message
import json
from time import gmtime, strftime

from Account.Account import Account
from Account.Transaction import Transaction
from Terminal.print import Print
from Terminal.bank_form import encrypt_pin, validate_pin,validate_userid,compare_pin,generate_id
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

    '''
        :Description: get user response from the menu or choices

        :Parameter: None
        :Return: Integer
    ''' 
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
        :Description: login user in their specific account 

        :Parameter: None
        :Return: Boolean
    '''
    def Login(self) -> bool:

        _print.header('Account Login')
        form_log.info(f'user:anonymous => [Login]: Starting')
        __user_id:str = _print.input('Enter Account-ID')
        '''
            validate user id format input
            and checking for existing account id
            and files in the storage folder
        '''

        index:int = 1
        while True:
            if validate_userid(__user_id) and _storage.validate_id(__user_id):
                form_log.info(f'user:anonymous => [Login]: Success Input => user-id({__user_id})')
                break
            if not _storage.validate_id(__user_id):
                _print.status(state='Warning',message='Wrong format of user id  - Pls! Try again')
            if not validate_userid(__user_id):
                _print.status(state='Warning',message='Wrong format of user id  - Pls! Try again')
            if index > 3:
                form_log.info(f'user:anonymous => [Login]: Failed User-ID input')
                _print.header('Login Attempt Failed!')
                exit(1)
            __user_id:str = _print.input('Enter Account-ID Again')  
            index = index + 1
        
        '''
            setup the account information
            before proceeding pin validation and comparing
            because this part needed to compare of account pin
            and user pin input
        '''
        self.__account.Setup(__user_id)
        
        __pin:str = _print.password('Enter Pin')
        '''
            validate user id format input and 
            comparing account pin and user pin 
            input
        '''
        index = 1
        
        while True:
            if validate_pin(__pin) and compare_pin(__pin,self.__account.Pin):
                form_log.info(f'user:anonymous => [Login]: Success Input => pin({__pin})')
                break
            if not compare_pin(__pin,self.__account.Pin):
                _print.status(state='Warning',message='Wrong pin number - Pls! Try again')
            if not validate_pin(__pin):
                _print.status(state='Warning',message='Only 6 digit pin number only - Pls! Try again')
            if index > 3:
                form_log.info(f'user:anonymous => [Login]: Failed Pin input')
                _print.header('Login Attempt Failed!')
                exit(1)
            __pin:str = _print.password('Enter Pin Again')

            index = index + 1
             
        '''
            only prompt for finally success login process
        '''
        form_log.info(f'user:anonymous => [Login]: Success Login => account-id({self.__account.Account_ID})')
        form_log.info(f'user:anonymous => [Login]: Ended')
        return True

    '''
        :Description: register user to get new account

        :Parameter: None
        :Return: None
    '''
    def Signup(self) -> None:
        _print.header("Registration")
        form_log.info('user:anonymous => [Signup]: Starting')
        self.__account_list:dict = _storage.fetch(list=True)

        #Generate user id
        __account_id:str = f"{generate_id(len(self.__account_list['Account-List']) + 1)}"
        form_log.info(f'user:anonymous => [Signup]: Generate Account ID => id({__account_id})') 
        
        # account name
        __name:str = _print.input('Enter Name')
        form_log.info(f'user:anonymous => [Signup]: Input Name => name({__name})')
        
        # re-ask pin number until the exact number is given
        __balance:float = float(_print.input('Enter Initial Deposite ( Min: 1000 )'))
        if __balance < 1000:
            while True:
                
                __balance:float = float(_print.input('Enter First Deposite ( Min: 1000 ) Again'))
                if __balance >= 1000:
                    form_log.info(f'user:anonymous => [Signup]: Input Initial Deposite => deposite({__balance})')
                    break
        
        # re-ask pin number until the right format of pin is given
        __pin:str = _print.password('Enter 6-Digit Pin')
        if validate_pin(__pin):
            while True:
                
                __pin:str = _print.password('Enter Pin to Confirm')
                
                if validate_pin(__pin):
                    __pin = bytes(encrypt_pin(__pin)).decode()
                    form_log.info(f'user:anonymous => [Signup]: Input Pin => pin({__pin})')
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
              
            #create account file in the database folder
            __account = Account()
            __account.Name = __name
            __account.Account_ID = __account_id
            __account.Pin = __pin
            __account.Balance = __balance
            print(__account)
        
            _storage.store(id=__account_id,data=__account.get_copy())
            form_log.info(f'user:anonymous => [Signup]: Created Account => account({__account.get_copy()})')
            
            #update list in the account list
            self.__account_list['Account-List'].append({
                'Name': __name,
                'Account-ID':__account_id,
                'Path':f'storage_accounts_v3/account-{__account_id}.json'
                })
            _storage.store(id='',data=self.__account_list,list=True)
            form_log.info(f'user:anonymous => [Signup]: Update the Account List')
            
            self.__account_list = {}
            form_log.info(f'user:anonymous => [Signup]: Successful Signup')
            form_log.info(f'user:anonymous => [Signup]: Ended')
            _print.header("Successfully Register!")
        
        if __confirm == 'N':
            form_log.info(f'user:anonymous => [Signup]: Failed Signup')
            form_log.info(f'user:anonymous => [Signup]: Ended')
            _print.header("Failed Registration!")


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
