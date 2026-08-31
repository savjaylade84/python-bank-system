'''
FileManager.py
==============
provides a collection of static methods for reading and writing
json files in the vault storage system includes safe json loading
and writing with proper error handling and validation

Author: John Jayson De Leon
Github: github.com/savjaylade
'''
import json

class FileManager:
    '''
        static class that handles all json file read and write
        operations for the vault storage system

        Note:
            all methods are static and do not require instantiation
            all file paths must be absolute or relative to the working directory
            json files are written with 4 space indentation for readability
    '''

    @staticmethod
    def read_json(path:str) -> dict:
        '''
            open and read a json file from the provided path
            and return its contents as a dictionary

            Args:
                path    (str)   : the file path of the json file to read

            Return:
                dict : the parsed json content of the file or error message

            Raises:
                FileNotFoundError : raised when the file does not exist
                                    or the json content is empty

            Note:
                opens the file in read mode using a context manager
                returns the parsed content only if it is not empty
                raises FileNotFoundError for both missing and empty files

            Example:
                read_json('/vault/account-123-456-7890.json')  -> { 'Account-ID': '123-456-7890', ... }
                read_json('/vault/empty.json')                 -> FileNotFoundError
                read_json('/vault/missing.json')               -> FileNotFoundError
        '''
        
        if not path:
            return {"File Path Error":"Empty Path Value"}
        
        with open(path,'r') as file:
            
            temp:dict = json.load(file)
            
            if not temp:
                return {"File Error":"Empty Value"}  
               
            return temp
        
        raise FileNotFoundError(f"Either [ Unable to load a json file ] or [ No file exist ]")

    @staticmethod
    def write_json(path:str,data:dict) -> bool:
        '''
            open a json file at the provided path and write
            the data dictionary to it then return true if successful

            Args:
                path    (str)   : the file path of the json file to write
                data    (dict)  : the dictionary data to serialize and write

            Return:
                Boolean : True if the data was written successfully
                          False if the data is empty or None

            Raises:
                None

            Note:
                opens the file in write mode which overwrites existing content
                writes json with 4 space indentation for readability
                returns False without writing if data is empty or falsy

            Example:
                write_json('/vault/account-123-456-7890.json', { 'Account-ID': '123-456-7890' })  -> True
                write_json('/vault/account-123-456-7890.json', { })                               -> False
                write_json('/vault/account-123-456-7890.json', None)                              -> False
        '''
        
        if not path:
            return False
        
        if not data:
            return False
        
        with open(path,'w') as file:
            
            if data:
                json.dump(data, file, indent=4)
                return True
            
        return False