from Utils import print,models
from Utils import crypto_io
from LogService.src import logger
from storage_accounts_v3.storage import Storage

def fetch_admin_data() -> None:
    
    # initialise the log,temp account holder, and date
    __form_log = logger.Log.initLogging(log_file='form.log')
    
    # check if successfully retrieve admin config
    try:
        __admin_config:dict = Storage().fetch(list=True)
        return __admin_config
    except FileNotFoundError as e:
        __form_log.error(f"{e.args}")
    
    return {}

def change_password() -> None:
    
    # initialise the log,temp account holder, and date
    __form_log = logger.Log.initLogging(log_file='form.log')
    
    __temp_config: dict = fetch_admin_data()
    
    print.pbanner(models.DivConfig(17,"="),'Admin Change Password')
    
    if not __temp_config:
        raise ValueError("Empty admin config")
    
    print.banner(models.DivConfig(17,"="),'Admin Login',end="\n")
    
    __password:str = "" 
    
    __index: int = 1
    
    while True:
        
        __new_password = print.prompt_pwd("Enter New Password")
        __form_log.info(f'admin: change password [{__new_password}]')
        
        if crypto_io.validate_password(__new_password):
           if print.prompt_pwd('Re-Enter New Password') == __new_password:
                __temp_config['Admin-Password'] = bytes(crypto_io.encrypt_password(__new_password)).decode()
                Storage.store(data=__temp_config,list=True)
                __form_log.info(f'admin: save new password [{__new_password}]')    
                break
        
        print.status(models.TransactionStatus.Warning,'Wrong Format of Password - Pls! Try Again')
        
        if __index > 3:
                __form_log.info(f'admin: failed to change password [{__new_password}]')
                break    
                    
        index = index + 1        

def change_account_pin() -> None:
    pass

def delete_account() -> None:
    pass

def ai_analysis() -> None:
    pass