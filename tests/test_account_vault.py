import unittest as unit 
from unittest.mock import patch
from contextlib import redirect_stdout
from AccountVault.FileManager import FileManager
from AccountVault.AdminManager import AdminManager


class test_account_vault(unit.TestCase):
    
    def test_read_json(self) -> None:
        
        test_dict = FileManager.read_json("AccountVault/account-list.json");
        
        self.assertIsInstance(test_dict,dict);
        
    def test_write_json(self) -> None:
        
        result = FileManager.write_json("",{})
        
        self.assertFalse(result)
        
    def test_load_list(self) -> None:
        
        result:dict = AdminManager.load_list()
       
        self.assertIsInstance(result,dict)
        
    def test_load_account_path(self) -> None:
        
        result:str = AdminManager.load_account_path("000-000-0002")
        
        self.assertIsInstance(result,str)
        
    def test_update_list(self) -> None:
        
        self.assertTrue(AdminManager.append_list({ 'Account-ID': '123-456-7890' }))
        
    def test_remove_in_list(self) -> None:
        
        self.assertTrue(AdminManager.remove_in_list('123-456-7890'))