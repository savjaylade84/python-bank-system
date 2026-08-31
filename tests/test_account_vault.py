import unittest as unit 
from unittest.mock import patch
from contextlib import redirect_stdout
from AccountVault.FileManager import FileManager



class test_account_vault(unit.TestCase):
    
    def test_read_json(self) -> None:
        
        test_dict = FileManager.read_json("AccountVault/account-list.json");
        
        self.assertIsInstance(test_dict,dict);
        
    def test_write_json(self) -> None:
        
        result = FileManager.write_json("",{})
        
        self.assertFalse(result)