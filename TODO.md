# TODO

---

## [  ] Unfinish - [x] Finish

---

### Admin Folder

- [ ]  auth.py
  - [ ]  login()
- [x]  menu.py
  - [x] get_menu_selection()
- [ ]  services.py
  - [x] change_password()
  - [x] change_account_pin()
  - [ ] delete_account()
  - [ ] ai_analysis()  
- [ ]  view.py
  - [ ]  account_list()
  - [ ]  account_info()
  - [ ]  account_history()
  - [ ]  edited_account_history()
  - [ ]  account_infors()

---

### Account Folder

- [ ] auth.py
  - [ ] login()
  - [ ] signup()
- [ ] IAccount.py
- [ ] ITransaction.py
- [ ] menu.py
  - [ ] get_menu_selection()
- [ ] services.py
  - [ ] deposite()
  - [ ] withdraw()
  - [ ] change_pin
  - [ ] save()
- [ ] Transaction.py
- [ ] view.py
  - [ ] balance()
  - [ ] transaction_history()
  - [ ] print_account_info()

---

### AccountVault Folder

- [x] FileManager.py
  - [x] _read_json()
  - [x] _write_json()
- [x] AdminManager.py
  - [x] AdminManager
    - [x] load_list()
    - [x] update_list()
    - [x] load_account_path()
    - [x] _remove_in_list()
- [x] AccountManager.py
  - [x] AccountManager
    - [x] load_account()
    - [x] find_by_id()
    - [x] find_all()
    - [x] load_path
    - [x] save()
    - [x] remove()
    - [x] exists()
- [x] config.py

---

### Utils Folder

- [ ] console.py
  - [x] print()
  - [x] status()
  - [x] divider()
  - [x] banner()
  - [x] label()
  - [x] entry()
  - [x] entries()
  - [x] list()
  - [x] prompt()
  - [x] prompt_pwd()
  - [x] menu()
  - [ ] remove Print class
  - [ ] remove string_config class
- [ ] credentials.py
- [ ] models.py
  - AccountType - (StrEnum)
  - TransactionStatus - (StrEnum)
  - DivConfig - (dataclass)
  - LabelEntry - (NamedTuple)

---

### Other

- [ ] remove the folder Operation
- [ ] migrate the code in the Operation
- [ ] migrate code of the admin.py
- [ ] migrate code of the Account.py
- [ ] restructure the folder, file, and code
- [ ] update the code of app.py
- [ ] update the code of bank_test.py
