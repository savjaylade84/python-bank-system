
from Utils import console, models,credential
from AccountVault.AccountManager import AccountManager
from AccountVault.AdminManager import AdminManager
from LogService.src import logger
from time import gmtime,strftime

# initialise the log,temp account holder, and date
form_log = logger.Log.initLogging(log_file='form.log')

def account_list() -> None:
    
    console.banner(models.DivConfig(17,"="),'Account List')
    form_log.info(f'admin => view account list')
    
    acc_list = AdminManager.load_list()
    
    for account in acc_list['Account-List']:
        console.entries(title=f"{account['Account-ID']} Information",
                        labels=[
                                    "Account Name",
                                    "Account ID",
                                    "Account File Path"        
                                ],
                        entries=[
                                    account['Name'],
                                    account['Account-ID'],
                                    account['Path']
                                ])
        
    console.divider(models.DivConfig(17,"#"))

def account_info() -> None:
    console.banner(models.DivConfig(17,"="),'View Account Information')
    
    while True:
        account_id:str = console.prompt('Enter Account-ID')
        
        if credential.validate_userid(account_id) and AccountManager.exists(account_id):
            acct:dict = AccountManager.load_account(account_id)
            console.entries(title=f"Account Information",
                            label=[
                                "Name",
                                "Account-ID",
                                "Balance"
                            ],
                            entries=[
                                acct['Name'],
                                acct['Account-ID'],
                                acct['Balance']
                            ])
            
        answer:str = console.prompt("View Other Account? [Y/N]")
        
        if answer.lower() == 'n':
            break

def account_history() -> None:
    
    console.banner(models.DivConfig(17,"="),'View Account History')
    
    account_id:str = console.prompt('Enter Account-ID')
    
    form_log.info(f'admin => view account:{account_id} history')
    
    if not AccountManager.exists(account_id):
        console.banner(models.DivConfig(17,"="),"Account Not Found")
        
    account:dict = AccountManager.load_account()
    
    if not account:    
        console.banner(models.DivConfig(17,"="),"Loaded Empty Account File")
        
    console.entries(title="Account Information",
                    labels=[
                        'Account Name',
                        'Account-ID'
                    ],
                    entries=[
                        account['Name'],
                        account['Account-ID']
                    ])
    
    if account['Transaction-History']:
        for transaction in account['Transaction-History']:
            
            if transaction:
                console.entries(title="Account History",
                                labels=[
                                    'Date',
                                    'Type',
                                    'Amount',
                                    'Balance'
                                ],
                                entries=[
                                    transaction['Date-Time'],
                                    transaction['Type'],
                                    transaction['Amount'],
                                    transaction['Balance']
                                ])
                
    console.divider(models.DivConfig(17,"#"))            
                
def edited_account_history() -> None:
    
    console.banner(models.DivConfig(17,"="),'View Edited Account History')
    form_log.info(f'admin => view edited accounts history')
    
    acc_list:dict = AdminManager.load_list()
    
    for edit in acc_list['Edited-Account-History']:
        console.entries(title="Edit History",
                        labels=[
                            'Date-Time',
                            'Account-ID',
                            'Edit',
                            'Value'
                        ],
                        entries=[
                            edit['Date-Time'],
                            edit['Account-ID'],
                            edit['Edited']['Edit'],
                            edit['Edited']['Value']
                        ])
    console.divider(models.DivConfig(17,"#"))
    
def account_infos() -> None:
    date:str = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()) 
    console.entry(entry=models.LabelEntry(
                                        title="Date",
                                        desc=f'{date}'
                                    ),
                                    title='Administration',
                                    start='\n',
                                    end='\n')