'''
    custom terminal print and output for the system
'''

from getpass import getpass

class string_formatter:
    
    def __init__(self) -> None:

        self.header_formatter:str = ''
        self.__title:str = ''
        self.__length:int = 0
    
    @property
    def title(self) -> str:
        
        return self.__title

    @title.setter
    def title(self,title:str) -> None:
        self.__title =  title


    @property
    def title_length(self) -> int:
        return len(self.__title)


    @property
    def header(self) -> None:
        pass
    
    @header.getter
    def header(self) -> str:
        return self.header_formatter
    
    @header.setter
    def header(self,string:str) -> None:
        self.title = string
        self.header_formatter = f''' 
{"="*17}{"=" * len(string)}{"="*17}
{"="*15}[ {self.title.upper()} ]{"="*15}
{"="*17}{"=" * len(string)}{"="*17}
'''
class Print:
   
    def __init__(self):
       self.__formatter = string_formatter()

    # print a custom divider header
    def header(self,string:str='') -> None:
        self.__formatter.header = string
        print(self.__formatter.header,end='')
        
    # print datas in a user information style
    def datas(self,header:str,data_header:list[str],datas:list) -> None:
        if header != '':
            self.__formatter.header = header
            print(self.__formatter.header,end='')
        
        for header,data in zip(data_header,datas):
            print(f'( {header} ): {data}')
        
        
    # print data in a user information style
    def data(self,header:str,data_header:str,data:str) -> None:
        if header != '':
            self.__formatter.header = header
            print(self.__formatter.header,end='')
        print(f'( {data_header} ): {data}')
    
    def input(self,string:str) ->str:
        return input(f'[ {string} ]: ')
    
    def password(self,string:str) -> str:
        return getpass(f'[ {string} ]:')
    
    # print a menu or command to user to choose
    def menu(self,header:str,menu_header:str,menu:list,prompt:str = '') -> str:
        if header != '':
            self.__formatter.header = header
            print(self.__formatter.header,end='')
            
        print(f'[ {menu_header} ]')
        index = 1
        for item in menu:
            print(f'[ {index} ]: {item}')
            index = index + 1
        
        if(prompt != ''):
            temp = self.input(prompt)
            if(int(temp) <= (len(menu) + 1)):
                return temp
  
        return ''
    
    def status(self,state:str='',message:str='') -> None:
        print(f'[ {state} ]: {message}')
        
    def border(self,extend_border:int = 30) -> None:
        print(f'{"=" * (extend_border + self.__formatter.title_length + 4)}'.strip())
        