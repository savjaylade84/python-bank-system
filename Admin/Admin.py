
''' 
        adminitration process for the internal force
        
'''

import json
from time import gmtime, strftime


from Account.Account import Account
from Terminal.print import Print
from storage_accounts_v3.storage import Storage

_print = Print()
_storage = Storage()

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
                                'Edit Account',
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
    
    def Edit_Account(self) -> None:
        pass
    
    def View_Account_Information(self) -> None:
        pass
    
    def View_List(self) -> None:
        _print.header('Account List')
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
                _print.header('Account History')
                with open(id['Path'],'r') as file:
                    __temp = json.load(file)
                for transaction in __temp['Transaction-History']:
                    _print.datas([
                                    'Date',
                                    'Type',
                                    'Amount',
                                    'Balance',
                                ],[
                                    transaction['Date-Time'],
                                    transaction['Type'],
                                    transaction['Amount'],
                                    transaction['Balance']
                                ])
                    _print.border()
        pass
    
    def View_Edited_Account_History(self) -> None:
        _print.header('Edit History')
        for edit in self.__account_list['Edited-Account-History']:
            _print.datas([
                            'Date-Time',
                            'Account-ID',
                            'Edit',
                            'Value'
                        ],[
                            edit['Date-Time'],
                            edit['Account-ID'],
                            edit['Edited']['Edit'],
                            edit['Edited']['Value']
                            
                        ])
            _print.border()
        pass
    
#-------------------[ Other Function ]----------------------------------- 
    
    def Change_Password(self) -> None:
        pass
    
    def Login(self) -> bool:
        _print.Header('Admin Login')
        __username:str = _print.input('Enter Username')
        __password:str = _print.input('Enter Password') 

        if __password == self.__account_list['Admin-Password'] and __username == self.__account_list['Admin-Username']:
            return True

        #retry until the login is success
        index:int = 1
        if __password != self.__account_list['Admin-Password'] or __username != self.__account_list['Admin-Username']:
            while True:
                if __password == self.__account_list['Admin-Password'] and __username == self.__account_list['Admin-Username']:
                    return True
                if index < 3:
                    _print.header('Login Attempt Failed!')
                    exit(1)
                index = index + 1
                
        
        
        return False
