'''
credential.py
============
provides a collection of validation, comparison, and encryption
functions to assist login and signup operations in the bank system
includes format validation for pin, password, and userid,
secure bcrypt hashing, and encrypted value comparison

Author: John Jayson De Leon
Github: github.com/savjaylade
'''
import re
import bcrypt

# regex search strings compile in the regex object
password_regex = re.compile('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
pin_regex = re.compile('^[0-9]{6}$')
userid_regex = re.compile('^[0-9]{3}[\-]{1}[0-9]{3}[\-]{1}[0-9]{4}')

def validate_pin(pin:str) -> bool:
    '''
        validate the pin number format retrieved from the user
        against the pin regex pattern and return true if valid
        
        Args:
            pin     (str)   : the pin number string to be validated
            
        Return: 
            Boolean : True if the pin matches the required format
                      False if the pin does not match
        
        Raises:
            None
        
        Note:
            accepted format: 6 digit numeric only
            example pattern: 123456
        
        Example:
            validate_pin('123456')  -> True
            validate_pin('12345')   -> False
            validate_pin('12345a')  -> False
    '''
    if(pin_regex.search(pin) != None):
        return True
    
    return False

def validate_password(password:str) -> bool:
    '''
        validate the password format retrieved from the user
        against the password regex pattern and return true if valid
        
        Args:
            password    (str)   : the password string to be validated
            
        Return: 
            Boolean : True if the password matches the required format
                      False if the password does not match
        
        Raises:
            None
        
        Note:
            accepted format: minimum 8 characters, must contain at least
            one uppercase, one lowercase, one digit, and one special character
            accepted special characters: @ $ ! % * ? &
        
        Example:
            validate_password('Password1!')  -> True
            validate_password('password')    -> False
            validate_password('12345678')    -> False
    '''
    if(password_regex.search(password) != None):
        return True
    
    return False

def validate_userid(userid:str) -> bool:
    '''
        validate the userid format retrieved from the user
        against the userid regex pattern and return true if valid
        
        Args:
            userid  (str)   : the userid string to be validated
            
        Return: 
            Boolean : True if the userid matches the required format
                      False if the userid does not match
        
        Raises:
            None
        
        Note:
            accepted format: 3 digits, dash, 3 digits, dash, 4 digits
            example pattern: 123-456-7890
        
        Example:
            validate_userid('123-456-7890')  -> True
            validate_userid('1234567890')    -> False
            validate_userid('123-456-789')   -> False
    '''
    if(userid_regex.search(userid) != None):
        return True
    
    return False

def compare_pin(pin:str,encrypt_string:str) -> bool:
    '''
        compare a plain text pin number against an encrypted
        pin string using bcrypt and return true if they match
        
        Args:
            pin             (str)   : the plain text pin number to compare
            encrypt_string  (str)   : the bcrypt hashed pin string to compare against
            
        Return: 
            Boolean : True if the pin matches the encrypted string
                      False if the pin does not match
        
        Raises:
            None
        
        Note:
            both values are encoded to utf-8 before comparison
            encrypt_string must be a valid bcrypt hashed string
            use encrypt_pin() to generate the encrypted value
        
        Example:
            hashed = encrypt_pin('123456')
            compare_pin('123456', hashed)   -> True
            compare_pin('000000', hashed)   -> False
    '''
    if(bcrypt.checkpw(pin.encode('utf-8'),encrypt_string)):
        return True
    
    return False

def compare_password(password:str, encrypt_string:str) -> bool:
    '''
        compare a plain text password against an encrypted
        password string using bcrypt and return true if they match
        
        Args:
            password        (str)   : the plain text password to compare
            encrypt_string  (str)   : the bcrypt hashed password string to compare against
            
        Return: 
            Boolean : True if the password matches the encrypted string
                      False if the password does not match
        
        Raises:
            None
        
        Note:
            both values are encoded to utf-8 before comparison
            encrypt_string must be a valid bcrypt hashed string
            use encrypt_password() to generate the encrypted value
        
        Example:
            hashed = encrypt_password('Password1!')
            compare_password('Password1!', hashed)  -> True
            compare_password('WrongPass1!', hashed) -> False
    '''
    if(bcrypt.checkpw(password.encode('utf-8'),encrypt_string)):
        return True
    
    return False

def encrypt_pin(pin:str) -> str:
    '''
        encrypt a pin number using bcrypt hash and salt
        and return the hashed string if the format is valid
        
        Args:
            pin     (str)   : the plain text pin number to encrypt
            
        Return: 
            String : the bcrypt hashed bytes of the pin number
        
        Raises:
            Exception : raised when the pin does not match
                        the required 6 digit numeric format
        
        Note:
            validates the pin format before encrypting
            uses bcrypt gensalt() to generate a unique salt per call
            the same pin will produce a different hash each time
        
        Example:
            encrypt_pin('123456')   -> b'$2b$12$...' (hashed bytes)
            encrypt_pin('12345')    -> Exception: Input Error: Wrong Pin Formatt
    '''
    if(not validate_pin(pin)):
        raise Exception('Input Error: Wrong Pin Formatt')
    
    return bcrypt.hashpw(pin.encode('utf-8'),bcrypt.gensalt())

def encrypt_password(password:str) -> str:
    '''
        encrypt a password using bcrypt hash and salt
        and return the hashed string if the format is valid
        
        Args:
            password    (str)   : the plain text password to encrypt
            
        Return: 
            String : the bcrypt hashed bytes of the password
        
        Raises:
            Exception : raised when the password does not match
                        the required format of minimum 8 characters
                        with uppercase, lowercase, digit, and special character
        
        Note:
            validates the password format before encrypting
            uses bcrypt gensalt() to generate a unique salt per call
            the same password will produce a different hash each time
        
        Example:
            encrypt_password('Password1!')  -> b'$2b$12$...' (hashed bytes)
            encrypt_password('weakpass')    -> Exception: Input Error: Wrong Password Format
    '''
    if(not validate_password(password)):
        raise Exception('Input Error: Wrong Password Format')
    
    return bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())