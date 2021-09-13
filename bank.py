from time import gmtime, strftime

#hold most of the the bank functionlity
class bank:

    #initialize variable that gonna use today
    def __init__(self):
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

        #get the account information in the file
        with open('accounts/account-000-0001.txt','r') as file:
            for data in file:
                self.info.append(data)
        self.name = self.info[0]
        self.account_id = self.info[1]
        self.balance = float(self.info[2])

        #print the account info
        print(f'==========[Account Information]==========\nDate: {self.date}\nAccount Name: {self.name}Account ID: {self.account_id}Account Balance: {self.balance}')

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

    def initReWriteBalance(self):
        #clear the list and supply it with fresh information
        self.info[2] = '{:n}'.format(self.balance)
        #write the fresh account information
        with open('accounts/account-000-0001.txt','w') as file:
            for data in self.info:
                file.write(data)



bank_system = bank()
exit_answer = False
answer = ''

#get account info
bank_system.getAccountInfo()
while not exit_answer:

    #get user instruction
    answer = bank_system.getCommand()

    if answer == '1':
        bank_system.initDeposite()
    elif answer == '2':
        bank_system.initWithdraw()
    elif answer == '3': 
        bank_system.initDeposite()
    elif answer == '4':
        print('==========[Exit Successful!]==========')
        bank_system.initReWriteBalance()
        break
    else:
        print("[Invalid Input]")
        
    answer = input('[Do you want to exit?] [ Y or N ]: ')
    if answer is 'Y' or answer is 'y':
        print('==========[Exit Successful!]==========')
        bank_system.initReWriteBalance()
        exit_answer = True
    elif answer is 'N' or answer is 'n':
        exit_answer = False
    else:
        print("[Invalid Input]")
        
    


    