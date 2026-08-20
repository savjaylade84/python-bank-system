from Utils import console,models
from Utils import credential
from LogService.src import logger
from AccountVault.AdminManager import AdminManager
from AccountVault.AccountManager import AccountManager
from dotenv import load_dotenv
from openai import OpenAI

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
    
    console.banner(models.DivConfig(17,"="),'Delete Account')
    
    while True:
        
        account_id = console.prompt('Enter Account-ID')
        
        if credential.validate_userid(account_id) and AccountManager.exists(account_id):
            if AccountManager.remove(account_id):
                console.status(models.TransactionStatus.Success,'Successfully Deleting The Account')
        else:
            console.status(models.TransactionStatus.Failed,'Unsuccessfull Deleting The Account')

        answer = console.prompt('Delete Other Account? [Y/N]')
        
        if answer.lower() == 'n':
            break

def ai_analysis() -> None:
    console.banner(models.DivConfig(17,"="),'AI Analysis')
    
    account_id:str = console.prompt('Enter Account-ID')
    if credential.validate_userid(account_id):
        acct:dict = AccountManager.load_account(account_id)
        form_log.info(f'admin:setup account => account - {account_id}')
        
    load_dotenv()       # loading the api key in .env file
    import os    
    
    client = OpenAI(
        
        base_url="https://openrouter.ai/api/v1",
        api_key=''.join(os.getenv('OPENROUTER_TOKEN'))
    )
    
    command:str = f'''
                        Job: Generate Short Version Financial Advice And Analysis
                        Rule:
                            1. follow the rule strictly and no mistake
                            2. Graphical Image is not allowed
                            3. text-based table is allowed
                            4. text-based illustration is allowed
                            5. advice must be short and direct to the point
                            6. alternative option is allowed
                            7. never show the full version of sensitive 
                            8. sensitive information must be in data-masking
                            9. 40 words per line is allowed
                            
                        Data: 
                        {acct['Edited-Account-History']}
                  '''
    
    completion = client.chat.completions.create(
        
            extra_headers={
                "HTTP-Referer":"",
                "X-Title":"",
            },
            extra_body={},
            model="deepseek/deepseek-chat-v3.1:free",
            messages=[
                {
                    "role":"user",
                    "content": command
                }
            ]
    )
    
    console.status(models.TransactionStatus.Info,"Output")
    
    solution:str = completion.choices[0].message.content
    console.print(solution,end='\n')
        