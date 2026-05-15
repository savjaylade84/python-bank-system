from Utils import console,models
from Utils import credential
from LogService.src import logger
from AccountVault.storage import Storage

def fetch_admin_data() -> dict | None :
    
    # initialise the log,temp account holder, and date
    form_log = logger.Log.initLogging(log_file='form.log')
    
    # check if successfully retrieve admin config
    try:
        admin_config:dict = Storage().fetch(as_list=True)
        return admin_config
    except FileNotFoundError as e:
        form_log.error(f"{e.args}")
    
    return {}

def change_password() -> None:
    
    # initialise the log,temp account holder, and date
    form_log = logger.Log.initLogging(log_file='form.log')
    
    temp_config: dict = fetch_admin_data()
    
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
                Storage.store(data=temp_config,list=True)
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