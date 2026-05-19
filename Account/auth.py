from Utils import console,models,credential
from AccountVault.AdminManager import AdminManager
from AccountVault.AccountManager import AccountManager
from Account import models as account_models
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
    
    console.banner(models.DivConfig,"Registration")
    form_log.info('user:anonymous => [Signup]: Starting')
    
    account_id:str = AccountManager.generate_id()
    form_log.info(f'user:anonymous => [Signup]: Generate Account ID => id({account_id})') 
    
    # get account name
    account_name = console.prompt('Enter Your Full-Name')
    form_log.info(f'user:anonymous => [Signup]: Input Name => name({account_name})')
    
    balance:float = 0.0
    pin:str = ""
    
    while True:
        
        # get the initial balance
        balance = float(console.prompt('Enter Initial Deposite (Min: 1000)'))
        
        if balance >= 1000:
            form_log.info(f'user:anonymous => [Signup]: Input Initial Deposite => deposite({balance})')
            break
    
    while True:
        
        # get the initial pin
        pin = console.prompt("Enter 6 Digit Pin")
        
        if credential.validate_pin(pin):
            pin = bytes(credential.encrypt_pin(pin)).decode()
            form_log.info(f'user:anonymous => [Signup]: Input Pin => pin({pin})')
            break
    
    console.entries(    title="Summary Details",
                        labels=[
                            'Name',
                            'Account-ID',
                            'Pin',
                            'Balance'
                        ],
                        entries=[
                            account_name,
                            account_id,
                            balance    
                        ]
                    )
    
    confirmation = console.prompt('Confirm Register [Y]:yes / [N]:no ')
    
    if confirmation.lower() == 'y':
        account = account_models.Account(
                                            Name=account_name,
                                            Account_ID=account_id,
                                            Pin=pin,
                                            Balance=balance
                                        )
        
        account_list:dict = AdminManager.load_list()
        
        account_list['Account-List'].append({
                    "Name": account_name,
                    "Account-ID": account_id,
                    "Path":f"AccountVault/account-{account_id}.json"
        })
        
        if AdminManager.update_list(account_list):
            if AccountManager.save(account_id,AccountManager.convert_dict(account)):
                form_log.info(f'user:anonymous => [Signup]: Successful Signup')
                console.banner(models.DivConfig(),"Successfully Register")
                return True
            
    form_log.info(f'user:anonymous => [Signup]: Failed Signup')
    console.banner(models.DivConfig(),"Unsuccessful Registration")  
    return False
        
