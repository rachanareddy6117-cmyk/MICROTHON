import os
import re
import networkx as nx
from typing import Dict, List, Any, Tuple

class HierarchicalDependencyGraphBuilder:
    """
    Constructs the full multi-tier cryptographic dependency graph:
    Repository -> Service -> Package -> Library -> Crypto API -> Algorithm -> Certificate -> Protocol
    """
    def __init__(self):
        self.graph = nx.DiGraph()

    def build_hierarchy(self, repo_name: str, target_dir: str, findings: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        self.graph.clear()

        # 1. Repository Node (Root)
        repo_node_id = f"REPO:{repo_name}"
        self.graph.add_node(repo_node_id, label=repo_name, node_type="repository", level=0)

        # 2. Discover Services (Subdirectories or root service)
        services = self._detect_services(target_dir)
        for s_name, s_path in services.items():
            s_node_id = f"SVC:{s_name}"
            self.graph.add_node(s_node_id, label=s_name, node_type="service", level=1)
            self.graph.add_edge(repo_node_id, s_node_id, relation="contains_service")

            # 3. Discover Packages / Modules within service
            files = self._get_service_files(s_path)
            for f_path in files:
                rel_f = os.path.relpath(f_path, target_dir)
                pkg_node_id = f"PKG:{rel_f}"
                self.graph.add_node(pkg_node_id, label=os.path.basename(f_path), node_type="package", level=2)
                self.graph.add_edge(s_node_id, pkg_node_id, relation="contains_file")

        # 4. Connect Findings (Crypto API -> Algorithm -> Certificate / Protocol)
        for f in findings:
            rel_file = os.path.relpath(f["file_path"], target_dir) if os.path.isabs(f["file_path"]) else f["file_path"]
            pkg_node_id = f"PKG:{rel_file}"
            
            # If package node wasn't added yet, add it
            if not self.graph.has_node(pkg_node_id):
                self.graph.add_node(pkg_node_id, label=os.path.basename(f["file_path"]), node_type="package", level=2)
                self.graph.add_edge(repo_node_id, pkg_node_id, relation="contains_file")

            # Crypto API node
            api_id = f"API:{f['category']}"
            if not self.graph.has_node(api_id):
                self.graph.add_node(api_id, label=f"API: {f['category']}", node_type="crypto_api", level=3)
            self.graph.add_edge(pkg_node_id, api_id, relation="invokes_api")

            # Algorithm Node
            algo_id = f"ALGO:{f['algorithm']}"
            if not self.graph.has_node(algo_id):
                self.graph.add_node(
                    algo_id,
                    label=f"{f['algorithm']} ({f.get('key_size_or_curve', 'standard')})",
                    node_type="algorithm",
                    vulnerability=f["vulnerability_level"],
                    level=4
                )
            self.graph.add_edge(api_id, algo_id, relation="implements_algorithm")

            # Protocol / Certificate Node
            if f["source_type"] == "certificate":
                cert_id = f"CERT:{f['id']}"
                self.graph.add_node(cert_id, label=f"Cert: {os.path.basename(f['file_path'])}", node_type="certificate", level=5)
                self.graph.add_edge(algo_id, cert_id, relation="signs_certificate")
            elif f["source_type"] == "config":
                proto_id = f"PROTO:{f['exposure_domain']}"
                self.graph.add_node(proto_id, label=f"Protocol: {f['exposure_domain']}", node_type="protocol", level=5)
                self.graph.add_edge(algo_id, proto_id, relation="secures_protocol")

        # Convert networkx graph to serializable nodes & edges
        nodes = []
        for n, d in self.graph.nodes(data=True):
            nodes.append({
                "id": n,
                "label": d.get("label", n),
                "node_type": d.get("node_type", "unknown"),
                "vulnerability": d.get("vulnerability"),
                "level": d.get("level", 0)
            })

        edges = []
        for u, v, d in self.graph.edges(data=True):
            edges.append({
                "source": u,
                "target": v,
                "relation": d.get("relation", "linked")
            })

        return nodes, edges

    def _detect_services(self, target_dir: str) -> Dict[str, str]:
        services = {}
        for item in os.listdir(target_dir):
            full = os.path.join(target_dir, item)
            if os.path.isdir(full) and item not in [".git", "venv", ".venv", "node_modules", "__pycache__"]:
                services[item] = full
        if not services:
            services["core_service"] = target_dir
        return services

    def _get_service_files(self, service_dir: str) -> List[str]:
        files = []
        for root, _, fs in os.walk(service_dir):
            for f in fs:
                if f.endswith((".py", ".js", ".ts", ".go", ".java", ".conf", ".tf")):
                    files.append(os.path.join(root, f))
        return files

graph_builder = HierarchicalDependencyGraphBuilder()
