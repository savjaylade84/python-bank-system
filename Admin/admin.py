
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
    

