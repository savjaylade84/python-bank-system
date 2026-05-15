from Utils import console,models
from Utils import credential
from LogService.src import logger
from AccountVault.AccountRepository import _get_account_list,_update_account_list,AccountRepository


REPOSITORY: AccountRepository = AccountRepository()

def change_password() -> None:
    
    # initialise the log,temp account holder, and date
    form_log = logger.Log.initLogging(log_file='form.log')
    
    temp_config: dict = _get_account_list()
    
    console.pbanner(models.DivConfig(17,"="),'Admin Change Password')
    
    if not temp_config:
        raise ValueError("Empty admin config")
    
    console.banner(models.DivConfig(17,"="),'Admin Login',end="\n")
    
    password:str = "" 
    
    index: int = 1
    
    while True:
        
        new_password = console.prompt_pwd("Enter New Password")
        form_log.info(f'admin: change password [{new_password}]')
        
        if credential.validate_password(new_password):
           if console.prompt_pwd('Re-Enter New Password') == new_password:
                temp_config['Admin-Password'] = bytes(credential.encrypt_password(new_password)).decode()
                if _update_account_list(temp_config):
                    form_log.info(f'admin: save new password [{new_password}]')    
                    break
        
        console.status(models.TransactionStatus.Warning,'Wrong Format of Password - Pls! Try Again')
        
        if index > 3:
                form_log.info(f'admin: failed to change password [{new_password}]')
                break    
                    
        index = index + 1        

def change_account_pin() -> None:
    pass

def delete_account() -> None:
    pass

def ai_analysis() -> None:
    pass