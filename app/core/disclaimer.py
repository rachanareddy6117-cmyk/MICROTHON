"""
Epistemic Humility & Risk Communication Framework.
Never claims the scan 'proves' quantum safety.
"""

LIMITATIONS_DISCLOSURE = {
    "warning_banner": "CRITICAL NOTICE: STATIC CRYPTOGRAPHIC AUDITING DOES NOT CONSTITUTE A PROOF OF QUANTUM SECURITY.",
    "statement": (
        "PQC-Migrate performs static pattern matching, abstract syntax tree (AST) inspection, and artifact "
        "parsing across codebases, configurations, and certificates. Under no circumstances should clean scan "
        "results be interpreted as an operational guarantee of quantum immunity. Cryptographic security is a "
        "continuous risk-communication and agility problem, not a one-time static proof."
    ),
    "blind_spots": [
        {
            "name": "Dynamic Runtime Key Loading",
            "description": "Keys fetched at runtime from Cloud KMS (AWS KMS, GCP KMS), HashiCorp Vault, or hardware HSMs cannot be verified statically."
        },
        {
            "name": "Transit Intermediaries & Cloud SaaS",
            "description": "Traffic traversing external CDNs, third-party payment gateways, or SaaS providers may negotiate legacy cipher suites unseen in source."
        },
        {
            "name": "Harvest Now, Decrypt Later (HNDL) Asymmetry",
            "description": "Historical network traffic already intercepted by adversaries will remain vulnerable to retrospective decryption when a CRQC is built."
        },
        {
            "name": "Side-Channel & Implementation Vulnerabilities",
            "description": "Post-quantum algorithms (ML-KEM, ML-DSA) remain susceptible to power analysis, cache timing, and memory corruption bugs in specific libraries."
        }
    ]
}

EPISTEMIC_GUIDELINES = [
    "Never label any codebase '100% Quantum Proof'.",
    "Communicate findings via 'Quantum Exposure Horizon' and 'Blast Radius'.",
    "Prioritize Cryptographic Agility and loose coupling over hardcoded patches.",
    "Enforce hybrid dual-mode migration (e.g. X25519 + ML-KEM-768) as the gold standard."
]
