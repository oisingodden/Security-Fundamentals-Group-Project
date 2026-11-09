import hashlib
import secrets
import hmac


def create_master_password(password):
    # Check the minimum password length.
    if len(password) < 14:
        raise ValueError("Use at least 14 characters.")

    # Generate a random salt.
    salt = secrets.token_bytes(16)

    # Hash the salt and password together using SHA-256.
    password_hash = hashlib.sha256(
        salt + password.encode("utf-8")
    ).hexdigest()

    # Return verification details without the original password.
    return {
        "algorithm": "sha256",
        "salt": salt.hex(),
        "password_hash": password_hash
    }


def verify_master_password(password, saved_details):
    # Convert the stored salt back into bytes.
    salt = bytes.fromhex(saved_details["salt"])

    # Repeat the calculation using the original salt.
    entered_hash = hashlib.sha256(
        salt + password.encode("utf-8")
    ).hexdigest()

    # Check whether the hashes match.
    return hmac.compare_digest(
        entered_hash,
        saved_details["password_hash"]
    )


if __name__ == "__main__":
    details = create_master_password(
        "Sample passphrase for testing"
    )

    print(
        "Correct password accepted:",
        verify_master_password(
            "Sample passphrase for testing",
            details
        )
    )

    print(
        "Incorrect password accepted:",
        verify_master_password(
            "This is the wrong password",
            details
        )
    )
