# TODO

## TODO file location

- ./TODO.md
- ./tests/TODO.md

---

## [  ] Unfinish - [x] Finish

---

### Admin Folder

- [x]  auth.py
  - [x]  login()
- [x]  menu.py
  - [x] get_menu_selection()
- [x]  services.py
  - [x] change_password()
  - [x] change_account_pin()
  - [x] delete_account()
  - [x] ai_analysis()  
- [x]  view.py
  - [x]  account_list()
  - [x]  account_info()
  - [x]  account_history()
  - [x]  edited_account_history()
  - [x]  account_infos()

---

### Account Folder

- [x] auth.py
  - [x] login()
  - [x] signup()
- [ ] IAccount.py
- [ ] ITransaction.py
- [x] menu.py
  - [x] get_menu_selection()
- [x] services.py
  - [x] deposite()
  - [x] withdraw()
  - [x] change_pin
  - [x] save() - remove
- [ ] Transaction.py
- [ ] view.py
  - [x] balance()
  - [ ] transaction_history()
  - [x] print_account_info()

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
  - [x] remove Print class
  - [ ] remove string_config class
- [x] credentials.py
- [x] models.py
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
- [ ] update the tests list
