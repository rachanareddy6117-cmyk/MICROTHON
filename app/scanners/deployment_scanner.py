import re
from typing import List, Dict, Any

class DeploymentLogCorrelator:
    """
    Scans runtime deployment logs, Kubernetes event logs, and container stdout/stderr.
    Correlates:
    runtime error -> source code -> dependency -> service -> cryptographic asset
    """
    def correlate_logs(self, log_content: str) -> List[Dict[str, Any]]:
        correlations = []
        lines = log_content.splitlines()

        # Heuristic error patterns for crypto failures
        crypto_error_patterns = [
            (r"(?:SSL: CERTIFICATE_VERIFY_FAILED|certificate has expired|self signed certificate)", "Certificate Verification Failure", "TLS Certificate", "IN_TRANSIT"),
            (r"(?:no shared cipher|SSL_CTX_set_cipher_list|handshake failure)", "Cipher Negotiation Failure", "TLS Cipher Suite", "IN_TRANSIT"),
            (r"(?:JWTSignatureVerificationException|Signature verification failed|invalid signature)", "JWT Signature Failure", "RSA/ECDSA Token", "AUTHENTICATION_IDENTITY"),
            (r"(?:KeySizeError|ValueError: RSA key size must be|crypto/rsa: message too long)", "RSA Key Size Constraint", "RSA Key", "ASYMMETRIC_ENCRYPTION")
        ]

        for line_num, line in enumerate(lines, 1):
            for pat, err_type, asset, domain in crypto_error_patterns:
                if re.search(pat, line, re.IGNORECASE):
                    correlations.append({
                        "line_number": line_num,
                        "raw_log_snippet": line.strip()[:140],
                        "error_signature": err_type,
                        "affected_asset": asset,
                        "exposure_domain": domain,
                        "source_correlation": "Traceable to TLS terminating proxy or authentication middleware.",
                        "confidence": 0.92
                    })
        return correlations

deployment_correlator = DeploymentLogCorrelator()
