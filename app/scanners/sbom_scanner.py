import json
from typing import List, Dict, Any

class SbomCbomParser:
    """
    Parses CycloneDX and SPDX SBOM/CBOM files.
    Identifies cryptographic components, libraries, and algorithm properties.
    """
    def parse_sbom(self, sbom_json_str: str) -> List[Dict[str, Any]]:
        findings = []
        try:
            data = json.loads(sbom_json_str)
        except Exception:
            return findings

        components = data.get("components", [])
        for comp in components:
            name = comp.get("name", "")
            desc = comp.get("description", "")
            crypto_props = comp.get("cryptoProperties", {})
            algo_props = crypto_props.get("algorithmProperties", {})
            
            # Check if this component has explicit crypto properties
            if crypto_props:
                findings.append({
                    "name": name,
                    "primitive": algo_props.get("primitive", "unknown"),
                    "security_level": algo_props.get("nistQuantumSecurityLevel", 0),
                    "is_quantum_vulnerable": algo_props.get("nistQuantumSecurityLevel", 0) < 2
                })
        return findings

sbom_parser = SbomCbomParser()
