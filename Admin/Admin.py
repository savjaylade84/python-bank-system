
''' 
    :Description: Administration account that usual manage account 

    :Functionality:
                    1. login to administrator account
                    2. view account list
                    3. view administrator account edit history
                    4. view account transaction history
                    5. change account pin
                    6. delete account
                    7. change administrator account password
                    8. view account information 
        
'''

import json
from time import gmtime, strftime


from Account.Account import Account
from Terminal.print import Print
from Terminal.bank_form import *
from storage_accounts_v3.storage import Storage
from Log.log import Log

_print = Print()
_storage = Storage()
admin_log = Log('admin.log').open()
form_log = Log('form.log').open()

class Admin:
    
    def __init__(self) -> None:
        self.__account_list:dict = _storage.fetch(list=True)
        self.__account:Account = Account()
        self.__date:str = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()) 
            
#-------------------[ instruction command ]-----------------------------------    

    '''
        :Description: show the option on the user then capture and send the option

        :Parameter: None
        :Return: Integer
    '''
    def get_instruction(self) -> int:
        return int(_print.menu(
                            header='New Transaction',
                            menu_header='Enter A Instruction',
                            menu=[
                                'View Account List',
                                'View Account Information',
                                'View Account History',
                                'View Edited Account History',
                                'Change Account Pin',
                                'Change Password',
                                'Delete Account',
                                'Exist'  
                            ],prompt='Enter')) 

#-------------------[ print account information ]-----------------------------------   

    '''
        :Description: show the information of the admin

        :Parameter: None
        :Return: None
    '''
    def print_account_info(self) -> None:
        _print.data(
                        header='Administration',
                        data_header='Date',
                        data=f'{self.__date}'
                    )   
  
#-------------------[ Manage Account ]----------------------------------- 

    '''
        :Description: change the account pin number 

        :Parameter: None
        :Return: None
    '''   
    def Change_Account_Pin(self) -> None:
        
        account_id:str = _print.input('Enter Account-ID')
        
        if validate_userid(account_id):
            self.__account.Setup(account_id)
            form_log.info(f'admin:edit account pin => account - {account_id}')

            new_pin:str = ''
            index:int = 0
            
            while True:
                
                new_pin = _print.password('Enter Password')
                form_log.info(f'admin:account - {account_id} => enter new pin [{new_pin}]')

                if validate_pin(new_pin):
                    if _print.pin('Re-Enter Pin') == new_pin:
                        self.__account.Pin = bytes(encrypt_pin(new_pin)).decode()
                        self.__account.Save()
                        form_log.info(f'admin:account - {account_id} => save new pin [{new_pin}]')
                        break

                _print.status(state='Warning',message='Wrong Format of Pin - Pls Try Again')

                if index > 3:
                    form_log.info(f'admin:account - {account_id} => Failed to enter new pin [{new_pin}]')
                    break

                index += 1

    '''
        :Description: view accounts detail information

        :Parameter: None
        :Return: None
    ''' 
    #unit testing
    def View_Account_Information(self) -> None:
        _print.header('View Account Information')

        account_id:str = ""
        answer:str = ""

        while True:

            account_id = _print.input("Enter Account-ID")

            if validate_userid(account_id) and _storage.validate_id(account_id):
                self.__account.Setup(account_id)
                _print.datas(
                    header = f'Account Information',
                    data_header= [
                        'Account ID',
                        'Name',
                        'Balance'
                    ],
                    datas = [
                        self.__account.Account_ID,
                        self.__account.Name,
                        self.__account.Balance
                    ]

                )
            
            answer = _print.input("View Other Account? [Y/N]")

            if answer.lower() == 'n':
                break


    '''
        :Description: delete a account from account list and folder

        :Parameter: None
        :Return: None
    ''' 
    # unit testing this
    def Delete_Account(self) -> None:
        _print.header('Delete Account')

        account_id:str = ""
        answer:str = ""

        while True:
            
            account_id = _print.input("Enter Account-ID")
        
            if  _storage.validate_id(account_id):
            #if validate_userid(account_id) and _storage.validate_id(account_id):
                if _storage.delete(account_id):
                    _print.status('Successfully Deleting The Account')
                else:
                    _print.status('Unsuccessfull Deleting The Account')

            answer = _print.input('Delete Other Account? [Y/N]')

            if answer.lower() == 'n':
                break            

    '''
        :Description: show list of a accounts

        :Parameter: None
        :Return: None
    ''' 
    def View_List(self) -> None:
        
        _print.header('Account List')

        admin_log.info(f'admin => view account list')
        for info in self.__account_list['Account-List']:
            _print.datas(
                        header='',
                        data_header=[
                            'Account Name',
                            'Account-ID'
                        ],
                        datas=[
                            info['Name'],
                            info['Account-ID']
                        ])
            _print.border()
        pass

    '''
        :Description: view the transaction history of a account

        :Parameter: None
        :Return: None
    ''' 
    def View_Account_History(self) -> None:
        
        __account_id:str = _print.input('Enter Account-ID')
        __temp:dict = {}
        
        admin_log.info(f'admin => view account:{__account_id} history')

        #check if any of the account list exit a account-id that user input
        for id in self.__account_list['Account-List']:
            
            #check for empty result first
            if id == '' or id == None:
                _print.header("Account Not Found!")
                break
            
            if(__account_id == id['Account-ID']) and id != '':
                _print.datas(
                            header='Account Information',
                            data_header=[
                                'Account Name',
                                'Account-ID'
                            ],
                            datas=[
                                id['Name'],
                                id['Account-ID']
                            ])
                
                try:
                    with open(id['Path'],'r') as file:
                        __temp = json.load(file)
                except IOError:
                    admin_log.exception(f'Account Error: attempted to open account-{id} file failed')
                except Exception as e:
                    admin_log.exception(f'Account Error: {e}')

                for transaction in __temp['Transaction-History']:
                    _print.datas(header='Account History',
                                 data_header=[
                                    'Date',
                                    'Type',
                                    'Amount',
                                    'Balance',
                                ],
                                datas=[
                                    transaction['Date-Time'],
                                    transaction['Type'],
                                    transaction['Amount'],
                                    transaction['Balance']
                                ])
                    _print.border()
        del __temp

    '''
        :Description: show the edit history of administrator account

        :Parameter: None
        :Return: None
    ''' 
    def View_Edited_Account_History(self) -> None:

        admin_log.info(f'admin => view edited accounts history')

        for edit in self.__account_list['Edited-Account-History']:
            _print.datas(header='Edit History',
                         data_header=[
                            'Date-Time',
                            'Account-ID',
                            'Edit',
                            'Value'
                        ],
                        datas=[
                            edit['Date-Time'],
                            edit['Account-ID'],
                            edit['Edited']['Edit'],
                            edit['Edited']['Value']
                            
                        ])
            _print.border()
    
#-------------------[ Other Function ]----------------------------------- 
    
    '''
        :Description: change the password of administrator account

        :Parameter: None
        :Return: None
    ''' 
    def Change_Password(self) -> None:
        
        _print.header('Admin Change Password')
        form_log.info(f'admin: change password')

        new_password:str = ""
        index:int = 0

        while True:

            new_password = _print.password('Enter New Password')
            form_log.info(f'admin: change password [{new_password}]')

            if validate_password(new_password):
                if _print.password('Re-Enter New Password') == new_password:
                    self.__account_list['Admin-Password'] = bytes(encrypt_password(new_password)).decode()
                    _storage.store(data=self.__account_list,list=True)
                    form_log.info(f'admin: save new password [{new_password}]')
                    break

            _print.status(state='Warning', message='Wrong Format of Password - Pls! Try Again')

            if index > 3:
                form_log.info(f'admin: failed to change password [{new_password}]')
                break

            index += 1


    '''
        :Description: login administrator account

        :Parameter: None
        :Return: Boolean
    ''' 
    def Login(self) -> bool:

        _print.header('Admin Login')
        form_log.info(f'admin => [Login]: starting')
        __password:str = _print.password('Enter Password') 

        index:int = 1

        while True:

            form_log.info(f'admin => [Login]: Retry({index})')

            admin_log.info(f'{compare_password(__password,self.__account_list['Admin-Password'])}')
            if compare_password(__password,self.__account_list['Admin-Password']):
                form_log.info(f'admin => [Login]: Success at Retry({index})')
                return True
                
            if index > 3:
                form_log.info(f'admin: => [Login]: Failed')
                _print.header('Login Attempt Failed!')
                exit(1)

            __password = _print.password('Re-Enter Password')

            index = index + 1
                
        return False
