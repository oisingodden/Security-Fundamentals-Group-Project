# Password Manager Application for NCI
# Ryan Farrell
# Oisin Godden
# Michael Flanagan

## Run the app

Install the dependencies, then start the command-line password manager:

```sh
python -m pip install -r requirements.txt
python app.py
```

On first run, create a master password of 14 or more characters. The app creates `passwords.vault` in the current folder. Later runs ask for the master password to open it. Use the menu to list, add, update, or delete saved credentials, generate a password, or change the master password. Keep the master password private; it cannot be recovered if lost.

## Master-password feature

Uses the Week 6 bcrypt calls: `gensalt()`, `hashpw()` and `checkpw()`.

### Setup

In the project folder on macOS/Linux:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Skip the first command if `.venv` already exists. On Windows use `py -m venv .venv`, then `.venv\Scripts\Activate.ps1` in PowerShell to activate it. Select the `.venv` interpreter in VS Code. The dependency is `bcrypt==5.0.0`.

Vault encryption also uses the `cryptography` package. `vault.py` encrypts JSON-compatible credentials with AES-GCM and derives its key from the master password using PBKDF2. It stores a bcrypt password check in the vault envelope; bcrypt verifies the master password, while PBKDF2 derives the encryption key. Use `save_vault(path, credentials, master_password)` and `load_vault(path, master_password)`. A wrong password or modified data raises `ValueError`. Keep vault files private and out of Git.

### Test

```sh
python -m tests.TestMasterPassword
python -m unittest tests.TestVault
```

Expected result: **6 out of 6 checks passed**.

### Functions for teammates

- `create_master_password(password)` returns `algorithm` and `password_hash` in a dictionary. Save both fields unchanged; bcrypt includes the salt in its hash.
- `verify_master_password(password, saved_details)` returns `True` or `False`.
- Creation requires at least 14 characters and at most 72 UTF-8 bytes. Invalid saved records are rejected.
- Old SHA-256 sample records must be recreated for this bcrypt version. The stored hash is for authentication, not an encryption key.

Use sample credentials while developing. Keep `.venv` and private vault files out of Git.
