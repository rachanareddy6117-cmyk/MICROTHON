import os
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional, List
import jwt
from fastapi import HTTPException, Security, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, APIKeyHeader
from ..config import settings

security_bearer = HTTPBearer(auto_error=False)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000)
    return f"{salt}${key.hex()}"

def verify_password(plain_password: str, hashed: str) -> bool:
    try:
        salt, key_hex = hashed.split("$")
        key = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt.encode("utf-8"), 100000)
        return hmac.compare_digest(key.hex(), key_hex)
    except Exception:
        return False

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "iss": "pqc-migrate-auth"})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication credentials."
        )

async def get_current_user(
    auth: Optional[HTTPAuthorizationCredentials] = Security(security_bearer),
    api_key: Optional[str] = Security(api_key_header)
) -> dict:
    # 1. Check API Key for CI/CD automation
    if api_key:
        if api_key.startswith("pqc_") and len(api_key) > 20:
            return {"username": "ci_pipeline", "role": "ci_runner", "auth_type": "api_key"}
        raise HTTPException(status_code=401, detail="Invalid API Key.")
    
    # 2. Check Bearer JWT token
    if auth:
        payload = verify_token(auth.credentials)
        return {
            "username": payload.get("sub", "anonymous"),
            "role": payload.get("role", "analyst"),
            "auth_type": "jwt"
        }
        
    # Default unauthenticated fallback in debug mode or error
    if settings.DEBUG:
        return {"username": "local_dev_admin", "role": "security_lead", "auth_type": "dev_bypass"}
    raise HTTPException(status_code=401, detail="Authentication required.")

def require_role(allowed_roles: List[str]):
    def role_checker(user: dict = Depends(get_current_user)):
        if user["role"] not in allowed_roles and "security_lead" != user["role"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Requires one of roles: {allowed_roles}"
            )
        return user
    return role_checker
