from dataclasses import dataclass,field
  
@dataclass
class Account_List:
    name:str = field(default=str)
    account_id:str = field(default=str)
    path:str = field(default=str)
    
@dataclass
class Edited_Account_History:
    date_time:str = field(default=str)
    account_id:str = field(default=str)
    editor:str = field(default=str)
    
@dataclass
class Admin:
    password:str = field(default=str)
    account_list:list[Account_List] = field(default=list[Account_List])
    
    

