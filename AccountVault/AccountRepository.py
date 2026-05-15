''' 
	this class serve as fetcher of the files in the storage 
'''
import json
import os 
from LogService.src import logger
from typing import Final

log = logger.Log.initLogging('storage.log').open()

VAULT_PATH:Final[str] = "AccountVault"
VAULT_LIST:Final[str] = "account-list.json"
ACCOUNT_LIST_FILE:str = f"{VAULT_PATH}/{VAULT_LIST}"

def _read_json(path:str) -> dict:
    
    try:
        with open(path,'r') as file:
            return json.load(file)
    except FileNotFoundError as e:
        log.exception(e)
        raise FileNotFoundError(f'File Error: File Doesn\'t exist')
    
def _write_json(path:str,data:dict) -> bool:
    
    try:
        with open(path,'w') as file:
            json.dump(data, file, indent=4)
            return True
    except FileNotFoundError:
        log.exception(e)
        raise FileNotFoundError(f'File Error: File Doesn\'t exist')
        
    return False

def _get_account_list() -> dict:    
    return _read_json(ACCOUNT_LIST_FILE)

def _get_account_path(id:str) -> str:
    return f"{VAULT_PATH}/account-{id}.json"

def _remove_account_in_list(id:str) -> bool:
    
    acc_list:dict = _get_account_list()
    
    if not acc_list:
        return False
    
    try:
        update_list = {
            **acc_list,
            "Account-List":[
                account for account in acc_list.get("Account-List",[])
                if account["Account-ID"] != id
            ]
        }
        
        _write_json(ACCOUNT_LIST_FILE,update_list)
    except Exception as e:
        log.exception(e)
        raise Exception("File Faile to save the account list in the file")

def _remove_account(id:str) -> bool:
    
    if _account_exist(id):
        if _remove_account_in_list(id):
            os.remove(_get_account_path(id))

def _account_exist(id:str) -> bool:
    acc_list:dict = _get_account_list()
    
    for account in acc_list['Account-List']:
        if account['Account-ID'] == id:
            return True
        
    return False 


class AccountRepository:
    
    def find_by_id(self,id:str) -> dict:
        
        if _account_exist(id):
            return _read_json(_get_account_path(id))
    
    def find_all(self) -> dict:
        return _get_account_list()
    
    def save(self,id:str,data:dict) -> bool:
        
        if _write_json(_get_account_path(id),data):
            return True
        
        return False
    
    def remove(self,id:str) -> bool:
        if _remove_account(id):
            return True
        return False
    
    def exists(self,id:str) -> bool:
        if _account_exist(id):
            return True
        return False

