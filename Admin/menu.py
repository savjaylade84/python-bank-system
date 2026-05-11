from Utils import print

'''
    :Description: show the option on the user then capture and send the option

    :Parameter: None
    :Return: Integer
'''

def get_instruction(self) -> int:
        
    # list of available list on the admin part
    __menu:list = [
                        'View Account List',
                        'View Account Information',
                        'View Account History',
                        'View Edited Account History',
                        'Change Account Pin',
                        'Change Password',
                        'Delete Account',
                        'AI Analysis',
                        'Exist'  
                    ]
        
    return int(print.menu(
                        instruction='Enter A Instruction',
                        menu =__menu,
                        prompt='Enter',
                        start="\n"
                    )) 