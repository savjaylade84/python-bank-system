'''
    tools that help login and signup ease of 
    validating the right format  
'''
import re

pin_regex = re.compile('^[0-9]{6}$')
userid_regex = re.compile('^[0-9]{3}[\-]{1}[0-9]{3}[\-]{1}[0-9]{4}')

def validate_pin(pin:str) -> bool:
    if(pin_regex.search(pin) != None):
        return True
    return False

def validate_userid(userid:str) -> bool:
    if(userid_regex.search(userid) != None):
        return True
    return False