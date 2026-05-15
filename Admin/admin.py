
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
import os
from time import gmtime, strftime
from dotenv import load_dotenv
from openai import OpenAI

from Account.Account import Account
from Utils import console
from Utils import models
from Utils.credential import *
from AccountVault.storage import Storage
from LogService.src import logger

_print = console.Print()
_storage = Storage()
admin_log = logger.Log.initLogging(log_file='admin.log')
form_log = logger.Log.initLogging(log_file='form.log')

load_dotenv()

class Admin:
    
    def __init__(self) -> None:
        self.__account_list:dict = _storage.fetch(list=True)
        self.__account:Account = Account()
        self.__date:str = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()) 
            

#-------------------[ print account information ]-----------------------------------   

    '''
        :Description: show the information of the admin

        :Parameter: None
        :Return: None
    '''
    def print_account_info(self) -> None:
        header = models.LabelEntry(
                                title="Date",
                                desc=f'{self.__date}'
                               )
        console.entry(header,title='Administration',start="\n",end="\n")   
  
#-------------------[ Manage Account ]----------------------------------- 

    '''
        :Description: analysis the financial history of the specific account

        :Parameter: None
        :Return: None
    '''   
    def AI_Analysis(self) -> None:

        console.banner(models.DivConfig(17,"="),'AI Analysis')

        account_id:str = _print.input('Enter Account-ID')
        if validate_userid(account_id):
            self.__account.Setup(account_id)
            form_log.info(f'admin:setup account => account - {account_id}')

            client = OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key= ''.join(os.getenv('TOKEN'))
            )
            completion = client.chat.completions.create(
                    extra_headers={
                    "HTTP-Referer": "", # Optional. Site URL for ran
                    "X-Title": "", # Optional. Site title for rankin
                },
                extra_body={},
                model="deepseek/deepseek-chat-v3.1:free",
                messages=[
                        {
                            "role": "user",
                            "content": f'''
                                            generate detail financial analysis and advise(without graph only context) on the following list of data below.

                                            Datas: {self.__account.Transaction_History}
                                        '''
                        }
                    ]
            )
            console.status(models.TransactionStatus.Info,"Output")

            solution:str = completion.choices[0].message.content
            console(solution, end="\n")

    '''
        :Description: change the account pin number 

        :Parameter: None
        :Return: None
    '''   
    def Change_Account_Pin(self) -> None:
        
        console.banner(models.DivConfig(17,"="),'Change Account Pin')
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

                console.status(models.TransactionStatus.Warning,'Wrong Format of Pin - Pls Try Again')

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

        console.banner(models.DivConfig(17,"="),'View Account Information')

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

        console.banner(models.DivConfig(17,"="),'Delete Account')

        account_id:str = ""
        answer:str = ""

        while True:
            
            account_id = _print.input("Enter Account-ID")
        
            if validate_userid(account_id) and _storage.validate_id(account_id):
                if _storage.delete(account_id):
                    console.status(models.TransactionStatus.Success,'Successfully Deleting The Account')
                else:
                    console.status(models.TransactionStatus.Failed,'Unsuccessfull Deleting The Account')

            answer = _print.input('Delete Other Account? [Y/N]')

            if answer.lower() == 'n':
                break            

    '''
        :Description: show list of a accounts

        :Parameter: None
        :Return: None
    ''' 
    def View_List(self) -> None:
        
        console.banner(models.DivConfig(17,"="),'Account List')
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
            console.divider(models.DivConfig(17,"#"))
        pass

    '''
        :Description: view the transaction history of a account

        :Parameter: None
        :Return: None
    ''' 
    def View_Account_History(self) -> None:
        
        console.banner(models.DivConfig(17,"="),'View Account History')
        __account_id:str = _print.input('Enter Account-ID')
        __temp:dict = {}
        
        admin_log.info(f'admin => view account:{__account_id} history')

        #check if any of the account list exit a account-id that user input
        for id in self.__account_list['Account-List']:
            
            #check for empty result first
            if id == '' or id == None:
                console.banner(models.DivConfig(17,"="),"Account Not Found!")
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
                    console.divider(models.DivConfig(17,"#"))
        del __temp

    '''
        :Description: show the edit history of administrator account

        :Parameter: None
        :Return: None
    ''' 
    def View_Edited_Account_History(self) -> None:
        
        console.banner(models.DivConfig(17,"="),'View Edited Account History')
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
            console.divider(models.DivConfig(17,"#"))
    
#-------------------[ Other Function ]----------------------------------- 
    
    '''
        :Description: change the password of administrator account

        :Parameter: None
        :Return: None
    ''' 
    def Change_Password(self) -> None:
        
        console.banner(models.DivConfig(17,"="),'Admin Change Password')
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

            console.status(models.TransactionStatus.Warning,'Wrong Format of Password - Pls! Try Again')

            if index > 3:
                form_log.info(f'admin: failed to change password [{new_password}]')
                break

            index += 1

