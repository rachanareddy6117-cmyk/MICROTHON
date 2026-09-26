from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List, Dict, Any
from ...ingestion.safe_unpack import secure_unpacker
from ...ingestion.git_importer import git_importer
from ...scanners.deployment_scanner import deployment_correlator

router = APIRouter(prefix="/repositories", tags=["Repositories & Deployments"])
REPOS_STORE = {}

@router.get("/")
def list_repositories():
    return list(REPOS_STORE.values())

@router.post("/import-git")
def import_git_repository(git_url: str = Form(...), name: str = Form("Imported-Git-Repo")):
    import uuid
    repo_id = uuid.uuid4().hex[:8]
    local_dir = git_importer.clone_repository(git_url, repo_id)
    repo = {
        "id": repo_id,
        "name": name,
        "git_url": git_url,
        "local_path": local_dir,
        "is_sandboxed": True,
        "source_type": "git"
    }
    REPOS_STORE[repo_id] = repo
    return repo

@router.post("/upload-archive")
async def upload_repo_archive(name: str = Form("Uploaded-Archive"), file: UploadFile = File(...)):
    import uuid
    if not file.filename.lower().endswith(".zip"):
        raise HTTPException(status_code=400, detail="Only safe ZIP archives are accepted.")
    
    repo_id = uuid.uuid4().hex[:8]
    content = await file.read()
    dest_dir = secure_unpacker.safely_extract_zip(content, repo_id)
    repo = {
        "id": repo_id,
        "name": name,
        "local_path": dest_dir,
        "is_sandboxed": True,
        "source_type": "zip_upload"
    }
    REPOS_STORE[repo_id] = repo
    return repo

@router.post("/{repo_id}/deployment-logs")
async def correlate_deployment_log(repo_id: str, log_file: UploadFile = File(...)):
    content = (await log_file.read()).decode("utf-8", errors="ignore")
    correlations = deployment_correlator.correlate_logs(content)
    return {
        "repo_id": repo_id,
        "total_errors_correlated": len(correlations),
        "correlations": correlations
    }
