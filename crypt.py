import hashlib
import secrets

class CryptoTool:
    @staticmethod
    def hash_password(password):
        salt = secrets.token_hex(16)
        combined = password + salt
        hashed = hashlib.sha256(combined.encode()).hexdigest()
        return f"{salt}:{hashed}"

    @staticmethod
    def verify_password(password, stored_hash):
        salt, hashed = stored_hash.split(":")
        combined = password + salt
        check_hash = hashlib.sha256(combined.encode()).hexdigest()
        return secrets.compare_digest(hashed, check_hash)

    @staticmethod
    def generate_token(length=32):
        return secrets.token_urlsafe(length)
