import io
import textwrap
import unittest as unit
from unittest.mock import patch
from Utils import console,models
from contextlib import redirect_stdout

class test_console(unit.TestCase):
    
    # you tell patch that you are going to use prompt_pwd
    @patch('Utils.console.prompt_pwd') 
    def test_prompt_pwd(self,mock_input) -> None:

        mock_input.return_value = "hello"
        
        result = console.prompt_pwd("enter")
        
        self.assertEqual(result,"hello")
        
    @patch('Utils.console.prompt') 
    def test_prompt(self,mock_input) -> None:
        
        mock_input.return_value = "hello"
        
        result = console.prompt("Enter")
        
        self.assertEqual(result,"hello")
        
    def test_print(self) -> None:
        
        # setup a text stream buffer to store the output
        tstream:io.StringIO = io.StringIO()
        
        # store the output while executing the console.print
        with redirect_stdout(tstream):
            console.print("hello")
        
        # test the store output and mock value
        self.assertEqual(tstream.getvalue(),"hello")
        
    def test_status(self) -> None:
        
        tstream:io.StringIO = io.StringIO()
        
        with redirect_stdout(tstream):
            console.status(models.TransactionStatus.Warning,"testing")
            
        self.assertEqual(tstream.getvalue(),"[ Warning ] : testing")
        
    def test_divider(self) -> None:
        
        config:models.DivConfig = models.DivConfig(count=5,style="*")
        tstream:io.StringIO = io.StringIO()
        
        with redirect_stdout(tstream):
            console.divider(config)
            
        self.assertEqual(tstream.getvalue(),"*****")
        
    def test_banner(self) -> None:
        
        config:models.DivConfig = models.DivConfig(count=4,style="*")
        tstream:io.StringIO = io.StringIO()
        
        with redirect_stdout(tstream):
            console.banner(config,"Information")
          
        #console.banner(config,"Information",end="\n")
          
        expected_output:str = textwrap.dedent("""*******************
**[ Information ]**
*******************""")
        
        self.assertMultiLineEqual(tstream.getvalue(),expected_output)
        
    def test_label(self) -> None:
        
        config:models.DivConfig = models.DivConfig(count=4,style="*")
        tstream:io.StringIO = io.StringIO()
        
        with redirect_stdout(tstream):
            console.label(config,"Hello")
            
        self.assertEqual(tstream.getvalue(),"**[ Hello ]**")
        
    def test_entry(self) -> None:
        
        config:models.DivConfig = models.DivConfig(count=4,style="*")
        entry:models.DivConfig = models.LabelEntry('Name','John')
        tstream:io.StringIO = io.StringIO()
        
        with redirect_stdout(tstream):
            console.entry(entry=entry,config=config,title="Information")
        
        #console.entry(entry=entry,config=config,title="Information")
        
        expected_output:str = textwrap.dedent("""*******************
**[ Information ]**
*******************
[ Name ] : John""")  
        
        self.assertMultiLineEqual(tstream.getvalue(),expected_output)
        
    def test_entries(self) -> None:
        ...
        
    def test_list(self) -> None:
        ...
        
    def test_menu(self) -> None:
        ...
        
        
if __name__ == '__main__':
    unit.main()