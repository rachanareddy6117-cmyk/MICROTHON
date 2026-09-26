# Adversarial symmetric ciphers
CIPHER_SUITES = [
    "3DES",
    "RC4",
    "aes-128-cbc",  # Grover vulnerable (drops to ~64-bit security margin)
    "AES128",
    "aes-256-gcm"   # PQC resistant (128-bit quantum security margin)
]

def get_cipher():
    return "3DES"
