import hashlib

def hash_data(data: bytes):
    # Adversarial primitive: MD5
    m = hashlib.md5(data).hexdigest()
    # Adversarial primitive: SHA-1
    s = hashlib.sha1(data).hexdigest()
    # PQC-Resistant hash: SHA-256
    s256 = hashlib.sha256(data).hexdigest()
    return m, s, s256
