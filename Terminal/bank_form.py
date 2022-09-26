'''
    tools that help login and signup ease of 
    validating the right format  
'''
from datetime import time
import re
import bcrypt
from random import Random

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

def compare_pin(pin:str,encrypt_string:str) -> bool:
    if(bcrypt.checkpw(pin.encode('utf-8'),encrypt_string.encode('utf-8'))):
        return True
    return False

def encrypt_pin(pin:str) -> str:
    if(validate_pin(pin)):
        return bcrypt.hashpw(pin.encode('utf-8'),bcrypt.gensalt())
    return ''

def generate_id(num_account:str) -> str:
    rand = Random()
    return f'{rand.randint(0,999):03}-{rand.randint(0,999):03}-{rand.randint(0,9999):04}'
