from Utils import console,models,credential
from LogService.src import logger
from Account import models as acc_models
from AccountVault.AccountManager import AccountManager
from dataclasses import asdict
from time import gmtime,strftime

s_log = logger.Log.initLogging('account.log')
t_log = logger.Log.initLogging('transaction.log')

# get the exact date and time for the timezone
def getDateTime() -> str:
    return strftime("%a, %d %b %Y %H:%M:%S +0000",gmtime())

#deposite() // not finish and polish yet
def deposit(id:str) -> None:
    console.banner(models.DivConfig(),'Deposite Process')
    
    account:dict = AccountManager.load_account(id)
    
    transaction:acc_models.Transaction = acc_models.Transaction()
    
    transaction.Date_Time = getDateTime()
    transaction.Balance = account['Balance']
    transaction.Type = acc_models.TransactionType.Deposit
    
    amount: float = 0.0
    
    while True:
        
        amount = float(console.prompt('Enter Amount (Min: 500)'))
        
        if amount > 500:
            break
    
    transaction.Amount = amount
    
    # do deposite here
    
    account['Transaction-History'].append(asdict(transaction))
    AccountManager.save(id, account)
    

#withdraw()
def withdraw(id:str) -> None:
    console.banner(models.DivConfig(),'Deposite Process')
    
    account:dict = AccountManager.load_account(id)
    
    transaction:acc_models.Transaction = acc_models.Transaction()
    
    transaction.Date_Time = getDateTime()
    transaction.Balance = account['Balance']
    transaction.Type = acc_models.TransactionType.Withdraw
    
    amount:float = 0.0
    
    while True:
        
        amount = float(console.prompt('Enter Amount (Min: 500)'))
        
        if amount > 500:
            break
    
    transaction.Amount = amount
    
    # do withdraw here
    
    account['Transaction-History'].append(asdict(transaction))
    AccountManager.save(id,account)
    
#change_pin()
def change_pin(id:str) -> None:
    console.banner(models.DivConfig(),'Change Pin')

    account:dict = AccountManager.load_account(id)

    index:int = 1
    pin:str = console.prompt_pwd('Enter 6-Digit Pin ')
    
    if not credential.validate_pin(pin) or len(pin) > 6:
        while True:
            pin = console.prompt_pwd("Enter Pin Again")
            
            if credential.validate_pin(pin) and len(pin) is 6:
                confirm:str = console.prompt('Conform New Pin [Y] yes | [N] no').lower()
                
                # save only after positive confirmation
                if confirm == 'y':
                    account['Pin'] = bytes(credential.encrypt_pin(pin)).decode()
                    AccountManager.save(id,account)
                    console.print("Successfully Change Pin!")
                    break
            
            if index > 3:
                console.banner(models.DivConfig(),'Failed to Change Pin')
                break
            
            index = index + 1
            
# remove the save() here because the AccountVault.AccountManager has save function
# to not repeat the function i remove the save()