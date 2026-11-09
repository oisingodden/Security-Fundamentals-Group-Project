# Password Manager Application for NCI
# Ryan Farrell
# Oisin Godden
# Michael Flanagan

## Master-password feature

Uses the Week 6 bcrypt calls: `gensalt()`, `hashpw()` and `checkpw()`.

### Setup

Install Python 3 and open a terminal in the project folder. Each teammate creates their own `.venv`; do not copy an environment between Windows and macOS.

#### Windows PowerShell

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If `py` is unavailable but `python --version` reports Python 3, use `python -m venv .venv` for the first command. Skip environment creation if this project's `.venv` already exists.

If PowerShell blocks the activation script, use the environment's Python directly, without changing execution-policy settings:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m tests.TestMasterPassword
```

#### Windows Command Prompt

```bat
py -3 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
```

Skip the first command if the environment already exists. Choose either the PowerShell or Command Prompt instructions, according to the terminal you use.

#### macOS or Linux

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Skip the first command if the environment already exists.

#### VS Code

Use **Python: Select Interpreter** in the Command Palette and select the interpreter inside `.venv`:

- Windows: `.venv\Scripts\python.exe`
- macOS/Linux: `.venv/bin/python`

Open a new terminal after selecting it. The dependency is `bcrypt==5.0.0`, installed from `requirements.txt`.

The environment commands follow the [Python virtual-environment documentation](https://docs.python.org/3/library/venv.html).

### Test

With the environment activated, run this from the project folder on either Windows or macOS/Linux:

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
