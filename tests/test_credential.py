import unittest as unit
import bcrypt

from Utils import credential

class test_account(unit.TestCase):
        
    def test_pin_validation(self) -> None:
        
        pin:str = '123456'
        
        self.assertEqual(credential.validate_pin(pin),True)
        
    def test_password_validation(self) -> None:
        
        password:str = 'Test@123'
        
        self.assertEqual(credential.validate_password(password),True)
    
    def test_userid_validation(self) -> None:
        
        userid:str = '123-123-1234'
        
        self.assertEqual(credential.validate_userid(userid),True)   
    
    def test_compare_passwords(self) -> None:
        ...
        
    def test_compare_pins(self) -> None:
        ...
        
    def test_pin_encryption(self) -> None:
        ...
        
    def test_password_encryption(self) -> None:
        ...
            
        
if __name__ == "__main__":
    unit.main()