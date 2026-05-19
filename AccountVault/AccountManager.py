import os 
from Utils import credential
from LogService.src import logger
from random import Random
from AccountVault.AdminManager import AdminManager
from AccountVault.FileManager import FileManager
from AccountVault.config import VAULT_PATH
from dataclasses import asdict
av_log = logger.Log.initLogging(log_file='storage.log')

class AccountManager:
    
    @staticmethod
    def load_account(id:str) -> dict:
        
        if not AccountManager.exists(id):
            raise KeyError(f"Account {id} not found")
        
        return FileManager.read_json(AdminManager.load_account_path(id))
        
    @staticmethod
    def find_by_id(id:str) -> dict:
        
        if not AccountManager.exists(id):
            raise KeyError(f"Account {id} not found") 
           
        return FileManager.read_json(AccountManager.load_path(id))
    
    @staticmethod
    def find_all() -> dict:
        return AdminManager.load_list()
    
    @staticmethod
    def load_path(id:str) -> str:
        return f"{VAULT_PATH}/account-{id}.json"
    
    @staticmethod
    def save(id:str,data:dict) -> bool:
        
        if FileManager.write_json(AccountManager.load_path(id),data):
            return True
        
        return False
    
    @staticmethod
    def remove(id:str) -> bool:
        
        if not AccountManager.exists(id):
            return False
        
        if not AdminManager.remove_in_list(id):
            return False
         
        os.remove(AccountManager.load_path(id))
        
        return True

    
    @staticmethod
    def exists(id:str) -> bool:
        acc_list:dict = AdminManager.load_list()
        
        if not acc_list:
            return False
            
        return any(account['Account-ID'] == id for account in acc_list['Account-List'])
    
    @staticmethod
    def generate_id() -> str:
        return f'{Random().randint(0,999):03}-{Random().randint(0,999):03}-{Random().randint(0,9999):04}'
    
    @staticmethod
    def convert_dict(data:any) -> dict:
        return asdict(data)