import unittest as unit
import bcrypt

from Utils import credential

class test_account(unit.TestCase):
    
    def encrypt_dummy_password(self,password:str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
    
    def encrypt_dummy_pin(self,pin:str) -> str:
        return bcrypt.hashpw(pin.encode('utf-8'),bcrypt.gensalt())
        
    def test_pin_validation(self) -> None:
        
        pin:str = '123456'
        
        self.assertTrue(credential.validate_pin(pin))
        
    def test_password_validation(self) -> None:
        
        password:str = 'Test@123'
        
        self.assertTrue(credential.validate_password(password))
    
    def test_userid_validation(self) -> None:
        
        userid:str = '123-123-1234'
        
        self.assertTrue(credential.validate_userid(userid))   
    
    def test_compare_passwords(self) -> None:
        
        dummy_password:str = self.encrypt_dummy_password("Hello@123")
        
        self.assertTrue(
                            credential.compare_password(
                                                            password="Hello@123",
                                                            encrypt_string=dummy_password
                                                        ))
        
    def test_compare_pins(self) -> None:
        dummy_pin:str = self.encrypt_dummy_password("123456")
        
        self.assertTrue(
                            credential.compare_pin(
                                                        pin="123456",
                                                        encrypt_string=dummy_pin
                                                    ))
        
    def test_pin_encryption(self) -> None:
        
        dummy_pin:str = "123456"
        hashed_pin:str = credential.encrypt_pin(dummy_pin)
        
        # check if dummy pin is encrypted by comparing the pre and post encrypted
        self.assertNotEqual(dummy_pin,hashed_pin)
        
        # check if dummy pin is equal to hashed version when 
        # compare using the bcrypt
        self.assertTrue(credential.compare_pin(dummy_pin,hashed_pin))
        
    def test_password_encryption(self) -> None:
        
        dummy_password:str = "Hello@123"
        hashed_password:str = credential.encrypt_password(dummy_password)
        
        self.assertNotEqual(dummy_password,hashed_password)
        
        self.assertTrue(credential.compare_pin(dummy_password,hashed_password))
            
        
if __name__ == "__main__":
    unit.main()