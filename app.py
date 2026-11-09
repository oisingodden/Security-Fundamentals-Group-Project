"""Simple command-line password manager."""

import getpass
from pathlib import Path

from PasswordGenerator import generate_password
from vault import load_vault, save_vault


VAULT_FILE = Path("passwords.vault")


def open_vault():
    """Create a new vault or open the existing one."""
    if VAULT_FILE.exists():
        master_password = getpass.getpass("Master password: ")
        return master_password, load_vault(VAULT_FILE, master_password)

    print("Welcome! Create a master password (at least 14 characters).")
    while True:
        master_password = getpass.getpass("New master password: ")
        if len(master_password) < 14:
            print("Use at least 14 characters.")
            continue
        if len(master_password.encode("utf-8")) > 72:
            print("Use at most 72 UTF-8 bytes.")
            continue
        if master_password != getpass.getpass("Confirm master password: "):
            print("Passwords did not match. Try again.")
            continue
        save_vault(VAULT_FILE, {}, master_password)
        print(f"Created vault: {VAULT_FILE}")
        return master_password, {}


def run_menu(credentials, master_password):
    while True:
        print("\n1. List credentials")
        print("2. Add or update credential")
        print("3. Delete credential")
        print("4. Generate a password")
        print("5. Change master password")
        print("6. Quit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            if not credentials:
                print("Vault is empty.")
            else:
                for site, entry in sorted(credentials.items()):
                    print(f"\n{site}\n  Username: {entry['username']}\n  Password: {entry['password']}")

        elif choice == "2":
            site = input("Website or service: ").strip()
            if not site:
                print("A website or service name is required.")
                continue
            username = input("Username: ").strip()
            password = getpass.getpass("Password (leave blank to generate one): ")
            if not password:
                password = generate_password()
                print("Generated password:", password)
            credentials[site] = {"username": username, "password": password}
            save_vault(VAULT_FILE, credentials, master_password)
            print("Credential saved.")

        elif choice == "3":
            site = input("Website or service to delete: ").strip()
            if site in credentials:
                del credentials[site]
                save_vault(VAULT_FILE, credentials, master_password)
                print("Credential deleted.")
            else:
                print("No credential found for that name.")

        elif choice == "4":
            length_text = input("Password length (default 20): ").strip()
            try:
                length = int(length_text) if length_text else 20
                print("Generated password:", generate_password(length))
            except ValueError as error:
                print("Invalid length:", error)

        elif choice == "5":
            new_password = getpass.getpass("New master password: ")
            if len(new_password) < 14:
                print("Use at least 14 characters.")
                continue
            if len(new_password.encode("utf-8")) > 72:
                print("Use at most 72 UTF-8 bytes.")
                continue
            if new_password != getpass.getpass("Confirm new master password: "):
                print("Passwords did not match. Master password unchanged.")
                continue
            save_vault(VAULT_FILE, credentials, new_password)
            master_password = new_password
            print("Master password changed.")

        elif choice == "6":
            print("Vault closed.")
            return
        else:
            print("Choose a number from 1 to 6.")


def main():
    try:
        master_password, credentials = open_vault()
        if not isinstance(credentials, dict):
            print("Vault data is invalid. The vault was not changed.")
            return
        run_menu(credentials, master_password)
    except (ValueError, OSError) as error:
        print("Could not open or save the vault:", error)


if __name__ == "__main__":
    main()
