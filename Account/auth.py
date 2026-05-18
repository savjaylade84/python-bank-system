from Utils import console,models,credential
from AccountVault.AdminManager import AdminManager
from AccountVault.AccountManager import AccountManager
from LogService.src import logger

form_log = logger.Log.initLogging(log_file='account.log')

#Login()
def login()-> bool:
    
    console.banner(models.DivConfig(),'Account Login')
    
    form_log.info(f'user:anonymous => [Login]: Starting')
    
    account_id:str = console.prompt('Enter Account-ID')
    
    attempt:int = 0
    
    while True:
        
        if credential.validate_userid(account_id) and AccountManager.exists(account_id):
            break
        
        console.status(status=models.TransactionStatus.Warning,
                       message='Wrong format of user id  - Pls! Try again')
        
        if attempt > 3:
            form_log.info(f'user:anonymous => [Login]: Failed User-ID input')
            console.banner(models.DivConfig(),title='Login Attempt Failed!')
            return False
            
        account_id = console.prompt('Re-Enter Account-ID')
        
        attempt = attempt + 1
        
    account = AccountManager.load_account(account_id)
    
    account_pin:str = console.prompt_pwd('Enter Pin')
    
    while True:
        
        if credential.validate_pin() and credential.compare_pin(account_pin,account['Pin']):
            break
        
        if not credential.compare_pin(account_pin,account['Pin']):
            console.status(status=models.TransactionStatus.Warning,
                        message='Wrong pin number - Pls! Try again')
        
        if not credential.validate_pin(account_pin):
            console.status(status=models.TransactionStatus.Warning,
                        message='Only 6 digit pin number only - Pls! Try again')
            
        if attempt > 3:
            form_log.info(f'user:anonymous => [Login]: Failed Pin input')
            console.banner(models.DivConfig(),title='Login Attempt Failed!')
            return False
        
        attempt = attempt + 1

    form_log.info(f'user:anonymous => [Login]: Success Login => account-id({account['Account-ID']})')
    form_log.info(f'user:anonymous => [Login]: Ended')
    return True   
            
        
    

#Signup()
def signup() -> bool:
    ...