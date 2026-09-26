from typing import List, Dict, Any

class PolicyRecommendationEngine:
    """
    AI-Assisted Policy Recommendation Generator.
    Analyzes observed TLS telemetry over time and recommends fine-tuned policy adjustments.
    """
    def generate_recommendations(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        recs = []
        if not events:
            return [{
                "title": "Baseline Hybrid Post-Quantum Enforcement",
                "recommended_action": "Enable Hybrid X25519+ML-KEM-768 for TLS 1.3 ingress",
                "rationale": "Protects against Harvest Now, Decrypt Later (HNDL) without breaking classical clients.",
                "confidence": 0.96
            }]

        blocked_count = sum(1 for e in events if e.get("decision") == "BLOCK")
        tls10_count = sum(1 for e in events if e.get("tls_version") in ["TLSv1.0", "TLSv1.1"])

        if tls10_count > 0:
            recs.append({
                "title": "Sunset Deprecated TLS 1.0/1.1 Gateways",
                "recommended_action": "Transition legacy client endpoints to mTLS proxies with modern TLS 1.3.",
                "rationale": f"Observed {tls10_count} legacy handshakes subject to POODLE/BEAST and quantum capture.",
                "confidence": 0.99
            })

        recs.append({
            "title": "Transition RSA Cipher Suites to ECDSA / ML-DSA",
            "recommended_action": "Update allowed_ciphers to favor ECDHE-ECDSA or PQC hybrid suites over RSA key exchange.",
            "rationale": "Decreases handshake blast radius and eliminates RSA modulus exposure.",
            "confidence": 0.93
        })

        return recs

recommendation_engine = PolicyRecommendationEngine()
