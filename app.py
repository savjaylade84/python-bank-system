
'''
     Author: John Jayson B. De Leon
     Github: github.com/savjaylade84
     Email: savjaylade84@gmail.com
'''

'''
    :Description: the main function that cohesive the other functionlity
                  and the flow of the system

    :Parameter: None
    :Return: None
'''   
def main() -> None:
    
    from Utils import console,models
    from typing import Final

    print("<<<<<<<<<<( Welcome to Mock Bank System! )>>>>>>>>>>>")
    print(f"\n[ Creator ]: John Jayson B. De Leon\n"+
          f"[ Gmail ]: savjaylade84@gmail.com\n"+
          f"[ Github ]: savjaylade84\n"+
          f"[ Version ]: 3.9v")
    
    while True:

        _exit_answer = False
        _answer = ''
        console.banner(models.DivConfig(17,"="),"Main Menu",end="\n")
        MENU:Final[list[str]] = [
                                    'Login',
                                    'Signup',
                                    'Admin',
                                    'Quit/Exit'
                                ]
        _answer:int = int(console.menu(
                                        instruction='Enter A Instruction',
                                        items=MENU,
                                        prompt_label='Enter',
                                        header='New Transaction',
                                        start="\n"
                                    )) 

        import Account.menu
        import Account.services
        import Account.models
        import Account.view
        import Account.auth

        if _answer == 1:
            #get account info
            if Account.auth.login():
                Account.view.print_account_info()
                while not _exit_answer:

                    #get user instruction
                    _answer = Account.menu.get_menu_selection()  

                    match _answer:
                        case 1:
                            Account.services.deposit()
                        case 2:
                            Account.services.withdraw()
                        case 3: 
                            Account.view.balance()
                        case 4:
                            Account.view.transaction_history()
                        case 5:
                            Account.services.change_pin()
                        case 6:
                            console.header('Exit Successful')
                            _exit_answer = True
                        case _:
                            console.status("Warning","Invalid Input!")


        elif _answer == 2:
            Account.auth.signup()
        elif _answer == 3:
            
            import Admin.auth
            import Admin.menu
            import Admin.services
            import Admin.view
                        
            #get account info
            if Admin.auth.login():
                Admin.view.account_infos()
                while not _exit_answer:

                    #get user instruction
                    _answer = Admin.menu.get_menu_selection()

                    match _answer:
                        case 1:
                            Admin.view.account_list()
                        case 2:
                            Admin.view.account_info()
                        case 3:
                            Admin.view.account_history()
                        case 4:
                            Admin.view.edited_account_history()
                        case 5:
                            Admin.services.change_account_pin()
                        case 6:
                            Admin.services.change_password()
                        case 7:
                            Admin.services.delete_account()
                        case 8:
                            Admin.services.ai_analysis()
                        case 9:
                            console.header('Exit Successful!')
                            #_bank_system.Save()
                            _exit_answer = True
                        case _:
                            print.status("Warning","Invalid Input!")
            # add something if login failed to enter three times
        elif _answer == 4:
            console.header('Exit Successful')
            exit(0)
        else:
            console.status("Warning","Invalid Input!")

    # free memory from object
    del _bank_system
    del _admin

if __name__ == '__main__':
    main()
