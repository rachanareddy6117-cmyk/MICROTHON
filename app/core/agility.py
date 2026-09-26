from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class CryptoProviderInterface(ABC):
    @abstractmethod
    def get_provider_name(self) -> str:
        pass

    @abstractmethod
    def is_pqc_capable(self) -> bool:
        pass

class CryptoAgilityRegistry:
    """
    Central registry for cryptographic agility.
    Decouples algorithm callers from hardcoded underlying cryptographic providers.
    """
    def __init__(self):
        self._providers: Dict[str, Any] = {}
        self._default_kem = "ML-KEM-768"
        self._default_dsa = "ML-DSA-65"
        self._default_symmetric = "AES-256-GCM"

    def register_provider(self, name: str, provider: Any):
        self._providers[name] = provider

    def get_recommended_algorithms(self) -> Dict[str, str]:
        return {
            "key_encapsulation": self._default_kem,
            "digital_signature": self._default_dsa,
            "symmetric_encryption": self._default_symmetric,
            "hybrid_kem": f"X25519+{self._default_kem}",
            "hybrid_dsa": f"ECDSA_P256+{self._default_dsa}"
        }

agility_registry = CryptoAgilityRegistry()
