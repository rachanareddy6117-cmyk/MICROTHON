from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from typing import List, Dict, Any, Optional
from ...ingestion.pdf_processor import pdf_processor

router = APIRouter(prefix="/projects", tags=["Projects & Spec Scanning"])

# In-memory storage mock for quick standalone responses
PROJECTS_STORE = {}

@router.get("/")
def list_projects():
    return list(PROJECTS_STORE.values())

@router.post("/")
def create_project(name: str = Form(...), description: str = Form("")):
    import uuid
    p_id = f"PROJ-{uuid.uuid4().hex[:6].upper()}"
    proj = {
        "id": p_id,
        "name": name,
        "description": description,
        "technology_stack": [],
        "budget": "Not specified",
        "timeline": "TBD",
        "risks": []
    }
    PROJECTS_STORE[p_id] = proj
    return proj

@router.post("/{project_id}/scan-spec-pdf")
async def scan_project_pdf(project_id: str, file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF specification documents are accepted.")
    
    content = await file.read()
    extracted = pdf_processor.extract_specifications(content)
    
    if project_id in PROJECTS_STORE:
        PROJECTS_STORE[project_id].update({
            "technology_stack": extracted["technology_stack"],
            "budget": extracted["budget"],
            "timeline": extracted["timeline"],
            "vendors": extracted["vendors"],
            "risks": extracted["identified_risks"],
            "scope": extracted["scope"]
        })
    
    return {
        "project_id": project_id,
        "filename": file.filename,
        "specifications": extracted
    }
