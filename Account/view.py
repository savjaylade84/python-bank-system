from Utils import console,models
from AccountVault.AccountManager import AccountManager
from LogService.src import logger

t_log = logger.Log.initLogging(log_file='transaction.log')

#balance()
def balance(id:str) -> None:
    
    account:dict = AccountManager.load_account(id)

    console.entry(models.LabelEntry('Balance',account['Balance']),title='Current Balance')
    t_log.info(f'account:{account['Account-ID']} => [Balance]: Show')
    
#transaction_history()
#print_account_info()
def account_infos(id:str) -> None:
    console.banner(models.DivConfig(),'View Account Information')
    
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