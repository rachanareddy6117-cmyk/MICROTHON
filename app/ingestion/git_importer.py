import os
import subprocess
import shutil
from fastapi import HTTPException
from ..config import settings

class SandboxedGitImporter:
    """
    Clones Git repositories securely into an isolated sandbox folder.
    Guarantees no local hooks, pre-commit, or post-checkout scripts execute.
    """
    def __init__(self, dest_base_dir: str = settings.SANDBOX_TEMP_DIR):
        self.dest_base_dir = dest_base_dir
        os.makedirs(self.dest_base_dir, exist_ok=True)

    def clone_repository(self, git_url: str, repo_id: str, branch: str = "main") -> str:
        # Validate git URL syntax to prevent command injection
        if not (git_url.startswith("https://") or git_url.startswith("http://") or git_url.startswith("git@")):
            raise HTTPException(status_code=400, detail="Invalid Git URL protocol. Must use HTTPS or SSH.")

        target_dir = os.path.join(self.dest_base_dir, f"git_{repo_id}")
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir, ignore_errors=True)
        os.makedirs(target_dir, exist_ok=True)

        # Clone with --depth 1 and disable template/hook execution
        cmd = [
            "git", "clone",
            "--depth", "1",
            "--branch", branch,
            "--config", "core.hooksPath=/dev/null",  # Prevent malicious hook execution
            git_url,
            target_dir
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
            if result.returncode != 0:
                # If branch fails, retry without specific branch
                cmd_fallback = ["git", "clone", "--depth", "1", "--config", "core.hooksPath=/dev/null", git_url, target_dir]
                fb_res = subprocess.run(cmd_fallback, capture_output=True, text=True, timeout=90)
                if fb_res.returncode != 0:
                    raise HTTPException(status_code=400, detail=f"Git clone failed: {fb_res.stderr[:200]}")
        except subprocess.TimeoutExpired:
            raise HTTPException(status_code=408, detail="Git clone operation timed out.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Git import error: {str(e)}")

        return target_dir

git_importer = SandboxedGitImporter()
