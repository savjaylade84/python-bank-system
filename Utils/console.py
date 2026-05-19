'''

console.py
==========
different style print and input for the bank system

Author: John Jayson De Leon
GithubL: github.com/savjaylade
'''

import sys
from getpass import getpass
from Utils import models

def print(message:str,start="",end="") -> None:
    '''
        print in the terminal
        
        Args:
            message (str)
            start   (str)
            end     (str)
            
        Return: 
            None
        
        Raises:
            None
        
        Note:
            None
        
        Example:
            print('Hello World')
            print('Hello World',end='\n')
    '''
    sys.stdout.write(f"{start}{message}{end}")

def status(status:models.TransactionStatus,message:str,start="",end="") -> None:
    '''
        print with notice style in the terminal
        
        Args:
            status  (Utils.models.TransactionStatus)
            message (str)
            start   (str)
            end     (str)
            
        Return: 
            None
        
        Raises:
            None
        
        Note:
            None
        
        Example:
            status(Utils.models.Transaction.Warning,'This is a Warning')
            status(Utils.models.Transaction.Warning,'This is a Warning',end='\n')
    '''
    print(f"[ {status.name} ] : {message}",start,end)

def divider(config:models.DivConfig,start="",end="") -> None:
    '''
        print divider in the terminal
        
        Args:
            config  (Utils.models.DivConfig)
            start   (str)
            end     (str)
            
        Return: 
            None
        
        Raises:
            None
        
        Note:
            None
        
        Example:
            divider(Utils.models.DivConfig(count=17,style=#))
            divider(Utils.models.DivConfig())
    '''
    print(f"{config.count * config.style}",start,end)

def banner(config:models.DivConfig,title:str,start="",end="") -> None:
    '''
        print a banner or header style in the terminal
        
        Args:
            config  (Utils.models.DivConfig)
            title   (str)
            start   (str)
            end     (str)
            
        Return: 
            None
        
        Raises:
            None
        
        Note:
            None
        
        Example:
            banner(Utils.models.DivConfig(),title="Hello")
    '''
    border:str = (config.count - 2) * config.style
    border_side:str = (config.count * 2 + len(title) - 2) * config.style
    print(f"{border_side}\n{border}[{title}]{border}\n{border_side}",start,end)

def label(config:models.DivConfig,title:str,start="",end="") -> None:
    '''
        print a label style in the terminal
        
        Args:
            config  (Utils.models.DivConfig)
            title   (str)
            start   (str)
            end     (str)
            
        Return: 
            None
        
        Raises:
            None
        
        Note:
            None
        
        Example:
            label(Utils.models.DivConfig,title='Hello World')
    '''
    border:str = config.count * config.style
    print(f"{border}[{title}]{border}",start,end)

def entry(entry:models.LabelEntry | tuple,title="",start="",end="") -> None:

    '''
        print in a entry of data in the terminal
        
        Args:
            entry   (Utils.models.LabelEntry)
            title   (str)
            start   (str)
            end     (str)
            
        Return: 
            None
        
        Raises:
            None
        
        Note:
            can directly use the banner()
        
        Example:
            print(Utils.models.LabelEntry("title","desc"),title='Hello World')
    '''
    
    # convert regular tuple into section_header tuple
    if not isinstance(entry,models.LabelEntry):
        entry = models.LabelEntry._make(entry)
    
    if title:
        banner(models.DivConfig(),title,start,end)
        print(f"[ {entry.title} ] : {entry.desc}",start)

def entries(labels:list[str],entries:list,title="",start="",end="") -> None:
    '''
        print entries in the terminal
        
        Args:
            labels  (list[str])
            entries (list)
            title   (str)
            start   (str)
            end     (str)
            
        Return: 
            None
        
        Raises:
            None
        
        Note:
            can directly use the banner()
        
        Example:
            entries(title='title',labels=['label'],entries=['hello world'])
    '''
    if title:
        banner(models.DivConfig(),title)
        
    for entry,info in zip(labels,entries):
        entry(entry,info,start,end)
      
def list(items:list,start="",end="") -> None:
    '''
        print a numbered list of items in the terminal
        
        Args:
            items   (list)
            start   (str)
            end     (str)
            
        Return: 
            None
        
        Raises:
            None
        
        Note:
            None
        
        Example:
            list(['item1','item2','item3'])
            list(['item1','item2'],end='\n')
    '''
    for index, item in enumerate(items):
        entry((index + 1,item),start,end)
  
def prompt(label:str,start="",end=""):
    '''
        get user input with a label style in the terminal
        
        Args:
            label   (str)
            start   (str)
            end     (str)
            
        Return: 
            String
        
        Raises:
            None
        
        Note:
            None
        
        Example:
            prompt('Enter Name')
            prompt('Enter Name',end='\n')
    '''
    print(f"{start}[ {label} ] : {end}")
    sys.stdout.flush()
    data = sys.stdin.readline()
    return data 

def prompt_pwd(label:str) -> None:
    '''
        get user password input without showing
        the data in the terminal
        
        Args:
            label   (str)
            
        Return: 
            String
        
        Raises:
            None
        
        Note:
            None
        
        Example:
            prompt_pwd('Enter Password')
    '''
    return getpass(f"[ {label} ] : ")

def menu(instruction:str,items:list,prompt_label:str,header:str="",start="") -> str:
    '''
        print a menu with banner, numbered list, and prompt
        in the terminal
        
        Args:
            instruction     (str)
            items           (list)
            prompt_label    (str)
            header          (str)
            start           (str)
            
        Return: 
            String
        
        Raises:
            IOError: if instruction is empty
        
        Note:
            None
        
        Example:
            menu('Select Option',['Login','Exit'],'Enter Choice',header='Main Menu')
    '''
    if(header):
        banner(models.DivConfig(),header,start=start)
    
    if(instruction):
        banner(models.DivConfig,instruction,start=start)
        list(items,end="\n")
        return prompt(prompt_label,start)

    raise IOError    
