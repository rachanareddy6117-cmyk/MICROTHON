import os
import zipfile
import shutil
import tempfile
from typing import Dict, Any, List
from fastapi import HTTPException
from ..config import settings

class SecureArchiveUnpacker:
    """
    Secure archive extractor enforcing strict defense-in-depth:
    - Path traversal prevention (rejects '../', leading slashes, and outside links)
    - Zip bomb mitigation (compression ratio <= 100, max size <= 250MB)
    - File count limit (<= 10,000 files)
    - Never executes extracted files
    """
    def __init__(self, dest_base_dir: str = settings.SANDBOX_TEMP_DIR):
        self.dest_base_dir = dest_base_dir
        os.makedirs(self.dest_base_dir, exist_ok=True)

    def safely_extract_zip(self, zip_file_bytes: bytes, session_id: str) -> str:
        target_dir = os.path.join(self.dest_base_dir, f"repo_{session_id}")
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir, ignore_errors=True)
        os.makedirs(target_dir, exist_ok=True)

        temp_zip = os.path.join(target_dir, "upload.zip")
        with open(temp_zip, "wb") as f:
            f.write(zip_file_bytes)

        try:
            with zipfile.ZipFile(temp_zip, "r") as zf:
                total_uncompressed = 0
                total_files = len(zf.infolist())

                if total_files > 10000:
                    raise HTTPException(status_code=400, detail="Archive exceeds maximum allowed file count (10,000).")

                for info in zf.infolist():
                    # 1. Zip bomb check
                    total_uncompressed += info.file_size
                    if total_uncompressed > settings.MAX_UNCOMPRESSED_ZIP_BYTES:
                        raise HTTPException(status_code=400, detail="Zip bomb detected: uncompressed size exceeds limits.")
                    
                    if info.compress_size > 0:
                        ratio = info.file_size / info.compress_size
                        if ratio > settings.MAX_ZIP_RATIO:
                            raise HTTPException(status_code=400, detail=f"Zip bomb detected: compression ratio {ratio:.1f} exceeds limit.")

                    # 2. Path traversal check
                    filename = info.filename
                    if filename.startswith("/") or filename.startswith("\\") or ".." in filename:
                        raise HTTPException(status_code=400, detail="Malicious path traversal detected in archive.")

                    resolved_path = os.path.abspath(os.path.join(target_dir, filename))
                    if not resolved_path.startswith(os.path.abspath(target_dir)):
                        raise HTTPException(status_code=400, detail="Archive path escapes sandbox boundary.")

                # Extract safely
                zf.extractall(target_dir)

        finally:
            if os.path.exists(temp_zip):
                os.remove(temp_zip)

        return target_dir

secure_unpacker = SecureArchiveUnpacker()
