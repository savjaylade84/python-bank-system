import unittest as unit
from unittest.mock import patch
from Utils import console

class test_console(unit.TestCase):
    
    @patch('Utils.console.prompt_pwd')
    def test_prompt_pwd(self,mock_input):

        mock_input.return_value = "hello"
        
        result = console.prompt_pwd("enter")
        
        self.assertEqual(result,"hello")
        
        
if __name__ == '__main__':
    unit.main()