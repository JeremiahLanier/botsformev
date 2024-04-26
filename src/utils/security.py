from cryptography.fernet import Fernet


class SecurityManager:
    def __init__(self, key):
        self.cipher_suite = Fernet(key)

    def encrypt(self, message):
        """Encrypt a message."""
        return self.cipher_suite.encrypt(message.encode())

    def decrypt(self, token):
        """Decrypt a token."""
        return self.cipher_suite.decrypt(token).decode()
