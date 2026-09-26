"""
Authoritative NIST Post-Quantum Cryptography (PQC) Standards Catalog (Aug 2024 Final Standards):
- FIPS 203: ML-KEM (Module-Lattice-based Key-Encapsulation Mechanism / CRYSTALS-Kyber)
- FIPS 204: ML-DSA (Module-Lattice-based Digital Signature Algorithm / CRYSTALS-Dilithium)
- FIPS 205: SLH-DSA (Stateless Hash-based Digital Signature Algorithm / SPHINCS+)
- RFC 8554 / RFC 8391: LMS / XMSS (Stateful Hash-Based Signatures)
"""

NIST_STANDARDS_CATALOG = {
    "FIPS_203": {
        "name": "ML-KEM",
        "standard": "NIST FIPS 203",
        "parameter_sets": ["ML-KEM-512", "ML-KEM-768", "ML-KEM-1024"],
        "recommended": "ML-KEM-768",
        "use_case": "General Key Exchange & Public Key Encryption",
        "replaces": ["RSA-2048", "RSA-4096", "ECDH", "DH", "X25519"]
    },
    "FIPS_204": {
        "name": "ML-DSA",
        "standard": "NIST FIPS 204",
        "parameter_sets": ["ML-DSA-44", "ML-DSA-65", "ML-DSA-87"],
        "recommended": "ML-DSA-65",
        "use_case": "General Digital Signatures & Public Key Authentication",
        "replaces": ["RSA PKCS#1v1.5/PSS", "ECDSA (P-256, secp256k1)", "Ed25519", "DSA"]
    },
    "FIPS_205": {
        "name": "SLH-DSA",
        "standard": "NIST FIPS 205",
        "parameter_sets": ["SLH-DSA-SHA2-128s", "SLH-DSA-SHAKE-128s", "SLH-DSA-SHA2-256s"],
        "recommended": "SLH-DSA-SHA2-128s",
        "use_case": "Stateless Hash-Based Signatures (Conservative root PKI & firmware)",
        "replaces": ["RSA Root CA Signatures", "Long-term archive code signing"]
    }
}

def get_nist_recommendation(algorithm: str) -> dict:
    algo_up = algorithm.upper()
    if any(k in algo_up for k in ["RSA", "ECDSA", "ED25519", "DSA", "SIGN"]):
        return {
            "primary": "FIPS 204: ML-DSA-65",
            "conservative": "FIPS 205: SLH-DSA-SHA2-128s",
            "hybrid": "Composite Classical + ML-DSA-65 (Dual Signature)",
            "signature_expansion_warning": "ML-DSA-65 signature is 3,309 bytes (13x larger than RSA-2048)."
        }
    elif any(k in algo_up for k in ["ECDH", "DH", "X25519", "KEM", "EXCHANGE"]):
        return {
            "primary": "FIPS 203: ML-KEM-768",
            "hybrid": "Hybrid X25519 + ML-KEM-768 (X25519Kyber768 draft)",
            "key_expansion_warning": "ML-KEM-768 ciphertext is 1,088 bytes."
        }
    elif "128" in algo_up and "AES" in algo_up:
        return {
            "primary": "AES-256-GCM",
            "hybrid": "AES-256-GCM or ChaCha20-Poly1305",
            "key_expansion_warning": "Upgrade key length from 128 to 256 bits to preserve 128-bit quantum security."
        }
    return {
        "primary": "FIPS 203 (ML-KEM-768) or FIPS 204 (ML-DSA-65)",
        "hybrid": "Hybrid Classical + Post-Quantum scheme",
        "key_expansion_warning": "Verify network buffer and header limits."
    }
