from Utils import console,models
from Utils import credential
from LogService.src import logger
from AccountVault.AdminManager import AdminManager
from AccountVault.AccountManager import AccountManager

# initialise the log,temp account holder, and date
form_log = logger.Log.initLogging(log_file='form.log')

admin_repo: dict = AdminManager.load_list()

def change_password() -> bool:
    
    console.pbanner(models.DivConfig(17,"="),'Admin Change Password')
    
    if not admin_repo:
        return False
    
    console.banner(models.DivConfig(17,"="),'Admin Login',end="\n")
    
    attempt: int = 1
    
    while True:
        
        new_password = console.prompt_pwd("Enter New Password")
        form_log.info(f'admin: change password [{new_password}]')
        
        if credential.validate_password(new_password):
           if console.prompt_pwd('Re-Enter New Password') == new_password:
                admin_repo['Admin-Password'] = bytes(credential.encrypt_password(new_password)).decode()
                if AdminManager.update_list(admin_repo):
                    form_log.info(f'admin: save new password [{new_password}]')    
                    return True
        
        console.status(models.TransactionStatus.Warning,'Wrong Format of Password - Pls! Try Again')
        
        if attempt > 3:
                form_log.info(f'admin: failed to change password [{new_password}]')
                return False    
                    
        attempt = attempt + 1        

def change_account_pin() -> bool:
    
    console.banner(models.DivConfig(17,"="),'Change Account Pin')
    
    account_id:str = console.prompt('Enter Account-ID')
    account:dict = {}
    
    if AccountManager.find_by_id(account_id):
        account = AccountManager.load_account(account_id)
        
    attempt:int = 0
    
    while True:
        
        new_pin:str = console.prompt_pwd('Enter Pin')
        form_log.info(f'admin:account - {account_id} => enter new pin [{new_pin}]')
        
        if credential.validate_pin(new_pin):
            if console.prompt_pwd('Re-Enter Pin') == new_pin:
                account['Pin'] = bytes(credential.encrypt_pin(new_pin)).decode()
                if AccountManager.save(account):
                    form_log.info(f'admin:account - {account_id} => save new pin [{new_pin}]')
                    return True
        
        console.status(models.TransactionStatus.Warning,'Wrong Format of Pin - Pls Try Again')
        
        if attempt > 3:
            form_log.info(f'admin:account - {account_id} => Failed to enter new pin [{new_pin}]')
            return False
        
        attempt = attempt + 1
            

def delete_account() -> None:
    pass

def ai_analysis() -> None:
    pass