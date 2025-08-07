import unittest as unit
import bcrypt


from Account.Account import Account
from Terminal.bank_form import compare_pin,encrypt_pin,validate_pin


class test_account(unit.TestCase):

    def setup(self):
        self.pin = '123456'
    
        
    def test_pin_encryption(self):
        self.setup()
        #test the encryption
        encrypt_temp = encrypt_pin(self.pin)
        self.assertEqual(compare_pin(self.pin,encrypt_temp.decode()),True)
        
    def test_pin_validation(self):
        self.setup()
        #test regex of the pin
        self.assertEqual(validate_pin(self.pin),True)
        
        
        
        
        
        
        
if __name__ == "__main__":
    unit.main()
