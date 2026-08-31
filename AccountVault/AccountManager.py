'''
AccountManager.py
=================
provides a collection of static methods for managing bank accounts
in the vault storage system includes loading, finding, saving,
removing, and generating account data through the file and admin manager

Author: John Jayson De Leon
Github: github.com/savjaylade
'''
import os 
from Utils import credential
from LogService.src import logger
from random import Random
from AccountVault.AdminManager import AdminManager
from AccountVault.FileManager import FileManager
from AccountVault import config
from dataclasses import asdict
av_log = logger.Log.initLogging(log_file='storage.log')

class AccountManager:
    '''
        static class that handles all account storage operations
        in the vault system including reading, writing, removing,
        and generating account data through FileManager and AdminManager

        Note:
            all methods are static and do not require instantiation
            account data is stored as json files in the vault path
            account list is managed separately through AdminManager
    '''
    
    @staticmethod
    def load_account(id:str) -> dict:
        '''
            load an account data from the admin manager path
            using the provided account id and return it as a dict
            
            Args:
                id  (str)   : the unique account id to load
                
            Return:
                dict : the account data retrieved from the json file
            
            Raises:
                KeyError : raised when the account id does not exist
                           in the account list
            
            Note:
                uses AdminManager.load_account_path() to resolve the file path
                use find_by_id() to load from the standard vault path instead
            
            Example:
                load_account('123-456-7890')  -> { 'Account-ID': '123-456-7890', ... }
                load_account('000-000-0000')  -> KeyError: Account 000-000-0000 not found
        '''
        if not AccountManager.exists(id):
            raise KeyError(f"Account {id} not found")
        
        return FileManager.read_json(AdminManager.load_account_path(id))
        
    @staticmethod
    def find_by_id(id:str) -> dict:
        '''
            find and load an account data from the standard vault path
            using the provided account id and return it as a dict
            
            Args:
                id  (str)   : the unique account id to find
                
            Return:
                dict : the account data retrieved from the json file
            
            Raises:
                KeyError : raised when the account id does not exist
                           in the account list
            
            Note:
                uses AccountManager.load_path() to resolve the standard vault path
                use load_account() to load from the admin manager path instead
            
            Example:
                find_by_id('123-456-7890')  -> { 'Account-ID': '123-456-7890', ... }
                find_by_id('000-000-0000')  -> KeyError: Account 000-000-0000 not found
        '''
        if not AccountManager.exists(id):
            raise KeyError(f"Account {id} not found") 
           
        return FileManager.read_json(AccountManager.load_path(id))
    
    @staticmethod
    def find_all() -> dict:
        '''
            retrieve the full list of all accounts stored
            in the admin manager and return it as a dict
            
            Args:
                None
                
            Return:
                dict : the complete account list retrieved from AdminManager
            
            Raises:
                None
            
            Note:
                delegates directly to AdminManager.load_list()
                returns an empty dict if no accounts exist
            
            Example:
                find_all()  -> { 'Account-List': [ { 'Account-ID': '123-456-7890' }, ... ] }
                find_all()  -> { }
        '''
        return AdminManager.load_list()
    
    @staticmethod
    def load_path(id:str) -> str:
        '''
            construct and return the standard vault file path
            for the account json file using the provided account id
            
            Args:
                id  (str)   : the unique account id to build the path for
                
            Return:
                String : the full file path to the account json file
            
            Raises:
                None
            
            Note:
                path format: {VAULT_PATH}/account-{id}.json
                does not check if the file exists at the returned path
            
            Example:
                load_path('123-456-7890')  -> '/vault/account-123-456-7890.json'
        '''
        return f"{config.VAULT_PATH}/account-{id}.json"
    
    @staticmethod
    def save(id:str,data:dict) -> bool:
        '''
            save the provided account data as a json file
            in the vault path using the account id and return
            true if the operation was successful
            
            Args:
                id      (str)   : the unique account id used to build the file path
                data    (dict)  : the account data to write to the json file
                
            Return:
                Boolean : True if the file was written successfully
                          False if the write operation failed
            
            Raises:
                None
            
            Note:
                uses AccountManager.load_path() to resolve the file path
                overwrites the existing file if it already exists
            
            Example:
                save('123-456-7890', { 'Account-ID': '123-456-7890' })  -> True
                save('123-456-7890', { })                                -> False
        '''
        if FileManager.write_json(AccountManager.load_path(id),data):
            return True
        
        return False
    
    @staticmethod
    def remove(id:str) -> bool:
        '''
            remove an account from the vault by deleting its json file
            and removing it from the admin manager account list
            then return true if the operation was successful
            
            Args:
                id  (str)   : the unique account id to remove
                
            Return:
                Boolean : True if the account was removed successfully
                          False if the account does not exist or
                          removal from the admin list failed
            
            Raises:
                None
            
            Note:
                checks existence before attempting removal
                removes from AdminManager list first before deleting the file
                uses os.remove() to delete the account json file
            
            Example:
                remove('123-456-7890')  -> True
                remove('000-000-0000')  -> False
        '''
        if not AccountManager.exists(id):
            return False
        
        if not AdminManager.remove_in_list(id):
            return False
         
        os.remove(AccountManager.load_path(id))
        
        return True

    @staticmethod
    def exists(id:str) -> bool:
        '''
            check if an account with the provided id exists
            in the admin manager account list and return true if found
            
            Args:
                id  (str)   : the unique account id to check
                
            Return:
                Boolean : True if the account id exists in the account list
                          False if the list is empty or the id is not found
            
            Raises:
                None
            
            Note:
                loads the full account list from AdminManager on every call
                returns False immediately if the account list is empty
                uses any() to search through the Account-List collection
            
            Example:
                exists('123-456-7890')  -> True
                exists('000-000-0000')  -> False
        '''
        acc_list:dict = AdminManager.load_list()
        
        if not acc_list:
            return False
            
        return any(account['Account-ID'] == id for account in acc_list['Account-List'])
    
    @staticmethod
    def generate_id() -> str:
        '''
            generate a random unique account id in the standard
            format and return it as a formatted string
            
            Args:
                None
                
            Return:
                String : a randomly generated account id string
            
            Raises:
                None
            
            Note:
                format: 3 digits, dash, 3 digits, dash, 4 digits
                uses Random() to generate each numeric segment independently
                does not guarantee uniqueness against existing account ids
            
            Example:
                generate_id()  -> '123-456-7890'
                generate_id()  -> '047-382-1095'
        '''
        return f'{Random().randint(0,999):03}-{Random().randint(0,999):03}-{Random().randint(0,9999):04}'
    
    @staticmethod
    def convert_dict(data:any) -> dict:
        '''
            convert a dataclass instance into a dictionary
            and return it as a plain dict object
            
            Args:
                data    (any)   : the dataclass instance to convert
                
            Return:
                dict : the dataclass fields and values as a plain dictionary
            
            Raises:
                None
            
            Note:
                uses dataclasses.asdict() for conversion
                only works with dataclass instances not regular objects
                nested dataclass fields are also converted recursively
            
            Example:
                convert_dict(AccountModel(...))  -> { 'Account-ID': '123-456-7890', ... }
        '''
        return asdict(data)