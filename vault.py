import hashlib
import json

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from MasterPassword import create_master_password, verify_master_password


VAULT_FORMAT = "securevault-bcrypt-aesgcm-v1"


def _key(password, salt):
    # Prototype key construction, not a slow password-hardening method.
    return hashlib.sha256(salt + password.encode("utf-8")).digest()


def encrypt_vault(credentials, password):
    authentication = create_master_password(password)
    salt = get_random_bytes(16)
    nonce = get_random_bytes(12)
    key = _key(password, salt)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    plaintext = json.dumps(credentials).encode("utf-8")
    # The tag is used to check that encrypted data was not changed.
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)

    return {
        "format": VAULT_FORMAT,
        "authentication": authentication,
        "salt": salt.hex(),
        "nonce": nonce.hex(),
        "ciphertext": ciphertext.hex(),
        "tag": tag.hex()
    }


def decrypt_vault(envelope, password):
    try:
        if envelope["format"] != VAULT_FORMAT:
            raise ValueError("Unsupported vault format.")

        if not verify_master_password(password, envelope["authentication"]):
            raise ValueError("Master password did not match.")

        salt = bytes.fromhex(envelope["salt"])
        nonce = bytes.fromhex(envelope["nonce"])
        ciphertext = bytes.fromhex(envelope["ciphertext"])
        tag = bytes.fromhex(envelope["tag"])

        if len(salt) != 16 or len(nonce) != 12 or len(tag) != 16:
            raise ValueError("Invalid vault values.")

        key = _key(password, salt)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        credentials = json.loads(plaintext.decode("utf-8"))
        if not isinstance(credentials, dict):
            raise ValueError("Invalid credential collection.")
        return credentials
    except (KeyError, TypeError, ValueError, AttributeError):
        raise ValueError("Wrong password or invalid/unsupported vault data. Keep the original file; older prototype vaults are not converted automatically.")


def save_vault(path, credentials, password):
    envelope = encrypt_vault(credentials, password)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(envelope, file)


def load_vault(path, password):
    with open(path, "r", encoding="utf-8") as file:
        envelope = json.load(file)
    return decrypt_vault(envelope, password)