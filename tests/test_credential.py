import unittest as unit
import bcrypt

from Utils.credential import compare_pin,encrypt_pin,validate_pin

class test_account(unit.TestCase):

    def setup(self):
        self.pin = '123456'
    
        
    def test_pin_validation(self) -> None:
        self.setup()
        #test the encryption
        encrypt_temp = encrypt_pin(self.pin)
        self.assertEqual(compare_pin(self.pin,encrypt_temp.decode()),True)
        
    def test_password_validation(self) -> None:
        ...
    
    def test_userid_validation(self) -> None:
        ...   
    
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