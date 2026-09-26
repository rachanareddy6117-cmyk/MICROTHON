import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class HandshakeMetadata(BaseModel):
    client_ip: str = "127.0.0.1"
    endpoint: str = "/api/v1/checkout"
    tls_version: str = "TLSv1.3"  # TLSv1.0, TLSv1.1, TLSv1.2, TLSv1.3
    cipher_suite: str = "TLS_AES_256_GCM_SHA384"
    public_key_algorithm: str = "RSA"
    public_key_bits: int = 2048
    cert_signature_algorithm: str = "sha256WithRSAEncryption"
    crypto_provider: str = "OpenSSL_3_2"
    has_downgrade_indicator: bool = False

class CryptoFirewallDecisionEngine:
    """
    Defensive Crypto Policy Enforcement Gateway decision engine.
    Uses mature standard components for low-level TLS (Envoy, OpenSSL, OPA)
    and implements the custom cryptographic decision layer:
    - Evaluates TLS version, cipher suite, key sizes, signatures, and downgrade indicators
    - Returns ALLOW, MONITOR, WARN, REVIEW, BLOCK
    - Fail-safe default: secures boundaries without indiscriminate downtime
    """
    def __init__(self, policy_manager):
        self.policy_manager = policy_manager
        self.events_history: List[Dict[str, Any]] = []

    def evaluate_handshake(self, meta: HandshakeMetadata) -> Dict[str, Any]:
        policy = self.policy_manager.get_active_policy()
        exceptions = self.policy_manager.get_active_exceptions(meta.endpoint)

        decision = "ALLOW"
        matched_rule = "Default Baseline"
        reasons = []

        # 1. Check active temporary exceptions first
        for exc in exceptions:
            if exc["allowed_cipher_or_algo"].upper() in meta.cipher_suite.upper():
                decision = "MONITOR"
                matched_rule = f"Exception: {exc['business_justification'][:40]}"
                reasons.append("Handshake allowed under active temporary security exception.")
                break

        if decision != "MONITOR":
            # 2. TLS Version Checks
            if meta.tls_version in ["TLSv1.0", "TLSv1.1", "SSLv3"]:
                decision = "BLOCK"
                matched_rule = "Rule: Block Deprecated TLS Protocols"
                reasons.append(f"Forbidden legacy protocol: {meta.tls_version}. Minimum required is {policy['minimum_tls']}.")
            
            # 3. Downgrade Indicator Check
            elif meta.has_downgrade_indicator:
                decision = "BLOCK"
                matched_rule = "Rule: Prevent Cryptographic Downgrade Attack"
                reasons.append("TLS handshake contains client downgrade sentinel indicators.")

            # 4. SHA-1 Signature Check
            elif "SHA1" in meta.cert_signature_algorithm.upper() or "MD5" in meta.cert_signature_algorithm.upper():
                decision = "BLOCK"
                matched_rule = "Rule: Reject Deprecated Certificate Signatures"
                reasons.append(f"Certificate uses broken signature hash: {meta.cert_signature_algorithm}.")

            # 5. Weak Key Size Check
            elif meta.public_key_algorithm == "RSA" and meta.public_key_bits < policy["minimum_rsa_key_size"]:
                decision = "BLOCK"
                matched_rule = "Rule: Enforce Minimum RSA Key Length"
                reasons.append(f"RSA key size {meta.public_key_bits} bits is below policy minimum {policy['minimum_rsa_key_size']}.")

            # 6. Blocked Algorithms Check
            elif any(blocked in meta.cipher_suite.upper() for blocked in policy.get("blocked_algorithms", [])):
                decision = "BLOCK"
                matched_rule = "Rule: Block Insecure Ciphers"
                reasons.append("Cipher suite contains prohibited algorithm (e.g. 3DES, RC4, NULL).")

            # 7. Classical Asymmetric Warning for HNDL
            elif policy.get("pqc_policy") == "PQC_MANDATORY" and "KYBER" not in meta.cipher_suite.upper() and "ML-KEM" not in meta.cipher_suite.upper():
                decision = "REVIEW"
                matched_rule = "Rule: Post-Quantum Mandatory Enforcement"
                reasons.append("Endpoint mandates PQC/Hybrid key encapsulation.")

            elif "ECDHE" in meta.cipher_suite.upper() or "RSA" in meta.cipher_suite.upper():
                decision = "WARN"
                matched_rule = "Rule: Quantum-Vulnerable Key Exchange Monitoring"
                reasons.append("Handshake completed using classical key exchange vulnerable to Shor's algorithm (HNDL risk).")

        event = {
            "event_id": f"FW-{uuid.uuid4().hex[:8].upper()}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "client_ip": meta.client_ip,
            "endpoint": meta.endpoint,
            "tls_version": meta.tls_version,
            "cipher_suite": meta.cipher_suite,
            "decision": decision,
            "rule_matched": matched_rule,
            "reasons": reasons,
            "telemetry_metadata": meta.model_dump()
        }
        self.events_history.append(event)
        if len(self.events_history) > 1000:
            self.events_history.pop(0)

        return event
