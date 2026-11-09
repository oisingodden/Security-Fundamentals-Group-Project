import json
import tempfile
import unittest
from pathlib import Path

from MasterPassword import verify_master_password
from vault import decrypt_vault, encrypt_vault, load_vault, save_vault


class VaultTests(unittest.TestCase):
    def setUp(self):
        self.credentials = {
            "example.com": {"username": "alice", "password": "sample secret"}
        }
        self.password = "Sample master passphrase"
        self.unsupported_envelope = {'salt': 'MDEyMzQ1Njc4OWFiY2RlZg==', 'nonce': 'MDEyMzQ1Njc4OWFi', 'ciphertext': '7jrTRuvvpYSOEqOCvfuDNnfFRv3PxKlrjxtPwqiePap22xTAGSsQdQizUIUirr7GVSDxXvdttA+1aycLGGxQ3JDHAUDCZIRmCHJVAQDYSq+pU9s='}

    def test_encrypt_decrypt_round_trip(self):
        envelope = encrypt_vault(self.credentials, self.password)
        self.assertNotIn("sample secret", json.dumps(envelope))
        self.assertEqual(decrypt_vault(envelope, self.password), self.credentials)

    def test_bcrypt_record_is_saved_and_used(self):
        envelope = encrypt_vault(self.credentials, self.password)
        self.assertEqual(envelope["authentication"]["algorithm"], "bcrypt")
        self.assertTrue(verify_master_password(self.password, envelope["authentication"]))
        envelope["authentication"]["password_hash"] = "damaged hash"
        with self.assertRaises(ValueError):
            decrypt_vault(envelope, self.password)

    def test_rejects_incorrect_password(self):
        envelope = encrypt_vault(self.credentials, self.password)
        with self.assertRaises(ValueError):
            decrypt_vault(envelope, "incorrect master password")

    def test_rejects_altered_ciphertext(self):
        envelope = encrypt_vault(self.credentials, self.password)
        first = "0" if envelope["ciphertext"][0] != "0" else "1"
        envelope["ciphertext"] = first + envelope["ciphertext"][1:]
        with self.assertRaises(ValueError):
            decrypt_vault(envelope, self.password)

    def test_rejects_altered_tag(self):
        envelope = encrypt_vault(self.credentials, self.password)
        first = "0" if envelope["tag"][0] != "0" else "1"
        envelope["tag"] = first + envelope["tag"][1:]
        with self.assertRaises(ValueError):
            decrypt_vault(envelope, self.password)

    def test_safe_file_round_trip_and_wrong_password(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "credentials.vault"
            save_vault(path, self.credentials, self.password)
            self.assertEqual(load_vault(path, self.password), self.credentials)
            with self.assertRaises(ValueError):
                load_vault(path, "incorrect master password")

    def test_changed_master_password(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "credentials.vault"
            save_vault(path, self.credentials, self.password)
            contents = load_vault(path, self.password)
            new_password = "Different sample master passphrase"
            save_vault(path, contents, new_password)
            self.assertEqual(load_vault(path, new_password), self.credentials)
            with self.assertRaises(ValueError):
                load_vault(path, self.password)

    def test_unsupported_file_is_not_modified(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "old.vault"
            path.write_text(json.dumps(self.unsupported_envelope), encoding="utf-8")
            original = path.read_bytes()
            with self.assertRaises(ValueError):
                load_vault(path, self.password)
            self.assertEqual(path.read_bytes(), original)

    def test_old_or_damaged_formats_are_rejected(self):
        for envelope in ({}, {"format": "old-format"}):
            with self.assertRaises(ValueError):
                decrypt_vault(envelope, self.password)


if _name_ == "_main_":
    unittest.main()