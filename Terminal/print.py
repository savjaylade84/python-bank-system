'''
    custom terminal print and output for the system
'''

from getpass import getpass

class string_formatter:

    def __init__(self) -> None:

        self.header_formatter:str = ''
        self.__title:str = ''
        self.__length:int = 0
 
    '''
        :Description: get title header for the terminal

        :Parameter: None
        :Return: String
    '''   
    @property
    def title(self) -> str:
        
        return self.__title

    '''
        :Description: set title header for the terminal

        :Parameter:
                    :title: string - :default: ''
        :Return: None
    '''
    @title.setter
    def title(self,title:str) -> None:
        self.__title =  title

    '''
        :Description: get title length that use for measuring the border 

        :Parameter: None
        :Return: Integer
    '''
    @property
    def title_length(self) -> int:
        return len(self.__title)


    @property
    def header(self) -> None:
        pass

    '''
        :Description: get the header formatter that use for proper style 
                      of the header that will be printed

        :Parameter: None
        :Return: String
    '''
    @header.getter
    def header(self) -> str:
        return self.header_formatter

    '''
        :Description: get the header formatter that use for proper style 
                      of the header that will be printed

        :Parameter:
                    :string: string - :default: ''
        :Return: None
    '''
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

    '''
        :Description: print costum style header in the terminal

        :Parameter:
                    :string: string - :default: ''
        :Return: None
    ''' 
    def header(self,string:str='') -> None:
        self.__formatter.header = string
        print(self.__formatter.header,end='')
        
    '''
        :Description: print multiple data in user information style in terminal

        :Parameter:
                    :header: string - :default: ''
                    :data_headr: list - string - :default: [string]
                    :datas: list - :default: []
        :Return: None
    ''' 
    def datas(self,header:str,data_header:list[str],datas:list) -> None:
        if header != '':
            self.__formatter.header = header
            print(self.__formatter.header,end='')
        
        for header,data in zip(data_header,datas):
            print(f'( {header} ): {data}')
        
    '''
        :Description: print the data in user information style in terminal

        :Parameter:
                    :header: string - :default: ''
                    :data_headr:string - :default: ''
                    :datas: string - :default: ''
        :Return: None
    '''       
    def data(self,header:str,data_header:str,data:str) -> None:
        if header != '':
            self.__formatter.header = header
            print(self.__formatter.header,end='')
        print(f'( {data_header} ): {data}')
    
    '''
        :Description: get the user data from terminal prompt 

        :Parameter:
                    :string: string - :default: ''
        :Return: String
    ''' 
    def input(self,string:str) ->str:
        return input(f'[ {string} ]: ')
    
    '''
        :Description: get the user password data from terminal prompt
                      without showing the data in the terminal

        :Parameter:
                    :string: string - :default: ''
        :Return: String
    ''' 
    def password(self,string:str) -> str:
        return getpass(f'[ {string} ]:')
    
    '''
        :Description: print the menu or choices that represent the functionalities
                      of the system to the user 

        :Parameter:
                    :header: string - :default: ''
                    :menu_headr: string - :default: ''
                    :menu: list - :default: []
                    :prompt: string - :default: ''
        :Return: None
    ''' 
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
    
    '''
        :Description: print the status or progress in the system

        :Parameter:
                    :message: string - :default: ''
        :Return: None
    ''' 
    def status(self,state:str='',message:str='') -> None:
        print(f'[ {state} ]: {message}')

    '''
        :Description: print border that seperate each operation that
                      conduct in the system

        :Parameter:
                    :extend_border: int - :default: 0
        :Return: None
    '''     
    def border(self,extend_border:int = 30) -> None:
        print(f'{"=" * (extend_border + self.__formatter.title_length + 4)}'.strip())
        