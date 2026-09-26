import networkx as nx
from typing import Dict, List, Any

class BlastRadiusCalculator:
    """
    Computes cryptographic blast radius:
    - Direct callers vs transitive impacted services
    - Operational domain weight (In-Transit vs Auth vs Storage)
    - Criticality score (0 - 100)
    """
    def calculate(self, graph_builder, findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        g = graph_builder.graph
        blast_radii = []

        for f in findings:
            algo_id = f"ALGO:{f['algorithm']}"
            
            # Count incoming dependencies to this algorithm
            direct_callers = list(g.predecessors(algo_id)) if g.has_node(algo_id) else []
            
            # Transitive caller propagation
            transitive_impacted = []
            if g.has_node(algo_id):
                try:
                    rev_g = g.reverse()
                    transitive_impacted = [n for n in nx.descendants(rev_g, algo_id) if n.startswith("PKG:") or n.startswith("SVC:")]
                except Exception:
                    transitive_impacted = direct_callers

            base = 40.0
            if f.get("exposure_domain") == "IN_TRANSIT":
                base += 35.0  # Immediate HNDL threat
            elif f.get("exposure_domain") == "AUTHENTICATION_IDENTITY":
                base += 25.0
            elif f.get("exposure_domain") == "AT_REST":
                base += 15.0

            dep_factor = min(len(transitive_impacted) * 5.0, 25.0)
            score = round(min(100.0, base + dep_factor), 1)

            blast_radii.append({
                "finding_id": f["id"],
                "algorithm": f["algorithm"],
                "location": f"{f['file_path']}:{f.get('line_number', 1)}",
                "direct_dependents_count": len(direct_callers),
                "transitive_impacted_count": len(transitive_impacted),
                "transitive_impacted_files": transitive_impacted[:10],
                "criticality_score": score,
                "operational_impact": "Severe: Perimeter / External In-Transit" if f.get("exposure_domain") == "IN_TRANSIT" else "High: Authentication Backbone"
            })
        return blast_radii

blast_calculator = BlastRadiusCalculator()
