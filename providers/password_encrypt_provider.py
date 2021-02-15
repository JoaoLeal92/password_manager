import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class PasswordEncryptProvider:
    def __init__(self, salt, master_password):
        self.kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                              length=32,
                              salt=salt,
                              iterations=100000,
                              backend=default_backend())

        key = base64.urlsafe_b64encode(self.kdf.derive(master_password.encode()))
        self.fernet_key = Fernet(key)

    def encrypt_password(self, password):
        encrypted_password = self.fernet_key.encrypt(password.encode())
        return encrypted_password

    def decrypt_password(self, encrypted_password):
        decrypted_password = self.fernet_key.decrypt(encrypted_password)
        return decrypted_password.decode()
