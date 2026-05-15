'''
    tools that help login and signup ease of 
    validating the right format  
'''
from datetime import time
import re
import bcrypt
from random import Random

# regex search strings compile in the regex object
password_regex = re.compile('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
pin_regex = re.compile('^[0-9]{6}$')
userid_regex = re.compile('^[0-9]{3}[\-]{1}[0-9]{3}[\-]{1}[0-9]{4}')

'''
    :Description: validate the pin number format that retrieve in 
                  the user using a pin number regex

    :Parameter:
                :pin: string - :default: ''
    :Return: Boolean
''' 
def validate_pin(pin:str) -> bool:
    
    if(pin_regex.search(pin) != None):
        return True
    
    return False

'''
    :Description: validate the password format that retrieve in 
                  the user using a password regex

    :Parameter:
                :password: string - :default: ''
    :Return: Boolean
''' 
def validate_password(password:str) -> bool:
    
    if(password_regex.search(password) != None):
        return True
    
    return False

'''
    :Description: validate the userid format that retrieve in 
                  the user using a userid regex

    :Parameter:
                :userid: string - :default: ''
    :Return: Boolean
''' 
def validate_userid(userid:str) -> bool:
    
    if(userid_regex.search(userid) != None):
        return True
    
    return False

'''
    :Description: compare two different pin number that is in encrypted format

    :Parameter:
                :pin: string - :default: ''
                :encrypt_string: string - :default: ''
    :Return: Boolean
''' 
def compare_pin(pin:str,encrypt_string:str) -> bool:
    
    if(bcrypt.checkpw(pin.encode('utf-8'),encrypt_string.encode('utf-8'))):
        return True
    
    return False

'''
    :Description: compare two different password that is in encrypted format

    :Parameter:
                :password: string - :default: ''
                :encrypt_string: string - :default: ''
    :Return: Boolean
''' 
def compare_password(password:str, encrypt_string:str) -> bool:

    if(bcrypt.checkpw(password.encode('utf-8'),encrypt_string.encode('utf-8'))):
        return True
    
    return False

'''
    :Description: encrypt pin number using hash & salt

    :Parameter:
                :pin: string - :default: ''
    :Return: String
''' 
def encrypt_pin(pin:str) -> str:
    
    if(not validate_pin(pin)):
        raise Exception('Input Error: Wrong Pin Formatt')
    
    return bcrypt.hashpw(pin.encode('utf-8'),bcrypt.gensalt())

'''
    :Description: encrypt passwod using hash & salt

    :Parameter:
                :password: string - :default: ''
    :Return: String
''' 
def encrypt_password(password:str) -> str:

    if(not validate_password(password)):
        raise Exception('Input Error: Wrong Password Format')
    
    return bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

'''
    :Description: generate random account number for new account

    :Parameter:
                :num_account: string - :default: ''
    :Return: String
''' 
def generate_id(num_account:str) -> str:
    
    rand = Random()
    
    return f'{rand.randint(0,999):03}-{rand.randint(0,999):03}-{rand.randint(0,9999):04}'
