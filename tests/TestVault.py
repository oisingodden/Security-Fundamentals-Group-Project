import base64
import json
import tempfile
import unittest
from pathlib import Path

from vault import decrypt_vault, encrypt_vault, load_vault, save_vault


class VaultTests(unittest.TestCase):
    def setUp(self):
        self.credentials = {
            "example.com": {"username": "alice", "password": "sample secret"}
        }
        self.password = "Sample master passphrase"

    def test_encrypt_decrypt_round_trip(self):
        envelope = encrypt_vault(self.credentials, self.password)
        self.assertNotIn("sample secret", json.dumps(envelope))
        self.assertEqual(decrypt_vault(envelope, self.password), self.credentials)

    def test_rejects_incorrect_password(self):
        envelope = encrypt_vault(self.credentials, self.password)
        with self.assertRaises(ValueError):
            decrypt_vault(envelope, "incorrect master password")

    def test_rejects_altered_ciphertext(self):
        envelope = encrypt_vault(self.credentials, self.password)
        raw = bytearray(base64.b64decode(envelope["ciphertext"]))
        raw[0] ^= 1
        envelope["ciphertext"] = base64.b64encode(raw).decode("ascii")
        with self.assertRaises(ValueError):
            decrypt_vault(envelope, self.password)

    def test_safe_file_round_trip_and_wrong_password(self):
        with tempfile.TemporaryDirectory(dir=".") as directory:
            path = Path(directory) / "credentials.vault"
            save_vault(path, self.credentials, self.password)
            self.assertEqual(load_vault(path, self.password), self.credentials)
            with self.assertRaises(ValueError):
                load_vault(path, "incorrect master password")


if __name__ == "__main__":
    unittest.main()
