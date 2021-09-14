
# Author: John Jayson B. De Leon
# Github: github.com/savjaylade84
# Email: savjaylade84@gmail.com

from time import gmtime, strftime
from pathlib import Path

#hold most of the the bank functionlity
class bank:

    #initialize variable that gonna use today
    def __init__(self):
        self.account_numbers = []
        self.path = ""
        self.user_id = ""
        self.password = ""
        self.path = ""
        self.info = []
        self.name = ""
        self.account_id = "" 
        self.balance = ""
        self.date = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())   #set already the time so it don't needed it later

    #get the instruction or command from the list of command that prompted to the user
    def getCommand(self):
        print(f'==========[New Transaction]==========\n[Enter A Instruction]\n[1]:Deposite\n[2]:Withdraw\n[3]:Balance\n[4]:Exit')
        self.instruction_code = input("[Enter]: ")
        return self.instruction_code

    #get the user or account info 
    def getAccountInfo(self):

        self.name = self.info[0]
        self.account_id = self.info[1]
        self.balance = float(self.info[2])

        #print the account info
        print(f'==========[Account Information]==========\nDate: {self.date}\nAccount Name: {self.name}\nAccount ID: {self.account_id}\nAccount Balance: {self.balance}')

    #------------------- basic bank functionlity -----------------------------------
    def initDeposite(self):
        self.amount = float(input('[Enter a Amount]: '))
        if(self.amount < 0):
            print('[Ineffecient Amount]')
            pass
        self.balance = self.balance + self.amount
        print(self.balance)
        pass
    
    def initWithdraw(self):
        self.amount = float(input('[Enter a Amount]: '))
        if(self.amount > self.balance or self.amount < 0):
            print('[Ineffecient Amount!]')
            pass
        self.balance = self.balance - self.amount
        print(self.balance)
        pass

    def initBalance(self):
        print(self.balance)
        pass

    #------------------- basic account functionality -----------------------------------
    def initReWriteBalance(self):
        #clear the list and supply it with fresh information
        self.info[2] = '{:n}'.format(self.balance)
        #write the fresh account information
        with open(f'accounts/account-{self.user_id}.txt','r+') as file:
            for data in self.info:
                file.write(f'{data}\n')

    def initLogin(self):
        print('==========[Account Login]==========')
        self.user_id = input('[Enter User-ID]:')
        self.path = Path(f'accounts/account-{self.user_id}.txt')

        #retry until the correct userid is given or else exit
        index = 1
        while not self.path.exists():
            self.user_id = input('[Enter User-ID Again]:')
            self.path = Path(f'accounts/account-{self.user_id}.txt')
            if index < 3:
                print('==========[Login Attempt Failed!]==========')
                exit(1)
            index = index + 1

        #collect all the info according to the user id
        with open(f'accounts/account-{self.user_id}.txt','r') as file:
            for data in file:
                self.info.append(data.rstrip())

        self.password = input('[Enter Password]:')        
        if self.password == self.info[3]:
            return True
        return False

    def initSignup(self):
        #get the list of accounts in the system
        with open(f'accounts/account-numbers.txt','r') as file:
            for data in file:
                self.account_numbers.append(data.rstrip())

        #add account id accoording to the list
        self.user_id = f'000-000{len(self.account_numbers) + 1}' 
        #get and add other user info 
        self.info.append(input('[Enter Name]:'))
        self.info.append(self.user_id)
        self.info.append(input('[Enter Amount]:'))
        self.info.append(input('[Enter Password]:'))
        #write the user info in the new file
        with open(f'accounts/account-{self.user_id}.txt','w') as file:
                for data in self.info:
                    file.write(f'{data}\n')
        #update the account list
        with open(f'accounts/account-numbers.txt','a') as file:
            file.write(f'\n{self.info[0]}|{self.user_id}')
        print("==========[Successful Login!]==========")

    #clear everything
    def initClear(self):
        self.account_numbers = []
        self.path = ""
        self.user_id = ""
        self.password = ""
        self.path = ""
        self.info = []
        self.name = ""
        self.account_id = "" 
        self.balance = ""


bank_system = bank()
exit_answer = False
answer = ''
 
while True:
    print("==========[Welcome to Mock Bank System!]==========")
    answer = input(f'Enter a the command\n(1) Login\n(2) Signup\n(3) Quit / Exit\n[Enter]:')

    if answer == '1':
        #get account info
        if bank_system.initLogin():
            bank_system.getAccountInfo()
            while not exit_answer:

                #get user instruction
                answer = bank_system.getCommand()

                if answer == '1':
                    bank_system.initDeposite()
                elif answer == '2':
                    bank_system.initWithdraw()
                elif answer == '3': 
                    bank_system.initBalance()
                elif answer == '4':
                    print('==========[Exit Successful!]==========')
                    bank_system.initReWriteBalance()
                    bank_system.initClear()
                    break
                else:
                    print("[Invalid Input]")
                    
                answer = input('[Do you want to exit?] [ Y or N ]: ')
                if answer is 'Y' or answer is 'y':
                    print('==========[Exit Successful!]==========')
                    bank_system.initReWriteBalance()
                    bank_system.initClear()
                    exit_answer = True
                elif answer is 'N' or answer is 'n':
                    exit_answer = False
                else:
                    print("[Invalid Input]")
    elif answer == '2':
        bank_system.initSignup()
    elif answer == '3':
        exit(0)
    else:
        print('[Wrong Input!]')
        
    


    