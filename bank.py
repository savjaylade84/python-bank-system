
# Author: John Jayson B. De Leon
# Github: github.com/savjaylade84
# Email: savjaylade84@gmail.com

from time import gmtime, strftime
from pathlib import Path

class BankError(Exception):
    ''' 
        Custom made error class for any error that
        may occur in the bank system
    '''

    def __init__(self,message:str) -> None:
        self.message = message

#hold most of the the bank functionlity
class bank:

    def __init__(self) -> None:
        self._account_numbers:list = []
        self._path:str = ""
        self._user_id:str = ""
        self._password:str = ""
        self._path:str = ""
        self._info:str = []
        self._name:str = ""
        self._account_id:str = "" 
        self._balance:float = 0.0
        self._date = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())   #set already the time so it don't needed it later

    #get the instruction or command from the list of command that prompted to the user
    def getCommand(self) -> int:
        print(f'\n==========[New Transaction]==========\n[Enter A Instruction]\n[1]:Deposite\n[2]:Withdraw\n[3]:Balance\n[4]:Exit')
        self._instruction_code = int(input("[Enter]: "))
        return self._instruction_code

    #get the user or account info 
    def getAccountInfo(self) -> None:

        self._name = self._info[0]
        self._account_id = self._info[1]
        self._balance = float(self._info[2])

        #print the account info
        print(f'\n==========[Account Information]==========\nDate: {self._date}\nAccount Name: {self._name}\nAccount ID: {self._account_id}\nAccount Balance: {self._balance}')

    #------------------- basic bank functionlity -----------------------------------
    def initDeposite(self) -> None:
        print('\n==========[Deposite Process]==========')
        
        while True:
            self._amount = float(input('[Enter a Amount]: '))

            if(self._amount < 0):
                print('[Ineffecient Amount]')

            answer:str = input('[Confirm Transaction [Y] yes / [N] no]:')
            if(answer == 'N'):
                answer = input('[Proceed To Exit [Y] yes / [N] no]:')
                if(answer == 'Y'):
                    break
            elif(answer == 'Y'):
                self._balance = self._balance + self._amount
                print('[Success]: Process is Successfully Done!')
                print(f'(Balance):{self._balance}')
                break
            else:
                print('[Wrong Input!]')

        pass

        pass
    
    def initWithdraw(self) -> None:
        print('\n==========[Withdraw Process]==========')

        while True:
            self._amount = float(input('[Enter a Amount]: '))

            if(self._amount > self._balance or self._amount < 0):
                print('[Ineffecient Amount!]')

            answer:str = input('[Confirm Transaction [Y] yes / [N] no]:')
            if(answer == 'N'):
                answer = input('[Proceed To Exit [Y] yes / [N] no]:')
                if(answer == 'Y'):
                    break
            elif(answer == 'Y'):
                self._balance = self._balance - self._amount
                print('[Success]: Process is Successfully Done!')
                print(f'(Balance):{self._balance}')
                break
            else:
                print('[Wrong Input!]')

        pass

    def initBalance(self) -> None:
        print('\n==========[Current Balance]==========')
        print(f'(Balance):{self._balance}')
        pass

    #------------------- basic account functionality -----------------------------------
    def initReWriteBalance(self) -> None:
        #clear the list and supply it with fresh information
        self._info[2] = '{:n}'.format(self._balance)

        #write the fresh account information
        with open(f'accounts/account-{self._user_id}.txt','r+') as file:
            for data in self._info:
                file.write(f'{data}\n')

    def initLogin(self) -> bool:
        print('\n==========[Account Login]==========')
        self._user_id = input('[Enter User-ID]:')
        self._path = Path(f'accounts/account-{self._user_id}.txt')

        #retry until the correct userid is given or else exit
        index = 1
        while not self._path.exists():
            self._user_id = input('[Enter User-ID Again]:')
            self._path = Path(f'accounts/account-{self._user_id}.txt')
            if index < 3:
                print('==========[Login Attempt Failed!]==========')
                exit(1)
            index = index + 1

        #collect all the info according to the user id
        with open(f'accounts/account-{self._user_id}.txt','r') as file:
            for data in file:
                self._info.append(data.rstrip())

        self._password = input('[Enter Password]:')        
        if self._password == self._info[3]:
            return True
        return False

    def initSignup(self) -> None:
        print("\n==========[Registration]==========")
        #get the list of accounts in the system
        with open(f'accounts/account-numbers.txt','r') as file:
            for data in file:
                self._account_numbers.append(data.rstrip())

        #add account id accoording to the list
        self._user_id = f'000-000{len(self._account_numbers) + 1}' 
        #get and add other user info 
        self._info.append(input('[Enter Name]:'))
        self._info.append(self._user_id)
        self._info.append(input('[Enter Amount]:'))

        print('[Note]: Password limit range is 18-200 characters only')
        index:int = 0
        temp:str = ""
        while index < 3:            

            ''' 
                only write the newly account in a file if the 
                password requirements is meet until the three
                allowed re-entry of password is done.

            '''
            temp = input('[Enter Password]:')
            if(self._password_max_length(temp) and index < 2):
                self._info.append(temp)
                        #write the user info in the new file
                with open(f'accounts/account-{self._user_id}.txt','w') as file:
                        for data in self._info:
                            file.write(f'{data}\n')

                #update the account list
                with open(f'accounts/account-numbers.txt','a') as file:
                    file.write(f'\n{self._info[0]}|{self._user_id}')
                print(f'\nDetails:\nAccount-ID:{self._info[1]}\nAccount Name:{self._info[0]}\nAccount Username:{self._info[1]}\n')
                print("==========[Successfully!]==========")
                break

            if(index < 2):
                print("[[[ Try Again Pls! ]]]")
            else:
                print("==========[Terminated Process!]==========")
                print('[[[ Opps! You Already Tried 3 Times Now ]]]')

            index = index + 1

    def _password_max_length(self,password:str) -> bool:
        if(len(password) < 18):
            print(f'[Warning!]: Password Over Meet the Expected Minimum Character')
            return False

        if(len(password) > 200):
            print(f'[Warning!]: Password Over Meet the Expected Miximum Character')
            return False
        
        return True

    #clear everything
    def initClear(self) -> None:
        self._account_numbers = []
        self._path = ""
        self._user_id = ""
        self._password = ""
        self._path = ""
        self._info = []
        self._name = ""
        self._account_id = "" 
        self._balance = ""


bank_system = bank()
exit_answer = False
answer = ''


if __name__ == '__main__':

    print("<<<<<<<<<<( Welcome to Mock Bank System!)>>>>>>>>>>>")
    print(f"\n[Creator]: John Jayson B. De Leon\n[Gmail]: savjaylade84@gmail.com\n[Github]: savjaylade84\n[Version]: 2.8v\n")
    while True:
        print("\n==========[Main Menu]==========")
        answer:int = int(input(f'Enter a the command\n(1) Login\n(2) Signup\n(3) Quit / Exit\n[Enter]:'))

        if answer == 1:
            #get account info
            if bank_system.initLogin():
                bank_system.getAccountInfo()
                while not exit_answer:

                    #get user instruction
                    answer = bank_system.getCommand()

                    if answer == 1:
                        bank_system.initDeposite()
                    elif answer == 2:
                        bank_system.initWithdraw()
                    elif answer == 3: 
                        bank_system.initBalance()
                    elif answer == 4:
                        print('==========[Exit Successful!]==========')
                        bank_system.initReWriteBalance()
                        bank_system.initClear()
                        break
                    else:
                        print("[Invalid Input]")

        elif answer == 2:
            bank_system.initSignup()
            bank_system.initClear()
        elif answer == 3:
            bank_system.initClear()
            print('\n==========[Exit Successful!]==========')
            exit(0)
        else:
            print('[Wrong Input!]')
        bank_system.initClear()
        
    


    