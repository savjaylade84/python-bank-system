'''
    custom terminal print and output for the system
'''
class Print:
    
    # print a custom divider header
    def header(self,string:str='') -> None:
        print(f'{"="*10}[ {string} ]{"="*10}')
        
    # print datas in a user information style
    def datas(self,header:str,data_header:list[str],datas:list) -> None:
        if header != '':
            self.header(header)
        
        for header,data in zip(data_header,datas):
            print(f'[ {header} ]: [ {data} ]')
        
        
    # print data in a user information style
    def data(self,header:str,data_header:str,data:str) -> None:
        if header != '':
            self.header(header)
        print(f'( {data_header} ): {data}')
    
    def input(self,string:str) ->str:
        return input(f'[ {string} ]: ')
    
    # print a menu or command to user to choose
    def menu(self,header:str,menu_header:str,menu:list,prompt:str = '') -> str:
        if header != '':
            self.header(header)
            
        print(f'[ {menu_header} ]')
        index = 1
        for item in menu:
            print(f'[ {index} ]: [ {item} ]')
            index = index + 1
        
        if(prompt != ''):
            temp = self.input(prompt)
            if(int(temp) <= (len(menu) + 1)):
                return temp
  
        return ''
    
        
    def border() -> None:
        print('=' * 30)
        