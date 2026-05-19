from Utils import console,models
from AccountVault.AccountManager import AccountManager

#balance()
#transaction_history()
#print_account_info()
def account_infos(id:str) -> None:
    console.banner(models.DivConfig(17,"="),'View Account Information')
    
    account:dict = AccountManager.load_account(id)
    console.entries(
                        title='Account Information',
                        labels=[
                                    'Date',
                                    'Account Name',
                                    'Account ID',
                                    'Account Balance'                           
                                ],
                        entries=[
                                    '',
                                    account['Name'],
                                    account['Account-ID'],
                                    account['Balance']
                                ]
                    )