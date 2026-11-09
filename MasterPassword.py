<<<<<<< HEAD
import hashlib
import secrets
import hmac 

ITERATIONS = 600_000
=======
import bcrypt


def create_master_password(password):
    # Our project requires at least 14 characters.
    if len(password) < 14:
        raise ValueError("Use at least 14 characters.")

    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        raise ValueError("Use at most 72 UTF-8 bytes.")

    # Bcrypt stores the random salt inside the resulting hash.
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password_bytes, salt)

    return {
        "algorithm": "bcrypt",
        "password_hash": password_hash.decode("utf-8")
    }


def verify_master_password(password, saved_details):
    try:
        if saved_details["algorithm"] != "bcrypt":
            return False

        password_bytes = password.encode("utf-8")
        if len(password_bytes) > 72:
            return False

        stored_hash = saved_details["password_hash"].encode("utf-8")
        return bcrypt.checkpw(password_bytes, stored_hash)
    except (KeyError, ValueError, TypeError, AttributeError):
        # Missing or damaged saved details should not crash the app.
        return False


if __name__ == "__main__":
    password = "Sample passphrase for testing"
    details = create_master_password(password)
    print("Correct password accepted:", verify_master_password(password, details))
    print("Incorrect password accepted:", verify_master_password("Wrong password", details))
>>>>>>> 1275197566c1cbea75f26c538d24ea0dadc695ca
