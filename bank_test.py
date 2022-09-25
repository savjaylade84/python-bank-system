import unittest as unit
from Account.Account import Account


class test_account(unit.TestCase):

    def setup(self):
        self.account = Account()
        self.account.Setup('000-000-0001')
    def test_account_properties(self):
        self.setup()
        self.assertFalse(self.account.Name,None)
        
        
        
        
if __name__ == "__main__":
    unit.main()