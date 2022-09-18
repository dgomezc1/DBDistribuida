import hashlib

def key_encryption(key: str):
    encrypted = hashlib.sha1(key.encode()).hexdigest()
    return {
        "key": encrypted,
        "n": int(encrypted, 16)
    }