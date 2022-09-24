from Account.Account import Account
from Account.Transaction import Transaction
from Operation.Operation import Operation
from storage_accounts_v3.storage import Storage as storage
from Terminal.print import Print


account = Account()
account.Setup('000-000-1')
print(account.Name)
# print(Transaction())
# print(Operation())
# print(storage())

# print(storage().fetch())
# _print = Print()

# print(_print.menu(
#                     header='New Transaction',
#                     menu_header='Enter A Instruction',
#                     menu=[
#                         'Login',
#                         'Signup',
#                         'Admin',
#                         'Quit / Exit'
#                     ],prompt='Enter'))