# SecureVault

NCI Security Fundamentals & Development CA1 group project.

Group members: Ryan Farrell, Oisin Godden and Michael Flanagan.

## Features

- Create and open a password vault using a master password.
- Add, view, update and delete saved credentials.
- Generate passwords and display strength advice.
- Change the master password.

The app runs in the terminal. It uses bcrypt for master-password verification and AES-GCM for encrypted storage.

## Setup and run

Install Python 3, open the project folder in VS Code and open a terminal.

### Windows PowerShell

```powershell
python -m pip install -r requirements.txt
python app.py
```

### Mac or Linux

```sh
# Skip this command if .venv already exists.
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python app.py
```

`requirements.txt` installs bcrypt and PyCryptodome.

On first run, choose and confirm a master password of at least 14 characters. The app saves entries in `passwords.vault`. Run `app.py` again to reopen it. There is no reset if you forget the master password.

## Tests

Run these from the main project folder.

Windows PowerShell:

```powershell
python -m tests.TestMasterPassword
python -m tests.TestVault
```

Mac or Linux:

```sh
.venv/bin/python -m tests.TestMasterPassword
.venv/bin/python -m tests.TestVault
```

Expected results: 6 authentication checks and 9 vault checks pass.

## Notes

This is a coursework prototype. Use sample credentials only. Keep vault files and `.venv` out of Git.

Older prototype vault formats are not supported. Keep a backup of old files rather than deleting them.
