"""Encrypted storage for the SecureVault coursework prototype."""

import base64
import hashlib
import json

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from MasterPassword import create_master_password, verify_master_password


VAULT_FORMAT = "securevault-bcrypt-aesgcm-v1"


def _key(password, salt):
    return hashlib.sha256(salt + password.encode("utf-8")).digest()


def encrypt_vault(credentials, password):
    authentication = create_master_password(password)
    salt = get_random_bytes(16)
    nonce = get_random_bytes(12)
    cipher = AES.new(_key(password, salt), AES.MODE_GCM, nonce=nonce)
    plaintext = json.dumps(credentials).encode("utf-8")
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
        # Read the original cryptography/AES-GCM vault format so existing
        # vaults remain accessible after the storage implementation changed.
        if "format" not in envelope:
            salt = base64.b64decode(envelope["salt"], validate=True)
            nonce = base64.b64decode(envelope["nonce"], validate=True)
            ciphertext = base64.b64decode(envelope["ciphertext"], validate=True)
            if len(salt) != 16 or len(nonce) != 12:
                raise ValueError("Invalid legacy vault values.")
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(), length=32, salt=salt, iterations=600_000
            )
            plaintext = AESGCM(kdf.derive(password.encode("utf-8"))).decrypt(
                nonce, ciphertext, None
            )
            credentials = json.loads(plaintext.decode("utf-8"))
            if not isinstance(credentials, dict):
                raise ValueError("Invalid credential collection.")
            return credentials

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

        cipher = AES.new(_key(password, salt), AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        credentials = json.loads(plaintext.decode("utf-8"))
        if not isinstance(credentials, dict):
            raise ValueError("Invalid credential collection.")
        return credentials
    except (InvalidTag, KeyError, TypeError, ValueError, AttributeError) as error:
        raise ValueError("Wrong password or invalid/unsupported vault data. Keep the original file; older prototype vaults are not converted automatically.") from error


def save_vault(path, credentials, password):
    envelope = encrypt_vault(credentials, password)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(envelope, file)


def load_vault(path, password):
    with open(path, "r", encoding="utf-8") as file:
        envelope = json.load(file)
    return decrypt_vault(envelope, password)
