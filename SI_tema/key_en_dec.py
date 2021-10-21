from cryptography.fernet import Fernet

class Encrypt:
    def __init__(self, K1):
        self.K1 = K1

    def encrypt_key(self, message):
        f = Fernet(self.K1)
        encrypted_message = f.encrypt(message)
        return encrypted_message

    def decrypt_key(self, message):
        f = Fernet(self.K1)
        decrypted_message = f.decrypt(message)
        return decrypted_message
