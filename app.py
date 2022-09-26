
'''
     Author: John Jayson B. De Leon
     Github: github.com/savjaylade84
     Email: savjaylade84@gmail.com
'''


from Operation.Operation import Operation
from Admin.Admin import Admin
from Terminal.print import Print

    
def main() -> None:
    _bank_system = Operation()
    _admin = Admin()
    _print = Print()
    _exit_answer = False
    _answer = ''

    print("<<<<<<<<<<( Welcome to Mock Bank System! )>>>>>>>>>>>")
    print(f"\n[ Creator ]: John Jayson B. De Leon\n"+
          f"[ Gmail ]: savjaylade84@gmail.com\n"+
          f"[ Github ]: savjaylade84\n"+
          f"[ Version ]: 3.9v")
    while True:
        _print.header("Main Menu")
        _answer:int = int(_print.menu(
                                header='New Transaction',
                                menu_header='Enter A Instruction',
                                menu=[
                                    'Login',
                                    'Signup',
                                    'Admin',
                                    'Quit / Exit'
                                ],prompt='Enter')) 

        if _answer == 1:
            #get account info
            if _bank_system.Login():
                _bank_system.print_account_info()
                while not _exit_answer:

                    #get user instruction
                    _answer = _bank_system.get_instruction()

                    if _answer == 1:
                        _bank_system.Deposite()
                    elif _answer == 2:
                        _bank_system.Withdraw()
                    elif _answer == 3: 
                        _bank_system.Balance()
                    elif _answer == 4:
                        _bank_system.Transaction_History()
                    elif _answer == 5:
                        _bank_system.Change_Pin()
                    elif _answer == 6:
                        _print.header('Exit Successful!')
                        #_bank_system.Save()
                        break
                    else:
                        _print.status("Warning","Invalid Input!")

        elif _answer == 2:
            _bank_system.Signup()
        elif _answer == 3:
            #get account info
            if _admin.Login():
                _admin.print_account_info()
                while not _exit_answer:

                    #get user instruction
                    _answer = _admin.get_instruction()

                    if _answer == 1:
                        _admin.View_List()
                    elif _answer == 2:
                        _admin.View_Account_Information()
                    elif _answer == 3: 
                        _admin.View_Account_History()
                    elif _answer == 4:
                        _admin.View_Edited_Account_History()
                    elif _answer == 5:
                        _admin.Edit_Account()
                    elif _answer == 6:
                        _admin.Change_Password()
                    elif _answer == 7:
                        _print.header('Exit Successful!')
                        #_bank_system.Save()
                        break
                    else:
                        _print.status("Warning","Invalid Input!")
        elif _answer == 4:
            _print.header('Exit Successful')
            exit(0)
        else:
            _print.status("Warning","Invalid Input!")
    del _bank_system
    del _admin

if __name__ == '__main__':
    main()
