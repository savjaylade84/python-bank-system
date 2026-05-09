import re
import bcrypt
password_regex = re.compile('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
def validate_password(password:str) -> bool:
    
    if(password_regex.search(password)):
        return True
    
    return False

def encrypt_password(password:str) -> str:

    if(not validate_password(password)):
        raise Exception('Input Error: Wrong Password Format')
    
    return bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

print(encrypt_password("Deleon@231999"))