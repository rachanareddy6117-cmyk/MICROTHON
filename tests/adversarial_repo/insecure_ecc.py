from cryptography.hazmat.primitives.asymmetric import ec

# Adversarial primitive: ECDSA with Bitcoin curve secp256k1 (vulnerable to Shor's ECDLP)
def create_ecdsa_key():
    return ec.generate_private_key(ec.SECP256K1())

# Adversarial primitive: ECDH Key Exchange
def compute_ecdh_shared(private_key, peer_public_key):
    return private_key.exchange(ec.ECDH(), peer_public_key)

# Dynamic algorithm resolution wrapper
def dynamic_crypto_wrapper(algo_name="rsa"):
    if algo_name == "rsa":
        return generate_standard_rsa()
