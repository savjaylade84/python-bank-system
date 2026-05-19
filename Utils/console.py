'''
console.py
==========
provides a collection of styled print and input functions
for displaying formatted output in the terminal for the bank system
includes support for banners, labels, dividers, menus, entries,
and secure password input

Author: John Jayson De Leon
Github: github.com/savjaylade
'''

import sys
from getpass import getpass
from Utils import models

def print(message:str,start="",end="") -> None:
    '''
        write a message directly to the terminal
        using stdout without the default newline behavior
        
        Args:
            message (str)   : the text content to display in the terminal
            start   (str)   : string to prepend before the message
            end     (str)   : string to append after the message
            
        Return: 
            None
        
        Raises:
            None
        
        Note:
            overrides the built-in print() function
            uses sys.stdout.write() for direct output control
            no newline is added by default
        
        Example:
            print('Hello World')
            print('Hello World', end='\n')
            
            Output:
                Hello World
    '''
    sys.stdout.write(f"{start}{message}{end}")

def status(status:models.TransactionStatus,message:str,start="",end="") -> None:
    '''
        print a transaction status notice with a labeled
        style format in the terminal
        
        Args:
            status  (Utils.models.TransactionStatus)    : the transaction status enum 
                                                          used as the label indicator
            message (str)                               : the status description or 
                                                          details to display
            start   (str)                               : string to prepend before the output
            end     (str)                               : string to append after the output
            
        Return: 
            None
        
        Raises:
            None
        
        Note:
            uses the name attribute of the TransactionStatus enum as the label
            output format: [ status ] : message
        
        Example:
            status(Utils.models.TransactionStatus.Warning, 'Insufficient Balance')
            status(Utils.models.TransactionStatus.Success, 'Deposit Complete', end='\n')
            
            Output:
                [ Warning ] : Insufficient Balance
    '''
    print(f"[ {status.name} ] : {message}",start,end)

def divider(config:models.DivConfig,start="",end="") -> None:
    '''
        print a horizontal divider line in the terminal
        based on the provided configuration style and count
        
        Args:
            config  (Utils.models.DivConfig)    : configuration object that defines
                                                  the style character and repeat count
                                                  of the divider
            start   (str)                       : string to prepend before the divider
            end     (str)                       : string to append after the divider
            
        Return: 
            None
        
        Raises:
            None
        
        Note:
            the length and character of the divider is 
            controlled by DivConfig.count and DivConfig.style
            output format: ==================
        
        Example:
            divider(Utils.models.DivConfig(count=17, style='='))
            divider(Utils.models.DivConfig(), end='\n')
            
            Output:
                =================
    '''
    print(f"{config.count * config.style}",start,end)

def banner(config:models.DivConfig,title:str,start="",end="") -> None:
    '''
        print a banner with a bordered title header style
        in the terminal using the provided configuration
        
        Args:
            config  (Utils.models.DivConfig)    : configuration object that defines
                                                  the style character and repeat count
                                                  of the border
            title   (str)                       : the text to display inside the banner
            start   (str)                       : string to prepend before the banner
            end     (str)                       : string to append after the banner
            
        Return: 
            None
        
        Raises:
            None
        
        Note:
            the border width automatically adjusts based
            on the length of the title
            output format:
                ===============
                ======[title]======
                ===============
        
        Example:
            banner(Utils.models.DivConfig(), title='Main Menu')
            banner(Utils.models.DivConfig(), title='Dashboard', end='\n')
            
            Output:
                ===================
                ======[Main Menu]======
                ===================
    '''
    border:str = (config.count - 2) * config.style
    border_side:str = (config.count * 2 + len(title) - 2) * config.style
    print(f"{border_side}\n{border}[{title}]{border}\n{border_side}",start,end)

def label(config:models.DivConfig,title:str,start="",end="") -> None:
    '''
        print a compact inline label with border style
        on both sides of the title in the terminal
        
        Args:
            config  (Utils.models.DivConfig)    : configuration object that defines
                                                  the style character and repeat count
                                                  of the border
            title   (str)                       : the text to display inside the label
            start   (str)                       : string to prepend before the label
            end     (str)                       : string to append after the label
            
        Return: 
            None
        
        Raises:
            None
        
        Note:
            unlike banner() this prints a single line only
            the border appears on both sides of the title
            output format: =====[title]=====
        
        Example:
            label(Utils.models.DivConfig(), title='Account Info')
            label(Utils.models.DivConfig(), title='Summary', end='\n')
            
            Output:
                =====[Account Info]=====
    '''
    border:str = config.count * config.style
    print(f"{border}[{title}]{border}",start,end)

def entry(entry:models.LabelEntry | tuple,title="",start="",end="") -> None:
    '''
        print a single labeled data entry in the terminal
        and optionally display a banner header above it
        
        Args:
            entry   (Utils.models.LabelEntry | tuple)   : the data entry to display,
                                                          accepts a LabelEntry object
                                                          or a plain tuple that will be
                                                          converted automatically
            title   (str)                               : optional banner title to display
                                                          above the entry
            start   (str)                               : string to prepend before the output
            end     (str)                               : string to append after the output
            
        Return: 
            None
        
        Raises:
            None
        
        Note:
            plain tuples are automatically converted to LabelEntry
            banner is only printed when title is provided
            output format: [ title ] : desc
        
        Example:
            entry(Utils.models.LabelEntry('Name', 'John'), title='Account Info')
            entry(('Balance', '5000.00'))
            
            Output:
                ===================
                =====[Account Info]=====
                ===================
                [ Name ] : John
    '''
    
    # convert regular tuple into section_header tuple
    if not isinstance(entry,models.LabelEntry):
        entry = models.LabelEntry._make(entry)
    
    if title:
        banner(models.DivConfig(),title,start,end)
        print(f"[ {entry.title} ] : {entry.desc}",start)

def entries(labels:list[str],entries:list,title="",start="",end="") -> None:
    '''
        print multiple labeled data entries in the terminal
        and optionally display a banner header above all entries
        
        Args:
            labels  (list[str]) : list of label names for each entry field
            entries (list)      : list of values corresponding to each label
            title   (str)       : optional banner title to display above the entries
            start   (str)       : string to prepend before each entry
            end     (str)       : string to append after each entry
            
        Return: 
            None
        
        Raises:
            None
        
        Note:
            labels and entries are paired using zip()
            excess items beyond the shorter list are ignored
            banner is only printed when title is provided
            output format:
                [ label1 ] : entry1
                [ label2 ] : entry2
        
        Example:
            entries(
                title   = 'Account Info',
                labels  = ['Name', 'Balance', 'Status'],
                entries = ['John', '5000.00', 'Active']
            )
            
            Output:
                ===================
                =====[Account Info]=====
                ===================
                [ Name ]    : John
                [ Balance ] : 5000.00
                [ Status ]  : Active
    '''
    if title:
        banner(models.DivConfig(),title)
        
    for entry,info in zip(labels,entries):
        entry(entry,info,start,end)

def list(items:list,start="",end="") -> None:
    '''
        print a numbered list of items in the terminal
        using the entry() format style
        
        Args:
            items   (list)  : collection of items to be displayed
            start   (str)   : string to prepend before each item
            end     (str)   : string to append after each item
            
        Return: 
            None
        
        Raises:
            None
        
        Note:
            index starts at 1 not 0
            output format: [ index ] : item
        
        Example:
            list(['Deposit', 'Withdraw', 'Exit'])
            
            Output:
                [ 1 ] : Deposit
                [ 2 ] : Withdraw
                [ 3 ] : Exit
    '''
    for index, item in enumerate(items):
        entry((index + 1,item),start,end)

def prompt(label:str,start="",end=""):
    '''
        get user input with a label style prompt in the terminal
        and return the input as a string
        
        Args:
            label   (str)   : label to display before the input field
            start   (str)   : string to prepend before the prompt
            end     (str)   : string to append after the prompt
            
        Return: 
            String : the raw input string from the user including newline
        
        Raises:
            None
        
        Note:
            flushes stdout before reading to ensure the prompt
            is visible before the user types
            output format: [ label ] : 
        
        Example:
            name = prompt('Enter Name')
            age  = prompt('Enter Age', end='\n')
            
            Output:
                [ Enter Name ] : 
    '''
    print(f"{start}[ {label} ] : {end}")
    sys.stdout.flush()
    data = sys.stdin.readline()
    return data 

def prompt_pwd(label:str) -> None:
    '''
        get user password input without showing
        the characters typed in the terminal
        
        Args:
            label   (str)   : label to display before the password field
            
        Return: 
            String : the raw password string entered by the user
        
        Raises:
            None
        
        Note:
            uses getpass to hide input from the terminal
            suitable for sensitive data such as PIN or password
            output format: [ label ] : 
        
        Example:
            pwd = prompt_pwd('Enter Password')
            pin = prompt_pwd('Enter PIN')
            
            Output:
                [ Enter Password ] : 
    '''
    return getpass(f"[ {label} ] : ")

def menu(instruction:str,items:list,prompt_label:str,header:str="",start="") -> str:
    '''
        print a complete menu interface composed of a banner header,
        instruction label, numbered list of items, and an input prompt
        then return the user selection as a string
        
        Args:
            instruction     (str)   : label describing the menu purpose
            items           (list)  : list of options to display
            prompt_label    (str)   : label for the input prompt
            header          (str)   : optional banner title shown above the menu
            start           (str)   : string to prepend before each printed line
            
        Return: 
            String : the raw input string from the user selection
        
        Raises:
            IOError : raised when instruction is empty or not provided
        
        Note:
            header is optional; if empty the banner will be skipped
            instruction must not be empty otherwise IOError is raised
            output format:
                ###########
                ##[header]##
                ###########
                ###############
                ##[instruction]##
                ###############
                [ 1 ] : item
                [ 2 ] : item
                [ prompt_label ] : 
        
        Example:
            choice = menu(
                instruction  = 'Select Option',
                items        = ['Deposit', 'Withdraw', 'Exit'],
                prompt_label = 'Enter Choice',
                header       = 'Main Menu'
            )
            
            Output:
                #############
                ##[Main Menu]##
                #############
                ##################
                ##[Select Option]##
                ##################
                [ 1 ] : Deposit
                [ 2 ] : Withdraw
                [ 3 ] : Exit
                [ Enter Choice ] : 
    '''
    if(header):
        banner(models.DivConfig(),header,start=start)
    
    if(instruction):
        banner(models.DivConfig,instruction,start=start)
        list(items,end="\n")
        return prompt(prompt_label,start)

    raise IOError