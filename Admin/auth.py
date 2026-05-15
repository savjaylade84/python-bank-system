from LogService.src import logger
from AccountVault.AccountRepository import _get_account_list
from Utils import console, models
from Utils.credential import compare_password


'''
        :Description: login administrator account

        :Parameter: None
        :Return: Boolean
''' 

def login():
    
    # initialise the log,temp account holder, and date
    form_log = logger.Log.initLogging(log_file='form.log')
    
    # get the master list of the account
    admin_config:dict = _get_account_list()

    console.banner(models.DivConfig(17,"="),'Admin Login',end="\n")
    
    password:str = console.prompt_pwd("Enter Password")
    
    index: int = 1
    
    while True:
        
        # compare the password here before do something if it failed
        if compare_password(password,admin_config['Admin-Password']):
            form_log.info(f'admin => [Login]: Success({index})')
            return True
            
        form_log.info(f'admin => [Login]: Retry({index})')
        
        # break the loop if the input exceed 3 re-entry
        if index > 3:
            form_log.info(f'admin => [Login]: Failed({index})')
            console.banner(models.DivConfig(17,"="),'Login Attempt Failed!')
            break
            
        password = console.prompt_pwd('Re-Enter Password')
        
        index = index + 1
        
    return False