from MasterPassword import (
    create_master_password,
    verify_master_password
)


def main():
    password = "Sample passphrase for testing"
    details = create_master_password(password)
    failures = 0

    # Check 1: The correct password should be accepted.
    if verify_master_password(password, details):
        print("PASS: Correct password accepted")
    else:
        print("FAIL: Correct password rejected")
        failures += 1

    # Check 2: An incorrect password should be rejected.
    if not verify_master_password("Wrong password", details):
        print("PASS: Incorrect password rejected")
    else:
        print("FAIL: Incorrect password accepted")
        failures += 1

    # Check 3: A short password should cause an error.
    try:
        create_master_password("short")
        print("FAIL: Short password accepted")
        failures += 1
    except ValueError:
        print("PASS: Short password rejected")

    # Create the same password again to check the salt and resulting hash.
    second_details = create_master_password(password)

    # Check 4: Each new master password should get a different salt.
    if details["salt"] != second_details["salt"]:
        print("PASS: Different salts generated")
    else:
        print("FAIL: Salts are identical")
        failures += 1

    # Check 5: Different salts should produce different hashes here.
    if details["password_hash"] != second_details["password_hash"]:
        print("PASS: Different hashes generated")
    else:
        print("FAIL: Hashes are identical")
        failures += 1

    # Check 6: The returned values should not contain the original password.
    if password not in details.values():
        print("PASS: Original password not returned")
    else:
        print("FAIL: Original password was returned")
        failures += 1

    print("\nChecks passed:", 6 - failures, "out of 6")

    # Give the terminal an error result if any check failed.
    if failures > 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
