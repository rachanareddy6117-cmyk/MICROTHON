from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from .scans import SCANS_STORE

router = APIRouter(prefix="/dependencies", tags=["Dependency Graph & Blast Radius"])

@router.get("/graph/{scan_id}")
def get_dependency_graph(scan_id: str):
    if scan_id not in SCANS_STORE:
        raise HTTPException(status_code=404, detail="Scan not found.")
    s = SCANS_STORE[scan_id]
    return {
        "nodes": s.dependency_nodes,
        "edges": s.dependency_edges,
        "blast_radii": s.blast_radii
    }
