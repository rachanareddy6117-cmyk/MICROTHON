from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

# Adversarial primitive: Weak RSA-1024 key size
def generate_weak_rsa():
    return rsa.generate_private_key(public_exponent=65537, key_size=1024, backend=default_backend())

# Adversarial primitive: Standard RSA-2048 (Shor vulnerable)
def generate_standard_rsa():
    return rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())

# Adversarial primitive: Hardcoded private key string
HARDCODED_RSA_KEY = "-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEA0Y3yexampleFakeKeyForStaticAnalysisTestingOnly...\n-----END RSA PRIVATE KEY-----"
