from Utils import console,models,credential
from LogService.src import logger
from Account import models as acc_models
from AccountVault.AccountManager import AccountManager
from dataclasses import asdict

s_log = logger.Log.initLogging('account.log')
t_log = logger.Log.initLogging('transaction.log')

#deposite() // not finish and polish yet
def deposit(id:str) -> None:
    console.banner(models.DivConfig(),'Deposite Process')
    
    account:dict = AccountManager.load_account(id)
    
    transaction:acc_models.Transaction = acc_models.Transaction()
    
    transaction.Date_Time = ""
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
    
    transaction.Date_Time = ""
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
    ...
#save()
def save() -> None:
    ...