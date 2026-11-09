# Password Manager Application for NCI
# Ryan Farrell
# Oisin Godden
# Michael Flanagan

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

### Test

```sh
python -m tests.TestMasterPassword
```

Expected result: **6 out of 6 checks passed**.

### Functions for teammates

- `create_master_password(password)` returns `algorithm` and `password_hash` in a dictionary. Save both fields unchanged; bcrypt includes the salt in its hash.
- `verify_master_password(password, saved_details)` returns `True` or `False`.
- Creation requires at least 14 characters and at most 72 UTF-8 bytes. Invalid saved records are rejected.
- Old SHA-256 sample records must be recreated for this bcrypt version. The stored hash is for authentication, not an encryption key.

Use sample credentials while developing. Keep `.venv` and private vault files out of Git.
