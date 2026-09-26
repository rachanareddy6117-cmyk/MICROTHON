from __future__ import annotations

import hashlib
import os
import re
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import List

from fastapi import UploadFile

from backend.app.config import settings


def _safe_name(name: str) -> str:
    normalized = os.path.normpath(name)
    if normalized.startswith("../") or normalized.startswith("..\\"):
        raise ValueError("Path traversal is not allowed.")
    return normalized


async def validate_upload(file: UploadFile) -> None:
    if not file.filename:
        raise ValueError("Uploaded file is missing a name.")
    suffix = Path(file.filename).suffix.lower().lstrip(".")
    if suffix not in {"pdf", "zip", "json", "yaml", "yml", "crt", "pem", "sbom", "cbom", "git"}:
        raise ValueError("Unsupported file type for secure ingestion.")
    if file.size and file.size > settings.max_upload_bytes:
        raise ValueError("Uploaded file exceeds the maximum allowed size.")


async def safe_extract_zip(zip_bytes: bytes, target_dir: str) -> List[str]:
    if len(zip_bytes) > settings.max_upload_bytes:
        raise ValueError("ZIP exceeds allowed size.")
    with tempfile.TemporaryDirectory() as tmp:
        zip_path = Path(tmp) / "upload.zip"
        zip_path.write_bytes(zip_bytes)
        with zipfile.ZipFile(zip_path) as archive:
            if len(archive.namelist()) > 2000:
                raise ValueError("ZIP contains too many entries.")
            total_size = 0
            extracted: List[str] = []
            for info in archive.infolist():
                total_size += info.file_size
                if total_size > settings.max_upload_bytes:
                    raise ValueError("ZIP content exceeds resource limits.")
                target = _safe_name(info.filename)
                if info.is_dir():
                    continue
                target_path = Path(target_dir) / target
                target_path.parent.mkdir(parents=True, exist_ok=True)
                if not str(target_path).startswith(str(Path(target_dir).resolve())):
                    raise ValueError("ZIP extraction path is invalid.")
                extracted_file = archive.read(info.filename)
                # Prevent malicious scripts from being executed during extraction.
                if info.filename.lower().endswith((".exe", ".dll", ".sh", ".ps1", ".bat", ".cmd")):
                    raise ValueError("Executable payloads are not allowed.")
                target_path.write_bytes(extracted_file)
                extracted.append(str(target_path))
        return extracted


async def compute_hash(file_bytes: bytes) -> str:
    return hashlib.sha256(file_bytes).hexdigest()


def sanitize_repository_path(path: str) -> str:
    cleaned = os.path.normpath(path)
    if cleaned.startswith(".."):
        raise ValueError("Repository path is invalid.")
    return cleaned


def secure_repo_snapshot(repo_path: str) -> str:
    target = Path(repo_path)
    if not target.exists():
        raise ValueError("Repository path does not exist.")
    archive_path = target.parent / f"{target.name}-snapshot.zip"
    shutil.make_archive(str(archive_path.with_suffix("")), "zip", str(target))
    return str(archive_path)
