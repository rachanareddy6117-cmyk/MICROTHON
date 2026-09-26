from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = "PQC-Migrate"
    api_v1_prefix: str = "/api/v1"
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    postgres_url: str = os.getenv("PQC_DB_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/pqc_migrate")
    jwt_secret: str = os.getenv("JWT_SECRET", "dev-secret-change-me")
    rate_limit_per_minute: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    allowed_upload_types: tuple[str, ...] = ("pdf", "zip", "git", "json", "yaml", "crt", "pem", "sbom", "cbom")
    max_upload_bytes: int = 10 * 1024 * 1024 * 1024


settings = Settings()
