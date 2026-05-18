
from Utils import console, models,credential
from AccountVault.AccountManager import AccountManager
from AccountVault.AdminManager import AdminManager
from LogService.src import logger

# initialise the log,temp account holder, and date
form_log = logger.Log.initLogging(log_file='form.log')

#View_List()
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

#View_Account_Information()
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

#View_Account_History()
def account_history() -> None:
    pass

#View_Edited_Account_History()
def edited_account_history() -> None:
    pass

#print_account_info()
def account_infos() -> None:
    pass