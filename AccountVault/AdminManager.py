'''
AdminManager.py
===============
provides a collection of static methods for managing the master
account list file in the vault storage system includes loading,
updating, path resolving, and removing accounts from the list

Author: John Jayson De Leon
Github: github.com/savjaylade
'''
import json
from LogService.src import logger
from AccountVault.config import ACCOUNT_LIST_FILE
from AccountVault.FileManager import FileManager

av_log = logger.Log.initLogging(log_file='storage.log')


class AdminManager:
    '''
        static class that handles all operations related to the
        master account list file in the vault storage system
        including reading, writing, and managing account entries

        Note:
            all methods are static and do not require instantiation
            account list is stored as a single json file defined in ACCOUNT_LIST_FILE
            individual account file paths are also tracked inside the account list
    '''
    
    @staticmethod
    def load_list() -> dict:
        '''
            load and return the master account list
            from the vault storage as a dictionary
            
            Args:
                None
                
            Return:
                dict : the full account list data retrieved from the json file
            
            Raises:
                None
            
            Note:
                reads directly from ACCOUNT_LIST_FILE via FileManager
                returns an empty dict if the file does not exist or is empty
            
            Example:
                load_list()  -> { 'Account-List': [ { 'Account-ID': '123-456-7890', ... } ] }
                load_list()  -> { }
        '''
        return FileManager.read_json(ACCOUNT_LIST_FILE)
    
    @staticmethod
    def update_list(data:dict) -> bool:
        '''
            overwrite the master account list file with the
            provided data and return true if successful
            
            Args:
                data    (dict)  : the updated account list data to write to the file
                
            Return:
                Boolean : True if the file was written successfully
                          False if the write operation failed
            
            Raises:
                None
            
            Note:
                writes directly to ACCOUNT_LIST_FILE via FileManager
                completely overwrites the existing file content
            
            Example:
                update_list({ 'Account-List': [ { 'Account-ID': '123-456-7890' } ] })  -> True
                update_list({ })                                                         -> False
        '''
        if FileManager.write_json(ACCOUNT_LIST_FILE,data):
            return True
        
        return False
    
    @staticmethod
    def load_account_path(id:str) -> str:
        '''
            find and return the file path of a specific account
            from the master account list using the provided account id
            
            Args:
                id  (str)   : the unique account id to search for
                
            Return:
                String : the file path of the account json file
            
            Raises:
                FileNotFoundError : raised when the account list is empty
                                    or the file does not exist
                KeyError          : raised when the account id is not found
                                    in the account list
            
            Note:
                uses next() to get the first matching account entry
                the file path is stored inside each account entry as 'Path'
                use AccountManager.load_path() for the standard vault path instead
            
            Example:
                load_account_path('123-456-7890')  -> '/vault/account-123-456-7890.json'
                load_account_path('000-000-0000')  -> KeyError: Account ID '000-000-0000' not found
        '''
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
        '''
            remove a specific account entry from the master account
            list using the provided account id and save the updated
            list then return true if the operation was successful
            
            Args:
                id  (str)   : the unique account id to remove from the list
                
            Return:
                Boolean : True if the account was removed and the list was saved successfully
                          False if the account list is empty or the write operation failed
            
            Raises:
                None
            
            Note:
                loads the full account list before filtering
                builds a new list excluding the matching account id
                uses dict unpacking to preserve all other fields in the list
                does not raise an error if the id is not found in the list
            
            Example:
                remove_in_list('123-456-7890')  -> True
                remove_in_list('000-000-0000')  -> True  (id not found, list saved unchanged)
                remove_in_list('123-456-7890')  -> False (empty list)
        '''
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