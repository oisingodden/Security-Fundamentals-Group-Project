import json
import tempfile
from pathlib import Path

from MasterPassword import verify_master_password
from vault import decrypt_vault, encrypt_vault, load_vault, save_vault


def main():
    credentials = {
        "example.com": {"username": "alice", "password": "sample secret"}
    }
    password = "Sample master passphrase"
    failures = 0

    # Check 1: Encrypt and decrypt the same credentials.
    envelope = encrypt_vault(credentials, password)
    restored = decrypt_vault(envelope, password)
    if restored == credentials and "sample secret" not in json.dumps(envelope):
        print("PASS: Credentials encrypted and decrypted")
    else:
        print("FAIL: Encryption or decryption was incorrect")
        failures = failures + 1

    # Check 2: The saved bcrypt record must be valid and used on opening.
    envelope = encrypt_vault(credentials, password)
    record_valid = verify_master_password(password, envelope["authentication"])
    envelope["authentication"]["password_hash"] = "damaged hash"
    try:
        decrypt_vault(envelope, password)
        print("FAIL: Damaged bcrypt record accepted")
        failures = failures + 1
    except ValueError:
        if record_valid:
            print("PASS: Bcrypt record saved and checked")
        else:
            print("FAIL: Original bcrypt record was invalid")
            failures = failures + 1

    # Check 3: Reject the wrong master password.
    envelope = encrypt_vault(credentials, password)
    try:
        decrypt_vault(envelope, "Wrong sample master password")
        print("FAIL: Wrong master password accepted")
        failures = failures + 1
    except ValueError:
        print("PASS: Wrong master password rejected")

    # Check 4: Change one character of the ciphertext.
    envelope = encrypt_vault(credentials, password)
    if envelope["ciphertext"][0] == "0":
        first = "1"
    else:
        first = "0"
    envelope["ciphertext"] = first + envelope["ciphertext"][1:]
    try:
        decrypt_vault(envelope, password)
        print("FAIL: Changed ciphertext accepted")
        failures = failures + 1
    except ValueError:
        print("PASS: Changed ciphertext rejected")

    # Check 5: Change one character of the authentication tag.
    envelope = encrypt_vault(credentials, password)
    if envelope["tag"][0] == "0":
        first = "1"
    else:
        first = "0"
    envelope["tag"] = first + envelope["tag"][1:]
    try:
        decrypt_vault(envelope, password)
        print("FAIL: Changed tag accepted")
        failures = failures + 1
    except ValueError:
        print("PASS: Changed tag rejected")

    # Use a temporary folder so tests cannot change the user's own vault.
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "sample.vault"

        # Check 6: Save and reopen a file, then reject a wrong password.
        save_vault(path, credentials, password)
        restored = load_vault(path, password)
        try:
            load_vault(path, "Wrong sample master password")
            print("FAIL: Saved file opened with a wrong password")
            failures = failures + 1
        except ValueError:
            if restored == credentials:
                print("PASS: File saved and reopened correctly")
            else:
                print("FAIL: Saved credentials were not restored")
                failures = failures + 1

        # Check 7: Re-encrypt with a new master password.
        new_password = "Different sample master passphrase"
        save_vault(path, credentials, new_password)
        restored = load_vault(path, new_password)
        try:
            load_vault(path, password)
            print("FAIL: Old master password still accepted")
            failures = failures + 1
        except ValueError:
            if restored == credentials:
                print("PASS: New master password works and old one fails")
            else:
                print("FAIL: Credentials changed during password change")
                failures = failures + 1

        # Check 8: Reject an unsupported file without modifying it.
        with open(path, "w", encoding="utf-8") as file:
            json.dump({"format": "old-format"}, file)
        with open(path, "r", encoding="utf-8") as file:
            original = file.read()
        try:
            load_vault(path, password)
            print("FAIL: Unsupported file accepted")
            failures = failures + 1
        except ValueError:
            with open(path, "r", encoding="utf-8") as file:
                unchanged = file.read()
            if original == unchanged:
                print("PASS: Unsupported file rejected without changing it")
            else:
                print("FAIL: Unsupported file was changed")
                failures = failures + 1

    # Check 9: Reject empty and unsupported records.
    all_rejected = True
    for invalid_record in [{}, {"format": "old-format"}]:
        try:
            decrypt_vault(invalid_record, password)
            all_rejected = False
        except ValueError:
            pass
    if all_rejected:
        print("PASS: Empty and unsupported records rejected")
    else:
        print("FAIL: Invalid record accepted")
        failures = failures + 1

    print("\nChecks passed:", 9 - failures, "out of 9")
    if failures > 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
