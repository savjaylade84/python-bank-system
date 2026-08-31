from typing import Final
# Name of the folder where the account file sit in
VAULT_PATH:Final[str] = "AccountVault"

# the master list of account files in the folder
VAULT_LIST:Final[str] = "account-list.json"

# the file name of the master list
ACCOUNT_LIST:Final[str] = "Account-List"

# full path of the master list file
ACCOUNT_LIST_FILE:str = f"{VAULT_PATH}/{VAULT_LIST}"