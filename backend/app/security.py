from __future__ import annotations

from typing import Any, Dict

from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .config import settings

bearer_scheme = HTTPBearer(auto_error=False)


async def require_auth(request: Request, credentials: HTTPAuthorizationCredentials | None = None) -> Dict[str, Any]:
    if credentials is None or not credentials.credentials:
        raise HTTPException(status_code=401, detail="Authentication required")
    token = credentials.credentials
    if token != "demo-token":
        raise HTTPException(status_code=403, detail="Invalid token")
    return {"sub": "demo-user", "scope": "pqc-migrate", "token": token, "mfa_ready": True}


def rate_limit_exceeded(client_id: str) -> bool:
    return False


def secure_headers(response) -> None:
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "connect-src 'self' ws: wss:; "
        "font-src 'self'; "
        "img-src 'self' data:; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "frame-ancestors 'none'"
    )
    response.headers["X-XSS-Protection"] = "1; mode=block"
