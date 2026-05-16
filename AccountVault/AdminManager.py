import json
from LogService.src import logger
from AccountVault.config import ACCOUNT_LIST_FILE
from AccountVault.FileManager import FileManager

av_log = logger.Log.initLogging(log_file='storage.log')


class AdminManager:
    
    @staticmethod
    def load_list() -> dict:    
        return FileManager.read_json(ACCOUNT_LIST_FILE)
    
    @staticmethod
    def update_list(data:dict) -> bool:
        
        if FileManager.write_json(ACCOUNT_LIST_FILE,data):
            return True
        
        return False
    
    @staticmethod
    def load_account_path(id:str) -> str:
        
        acc_list:dict = AdminManager.load_list()
        
        if not acc_list:
            raise FileNotFoundError("Empty Account List")
            
        # get the first item that meet condition
        account = next(
                        (account for account in acc_list['Account-List'] if account['Account-ID'] == id),
                        None    
                        )
        if not account:
            raise KeyError(f"Account ID '{id}' not found")
        
        return account['Path'] 
    
    @staticmethod
    def remove_in_list(id:str) -> bool:
        
        acc_list:dict = AdminManager.load_list()
        
        if not acc_list:
            return False
        
        update_list = {
            **acc_list,
            "Account-List":[
                account for account in acc_list.get("Account-List",[])
                if account["Account-ID"] != id
            ]
        }
        
        if not update_list:
            return False
            
        if FileManager.write_json(ACCOUNT_LIST_FILE,update_list):
            return True
        
        return False
            