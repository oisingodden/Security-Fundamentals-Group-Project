"""Basic encrypted vault storage."""

import base64
import json
import os
from pathlib import Path

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


def _key(password, salt):
    """Turn the master password into a 256-bit encryption key."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt, iterations=600_000
    )
    return kdf.derive(password.encode("utf-8"))


def encrypt_vault(credentials, password):
    """Encrypt credentials and return an envelope that can be saved as JSON."""
    salt = os.urandom(16)
    nonce = os.urandom(12)
    plaintext = json.dumps(credentials).encode("utf-8")
    ciphertext = AESGCM(_key(password, salt)).encrypt(nonce, plaintext, None)

    return {
        "salt": base64.b64encode(salt).decode("ascii"),
        "nonce": base64.b64encode(nonce).decode("ascii"),
        "ciphertext": base64.b64encode(ciphertext).decode("ascii"),
    }


def decrypt_vault(envelope, password):
    """Decrypt an envelope; reject wrong passwords and modified data."""
    try:
        salt = base64.b64decode(envelope["salt"], validate=True)
        nonce = base64.b64decode(envelope["nonce"], validate=True)
        ciphertext = base64.b64decode(envelope["ciphertext"], validate=True)
        plaintext = AESGCM(_key(password, salt)).decrypt(nonce, ciphertext, None)
        return json.loads(plaintext.decode("utf-8"))
    except (InvalidTag, KeyError, TypeError, ValueError) as error:
        raise ValueError("Wrong password or invalid vault data.") from error


def save_vault(path, credentials, password):
    """Encrypt credentials and write the vault file."""
    Path(path).write_text(
        json.dumps(encrypt_vault(credentials, password)), encoding="utf-8"
    )


def load_vault(path, password):
    """Read and decrypt a vault file."""
    envelope = json.loads(Path(path).read_text(encoding="utf-8"))
    return decrypt_vault(envelope, password)
