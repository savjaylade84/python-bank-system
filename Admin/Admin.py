
''' 
        adminitration process for the internal force
        
'''

import json
from time import gmtime, strftime


from Account.Account import Account
from Terminal.print import Print
from Terminal.bank_form import validate_password,compare_password,encrypt_password,validate_userid,validate_pin,encrypt_pin
from storage_accounts_v3.storage import Storage
from Log.log import Log

_print = Print()
_storage = Storage()
admin_log = Log('admin.log').open()
form_log = Log('form.log').open()

class Admin:
    
    def __init__(self) -> None:
        
        self.__account_list:dict = _storage.fetch(list=True)
        self.__account:Account
        self.__date:str = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()) 
            
#-------------------[ instruction command ]-----------------------------------    

    def get_instruction(self) -> int:
        return int(_print.menu(
                            header='New Transaction',
                            menu_header='Enter A Instruction',
                            menu=[
                                'View Account List',
                                'View Account Information',
                                'View Account History',
                                'View Edited Account History',
                                'Change Account Password',
                                'Change Password',
                                'Exist'  
                            ],prompt='Enter')) 

#-------------------[ print account information ]-----------------------------------   
    
    def print_account_info(self) -> None:
        _print.data(
                        header='Administration',
                        data_header='Date',
                        data=f'{self.__date}'
                    )   
  
#-------------------[ Manage Account ]----------------------------------- 
    
    # change this from edit account to edit account pin
    def Change_Account_Pin(self) -> None:
        
        userid:str = _print.input('Enter Account-ID')
        
        if validate_userid(userid):
            self.__account = _storage.fetch(userid)

            new_pin:str = ''
            index:int = 0
            
            while True:
                
                new_pin = _print.password('Enter Password')
                if validate_pin(new_pin):
                    if _print.pin('Re-Enter Pin') == new_pin:
                        self.__account['Pin'] = bytes(encrypt_pin(new_pin)).decode()
                        break

                _print.status(state='Warning',message='Wrong Format of Pin - Pls Try Again')

                if index > 3:
                    break

                index += 1

        pass
    
    def View_Account_Information(self) -> None:
        pass
    
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
    
    def View_Account_History(self) -> None:
        
        __account_id:str = _print.input('Enter Account-ID')
        __temp:dict = {}
        
        admin_log.info(f'admin => view account:{__account_id} history')
        #check if any of the account list exit a account-id that user input
        for id in self.__account_list['Account-List']:
            
            #check for empty result first
            if id == '':
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
                with open(id['Path'],'r') as file:
                    __temp = json.load(file)
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
        pass
    
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
        pass
    
#-------------------[ Other Function ]----------------------------------- 
    
    # Todo: under construction
    def Change_Password(self) -> None:
        
        _print.header('Admin Change Password')
        new_password:str = ""
        index:int = 0

        while True:

            new_password = _print.password('Enter New Password')

            if validate_password(new_password):
                if _print.password('Re-Enter New Password') == new_password:
                    self.__account_list['Admin-Password'] = bytes(encrypt_password(new_password)).decode()
                    _storage.store(data=self.__account_list,list=True)
                    break

            _print.status(state='Warning', message='Wrong Format of Password - Pls! Try Again')

            if index > 3:
                break

            index += 1


    
    def Login(self) -> bool:

        _print.header('Admin Login')
        form_log.info(f'admin => [Login]: starting')
        __password:str = _print.password('Enter Password') 

        if compare_password(__password,self.__account_list['Admin-Password']):
            form_log.info(f'admin => [Login]: Success')
            return True

        # update this code
        #retry until the login is success
        index:int = 1
        if not compare_password(__password, self.__account_list['Admin-Password']):

            while True:

                form_log.info(f'admin => [Login]: Retry({index})')

                if compare_password(__password,self.__account_list['Admin-Password']):
                    form_log.info(f'admin => [Login]: Success at Retry({index})')
                    return True
                
                if index < 3:
                    form_log.info(f'admin: => [Login]: Failed')
                    _print.header('Login Attempt Failed!')
                    exit(1)

                index = index + 1
                
        return False
