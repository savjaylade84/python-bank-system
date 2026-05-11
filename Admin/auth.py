from LogService.src import logger
from storage_accounts_v3.storage import Storage
from Utils import print, models
from Utils.crypto_io import compare_password


'''
        :Description: login administrator account

        :Parameter: None
        :Return: Boolean
''' 
def login():
    
    # initialise the log,temp account holder, and date
    __form_log = logger.Log.initLogging(log_file='form.log')
    
    # check if successfully retrieve admin config
    try:
        __admin_config:dict = Storage().fetch(list=True)
    except FileNotFoundError as e:
        __form_log.error(f"{e.args}")
        
    print.banner(models.DivConfig(17,"="),'Admin Login',end="\n")
    
    __password:str = print.prompt_pwd("Enter Password")
    
    __index: int = 1
    
    while True:
        
        # compare the password here before do something if it failed
        if compare_password(__password,__admin_config['Admin-Password']):
            __form_log.info(f'admin => [Login]: Success({__index})')
            return True
            
        __form_log.info(f'admin => [Login]: Retry({__index})')
        
        # break the loop if the input exceed 3 re-entry
        if __index > 3:
            __form_log.info(f'admin => [Login]: Failed({__index})')
            print.banner(models.DivConfig(17,"="),'Login Attempt Failed!')
            break
            
        __password = print.prompt_pwd('Re-Enter Password')
        
        index = index + 1
        
    return False