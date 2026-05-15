
'''
     Author: John Jayson B. De Leon
     Github: github.com/savjaylade84
     Email: savjaylade84@gmail.com
'''

from Operation.Operation import Operation
from Utils.console import Print

'''
    :Description: the main function that cohesive the other functionlity
                  and the flow of the system

    :Parameter: None
    :Return: None
'''   
def main() -> None:
    _bank_system = Operation()
    _print = Print()

    print("<<<<<<<<<<( Welcome to Mock Bank System! )>>>>>>>>>>>")
    print(f"\n[ Creator ]: John Jayson B. De Leon\n"+
          f"[ Gmail ]: savjaylade84@gmail.com\n"+
          f"[ Github ]: savjaylade84\n"+
          f"[ Version ]: 3.9v")
    
    while True:

        _exit_answer = False
        _answer = ''
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

                    match _answer:
                        case 1:
                            _bank_system.Deposite()
                        case 2:
                            _bank_system.Withdraw()
                        case 3: 
                            _bank_system.Balance()
                        case 4:
                            _bank_system.Transaction_History()
                        case 5:
                            _bank_system.Change_Pin()
                        case 6:
                            _print.header('Exit Successful')
                            _exit_answer = True
                        case _:
                            _print.status("Warning","Invalid Input!")


        elif _answer == 2:
            _bank_system.Signup()
        elif _answer == 3:
            
            from Admin import services
            from Admin import auth
            from Admin import view
            from Admin import menu
            
            #get account info
            if auth.login():
                view.account_infos()
                while not _exit_answer:

                    #get user instruction
                    _answer = menu.get_menu_selection()

                    match _answer:
                        case 1:
                            view.account_list()
                        case 2:
                            view.account_info()
                        case 3:
                            view.account_history()
                        case 4:
                            view.edited_account_history()
                        case 5:
                            services.change_account_pin()
                        case 6:
                            services.change_password()
                        case 7:
                            services.delete_account()
                        case 8:
                            services.ai_analysis()
                        case 9:
                            _print.header('Exit Successful!')
                            #_bank_system.Save()
                            _exit_answer = True
                        case _:
                            print.status("Warning","Invalid Input!")
            # add something if login failed to enter three times
        elif _answer == 4:
            _print.header('Exit Successful')
            exit(0)
        else:
            _print.status("Warning","Invalid Input!")

    # free memory from object
    del _bank_system
    del _admin

if __name__ == '__main__':
    main()
