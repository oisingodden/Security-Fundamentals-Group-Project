from MasterPassword import create_master_password, verify_master_password


def main():
    password = "Sample passphrase for testing"
    details = create_master_password(password)
    failures = 0

    # Check 1: Accept the correct password.
    if verify_master_password(password, details):
        print("PASS: Correct password accepted")
    else:
        print("FAIL: Correct password rejected")
        failures = failures + 1

    # Check 2: Reject an incorrect password.
    if not verify_master_password("Wrong password", details):
        print("PASS: Incorrect password rejected")
    else:
        print("FAIL: Incorrect password accepted")
        failures = failures + 1

    # Check 3: Reject a short password when creating a record.
    try:
        create_master_password("short")
        print("FAIL: Short password accepted")
        failures = failures + 1
    except ValueError:
        print("PASS: Short password rejected")

    # Check 4: The same password gets different randomly salted hashes.
    second_details = create_master_password(password)
    if details["password_hash"] != second_details["password_hash"]:
        print("PASS: Different hashes generated")
    else:
        print("FAIL: Hashes are identical")
        failures = failures + 1

    # Check 5: Reject a password longer than bcrypt's 72-byte limit.
    try:
        create_master_password("a" * 73)
        print("FAIL: Overlong password accepted")
        failures = failures + 1
    except ValueError:
        print("PASS: Overlong password rejected")

    # Check 6: Reject a damaged hash without crashing.
    invalid_details = {"algorithm": "bcrypt", "password_hash": "invalid hash"}
    if not verify_master_password(password, invalid_details):
        print("PASS: Invalid saved details rejected")
    else:
        print("FAIL: Invalid saved details accepted")
        failures = failures + 1

    print("\nChecks passed:", 6 - failures, "out of 6")
    if failures > 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
